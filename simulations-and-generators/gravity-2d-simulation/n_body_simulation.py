'''
N-body simulation
Author: Fraser Love, me@fraser.love
Created: 2021-07-06
Latest Release: v1.0.2, 2021-07-08
Python: v3.9.6
Dependencies: pygame

Simulating how N-bodies interact using gravitation as described newtonian physics. This program requires a huge amount of
computation and therefore cannot be ran in real-time. Instead images are saved at each time-step in the simulation, these
images can then be combined to create a video of the simulation at the desired frame-rate. It is reccomended to run this
simulation on a powerful CPU to speed up computation.
'''

import random, sys, math, time, os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

initial_objects = 1000   # Number of initial objects in the simulation
object_list = []  # List to hold all of the MassObjects in the simulation
G = 6.67408e-11  # Gravitational constant
time_step = 2500  # How much time has passed between every calculation - (lower more accurate: recommend < 10000)
max_v = 100  # A maximum velocity for objects to minimise inaccurate integrals of velocity
dimensions = (1920, 1080)  # Dimensions of the simulation
mass_to_radius_factor = 10  # Amount to which the radius should be scaled down by according to its weight
max_initial_velocity = 10  # Maximum initial velocity of objects
max_initial_mass = 40  # Maximum starting mass of objects
min_initial_mass = 10  # Minimum starting mass of objects
collisions = False  # Enables or disables particle collisions


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


def acceleration(object):
    a, ax, ay = 0, 0, 0
    for other in object_list:
        if other != object:
            dx = other.x_pos - object.x_pos
            dy = other.y_pos - object.y_pos
            r_sqr = (dx * dx) + (dy * dy)
            if r_sqr != 0:
                a = G * other.mass / r_sqr
            angle = math.atan2(dy, dx)
            ax += a * math.cos(angle)
            ay += a * math.sin(angle)
    return ax, ay


def update_pos(object_list):
    for object in object_list:
        ax, ay = acceleration(object)
        object.x_velocity += ax * time_step
        object.x_pos += object.x_velocity * time_step
        object.y_velocity += ay * time_step
        object.y_pos += object.y_velocity * time_step


def check_collisions(object_list):
    max_mass = 0
    for object in object_list:
        if collisions:
            for other in object_list:
                if object != other and object.mass > other.mass:
                    collision_radius = object.radius
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
    start_time = time.time()
    pygame.init()
    display = pygame.display.set_mode(dimensions)
    setup(object_list)
    step = 1
    os.makedirs("images/", exist_ok=True)
    while True:
        pygame.display.set_caption('Gravity Simulation     Step: {}     Time: {}    Objects: {}'.format(str(step), round(time.time() - start_time, 2), len(object_list)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
        max_mass = check_collisions(object_list)
        draw(object_list, max_mass)
        update_pos(object_list)
        pygame.image.save(display, "images/{}.jpg".format(step))
        step += 1


if __name__ == '__main__':
    main()
