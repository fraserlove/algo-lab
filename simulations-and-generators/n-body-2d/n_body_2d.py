'''
N-body simulation
Author: Fraser Love, me@fraser.love
Created: 2021-07-06
Latest Release: v1.0.3, 2021-07-10
Python: v3.9.6
Dependencies: pygame

Simulating how N-bodies interact using gravitation as described newtonian physics with the stable second-order Leapfrog
method of integration implemented to increase accuracy. This program requires a huge amount of computation and therefore
cannot be ran in real-time. Instead images are saved at each time-step in the simulation, these images can then be
combined to create a video of the simulation at the desired frame-rate. It is recommended to run this simulation on a
powerful CPU to speed up computation.
'''

import random, sys, time, os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Physical Constants and Variables
G = 6.67408e-11  # Gravitational constant
INITIAL_MAX_V = 0.00002  # Maximum initial velocity of particles
INITIAL_MASS = 100  # Starting mass of particles
INITIAL_MAX_S = 400  # Maximum initial displacement from the centre of the screen
SOFTENING_FACTOR = 0.5  # Amount of gravitational softening applied to particles
PARTICLE_COUNT = 1000  # Number of initial particles in the simulation
TIME_STEP = 5000 # Time delta between each calculation - lower is more accurate
INTEGRATION_METHOD = 'leapfrog'  # Method of integration to choose from (euler or leapfrog)

# Display Variables
DIMENSIONS = (1920, 1080)  # Dimensions of the simulations 'universe'
PARTICLE_RADIUS = 1


def random_displacement(dimension):
    centre = find_centre()
    if dimension == 'x':
        return random.randrange(centre[0] - INITIAL_MAX_S, centre[0] + INITIAL_MAX_S)
    else:
        return random.randrange(centre[1] - INITIAL_MAX_S, centre[1] + INITIAL_MAX_S)


def find_centre():
    return int(DIMENSIONS[0] / 2), int(DIMENSIONS[1] / 2)


def random_velocity():
    return random.uniform(-INITIAL_MAX_V, INITIAL_MAX_V)


def time_delta(start):
    return round(time.time() - start, 2)


class Particle:
    def __init__(self, mass, x, y, vx, vy):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0

    def accelerate(self, particles):
        ax, ay = 0, 0
        for other in particles:
            if other != self:
                dx = self.x - other.x
                dy = self.y - other.y
                r = ((dx * dx) + (dy * dy)) ** (1 / 2)
                # Calculating the particles acceleration using Newtonian gravitation and softening the result
                ax -= G * other.mass * dx / (r ** 2 + SOFTENING_FACTOR ** 2) ** (3 / 2)
                ay -= G * other.mass * dy / (r ** 2 + SOFTENING_FACTOR ** 2) ** (3 / 2)
        return ax, ay

    def position(self):
        return self.x, self.y


class Simulation:
    def __init__(self):
        self.particles = []  # List to hold all of the particles in the simulation
        self.particle_count = PARTICLE_COUNT
        self.dt = TIME_STEP
        self.integration = INTEGRATION_METHOD
        self.start_time = time.time()
        self.step = 1

    def generate_particles(self):
        for i in range(self.particle_count):
            self.particles.append(Particle(INITIAL_MASS, random_displacement('x'), random_displacement('y'), random_velocity(), random_velocity()))

    def simulate(self):
        for particle in self.particles:
            ax, ay = particle.accelerate(self.particles)

            if self.integration == 'leapfrog':
                # Leapfrog integration
                particle.vx += 1 / 2 * (particle.ax + ax) * self.dt
                particle.x += particle.vx * self.dt + 1 / 2 * particle.ax * self.dt * self.dt
                particle.vy += 1 / 2 * (particle.ay + ay) * self.dt
                particle.y += particle.vy * self.dt + 1 / 2 * particle.ay * self.dt * self.dt
                particle.ax = ax
                particle.ay = ay

            if self.integration == 'euler':
                # Euler integration
                particle.vx += ax * self.dt
                particle.x += particle.vx * self.dt
                particle.vy += ay * self.dt
                particle.y += particle.vy * self.dt
        self.step += 1


class Display:
    def __init__(self, simulation):
        pygame.init()
        os.makedirs("images/", exist_ok=True)
        self.display = pygame.display.set_mode(DIMENSIONS)
        self.simulation = simulation
        self.simulation.generate_particles()

    def draw(self):
        self.display.fill(pygame.Color('black'))
        for particle in self.simulation.particles:
            pygame.draw.circle(self.display, 'white', particle.position(), PARTICLE_RADIUS, 0)
        pygame.display.set_caption('N-Body (Step: {} Time: {} Particles: {})'.format(str(self.simulation.step), time_delta(self.simulation.start_time), len(self.simulation.particles)))
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            self.draw()
            pygame.image.save(self.display, "images/{}.jpg".format(self.simulation.step))
            self.simulation.simulate()


if __name__ == '__main__':
    nbody = Simulation()
    display = Display(nbody)
    display.run()
