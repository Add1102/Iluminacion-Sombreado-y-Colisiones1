import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from acciones import escenario as es, luces as lc, sonido as son, textos as txt
from personajes.lobo import Lobo
from acciones import objetos as obj 

pygame.init()
pygame.mixer.init()

display = (1200, 800)
initial_camera_pos = [0, 2, 10]
initial_camera_rot = [-10, 0]
initial_fov = 45
camera_pos = list(initial_camera_pos)
camera_rot = list(initial_camera_rot)
fov = initial_fov
camera_speed = 0.2
mouse_sensitivity = 0.1
show_instructions = True
show_acerca_de = False
modo_sombreado = 0

# --- Algoritmos de Colisión ---
def check_colision_AABB(bbox1, bbox2):
    # Verifica colisión AABB (Cajas Alineadas) en XZ
    return (bbox1[0] < bbox2[1] and bbox1[1] > bbox2[0] and
            bbox1[2] < bbox2[3] and bbox1[3] > bbox2[2])

def check_colision_Esfera(pos1, radio1, pos2, radio2):
    # Verifica colisión por Esfera (radio)
    dist_sq = (pos1[0] - pos2[0])**2 + (pos1[2] - pos2[2])**2
    return dist_sq < (radio1 + radio2)**2

def check_colision_Rombo(pos1, pos2, radio_rombo):
    # Verifica colisión por Distancia Manhattan (Rombo)
    dist_manhattan = abs(pos1[0] - pos2[0]) + abs(pos1[2] - pos2[2])
    return dist_manhattan < radio_rombo

def setup_opengl():
    # Configura el estado inicial de OpenGL luces, perspectiva
    lc.setup_lighting()
    glEnable(GL_NORMALIZE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, (display[0] / display[1]), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_CULL_FACE)

