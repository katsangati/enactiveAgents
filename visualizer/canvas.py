import math
from copy import deepcopy

UNIT = 10
BORDER = UNIT*2
WIDTH = 300
HEIGHT = 300
BLUE = (0, 128, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Agent:
    def __init__(self, center):
        self.center = center
        self.angle = 90
        self.get_vertices()
        self.color = BLUE

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
        self.color = BLUE
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
            self.color = RED
            return False
        return True

    def rotate(self, angle):
        self.color = BLUE
        self.angle += angle
        old_vertices = deepcopy(self.vertices)
        self.get_vertices()
        if not self.check_inside():
            self.vertices = old_vertices
            self.angle -= angle

    def feel_front(self, steps):
        self.color = GREEN
        a = math.radians(self.angle)
        sine = math.sin(a)
        cosine = math.cos(a)
        old_vertices = deepcopy(self.vertices)
        old_center = deepcopy(self.center)
        self.center = (self.center[0]+steps*UNIT*cosine, self.center[1]+steps*UNIT*sine)
        self.get_vertices()
        clear_ahead = self.check_inside()
        self.vertices = old_vertices
        self.center = old_center
        return clear_ahead

    def check_inside(self):
        """returns true if all the vertices are inside the field"""
        if self.center[0]-BORDER < 0 or self.center[0]+BORDER > WIDTH:
            return False
        if self.center[1]-BORDER < 0 or self.center[1]+BORDER > HEIGHT:
            return False
        return True

    def feel(self):
        return None