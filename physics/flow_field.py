import os
import math
import noise
import random
import numpy as np

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pygame.gfxdraw

class Particle:
    def __init__(self, pos, bounds, drag_coef=5e-2):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.zeros(2, dtype=float)
        self.acc = np.zeros(2, dtype=float)
        self.drag_coef = drag_coef
        self.bounds = np.array(bounds)

    def update(self, flowfield):
        ''' Updating the particle's position, velocity and acceleration '''
        self.vel += self.acc
        self.vel *= (1 - self.drag_coef)
        self.pos += self.vel
        self.pos = np.mod(self.pos, self.bounds)  # Wrap around the screen
        # Find the flowfield vector the particle lies on and apply the force
        self.acc = flowfield.nearest_vector(self.pos[0], self.pos[1])

class FlowField:
    def __init__(self, size, resolution=10, n_particles=20000, drag_coef=5e-2):
        self.t = 0
        self.resolution = resolution
        self.size = np.array(size)
        self.rows = size[1] // resolution
        self.cols = size[0] // resolution
        
        # Initialize vectors as 3D array: [rows, cols, 2]
        self.vectors = np.zeros((self.rows, self.cols, 2), dtype=float)
        
        # Create particles with random positions
        self.particles = []
        for _ in range(n_particles):
            random_pos = np.array([random.randint(0, size[0]), random.randint(0, size[1])])
            self.particles.append(Particle(random_pos, size, drag_coef))

    def nearest_vector(self, x, y):
        '''Get the nearest vector to the given coordinates.'''
        col = int(x // self.resolution)
        row = int(y // self.resolution)
        return self.vectors[row, col]
    
    def update_vectors(self, noise_res=1e-2, dt=1e-2, octaves=4):
        '''Generate 3D perlin noise and store as vectors in flowfield'''
        # Create coordinate grids
        y_coords = np.arange(self.rows) * noise_res
        x_coords = np.arange(self.cols) * noise_res
        
        # For Perlin noise, we still need to iterate as noise library doesn't support vectorization
        for row, y_off in enumerate(y_coords):
            for col, x_off in enumerate(x_coords):
                perlin = noise.pnoise3(x_off, y_off, self.t, octaves) * 4 * math.pi
                self.vectors[row, col, 0] = math.cos(perlin)
                self.vectors[row, col, 1] = math.sin(perlin)
                
        self.t += dt
        
    def update(self):
        '''Update the flow field and particles'''
        self.update_vectors()
        for particle in self.particles:
            particle.update(self)

def draw_vectors(display, flow_field):
    '''Draw the flow field vectors.'''
    for y in range(flow_field.rows):
        for x in range(flow_field.cols):
            vector = flow_field.vectors[y, x]
            start = (x * flow_field.resolution, y * flow_field.resolution)
            end = ((x + vector[0]) * flow_field.resolution, (y + vector[1]) * flow_field.resolution)
            pygame.draw.aaline(display, 'dark grey', end, start)

def draw_particles(display, particles):
    '''Draw the particles.'''
    for p in particles:
        pygame.gfxdraw.pixel(display, int(p.pos[0]), int(p.pos[1]), (255, 255, 255, 200))

def main():
    pygame.init()
    display = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Flow Field')

    flow_field = FlowField((600, 600))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        display.fill('black')

        flow_field.update()
        draw_vectors(display, flow_field)
        draw_particles(display, flow_field.particles)
        
        pygame.display.update()

if __name__ == '__main__':
    main()