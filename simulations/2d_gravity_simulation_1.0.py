"""
Version 1.0 of Gravity Simulation and Galaxy Formation
Version 2.0 relased with updated code - see github (https://github.com/FraserLove/python/simulations)

A Python 3.7 2D Simulation of Gravity
Developed by Fraser Love from 7/10/18 to 12/10/18
Dependencies: Pygame
Ran on CPU - Reccomended to use on High-Range CPU

Simulating the force of gravity on cellestial bodies and galaxy formation using Newtons laws,
with the Euler Method of Integration.
Measures the change in velocity and displacement after every time_step

Euler method assumes constant acceletation throught the whole timestep. This normally doesnt impact on results
to much but becomes noticible if accceleration rapidly increases like when two objects in close proximity pass by one another
and can lead to unequal calcualtion of force of gravity and send objects
spiraling out to infinity. An updatated version will be developed soon using the 2nd order
leapfrog integration method which gives more accurate values. This will mean no spiriling to infinity when objects pass in
close proximity to eachother and will lead to much better results for galaxy formation.

The Euler method is sympletic meaning that grabitational orbits should stay stable. A small enough time_step
will ensure that the acceleration is measured as accurate as possible and will lead to a more accurate simulation.

Every frame:
- Calculate the weight of each object to every other object
- Reslove the weight vector into x and y magnitudes
- Use Euler method to update velocity and position with the time_step
- Check if particles have collided and if so use conservation of momentum to update new particles mass and velocity
- Draw new objects on screen
"""
import random, pygame, sys, math
from pygame.locals import *

initial_objects = 200   # Number of initial objects in the simulation
object_list = []
G = 0.000067            # Gravitational constant
time_step = 10          # How much time has passed between every calculation
frame_rate = 60

pygame.init()
display = pygame.display.set_mode((1250,700))
display.fill(pygame.Color("black"))
clock = pygame.time.Clock()

class MassObject:
    def __init__(self, mass, x_pos, y_pos, x_vel, y_vel):
        self.mass = mass
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = x_vel
        self.y_velocity = y_vel

def setup(object_list):
    for i in range(initial_objects):
        object_list.append(MassObject(random.randrange(1, 100), random.randrange(1, 1250), random.randrange(1, 700), 0, 0))

def add_force(object_list, fg_x_list, fg_y_list):
    for object in object_list:
        fg_x = 0.0
        fg_y = 0.0
        for other in object_list:
            if other != object and object.x_pos - other.x_pos != 0:
                r = ((other.x_pos - object.x_pos)**2) + ((other.y_pos - object.y_pos)**2)
                fg = G * object.mass * other.mass / r
                angle = math.atan2((other.y_pos - object.y_pos), (other.x_pos - object.x_pos))
                fg_x += fg * math.cos(angle)
                fg_y += fg * math.sin(angle)
        fg_x_list[object_list.index(object)] = fg_x
        fg_y_list[object_list.index(object)] = fg_y

def update_pos(object_list, fg_x_list, fg_y_list):
    for object in object_list:
        object.x_velocity += fg_x_list[object_list.index(object)] / object.mass * time_step
        object.y_velocity += fg_y_list[object_list.index(object)] / object.mass * time_step
        object.x_pos += object.x_velocity * time_step
        object.y_pos += object.y_velocity * time_step

def check_collisions(object_list):
    for object in object_list:
        for other in object_list:
            if object != other:
                if (other.x_pos - object.x_pos < 10 and other.x_pos - object.x_pos > -10) and (other.y_pos - object.y_pos < 10 and other.y_pos - object.y_pos > -10):
                    object.x_velocity = (object.x_velocity * object.mass + other.x_velocity * other.mass) / (object.mass + other.mass)
                    object.y_velocity = (object.y_velocity * object.mass + other.y_velocity * other.mass) / (object.mass + other.mass)
                    object.mass += other.mass
                    object_list.remove(other)

def draw(object_list):
    for object in object_list:
        pygame.draw.rect(display, (255,255,255), (object.x_pos, object.y_pos, 5, 5), 0)
    pygame.display.update()
    clock.tick(frame_rate)

def main():
    setup(object_list)
    step = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
        display.fill(pygame.Color("black"))
        step += 1
        fg_x_list = [0 for i in range(len(object_list))]
        fg_y_list = [0 for i in range(len(object_list))]
        add_force(object_list, fg_x_list, fg_y_list)
        update_pos(object_list, fg_x_list, fg_y_list)
        check_collisions(object_list)
        draw(object_list)

main()
