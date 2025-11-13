from OpenGL.GL import *

def setup_lighting():
    # Configura las propiedades de la iluminación principal de la escena
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1])

def update_light_position():
    # Actualiza la posición de la luz en cada frame para que parezca fija en el mundo
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 10, 20, 1])

