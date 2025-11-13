from OpenGL.GL import *
from PIL import Image
import os

_texturas = []

def _load_single_texture(filename):
    # Carga una imagen, crea una textura OpenGL y devuelve su ID
        img = Image.open(filename).convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.tobytes()
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        return texture_id

def init_escenarios():
    # Carga todas las texturas del escenario y las almacena en una lista
    global _texturas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_imagenes = os.path.join(script_dir, '..', 'imagenes')
    
    nombres_escenarios = ["normal", "feliz", "triste", "enojado", "sorpresa", "aullido", "duda"]
    
    _texturas = []
    for nombre in nombres_escenarios:
        ruta = os.path.join(ruta_imagenes, f"{nombre}.png")
        _texturas.append(_load_single_texture(ruta))

def draw_escenario(index):
    # Dibuja un un cubo gigante usando la textura indicada
    if index >= len(_texturas) or _texturas[index] is None: 
        index = 0 
    if _texturas[index] is None:
        return 

    texture_id = _texturas[index]
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glDisable(GL_LIGHTING)
    glColor3f(1,1,1)
    
    q = 50.0 
    glBegin(GL_QUADS); glTexCoord2f(0, 0); glVertex3f(-q, -q, -q); glTexCoord2f(1, 0); glVertex3f(q, -q, -q); glTexCoord2f(1, 1); glVertex3f(q, q, -q); glTexCoord2f(0, 1); glVertex3f(-q, q, -q); glEnd()
    glBegin(GL_QUADS); glTexCoord2f(1, 0); glVertex3f(-q, -q, q); glTexCoord2f(0, 0); glVertex3f(q, -q, q);  glTexCoord2f(0, 1); glVertex3f(q, q, q); glTexCoord2f(1, 1); glVertex3f(-q, q, q); glEnd()
    glBegin(GL_QUADS); glTexCoord2f(0, 1); glVertex3f(-q, -q, -q); glTexCoord2f(1, 1); glVertex3f(q, -q, -q); glTexCoord2f(1, 0); glVertex3f(q, -q, q); glTexCoord2f(0, 0); glVertex3f(-q, -q, q); glEnd()
    glBegin(GL_QUADS); glTexCoord2f(0, 0); glVertex3f(-q, q, -q); glTexCoord2f(1, 0); glVertex3f(q, q, -q); glTexCoord2f(1, 1); glVertex3f(q, q, q); glTexCoord2f(0, 1); glVertex3f(-q, q, q); glEnd()
    glBegin(GL_QUADS); glTexCoord2f(1, 0); glVertex3f(-q, -q, q); glTexCoord2f(0, 0); glVertex3f(-q, -q, -q); glTexCoord2f(0, 1); glVertex3f(-q, q, -q); glTexCoord2f(1, 1); glVertex3f(-q, q, q); glEnd()
    glBegin(GL_QUADS); glTexCoord2f(0, 0); glVertex3f(q, -q, -q); glTexCoord2f(1, 0); glVertex3f(q, -q, q); glTexCoord2f(1, 1); glVertex3f(q, q, q); glTexCoord2f(0, 1); glVertex3f(q, q, -q); glEnd()

    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)

