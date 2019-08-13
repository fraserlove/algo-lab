"""
Perlin Noise Flow Field

Created 13/08/19
Developed by Fraser Love

A particle flow field using perlin noise to create a vector array to update particle
position, velocity and acceleration.
"""
import noise, os, random, math, particle
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Display Variables
dimensions = (1000, 600)
scale = 20
cols = dimensions[0] // scale
rows = dimensions[1] // scale
frame_rate = 60

# Perlin Noise Variables
noise_res = 0.08 # Controls the resolution of the perlin noise
octaves = 1 # Controls the roughness of the perlin noise
height = 1 # Coefficient of the height of perlin noise
z_increment = 0.01 # Controls how quick the perlin noise changes
particle_count = 10000

class Display:
    """ Object to control the display with pygame """
    def __init__(self):
        self.display = pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.particles = []
        self.z_off = 0
        self.setup()

    def setup(self):
        """ Setting up display and adding particles to particles array """
        pygame.display.set_caption("Perlin Noise Flow Field")
        self.display.fill(pygame.Color(255,255,255))
        pygame.display.update()
        self.add_particles(particle_count)
        self.run()

    def add_particles(self, amount):
        for i in range(amount):
            self.particles.append(particle.Particle())

    def perlin_noise(self):
        """ Creating 3D perlin noise and storing it as a vector in an array called flowfield """
        y_off = 0
        self.flowfield = []
        for y in range(rows):
            x_off = 0
            for x in range(cols):
                perlin = noise.pnoise3(x_off,y_off,self.z_off,octaves)* math.pi * 2 * height
                vector = particle.Vector(perlin)
                self.flowfield.append(vector)
                pygame.draw.aaline(self.display, (140,140,140), (x*scale, y*scale), ((x+vector.display_x)*scale, (y+vector.display_y)*scale), 1)
                x_off += noise_res
            y_off += noise_res
        self.z_off += z_increment

    def draw_particles(self):
        """ Updating particle kinematics and displaying particles on screen """
        for particle in self.particles:
            particle.update()
            particle.follow(self.flowfield)
            pygame.draw.rect(self.display, (0,0,0), (int(particle.pos.x), int(particle.pos.y), 2, 2))

    def run(self):
        """ Main program loop controling updating display, flowfield and particles """
        running = True
        while running:
            self.display.fill(pygame.Color(255,255,255))
            self.perlin_noise()
            self.draw_particles()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
            self.clock.tick(frame_rate)

if __name__ == "__main__":
    pygame.init()
    window = Display()
