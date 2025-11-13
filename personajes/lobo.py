import pygame
from OpenGL.GL import *
from math import sin, cos, pi, degrees, atan2
import random 
from acciones import objetos 
from acciones import sonido as son 

COLOR_LOBO = (0.5, 0.5, 0.5)
COLOR_HOCICO = (0.9, 0.9, 0.9)
COLOR_PATAS_OSCURAS = (0.2, 0.2, 0.2)
COLOR_PATITAS_BLANCAS = (0.9, 0.9, 0.9)
COLOR_NARIZ = (0.1, 0.1, 0.1)
COLOR_DANADO = (1.0, 0.3, 0.3) 
COLOR_SUETER = (1.0, 1.0, 0.2) 

class Lobo:
    # Maneja el estado, la lógica y el dibujo del personaje lobo.
    
    def __init__(self, posicion_inicial=[0, 0, 0]):
        # Inicializa al lobo
        self.posicion_inicial = posicion_inicial
        self.reset() 

    def reset(self):
        # Restaura todas las variables del lobo a su estado inicial
        self.posicion_x = self.posicion_inicial[0]
        self.posicion_z = self.posicion_inicial[2]
        self.altura_base = 1.25
        self.rotacion_y = -90.0
        self.health = 5 
        self.damage_timer = 0 
        self.acostado = False
        self.posicion_y_salto = 0.0
        self.ultimo_tiempo_salto = -10000 
        self.was_in_air = False
        self.expresion_actual = "normal"
        self.tiempo_ladrido = -1000
        self.angulo_hocico = 0.0 
        self.inclinacion_cabeza = 0.0
        self.inclinacion_cabeza_lateral = 0.0
        self.inclinacion_cuerpo = 0.0
        self.offset_cuerpo_x = 0.0
        self.offset_cuerpo_z = 0.0
        self.angulo_cola_pose = 0.0 
        self.angulo_cola_meneo = 0.0
        self.esta_caminando = False
        self.angulo_caminar = 0.0

    def mover(self, dx, dz):
        # Mueve al lobo en el plano XZ y actualiza su rotación
        if not self.acostado and self.health > 0:
            self.posicion_x += dx
            self.posicion_z += dz
            
            if dx != 0 or dz != 0:
                self.rotacion_y = -degrees(atan2(dz, dx))

    def recibir_dano(self, sonidos_dict):
        # Resta vida al lobo y reproduce un sonido
        if self.damage_timer <= 0 and self.health > 0:
            self.health -= 1
            self.damage_timer = 60 
            son.reproducir('impacto', sonidos_dict)
            
            if self.health <= 0:
                self.acostado = True
                self.altura_base = 0.4

    def get_bounding_box(self):
        # Devuelve la caja de colisión  del lobo
        return (
            self.posicion_x - 1.0, self.posicion_x + 1.0,
            self.posicion_z - 1.0, self.posicion_z + 1.0
        )

    def set_expresion(self, exp):
        # Establece la expresión facial
        self.expresion_actual = exp

    def toggle_acostarse(self):
        # Alterna entre estar de pie y acostado
        if self.health <= 0: return
        
        self.acostado = not self.acostado
        self.altura_base = 0.4 if self.acostado else 1.25

    def toggle_caminar(self):
        # Activa o desactiva la animación de caminar
        if self.health <= 0: return
        self.esta_caminando = not self.esta_caminando
    
    def ladrar(self, sonidos_dict):
        # Inicia la animación y el sonido de ladrido
        if self.acostado or self.health <= 0: return
        son.reproducir('ladrido', sonidos_dict) 
        self.angulo_hocico = -30.0 
        self.tiempo_ladrido = pygame.time.get_ticks() 
    
    def saltar(self):
        # Inicia un salto si no está acostado 
        if not self.acostado and self.health > 0 and pygame.time.get_ticks() - self.ultimo_tiempo_salto > 1000:
            self.ultimo_tiempo_salto = pygame.time.get_ticks()

    def actualizar_animaciones(self):
        # Actualiza el estado de todas las animaciones (cola, cabeza, salto, etc.) basado en el tiempo
        if self.damage_timer > 0:
            self.damage_timer -= 1
            
        if self.health <= 0:
            self.angulo_cola_meneo = 0
            self.angulo_cola_pose = -20.0 
            self.esta_caminando = False
            self.angulo_caminar = 0.0
            return False

        self.inclinacion_cabeza = 0.0
        self.inclinacion_cabeza_lateral = 0.0
        self.inclinacion_cuerpo = 0.0
        self.offset_cuerpo_x = 0.0
        self.offset_cuerpo_z = 0.0
        self.angulo_cola_pose = 0.0 
        self.angulo_cola_meneo = 0.0 
        
        tiempo_actual = pygame.time.get_ticks()

       
        if self.angulo_hocico != 0.0 and tiempo_actual - self.tiempo_ladrido > 400:
            self.angulo_hocico = 0.0 

        if self.expresion_actual == "normal":
            self.angulo_cola_meneo = 20 * sin(tiempo_actual * 0.003) 
        elif self.expresion_actual == "feliz":
            self.angulo_cola_meneo = 40 * sin(tiempo_actual * 0.01) 
        elif self.expresion_actual == "triste":
            self.inclinacion_cabeza = 20.0 
            self.angulo_cola_pose = -20.0 
        elif self.expresion_actual == "enojado":
            self.inclinacion_cabeza = -10.0 
            self.inclinacion_cuerpo = -10.0 
            self.angulo_cola_pose = 20.0 
        elif self.expresion_actual == "sorpresa":
            self.offset_cuerpo_x = sin(tiempo_actual * 0.1) * 0.05 
            self.offset_cuerpo_z = cos(tiempo_actual * 0.1) * 0.05
            self.angulo_cola_pose = 15.0 
        elif self.expresion_actual == "aullido": 
            self.inclinacion_cabeza = 0.0   
            self.inclinacion_cuerpo = 20.0  
            self.angulo_hocico = -25.0      
            self.angulo_cola_pose = 10.0 
        elif self.expresion_actual == "duda":
            self.inclinacion_cabeza_lateral = 20 * sin(tiempo_actual * 0.005) 
            self.angulo_cola_meneo = 10 * sin(tiempo_actual * 0.002) 
        else:
            self.angulo_cola_meneo = 20 * sin(tiempo_actual * 0.003)

        tiempo_desde_salto = pygame.time.get_ticks() - self.ultimo_tiempo_salto
        self.posicion_y_salto = 0
        if tiempo_desde_salto < 500:
            self.posicion_y_salto = 4.0 * (1.0) * (tiempo_desde_salto / 500.0) * (1 - tiempo_desde_salto / 500.0)
        
        if self.esta_caminando and not self.acostado:
            self.angulo_caminar = 30 * sin(tiempo_actual * 0.008) 
        else:
            self.angulo_caminar = 0.0

        landed_this_frame = False
        is_currently_in_air = self.posicion_y_salto > 0
        if self.was_in_air and not is_currently_in_air:
            landed_this_frame = True
        self.was_in_air = is_currently_in_air
        
        return landed_this_frame

    def _draw_cubo(self, escala, color):
        # Función para dibujar el color de daño
        glPushMatrix()
        if self.damage_timer > 0:
            glColor3fv(COLOR_DANADO)
        else:
            glColor3fv(color)
        objetos.draw_cube(escala=escala)
        glPopMatrix()

    def _dibujar_expresion(self):
        # Dibuja los ojos y las cejas del lobo según la expresión actual
        glPushMatrix()
        glTranslatef(0.41, 0.1, 0) 
        glRotatef(-90, 0, 1, 0)
        
        if self.acostado:
            glRotatef(0, 0, 0, 1) 
            
        glScalef(0.6, 0.6, 0.6) 
        glDisable(GL_LIGHTING); glColor3f(0, 0, 0); glLineWidth(3.0)
        eye_y, eye_x_offset = 0.1, 0.15 
        
        # Dibuja los ojos base
        glBegin(GL_QUADS) 
        for sign in [-1, 1]:
            glVertex3f(sign * eye_x_offset - 0.03, eye_y - 0.03, 0); glVertex3f(sign * eye_x_offset + 0.03, eye_y - 0.03, 0)
            glVertex3f(sign * eye_x_offset + 0.03, eye_y + 0.03, 0); glVertex3f(sign * eye_x_offset - 0.03, eye_y + 0.03, 0)
        glEnd()

        # Dibuja las cejas/líneas de expresión
        if self.expresion_actual == "feliz":
            glBegin(GL_LINES) 
            for sign in [-1, 1]:
                glVertex3f(sign * eye_x_offset - 0.08, eye_y + 0.1, 0); glVertex3f(sign * eye_x_offset, eye_y + 0.18, 0)
                glVertex3f(sign * eye_x_offset, eye_y + 0.18, 0); glVertex3f(sign * eye_x_offset + 0.08, eye_y + 0.1, 0)
            glEnd()
        elif self.expresion_actual == "triste":
            glBegin(GL_LINES) 
            glVertex3f(-eye_x_offset - 0.1, eye_y + 0.05, 0); glVertex3f(-eye_x_offset + 0.05, eye_y + 0.15, 0)
            glVertex3f(eye_x_offset + 0.1, eye_y + 0.05, 0); glVertex3f(eye_x_offset - 0.05, eye_y + 0.15, 0)
            glEnd()
        elif self.expresion_actual == "enojado":
            glBegin(GL_LINES) 
            glVertex3f(-eye_x_offset - 0.1, eye_y + 0.15, 0); glVertex3f(-eye_x_offset + 0.05, eye_y + 0.05, 0)
            glVertex3f(eye_x_offset + 0.1, eye_y + 0.15, 0); glVertex3f(eye_x_offset - 0.05, eye_y + 0.05, 0)
            glEnd()
        elif self.expresion_actual == "sorpresa":
            glBegin(GL_LINES) 
            glVertex3f(-eye_x_offset - 0.1, eye_y + 0.18, 0); glVertex3f(-eye_x_offset + 0.1, eye_y + 0.20, 0)
            glVertex3f(eye_x_offset + 0.1, eye_y + 0.18, 0); glVertex3f(eye_x_offset - 0.1, eye_y + 0.20, 0)
            glEnd()
        elif self.expresion_actual == "duda":
             glBegin(GL_LINES) 
             glVertex3f(-eye_x_offset - 0.1, eye_y + 0.05, 0); glVertex3f(-eye_x_offset + 0.05, eye_y + 0.15, 0) 
             glVertex3f(eye_x_offset - 0.08, eye_y + 0.1, 0); glVertex3f(eye_x_offset, eye_y + 0.18, 0) 
             glEnd()
            
        glEnable(GL_LIGHTING); glPopMatrix()

    def draw_lobo(self):
        # Dibuja todas las partes del lobo usando transformaciones
        glPushMatrix()
        
        glTranslatef(
            self.posicion_x + self.offset_cuerpo_x, 
            self.altura_base + self.posicion_y_salto, 
            self.posicion_z + self.offset_cuerpo_z
        )
        
        glRotatef(self.rotacion_y, 0, 1, 0)
        
        # Dibuja el cuerpo
        glPushMatrix()
        
        if self.acostado:
            glRotatef(-90, 1, 0, 0) 
        else:
            glRotatef(self.inclinacion_cuerpo, 0, 0, 1)
        
        self._draw_cubo(escala=(1.0, 0.5, 0.4), color=COLOR_SUETER) 
        
        # Dibuja la cabeza
        glPushMatrix()
        glTranslatef(1.2, 0.3, 0) 
        
        if not self.acostado:
            glRotatef(self.inclinacion_cabeza, 1, 0, 0) 
            glRotatef(self.inclinacion_cabeza_lateral, 0, 0, 1) 
            
        self._draw_cubo(escala=(0.4, 0.4, 0.35), color=COLOR_LOBO) 
        self._dibujar_expresion()
        
        # Dibuja el hocico (superior, nariz, inferior)
        glPushMatrix()
        glTranslatef(0.4, -0.05, 0) 
        self._draw_cubo(escala=(0.2, 0.07, 0.2), color=COLOR_HOCICO)
        glPushMatrix()
        glTranslatef(0.2, 0.0, 0) 
        self._draw_cubo(escala=(0.05, 0.05, 0.05), color=COLOR_NARIZ) 
        glPopMatrix() 
        glPopMatrix() 
        glPushMatrix()
        glTranslatef(0.4, -0.19, 0) 
        glRotatef(self.angulo_hocico, 0, 0, 1) 
        self._draw_cubo(escala=(0.2, 0.07, 0.2), color=COLOR_HOCICO)
        glPopMatrix() 
        
        glPopMatrix() # Fin Cabeza

        # Dibuja las orejas
        glPushMatrix()
        glTranslatef(1.0, 0.8, 0.15); glRotatef(45, 0, 1, 0)
        self._draw_cubo(escala=(0.1, 0.3, 0.05), color=COLOR_LOBO)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.0, 0.8, -0.15); glRotatef(-45, 0, 1, 0)
        self._draw_cubo(escala=(0.1, 0.3, 0.05), color=COLOR_LOBO)
        glPopMatrix()
        
        # Dibuja la cola
        glPushMatrix()
        glTranslatef(-1.2, 0.3, 0)
        glRotatef(self.angulo_cola_pose, 1, 0, 0)  
        glRotatef(self.angulo_cola_meneo, 0, 1, 0) 
        glTranslatef(-0.2, 0, 0)
        self._draw_cubo(escala=(0.3, 0.1, 0.1), color=COLOR_LOBO)
        glPopMatrix() # Fin Cola
        
        glPopMatrix() # Fin Cuerpo
        
        # Dibuja las patas delanteras
        glPushMatrix()
        glTranslatef(0.8, -0.75, 0.25)
        
        if self.acostado:
            glTranslatef(0, 1.0, 0); glRotatef(-90, 1, 0, 0) 
            
        # Pata Delantera Derecha
        glPushMatrix()
        glRotatef(self.angulo_caminar, 0, 0, 1) 
        self._draw_cubo(escala=(0.15, 0.5, 0.1), color=COLOR_PATAS_OSCURAS) 
        glPushMatrix()
        glTranslatef(0, -0.6, 0) 
        self._draw_cubo(escala=(0.15, 0.1, 0.1), color=COLOR_PATITAS_BLANCAS) 
        glPopMatrix() 
        glPopMatrix() # Fin Pata DR
        
        glTranslatef(0, 0, -0.5) 
        
        # Pata Delantera Izquierda
        glPushMatrix()
        glRotatef(-self.angulo_caminar, 0, 0, 1) 
        self._draw_cubo(escala=(0.15, 0.5, 0.1), color=COLOR_PATAS_OSCURAS)
        glPushMatrix()
        glTranslatef(0, -0.6, 0) 
        self._draw_cubo(escala=(0.15, 0.1, 0.1), color=COLOR_PATITAS_BLANCAS) 
        glPopMatrix() 
        glPopMatrix() # Fin Pata DI
        
        glPopMatrix() 

        # Dibuja las patas traseras
        glPushMatrix()
        glTranslatef(-0.8, -0.75, 0.25)
        
        if self.acostado:
            glTranslatef(0, 1.0, 0); glRotatef(-90, 1, 0, 0)
             
        # Pata Trasera Derecha
        glPushMatrix()
        glRotatef(-self.angulo_caminar, 0, 0, 1) 
        self._draw_cubo(escala=(0.15, 0.5, 0.1), color=COLOR_PATAS_OSCURAS)
        glPushMatrix()
        glTranslatef(0, -0.6, 0) 
        self._draw_cubo(escala=(0.15, 0.1, 0.1), color=COLOR_PATITAS_BLANCAS) 
        glPopMatrix() 
        glPopMatrix() # Fin Pata TR
        
        glTranslatef(0, 0, -0.5)
        
        # Pata Trasera Izquierda
        glPushMatrix()
        glRotatef(self.angulo_caminar, 0, 0, 1) 
        self._draw_cubo(escala=(0.15, 0.5, 0.1), color=COLOR_PATAS_OSCURAS)
        glPushMatrix()
        glTranslatef(0, -0.6, 0)
        self._draw_cubo(escala=(0.15, 0.1, 0.1), color=COLOR_PATITAS_BLANCAS) 
        glPopMatrix() 
        glPopMatrix() # Fin Pata TI
        
        glPopMatrix() 
        
        glPopMatrix()

