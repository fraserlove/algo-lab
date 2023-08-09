"""
A Python 3.7 2D Simulation of The Solar System
Developed by Fraser Love on 12/10/18
Dependencies: Pygame
Ran on CPU - Recommended to use on High-Range CPU

Code based on my Gravity Simulation Version 2.0
Simulating the movement of the solar system using Newtons laws,
with the Euler Method of Integration.
Measures the change in velocity and displacement after every time_step
All true values are used so simulation simulates the real motion of the solar system,
only the simulation has been scaled down to fit the screen and objects enlarged to become visible

Euler method assumes constant acceleration throughout the whole time-step. This normally doesnt impact on results
to much but becomes noticeable if acceleration rapidly increases like when two objects in close proximity pass by one another
and can lead to unequal calculation of force of gravity and send objects
spiraling out to infinity. An updated version will be developed soon using the 2nd order
leapfrog integration method which gives more accurate values. This will mean no spiraling to infinity when objects pass in
close proximity to each other and will lead to much better results for orbit stability

The Euler method is sympletic meaning that the orbit should stay stable. A small enough time_step
will ensure that the acceleration is measured as accurate as possible and will lead to a stable orbit.

Every frame:
- Calculate the weight of each object to every other object
- Resolve the weight vector into x and y magnitudes
- Use Euler method to update velocity and position with the time_step
- Draw new objects on screen
"""
import random, pygame, sys, math, time
from math import sqrt
from pygame.locals import *

# Variables set so in simulation 1 second = 10 days
object_list = []
G = 6.67408e-11  # Gravitational constant
time_step = 28800  # How much time has passed between every calculation - (lower more accurate)
frame_rate = 30  # time passed in sim = current time * time_step * frame_rate
trails = []  # List to store trail objects
trail_len = 100  # Sets the length of the planet trails

pygame.init()
display = pygame.display.set_mode((1250,700))
display.fill(pygame.Color("black"))
clock = pygame.time.Clock()
start_time = time.time()


class MassObject:
    def __init__(self, name, mass, x_pos, y_pos, x_vel, y_vel, colour, radius):
        self.name = name
        self.mass = mass                # In kg
        self.x_pos = x_pos              # In m from sun
        self.y_pos = y_pos              # In m from sun
        self.x_velocity = x_vel         # In km/s
        self.y_velocity = y_vel         # In km/s
        self.colour = colour
        self.radius = radius


def setup(object_list):
    x_mid = 6.25e10
    object_list.append(MassObject("Sun", 2e30, x_mid, 0, 0, 0, (255, 255, 0), 10))
    object_list.append(MassObject("Mercury", 3.285e23, x_mid, 5.7e10, 47000, 0, (0, 255, 255), 2))
    object_list.append(MassObject("Venus", 4.8e24, x_mid, 1.1e11, 35000, 0, (0, 255, 0), 4))
    object_list.append(MassObject("Earth", 6e24, x_mid, 1.5e11, 30000, 0, (0, 0, 255), 4))
    object_list.append(MassObject("Mars", 2.4e24, x_mid, 2.2e11, 24000, 0, (255, 0, 0), 3))
    #object_list.append(MassObject("Jupiter", 1e28, x_mid, 7.7e11, 13000, 0, (255, 255, 0)))
    #object_list.append(MassObject("Saturn", 5.7e26, x_mid, 1.4e12, 9000, 0, (255, 145, 0)))
    #object_list.append(MassObject("Uranus", 8.7e25, x_mid, 2.8e12, 6835, 0, (145, 255, 0)))
    #object_list.append(MassObject("Neptune", 1e26, x_mid, 4.5e12, 5477, 0, (255, 255, 145)))
    object_list.append(MassObject("Rocket", 2000, x_mid, 1.50001e11, 30000, 8000, (255, 255, 255), 1))


def furthest(object_list):
    for object in object_list:
        max = object.y_pos
        if object.y_pos > max:
            max = object.y_pos
    return max


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
        object.y_velocity += y_acc * time_step
        object.x_pos += object.x_velocity * time_step
        object.y_pos += object.y_velocity * time_step


def create_trails(object_list):
    for object in object_list:
        trails.append([])


def draw(object_list, r_furthest):
    for object in object_list:
        pygame.draw.circle(display, object.colour, (int((220 * object.x_pos / r_furthest)) + 550, int((220 * object.y_pos / r_furthest)) + 350), object.radius, 0)
        trails[object_list.index(object)].append((display, object.colour, (int((220 * object.x_pos / r_furthest)) + 550, int((220 * object.y_pos / r_furthest)) + 350), object.radius, 0))
    for trail in trails:
        for element in trail:
            if len(trail) > 0 and trail.index(element) > 0:
                ratio = trail.index(element)/len(trail)
                pygame.draw.circle(element[0], (int(element[1][0] * ratio), int(element[1][1] * ratio), int(element[1][2] * ratio)), element[2], element[3], element[4])
        while len(trail) > trail_len:
            trail.pop(0)
    pygame.display.update()
    clock.tick(frame_rate)


def main():
    setup(object_list)
    r_furthest = furthest(object_list)
    step = 1
    while True:
        pygame.display.set_caption('Gravity Simulation: Step {}  SimulationTime(s): {} RealTime: {}'.format(str(step), round(round(time.time() - start_time,2)* time_step * frame_rate,2), round(time.time() - start_time,2)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
        display.fill(pygame.Color("black"))
        step += 1
        update_pos(object_list)
        create_trails(object_list)
        draw(object_list, r_furthest)


if __name__ == '__main__':
    main()
