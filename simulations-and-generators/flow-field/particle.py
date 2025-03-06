"""
Particle and vector objects used in Perlin noise flow field

Created 13/08/19
Developed by Fraser Love
"""
import math

class Particle():
    def __init__(self, pos):
        self.pos = pos
        self.velocity = Vector()
        self.acc = Vector()
        self.max_speed = 15 # The maximum speed a particle can travel at, acts similarly to drag

    def update(self, dimensions):
        """ Updating the particles position, velocity and acceleration """
        self.velocity.update(self.acc)
        self.velocity.limit(self.max_speed)
        self.pos.update(self.velocity, dimensions)
        self.acc = Vector(0,0)

    def follow(self, flowfield, scale, cols):
        """ Finds the flowfield force vector the particle lies on and applies the force to the particle """
        x = self.pos.x // scale
        y = self.pos.y // scale
        index = int(x + y * cols)
        force = flowfield[index]
        self.acc.update(force)

class Vector:
    """ A vector object stored as a magnitude and direction or x and y components with methods
        to allow two 2D vectors to be added and vectors to be resolved into components """

    def __init__(self, x = 0, y = 0, angle = None, mag = 1):
        if angle:
            self.x = mag * math.cos(angle)
            self.y = mag * math.sin(angle)
        else:
            self.x = x
            self.y = y

    def unit(self):
        """ Returns the unit vector of the current vector """
        mag = math.hypot(self.x, self.y)
        if mag == 0:
            return Vector(0, 0)
        return Vector(self.x / mag, self.y / mag)

    def update(self, other, dimensions = None):
        """ Updates the vector by doing vector addition and if the vector is a position
            vector then checks to see if it can be wrapped to the other side of the screen """
        self.x += other.x
        self.y += other.y
        if dimensions:
            self.x %= dimensions[0]
            self.y %= dimensions[1]

    def limit(self, max_mag):
        """ Limits vector magnitude to max_mag """
        mag = math.hypot(self.x, self.y)
        if mag > max_mag:
            ratio = max_mag / mag
            self.x *= ratio
            self.y *= ratio
