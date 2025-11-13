import pygame
import os

def cargar_sonidos():
    # Carga todos los archivos de efectos de sonido desde la carpeta sonidos
    sounds = {}
    
    sound_files = {
        'aterrizaje': 'aterrizaje.mp3',
        'triste': 'triste.mp3',
        'feliz': 'feliz.mp3',
        'normal': 'normal.mp3',
        'enojado': 'enojado.mp3',
        'sorpresa': 'sorpresa.mp3',
        'aullido': 'aullido.mp3', 
        'duda': 'duda.mp3',
        'ladrido': 'ladrido.mp3',
        'impacto': 'impacto.mp3'
    }
    
    ruta_sonidos = 'sonidos'
    if not os.path.exists(ruta_sonidos):
        os.makedirs(ruta_sonidos)
        
    for name, filename in sound_files.items():
        path = os.path.join(ruta_sonidos, filename)
        if os.path.exists(path):
            sounds[name] = pygame.mixer.Sound(path)
            sounds[name].set_volume(0.5)
    return sounds

def reproducir(nombre, sonidos_dict):
    # Reproduce un efecto de sonido del diccionario
    if nombre in sonidos_dict:
        sonidos_dict[nombre].play()

def cargar_musica_fondo(archivo_musica="fondo.mp3"):
    # Carga el archivo de música de fondo 
    ruta_musica = os.path.join('sonidos', archivo_musica)
    if os.path.exists(ruta_musica):
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.set_volume(0.7)

def toggle_musica_fondo():
    # Alterna entre reproducir y detener la música de fondo
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.play(-1)

