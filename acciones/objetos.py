from OpenGL.GL import *
from OpenGL.GLU import * 
COLOR_CONTORNO = (0.1, 0.1, 0.1)
_quadric = None 

def draw_cube(escala=(1, 1, 1)):
    # Dibuja un cubo 3D con normales para iluminación y un contorno oscuro.
    glPushMatrix()
    glScalef(escala[0], escala[1], escala[2])
    
    vertices = [ [1,-1,-1], [1,1,-1], [-1,1,-1], [-1,-1,-1], [1,-1,1], [1,1,1], [-1,-1,1], [-1,1,1] ]
    normals = [ [0,0,-1], [0,0,1], [0,-1,0], [0,1,0], [-1,0,0], [1,0,0] ]
    faces = [ (0,1,2,3,0), (6,7,5,4,1), (0,3,6,4,2), (5,1,2,7,3), (2,3,6,7,4), (4,5,1,0,5) ]
    edges = [ (0,1), (1,2), (2,3), (3,0), (4,5), (5,7), (7,6), (6,4), (0,4), (1,5), (2,7), (3,6) ]

    glBegin(GL_QUADS)
    for face in faces:
        glNormal3fv(normals[face[4]])
        for i in face[:4]: glVertex3fv(vertices[i])
    glEnd()
    
    glDisable(GL_LIGHTING)
    glColor3fv(COLOR_CONTORNO)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge: glVertex3fv(vertices[vertex])
    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()

def draw_arbol(posicion):
    # Dibuja un árbol 
    glPushMatrix()
    glTranslatef(posicion[0], posicion[1], posicion[2])
    
    # Tronco
    glColor3f(0.5, 0.3, 0.1)
    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    draw_cube(escala=(0.5, 1.5, 0.5))
    glPopMatrix()
    
    # Hojas
    glColor3f(0.1, 0.6, 0.2)
    glPushMatrix()
    glTranslatef(0, 3.5, 0)
    draw_cube(escala=(1.2, 1.0, 1.2))
    glPopMatrix()
    
    glPopMatrix()

def draw_asteroide(posicion):
    # Dibuja una esfera para simular un asteroide
    global _quadric
    if _quadric is None:
        _quadric = gluNewQuadric()
        gluQuadricNormals(_quadric, GLU_SMOOTH)
    
    glPushMatrix()
    glTranslatef(posicion[0], posicion[1], posicion[2])
    glColor3f(0.4, 0.4, 0.4) 
    gluSphere(_quadric, 1.0, 32, 32) 
    glPopMatrix()


def draw_arbusto(posicion, color):
    # Dibuja un arbusto (esfera) con color personalizable
    global _quadric
    if _quadric is None:
        _quadric = gluNewQuadric()
        gluQuadricNormals(_quadric, GLU_SMOOTH)
    
    glPushMatrix()
    glTranslatef(posicion[0], posicion[1], posicion[2])
    
    glColor3fv(color) # Color dinámico
    
    gluSphere(_quadric, 1.5, 32, 32) 
    glPopMatrix()

def draw_flor(posicion, color, escala=1.0):
    # Dibuja una flor/cristal simple (dos cubos)
    glPushMatrix()
    glTranslatef(posicion[0], posicion[1] + 0.5 * escala, posicion[2])
    glScalef(escala, escala, escala)
    
    glColor3fv(color)
    
    glPushMatrix()
    glRotatef(45, 0, 1, 0)
    draw_cube(escala=(0.2, 0.7, 0.2))
    glPopMatrix()
    
    glPushMatrix()
    glRotatef(-45, 0, 1, 0)
    draw_cube(escala=(0.2, 0.7, 0.2))
    glPopMatrix()
    
    glPopMatrix()

def draw_corazon(posicion, color=(1.0, 0.1, 0.1)):
    glPushMatrix()
    glTranslatef(posicion[0], posicion[1], posicion[2])
    glScalef(0.5, 0.5, 0.5)
    
    glPushMatrix()
    glColor3fv(color) # <--- Color para el cubo 1
    glTranslatef(0, 0.5, 0); draw_cube(escala=(0.5, 0.5, 0.5))
    glPopMatrix()
    
    glPushMatrix()
    glColor3fv(color) # <--- Color para el cubo 2
    glTranslatef(0, 1.2, 0); draw_cube(escala=(1.0, 0.5, 0.5))
    glPopMatrix()
    
    glPushMatrix()
    glColor3fv(color) # <--- Color para el cubo 3
    glTranslatef(-0.7, 1.9, 0); draw_cube(escala=(0.5, 0.5, 0.5))
    glPopMatrix()
    
    glPushMatrix()
    glColor3fv(color) # <--- Color para el cubo 4
    glTranslatef(0.7, 1.9, 0); draw_cube(escala=(0.5, 0.5, 0.5))
    glPopMatrix()
    
    glPopMatrix()