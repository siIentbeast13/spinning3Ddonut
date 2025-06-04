import pygame
from math import pi, sin, cos
from random import randint


pygame.init()


def to_world_position(position:list[float,float]):
    return 400+position[0], 400-position[1]


screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
fov = 200


vertices = [
]


i=0
while i<2*pi:
    angle = 0
    while angle < 2*pi:
        vertices.append([(50+i*10)*sin(angle), (50+i*10)*cos(angle), sin(i)*20])
        if i > 0:
            vertices.append([(50+i*10)*sin(angle), (50+i*10)*cos(angle), -sin(i)*20])
        if i < 3:
            angle += 0.1
        else:
            angle += 0.05
    i+=0.1


def rotate_x(angle, vertices):
    for vertex in vertices:
        x, y, z = vertex
        vertex[1] = y*cos(angle) - z*sin(angle)
        vertex[2] = y*sin(angle) + z*cos(angle)

def rotate_y(angle, vertices):
    for vertex in vertices:
        x, y, z = vertex
        vertex[0] = x*cos(angle) + z*sin(angle)
        vertex[2] = -x*sin(angle) + z*cos(angle)



def pointVertices(vertices):
    tmpVertices = []
    for vertex in vertices:
        tmpVertices.append((vertex[2], vertex))
    tmpVertices.sort()
    sortedVertices = []
    for vertex in tmpVertices:
        sortedVertices.append(vertex[1])
    sortedVertices.reverse()

    vertices2D = []
    for vertex in sortedVertices:
        vertices2D.append((vertex[0]*fov/(vertex[2]+fov), vertex[1]*fov/(vertex[2]+fov)))
    
    i=0
    for vertex in vertices2D:
        c = max(min(200-sortedVertices[i][2], 255), 0)
        pygame.draw.circle(screen, (c,c,c), to_world_position(vertex), 3)
        i+=1

rotatingUp = False
rotatingDown = False
rotatingRight = False
rotatingLeft = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rotatingUp = True
            if event.key == pygame.K_DOWN:
                rotatingDown = True
            if event.key == pygame.K_LEFT:
                rotatingLeft = True
            if event.key == pygame.K_RIGHT:
                rotatingRight = True
            if event.key == pygame.K_EQUALS:
                fov -= 10
            if event.key == pygame.K_MINUS:
                fov += 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                rotatingUp = False
            if event.key == pygame.K_DOWN:
                rotatingDown = False
            if event.key == pygame.K_LEFT:
                rotatingLeft = False
            if event.key == pygame.K_RIGHT:
                rotatingRight = False
    screen.fill((0,0,0))

    rotate_x(0.1*(-int(rotatingUp) + int(rotatingDown)), vertices)
    rotate_y(0.1*(int(rotatingRight) - int(rotatingLeft)), vertices)

    pointVertices(vertices)
    
    pygame.display.flip()
    clock.tick(120)