"""
Version 4.0 of Gravity Simulation and Galaxy Formation

A Python 2D Simulation of Gravity
Developed by Fraser Love on 06/07/21
Dependencies: Pygame
Ran on CPU - Recommended to use on High-Range CPU

Simulating the force of gravity on celestial bodies and galaxy formation using Newtons laws and conservation of momentum.

This version of the program is designed to be as accurate as possible and therefore is not meant to be ran in real-time.
Instead the program save an image of the simulation after each step, these images can then be combined to create a video
file to show the whole simulation at the desired frame-rate.

Every frame:
- Calculate the weight of each object on every other object
- Resolve the weight vector into x and y magnitudes
- Update each objects velocity and position with the time_step
- Check if particles have collided and if so use conservation of momentum to update new particles mass and velocity
- Draw new objects on screen
"""
import random, pygame, sys, math, time
from math import sqrt
from pygame.locals import *

initial_objects = 1000   # Number of initial objects in the simulation
object_list = []
object_radius = 2
G = 6.67408e-11         # Gravitational constant
time_step = 5000       # How much time has passed between every calculation - (lower more accurate: recommend < 10000)
max_v = 100             # A maximum velocity for objects to minimise inaccurate integrals of velocity
dimensions = (1920, 1080)
mass_to_radius_factor = 10
max_initial_velocity = 10
max_initial_mass = 40
min_initial_mass = 10

start_time = time.time()

pygame.init()
display = pygame.display.set_mode(dimensions)
display.fill(pygame.Color("black"))
clock = pygame.time.Clock()

class MassObject:
    def __init__(self, mass, x_pos, y_pos, x_vel, y_vel):
        self.mass = mass
        self.radius = (mass / mass_to_radius_factor) ** (1/3)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = x_vel
        self.y_velocity = y_vel

def setup(object_list):
    for i in range(initial_objects):
        object_list.append(MassObject(random.randrange(min_initial_mass, max_initial_mass), random.randrange(1, dimensions[0]), random.randrange(1, dimensions[1]), random.randrange(-max_initial_velocity, max_initial_velocity) / 100000, random.randrange(-max_initial_velocity, max_initial_velocity) / 100000))

def add_force(object):
    x_acc = y_acc = 0.0
    for other in object_list:
        if other != object:
            r = ((other.x_pos - object.x_pos)**2) + ((other.y_pos - object.y_pos)**2)
            fg = G * object.mass * other.mass / r
            angle = math.atan2((other.y_pos - object.y_pos), (other.x_pos - object.x_pos))
            x_acc += fg * math.cos(angle) / object.mass
            y_acc += fg * math.sin(angle) / object.mass
    return x_acc, y_acc

def update_pos(object_list):
    for object in object_list:
        x_acc, y_acc = add_force(object)
        object.x_velocity += x_acc * time_step
        object.x_pos += object.x_velocity * time_step
        object.y_velocity += y_acc * time_step
        object.y_pos += object.y_velocity * time_step

def check_collisions(object_list):
    max_mass = 0
    for object in object_list:
        for other in object_list:
            if object != other and object.mass > other.mass:
                collision_radius = object.radius / 2
                if (collision_radius > abs(other.x_pos - object.x_pos)) and (collision_radius > abs(other.y_pos - object.y_pos)):
                    object.x_velocity = (object.x_velocity * object.mass + other.x_velocity * other.mass) / (object.mass + other.mass)
                    object.y_velocity = (object.y_velocity * object.mass + other.y_velocity * other.mass) / (object.mass + other.mass)
                    object.mass += other.mass
                    object.radius = (object.mass / mass_to_radius_factor) ** (1/3)
                    object_list.remove(other)

        if object.mass >= max_mass:
            max_mass = object.mass
    return max_mass

def draw(object_list, max_mass):
    display.fill(pygame.Color("black"))
    for object in object_list:
        brightness = int((math.log(object.mass) / math.log(max_mass)) * 255)
        pygame.draw.circle(display, (brightness, brightness, brightness), (int(object.x_pos), int(object.y_pos)), int(object.radius), 0)
    pygame.display.update()

def main():
    setup(object_list)
    step = 1
    while True:
        pygame.display.set_caption('Gravity Simulation: Step {}    RealTime: {}     Objects: {}'.format(str(step), round(time.time() - start_time, 2), len(object_list)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
        max_mass = check_collisions(object_list)
        draw(object_list, max_mass)
        update_pos(object_list)
        step += 1
        pygame.image.save(display, "images/{}.jpg".format(step))

main()
