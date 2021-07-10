import pygame, math

class Branch():
    """ A branch object storing a the start and end vectors and with methods to draw itself on screen and create new branches """
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.angle_offset = math.pi
        self.finished = False

    def show(self, display, branch_colour):
        pygame.draw.aaline(display, branch_colour, (self.start.x, self.start.y), (self.end.x, self.end.y), 1)

    def branch_off(self, angle, branch_reduction):
        """ Creating a new branch by calculating a vector betwen the start and end positions then rotating the vector by a given angle
            and then reducing the size of the branch so that we can finally add it to the end of the last branch """
        dir = Vector(v1=self.end, v2=self.start)
        dir.rotate(self.angle_offset+angle)
        dir.scalar_multi(branch_reduction)
        new_end = self.add_vectors(self.end, dir)
        new_branch = Branch(self.end, new_end)
        return new_branch

    def add_vectors(self, v1, v2):
        new_vector = Vector(v1.x-v2.x, v1.y-v2.y)
        return new_vector


class Vector():
    """ An object to store a vectors x and y values and provide methods of rotating it and multiplying it by a vector """
    def __init__(self, x=0, y=0, v1=None, v2=None):
        if v1 == None:
            self.x = x
            self.y = y
        else:
            self.x = v1.x - v2.x
            self.y = v1.y - v2.y

    def rotate(self, angle):
        x = self.x
        y = self.y
        self.x = x * math.cos(angle) - y * math.sin(angle)
        self.y = x * math.sin(angle) + y * math.cos(angle)

    def scalar_multi(self, scalar):
        self.x *= scalar
        self.y *= scalar
