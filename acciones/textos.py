import pygame
from OpenGL.GL import *

def _draw_text_internal(texto, x, y, fuente, color=(255, 255, 255), fondo=(0, 0, 100, 180)):
    # Función interna para dibujar texto en 2D sobre la pantalla
    glDisable(GL_LIGHTING); glDisable(GL_DEPTH_TEST)
    lineas = texto.strip().split('\n')
    for i, linea in enumerate(lineas):
        text_surface = fuente.render(linea.strip(), True, color, fondo)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glWindowPos2d(x, y - i * 25)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glEnable(GL_DEPTH_TEST); glEnable(GL_LIGHTING)

def draw_vidas(display, vidas_actuales):
    # Dibuja la barra de vidas en la esquina
    fuente = pygame.font.Font(None, 36)
    cuadro_lleno = "X"
    cuadro_vacio = "_" 
    texto_vidas = (cuadro_lleno + " ") * vidas_actuales + (cuadro_vacio + " ") * (5 - vidas_actuales)
    _draw_text_internal(texto_vidas, display[0] - 140, display[1] - 40, fuente, color=(255, 50, 50), fondo=(0,0,0,180))

def draw_game_over_overlay(display):
    # Muestra GAME OVER y  reiniciar
    fuente_grande = pygame.font.Font(None, 72)
    fuente_pequena = pygame.font.Font(None, 36)
    
    texto_go = "GAME OVER"
    texto_reiniciar = "Presiona 'Y' para reiniciar"
    
    x_go = (display[0] // 2) - 150
    x_reiniciar = (display[0] // 2) - 160
    y = display[1] // 2
    
    _draw_text_internal(texto_go, x_go, y + 20, fuente_grande, color=(255, 0, 0), fondo=(0,0,0,180))
    _draw_text_internal(texto_reiniciar, x_reiniciar, y - 30, fuente_pequena, color=(255, 255, 255), fondo=(0,0,0,180))


def draw_instructions_overlay(display):
    # Muestra el menú de los controles
    fuente = pygame.font.Font(None, 24)
    
    texto = """
    CONTROLES DE CÁMARA:
    - Mouse: Rotar camara
    - W,A,S,D: Mover camara
    - Q / E: Subir / Bajar camara
    - Rueda del Mouse: Zoom In / Zoom Out
    - R: Resetear vista de camara
    
    EXPRESIÓN / MOVIMIENTO / SONIDO / ESCENARIO (Teclas 1-7):
    1: Normal, 2: Feliz, 3: Triste, 4: Enojado, 5: Sorpresa, 6: Aullido, 7: Duda
    
    CONTROLES DEL LOBO:
    - Flechas: Mover al lobo
    - X: Acostarse (On/Off)
    - V: Caminar (On/Off)
    - Espacio: Saltar
    - L: Ladrar
    - C: Llamar Asteroide
    
    OTROS:
    - F: Cambiar modo de sombreado
    - M: Musica de fondo (On/Off)
    - H: Ocultar/Mostrar Instrucciones
    - P: Mostrar/Ocultar 'Acerca de'
    - Y: Reiniciar (si mueres)
    - ESC: Salir
    """
    _draw_text_internal(texto, 10, display[1] - 30, fuente)

def draw_acerca_de_overlay(display):
    # Muestra la pantalla Acerca de
    fuente = pygame.font.Font(None, 24)
    texto = """
    ACERCA DE:
    Personaje: Gustavo
    Desarrollado por: JOSE ADRIAN GARCIA MARTINEZ
    Graficación
    Desarrollado con Python, Pygame y PyOpenGL
    """
    _draw_text_internal(texto, 10, display[1] - 30, fuente)

def draw_modo_sombreado(display, modo_actual):
    # Muestra el modo de sombreado actual en la esquina inferior izquierda
    fuente = pygame.font.Font(None, 24)
    modos = [
        "Modo: Gouraud (Suave)",
        "Modo: Flat (Plano)"
    ]
    
    if modo_actual < 0 or modo_actual >= len(modos):
        modo_actual = 0
        
    texto = modos[modo_actual]
    _draw_text_internal(texto, 10, 30, fuente, color=(255, 255, 0), fondo=(0,0,0,180))