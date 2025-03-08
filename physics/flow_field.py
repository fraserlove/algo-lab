import os
import noise
import numpy as np
from typing import Tuple

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pygame.gfxdraw

D = 5e-2 # Damping (drag) factor

class FlowField:
    def __init__(self, n: int = 1, field_size: Tuple[int, int] = (1, 1), dt: float = 4e-2):
        self.t = 0
        self.dt = dt

        self.rows = field_size[0]
        self.cols = field_size[1]
        
        # Initialise vectors
        self.vectors = np.zeros((self.rows, self.cols, 2))
        
        # Initialise particles
        self.pos = np.random.rand(n, 2)
        self.vel = np.zeros((n, 2))
        self.acc = np.zeros((n, 2))
        
        # Get initial acceleration
        self.get_acceleration()

    def get_acceleration(self) -> np.ndarray:
        '''Calculate the acceleration on each particle.'''

        self.update_vectors()

        # Convert positions to grid indices
        rows = np.floor(self.pos[:, 0] * self.rows).astype(int)
        cols = np.floor(self.pos[:, 1] * self.cols).astype(int)

        # Vectorised lookup of flow vectors for each particle
        return self.vectors[rows, cols]
    
    def update_vectors(self, noise_res: float = 2e-2, octaves: int = 10) -> None:
        '''Generate 3D perlin noise and store as vectors in flowfield.'''
        # Create coordinate grids
        xs = np.arange(self.rows) * noise_res
        ys = np.arange(self.cols) * noise_res
        
        # Generate vectors from noise
        for row, x_off in enumerate(xs):
            for col, y_off in enumerate(ys):
                perlin = noise.pnoise3(x_off, y_off, self.t, octaves) * 4 * np.pi
                self.vectors[row, col, 0] = np.cos(perlin)
                self.vectors[row, col, 1] = np.sin(perlin)
    
    def step(self) -> None:
        '''Perform one step of the Leapfrog integration.'''
        self.vel += self.acc * self.dt / 2.0
        self.pos += self.vel * self.dt
        self.pos = np.mod(self.pos, 1.0) # Keep in [0,1] range
        self.acc = self.get_acceleration()
        self.vel += self.acc * self.dt / 2.0
        self.vel *= (1 - D)
        self.t += self.dt

def draw_particles(display: pygame.Surface, positions: np.ndarray) -> None:
    '''Draw the particles on the display.'''
    for i in range(len(positions)):
        # Scale positions to display coordinates
        x = int(positions[i, 0] * display.get_width())
        y = int(positions[i, 1] * display.get_height())
        pygame.gfxdraw.pixel(display, x, y, (255, 255, 255, 70))

def draw_vectors(display: pygame.Surface, vectors: np.ndarray) -> None:
    '''Draw the flow field vectors.'''
    for x in range(vectors.shape[0]):
        for y in range(vectors.shape[1]):
            vector = vectors[x, y]
            x_scale = display.get_width() / vectors.shape[0]
            y_scale = display.get_height() / vectors.shape[1]
            start = (x * x_scale, y * y_scale)
            end = ((x + vector[0]) * x_scale, (y + vector[1]) * y_scale)
            pygame.draw.aaline(display, (40, 40, 40), end, start)

def main() -> None:
    pygame.init()
    display = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Flow Field')

    sim = FlowField(n = 100000, field_size = (75, 75))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        sim.step()

        display.fill('black')
        draw_vectors(display, sim.vectors)
        draw_particles(display, sim.pos)
        pygame.display.flip()

if __name__ == '__main__':
    main()