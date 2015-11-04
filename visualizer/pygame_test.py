import pygame
import math
from copy import deepcopy
import random

__author__ = 'katja'


pygame.init()
clock = pygame.time.Clock()

UNIT = 10
BORDER = UNIT*2
WIDTH = 600
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False


class Agent:
    def __init__(self, center):
        self.center = center
        self.angle = 90
        self.get_vertices()

    def get_vertices(self):
        """center is an x,y-tuple; angle is a float"""
        a = self.rotate_point((self.center[0]-1*UNIT, self.center[1]-1*UNIT))
        b = self.rotate_point((self.center[0]-1*UNIT, self.center[1]+1*UNIT))
        c = self.rotate_point((self.center[0]+2*UNIT, self.center[1]))  # triangle head
        self.vertices = [a,b,c]

    def rotate_point(self, point):
        """Rotates a point around another centerPoint. Angle is in degrees.
        Rotation is counter-clockwise"""
        a = math.radians(self.angle)
        temp_point = point[0]-self.center[0], point[1]-self.center[1]
        temp_point = (temp_point[0]*math.cos(a)-temp_point[1]*math.sin(a), temp_point[0]*math.sin(a)+temp_point[1]*math.cos(a))
        temp_point = temp_point[0]+self.center[0] , temp_point[1]+self.center[1]
        return temp_point

    def move(self, steps):
        a = math.radians(self.angle)
        sine = math.sin(a)
        cosine = math.cos(a)
        old_vertices = deepcopy(self.vertices)
        old_center = deepcopy(self.center)
        self.center = (self.center[0]+steps*UNIT*cosine, self.center[1]+steps*UNIT*sine)
        self.get_vertices()
        if not self.check_inside():
            self.vertices = old_vertices
            self.center = old_center

    def rotate(self, angle):
        self.angle += angle
        old_vertices = deepcopy(self.vertices)
        self.get_vertices()
        if not self.check_inside():
            self.vertices = old_vertices
            self.angle -= angle

    def check_inside(self):
        """returns true or false for whether any of the vertices is inside the field"""
        if self.center[0]-BORDER < 0 or self.center[0]+BORDER > WIDTH:
            return False
        if self.center[1]-BORDER < 0 or self.center[1]+BORDER > HEIGHT:
            return False
        return True

kenny = Agent((random.randint(BORDER,WIDTH-BORDER), random.randint(BORDER,HEIGHT-BORDER)))

while not done:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                kenny.move(1)
            if event.key == pygame.K_LEFT:
                kenny.rotate(5)
            if event.key == pygame.K_RIGHT:
                kenny.rotate(-5)

    pygame.draw.polygon(screen, (0, 128, 255), kenny.vertices)
    pygame.display.flip()
    clock.tick(60)



