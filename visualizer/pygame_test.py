__author__ = 'katja'
import sys
import pygame
import math

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 500))
done = False

UNIT = 10

center = (50,50)
angle = 90
vertices = []


def rotatePoint(point):
    """Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    a = math.radians(angle)
    temp_point = point[0]-center[0] , point[1]-center[1]
    temp_point = (temp_point[0]*math.cos(a)-temp_point[1]*math.sin(a), temp_point[0]*math.sin(a)+temp_point[1]*math.cos(a))
    temp_point = temp_point[0]+center[0] , temp_point[1]+center[1]
    return temp_point

def getVertices():
    """center is an x,y-tuple; angle is a float"""
    global vertices
    a = (center[0]-1*UNIT, center[1]-1*UNIT)
    b = (center[0]-1*UNIT, center[1]+1*UNIT)
    c = (center[0]+2*UNIT, center[1])  # triangle head

    a = rotatePoint(a)
    b = rotatePoint(b)
    c = rotatePoint(c)

    vertices = [a,b,c]


def move(steps):
    global center
    a = math.radians(angle)
    sine = math.sin(a)
    cosine = math.cos(a)

    center = (center[0]+steps*UNIT*cosine, center[1]+steps*UNIT*sine)


getVertices()

while not done:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                move(1)
                getVertices()
            if event.key == pygame.K_LEFT:
                angle = angle+5
                getVertices()
            if event.key == pygame.K_RIGHT:
                angle = angle-5
                getVertices()


    pygame.draw.polygon(screen, (0, 128, 255), vertices)
    pygame.display.flip()
    clock.tick(60)



