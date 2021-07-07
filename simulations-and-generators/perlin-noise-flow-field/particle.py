"""
Particle and vector objects used in Perlin noise flow field

Created 13/08/19
Developed by Fraser Love
"""
import math, random, flow_field

class Particle():
    """ A particle object with info on position, velocity and acceleration with methods
        to update these values by inputting a force """
    def __init__(self):
        self.pos = Vector(x=random.randint(0,flow_field.dimensions[0]),y=random.randint(0,flow_field.dimensions[1]))
        self.velocity = Vector(x=0,y=0)
        self.acc = Vector(x=0,y=0)
        self.max_speed = 15 # The maximum speed a particle can travel at, acts similarly to drag

    def update(self):
        """ Updating the particles position, velocity and acceleration """
        self.velocity.update_vector(self.acc, False)
        self.velocity.limit_speed(self.max_speed)
        self.pos.update_vector(self.velocity, True)
        self.acc = Vector(0,0)

    def follow(self, flowfield):
        """ Finds the flowfield force vector the particle lies on and applies the force to the particle """
        x = self.pos.x // flow_field.scale
        y = self.pos.y // flow_field.scale
        index = int(x + y * flow_field.cols)
        force = flowfield[index]
        self.acc.update_vector(force, False)

class Vector:
    """ A vector object stored as a magnitude and direction or x and y components with methods
        to allow two 2D vectors to be added and vectors to be resolved into components """
    def __init__(self, angle=None, magnitude=1, x=None, y=None):
        if angle != None:
            self.angle = angle
            self.magnitude = magnitude
            self.resolve_vector()
        else:
            self.x = x
            self.y = y

    def resolve_vector(self):
        """ Resolves a vector into its x and y components to allow for vector addition """
        self.x = self.magnitude * math.cos(self.angle)
        self.y = self.magnitude * math.sin(self.angle)
        # Only display coordinates to show vector - not used in any calculations
        self.display_x = math.cos(self.angle)
        self.display_y = math.sin(self.angle)

    def update_vector(self, other, is_position):
        """ Updates the vector by doing vector addition and if the vector is a position
            vector then checks to see if it can be wrapped to the other side of the screen """
        self.x += other.x
        self.y += other.y
        if is_position:
            self.x = self.x % flow_field.dimensions[0]
            self.y = self.y % flow_field.dimensions[1]

    def limit_speed(self, max_speed):
        """ Function to calculate the velocity vectors speed and reduce the speed to less than
            the maximum speed """
        speed = math.hypot(self.x, self.y)
        if speed > max_speed:
            speed = max_speed
        theta = math.atan2(self.x, self.y)
        self.x = speed * math.sin(theta)
        self.y = speed * math.cos(theta)
