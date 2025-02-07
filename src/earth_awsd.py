import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from PIL import Image

angle_x, angle_y, angle_sun = 0, 0, 0  # Rotation angles for navigation

# Load image
image = Image.open("map2.jpg").convert("RGB")
image_width, image_height = image.size
pixels = image.load()

H, W = 200, 200  # Number of stacks and slices

def setup_lighting():
    """ Sets up OpenGL lighting with a moving sun that is independent of Earth's rotation. """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Sun moves in a circular path independent of Earth's rotation
    radius_sun_orbit = 5  # Distance of the sun from the Earth
    light_x = math.cos(math.radians(angle_sun)) * radius_sun_orbit
    light_y = math.sin(math.radians(angle_sun)) * radius_sun_orbit
    light_z = 0  # Keep some height to simulate realistic lighting

    light_position = [light_x, light_y, light_z, 0]  # Directional light

    ambient_light = [0.2, 0.2, 0.2, 0.5]
    diffuse_light = [0.8, 0.8, 0.8, 1.0]
    specular_light = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    # glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    # glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)



def draw_sphere(radius, slices, stacks):
    setup_lighting()
    """ Renders a sphere with per-vertex coloring from the image. """
    for i in range(stacks):
        lat0 = -math.pi * (-0.5 + (i / stacks))
        lat1 = -math.pi * (-0.5 + ((i + 1) / stacks))
        z0, zr0 = math.sin(lat0), math.cos(lat0)
        z1, zr1 = math.sin(lat1), math.cos(lat1)
        
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * (j / slices)
            x, y = math.cos(lng), math.sin(lng)

            img_x = int(j / slices * (image_width - 1))
            img_y0 = int(i / stacks * (image_height - 1))
            img_y1 = int((i + 1) / stacks * (image_height - 1))
            
            color0 = pixels[img_x, img_y0]
            color1 = pixels[img_x, img_y1]
            
            glColor3f(color0[0] / 255, color0[1] / 255, color0[2] / 255)
            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)

            glColor3f(color1[0] / 255, color1[1] / 255, color1[2] / 255)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
        glEnd()


def display():
    global angle_x, angle_y, angle_sun
    angle_sun += 1.5  # Adjust speed of sun movement
    if angle_sun >= 360:
        angle_sun -= 360  # Keep it within 0-360 degrees
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(5, 0, 0, 0, 0, 0, 0, 0, 1)

    glRotatef(angle_x, 0, 1, 0)
    glRotatef(angle_y, 0, 0, 1)
    draw_sphere(1, W, H)

    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 1, 10)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global angle_x, angle_y
    if key == b'w':
        angle_x -= 5
    elif key == b's':
        angle_x += 5
    elif key == b'a':
        angle_y -= 5
    elif key == b'd':
        angle_y += 5
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Navigable Earth")

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    
    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)
    # setup_lighting()
    
    glutMainLoop()


if __name__ == "__main__":
    main()