def main():
    # Función principal que ejecuta el bucle del juego
    global camera_pos, camera_rot, show_instructions, show_acerca_de, fov, modo_sombreado
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("GUSTAVO")
    
    setup_opengl()
    es.init_escenarios()
    
    sonidos_dict = son.cargar_sonidos()
    son.cargar_musica_fondo()
    son.toggle_musica_fondo()

    expresion_a_escenario = {
        "normal": 0, "feliz": 1, "triste": 2,
        "enojado": 3, "sorpresa": 4, "aullido": 5, "duda": 6
    }
    escenario_actual = 0
    
    personaje_lobo = Lobo(posicion_inicial=[0, -1.25, 0])
    
    # --- Definición de Objetos de Colisión ---
    
    # 1. Árbol (AABB)
    arbol_pos = [5, -1.25, 5] 
    arbol_bbox = (arbol_pos[0] - 0.7, arbol_pos[0] + 0.7, arbol_pos[2] - 0.7, arbol_pos[2] + 0.7)
    
    # 2. Arbusto (Esfera)
    arbusto_pos = [-5, -0.25, 5.0] 
    arbusto_radio = 1.5
    arbusto_color_original = [0.1, 0.5, 0.1]
    arbusto_color_interaccion = [1.0, 1.0, 0.0]
    arbusto_color_actual = list(arbusto_color_original)
    arbusto_timer_colision = 0

    # 3. Flor (Rombo)
    flor_pos = [-5, -1.25, -5]
    flor_radio_rombo = 2.0
    flor_color_original = [1.0, 0.2, 1.0]
    flor_color_interaccion = [1.0, 1.0, 1.0]
    flor_timer_colision = 0
    
    # 4. Asteroide (AABB)
    asteroide = {
        'pos': [0, 20, 0], 'cayendo': False,
        'velocidad_y': -0.3, 'radio': 1.0
    }
    
    # 5. Corazón (AABB)
    corazon_pos = [0, -0.75, -7]
    corazon_radio_bbox = 1.0
    corazon_bbox = (corazon_pos[0] - corazon_radio_bbox, corazon_pos[0] + corazon_radio_bbox,
                    corazon_pos[2] - corazon_radio_bbox, corazon_pos[2] + corazon_radio_bbox)
    corazon_visible = True
    corazon_respawn_timer = 0
    CORAZON_RESPAWN_TIME = 600 # 10 segundos
    
    # --- Fin Objetos ---
    
    def reset_game():
        # Reinicia el estado del lobo y la escena a sus valores iniciales
        nonlocal escenario_actual, asteroide, arbusto_color_actual, arbusto_timer_colision, flor_timer_colision, corazon_visible, corazon_respawn_timer
        personaje_lobo.reset()
        escenario_actual = 0
        asteroide['cayendo'] = False
        asteroide['pos'] = [0, 20, 0]
        
        arbusto_color_actual = list(arbusto_color_original)
        arbusto_timer_colision = 0
        flor_timer_colision = 0
        corazon_visible = True
        corazon_respawn_timer = 0
        
        camera_pos[:] = initial_camera_pos
        camera_rot[:] = list(initial_camera_rot)
        fov = initial_fov

    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    while True:
        # Manejo de eventos de entrada teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: fov = max(15, fov - 5)
                if event.button == 5: fov = min(90, fov + 5)
            
            if event.type == pygame.KEYDOWN:
                if event.key == K_y and personaje_lobo.health <= 0:
                    reset_game()
                    continue 

                expresion_map = {
                    K_1: "normal", K_2: "feliz", K_3: "triste",
                    K_4: "enojado", K_5: "sorpresa", K_6: "aullido", K_7: "duda"
                }
                
                if event.key in expresion_map:
                    expresion = expresion_map[event.key]
                    if personaje_lobo.health > 0: 
                        personaje_lobo.set_expresion(expresion)
                        son.reproducir(expresion, sonidos_dict)
                        escenario_actual = expresion_a_escenario.get(expresion, 0)

                if event.key == K_x: personaje_lobo.toggle_acostarse()
                if event.key == K_SPACE: personaje_lobo.saltar()
                if event.key == K_l: personaje_lobo.ladrar(sonidos_dict)
                if event.key == K_v: personaje_lobo.toggle_caminar()
                
                if event.key == K_c and not asteroide['cayendo'] and personaje_lobo.health > 0:
                    asteroide['cayendo'] = True
                    asteroide['pos'] = [personaje_lobo.posicion_x, 20, personaje_lobo.posicion_z]
                
                if event.key == K_h: show_instructions = not show_instructions; show_acerca_de = False
                if event.key == K_p: show_acerca_de = not show_acerca_de; show_instructions = False
                if event.key == K_m: son.toggle_musica_fondo()
                if event.key == K_r:
                    camera_pos[:], camera_rot[:], fov = list(initial_camera_pos), list(initial_camera_rot), initial_fov

                if event.key == K_f:
                    modo_sombreado = (modo_sombreado + 1) % 2

        # Lógica de movimiento de la cámara
        keys = pygame.key.get_pressed()
        rad_y = math.radians(camera_rot[1])
        if keys[K_w]: camera_pos[0] += camera_speed * math.sin(rad_y); camera_pos[2] -= camera_speed * math.cos(rad_y)
        if keys[K_s]: camera_pos[0] -= camera_speed * math.sin(rad_y); camera_pos[2] += camera_speed * math.cos(rad_y)
        if keys[K_a]: camera_pos[0] -= camera_speed * math.cos(rad_y); camera_pos[2] -= camera_speed * math.sin(rad_y)
        if keys[K_d]: camera_pos[0] += camera_speed * math.cos(rad_y); camera_pos[2] += camera_speed * math.sin(rad_y)
        if keys[K_q]: camera_pos[1] += camera_speed
        if keys[K_e]: camera_pos[1] -= camera_speed
        
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        camera_rot[1] += mouse_dx * mouse_sensitivity
        camera_rot[0] = max(-90, min(90, camera_rot[0] + mouse_dy * mouse_sensitivity))
        if pygame.event.get_grab(): pygame.mouse.set_pos(display[0] // 2, display[1] // 2)

        # Lógica de movimiento del lobo
        lobo_pos_actual = (personaje_lobo.posicion_x, 0, personaje_lobo.posicion_z)
        lobo_bbox = personaje_lobo.get_bounding_box()
        lobo_radio = 1.0
        
        if personaje_lobo.health > 0:
            dx, dz = 0, 0
            if keys[K_LEFT]: dx = -0.1
            if keys[K_RIGHT]: dx = 0.1
            if keys[K_UP]: dz = -0.1
            if keys[K_DOWN]: dz = 0.1
            
            if (dx != 0 or dz != 0):
                old_x, old_z = personaje_lobo.posicion_x, personaje_lobo.posicion_z
                personaje_lobo.mover(dx, dz)
                
                # Colisión AABB (Lobo vs Árbol)
                lobo_bbox_movido = personaje_lobo.get_bounding_box()
                if check_colision_AABB(lobo_bbox_movido, arbol_bbox):
                    personaje_lobo.recibir_dano(sonidos_dict)
                    personaje_lobo.posicion_x, personaje_lobo.posicion_z = old_x, old_z


        # Actualiza animaciones y sonidos
        if personaje_lobo.actualizar_animaciones():
            son.reproducir('aterrizaje', sonidos_dict)

        # Lógica de Interacciones
        
        # INTERACCIÓN 1 (Esfera): Lobo vs Arbusto
        if check_colision_Esfera(lobo_pos_actual, lobo_radio, arbusto_pos, arbusto_radio):
            arbusto_color_actual = arbusto_color_interaccion
            arbusto_timer_colision = 60
        
        # INTERACCIÓN 2 (Rombo): Lobo vs Flor
        if check_colision_Rombo(lobo_pos_actual, flor_pos, flor_radio_rombo):
            flor_timer_colision = 60
            
        # INTERACCIÓN 3 (AABB): Lobo vs Corazón
        if corazon_visible and personaje_lobo.health > 0:
            if check_colision_AABB(lobo_bbox, corazon_bbox):
                personaje_lobo.health = 5 # Restaura vida
                son.reproducir('feliz', sonidos_dict)
                corazon_visible = False
                corazon_respawn_timer = CORAZON_RESPAWN_TIME
        
        # Timers de interacción
        if arbusto_timer_colision > 0:
            arbusto_timer_colision -= 1
            if arbusto_timer_colision == 0:
                arbusto_color_actual = list(arbusto_color_original)
        
        if flor_timer_colision > 0:
            flor_timer_colision -= 1
            
        if not corazon_visible:
            corazon_respawn_timer -= 1
            if corazon_respawn_timer <= 0:
                corazon_visible = True

        # Lógica de física del asteroide
        if asteroide['cayendo']:
            asteroide['pos'][1] += asteroide['velocidad_y']
            
            # Colisión AABB (Lobo vs Asteroide)
            r_ast = asteroide['radio']
            ast_bbox = (asteroide['pos'][0] - r_ast, asteroide['pos'][0] + r_ast,
                        asteroide['pos'][2] - r_ast, asteroide['pos'][2] + r_ast)
            
            if check_colision_AABB(lobo_bbox, ast_bbox) and asteroide['pos'][1] <= (personaje_lobo.altura_base + 1.0):
                if personaje_lobo.health > 0:
                    personaje_lobo.recibir_dano(sonidos_dict)
                asteroide['cayendo'] = False 
                asteroide['pos'][1] = 20
            
            elif asteroide['pos'][1] < -5:
                asteroide['cayendo'] = False
                asteroide['pos'][1] = 20
        
        # Sección de dibujo
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluPerspective(fov, (display[0] / display[1]), 0.1, 200.0)
        glMatrixMode(GL_MODELVIEW); glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glLoadIdentity()
        
        glRotatef(camera_rot[0], 1, 0, 0); glRotatef(camera_rot[1], 0, 1, 0)
        glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])
        
        
        if modo_sombreado == 0: # 0: Gouraud 
            glEnable(GL_LIGHTING)
            glShadeModel(GL_SMOOTH)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            
        elif modo_sombreado == 1: # 1: Flat 
            glEnable(GL_LIGHTING)
            glShadeModel(GL_FLAT)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
            
        lc.update_light_position()
        es.draw_escenario(escenario_actual)
        
        # --- Dibujado de Objetos de Colisión ---
        
        # 1. Árbol (AABB)
        obj.draw_arbol(arbol_pos)
        
        # 2. Arbusto (Esfera)
        obj.draw_arbusto(arbusto_pos, arbusto_color_actual) 
        
        # 3. Flor (Rombo)
        escala_flor = 1.5 if flor_timer_colision > 0 else 1.0
        color_flor = flor_color_interaccion if flor_timer_colision > 0 else flor_color_original
        obj.draw_flor(flor_pos, color_flor, escala_flor)
        
        # 5. Corazón (AABB)
        if corazon_visible:
            obj.draw_corazon(corazon_pos)
            
        # 4. Asteroide (AABB)
        if asteroide['cayendo']:
            obj.draw_asteroide(asteroide['pos'])
            
        personaje_lobo.draw_lobo()

        # Dibujar la interfaz de usuario
        if show_instructions: txt.draw_instructions_overlay(display)
        if show_acerca_de: txt.draw_acerca_de_overlay(display)
        
        txt.draw_modo_sombreado(display, modo_sombreado) 
        txt.draw_vidas(display, personaje_lobo.health)
        
        if personaje_lobo.health <= 0:
            txt.draw_game_over_overlay(display)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()