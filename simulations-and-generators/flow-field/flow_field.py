'''
Perlin Noise Flow Field

A particle flow field simulation using perlin noise to create vector arrays that
control particle movement. Each frame is saved as an image that can be combined
into a video separately.
'''
import os
import math
import time
import noise
import random

from particle import Particle, Vector

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

# Configuration
DIMENSIONS = (1920, 1080)
SCALE = 20  # Resolution - lower value means more vectors
COLS = DIMENSIONS[0] // SCALE
ROWS = DIMENSIONS[1] // SCALE
PARTICLE_COUNT = 20000
PARTICLE_RADIUS = 1
SHOW_VECTORS = True
SHOW_PARTICLES = True

# Perlin Noise Settings
NOISE_RES = 0.01
OCTAVES = 4
HEIGHT = 1
Z_INCREMENT = 2e-2

class Display:
    '''Controls the display and simulation logic'''
    def __init__(self):
        self.display = pygame.display.set_mode(DIMENSIONS)
        pygame.display.set_caption('Flow Field')
        self.particles = [Particle(Vector(x=random.randint(0, DIMENSIONS[0]), y=random.randint(0, DIMENSIONS[1]))) for _ in range(PARTICLE_COUNT)]
        self.z_off = 0
        self.start_time = time.time()
        
    def perlin_noise(self):
        '''Generate 3D perlin noise and store as vectors in flowfield'''
        self.flowfield = []
        y_off = 0
        
        for y in range(ROWS):
            x_off = 0
            for x in range(COLS):
                # Normalize perlin noise to range [-1, 1] and map directly to angle [-π, π]
                perlin = noise.pnoise3(x_off, y_off, self.z_off, OCTAVES) * 4
                angle = math.pi * perlin  # Maps [-1,1] to [-2π,2π]
                vector = Vector(angle=angle)
                self.flowfield.append(vector)
                
                if SHOW_VECTORS:
                    dx = x * SCALE + vector.unit().x * SCALE
                    dy = y * SCALE + vector.unit().y * SCALE
                    pygame.draw.aaline(self.display, 'dark grey', (dx, dy), (x * SCALE, y * SCALE))
                x_off += NOISE_RES
            y_off += NOISE_RES
        self.z_off += Z_INCREMENT

    def update_particles(self):
        '''Update and draw particles'''
        for p in self.particles:
            p.update(DIMENSIONS)
            p.follow(self.flowfield, SCALE, COLS)
            if SHOW_PARTICLES:
                pygame.draw.rect(self.display, 'white', (int(p.pos.x), int(p.pos.y), PARTICLE_RADIUS, PARTICLE_RADIUS))

    def run(self):
        '''Main simulation loop'''
        os.makedirs('images/', exist_ok=True)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Render frame
            self.display.fill('black')
            self.perlin_noise()
            self.update_particles()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            # Update display and save frame
            pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    Display().run()
