import os
import numpy as np
from typing import Tuple

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pygame.gfxdraw

G = 6.674e-11 # Gravitational constant
D = 0.1 # Damping factor

class NBody:
    def __init__(self, n = 1, total_mass = 1, dt = 1e-3):
        self.t = 0
        self.dt = dt
        
        # Initialise particles
        self.mass = total_mass * np.ones((n, 1)) / n
        self.pos = np.random.randn(n, 3)
        self.vel = np.random.randn(n, 3)
        
        # Center of mass correction, remove mean velocity
        self.vel -= np.mean(self.mass * self.vel, 0) / np.mean(self.mass)
        
        # Initial acceleration
        self.acc = self.get_acceleration()
        
    def get_acceleration(self) -> np.ndarray:
        '''Calculate the acceleration on each particle. Newton's Law.'''
        x, y, z = self.pos[:,0:1], self.pos[:,1:2], self.pos[:,2:3]
        
        # Separations between particles
        dx, dy, dz = x.T - x, y.T - y, z.T - z

        # Inverse cube of distance
        inv_r3 = (dx**2 + dy**2 + dz**2 + D**2)
        inv_r3[inv_r3 > 0] = inv_r3[inv_r3 > 0]**(-1.5)

        # Acceleration components
        ax = G * (dx * inv_r3) @ self.mass
        ay = G * (dy * inv_r3) @ self.mass
        az = G * (dz * inv_r3) @ self.mass
        
        return np.hstack((ax, ay, az))
    
    def centre_of_mass(self) -> np.ndarray:
        '''Calculate the centre of mass of the system.'''
        return np.mean(self.mass * self.pos, 0)
    
    def get_energy(self) -> Tuple[float, float]:
        '''Get kinetic energy (KE) and potential energy (PE) of simulation.'''
        KE = 0.5 * np.sum(self.mass * self.vel**2)
        
        x, y, z = self.pos[:,0:1], self.pos[:,1:2], self.pos[:,2:3]
        # Separations between particles
        dx, dy, dz = x.T - x, y.T - y, z.T - z

        # Inverse distance
        inv_r = np.sqrt(dx**2 + dy**2 + dz**2)
        inv_r[inv_r > 0] = 1.0 / inv_r[inv_r > 0]

        # Potential energy (count each interaction only once with upper triangle)
        PE = G * np.sum(np.triu(-(self.mass * self.mass.T) * inv_r, 1))
        
        return KE, PE
    
    def step(self) -> None:
        '''Perform one step of the Leapfrog integration.'''
        self.vel += self.acc * self.dt / 2.0
        self.pos += self.vel * self.dt
        self.acc = self.get_acceleration()
        self.vel += self.acc * self.dt / 2.0
        self.t += self.dt
        
def draw_particles(screen: pygame.Surface, positions: np.ndarray) -> None:
    '''Draw particles on the screen.'''
    for p in range(len(positions)):
        # Scale positions to screen coordinates
        x = int(screen.get_width() / 2 + positions[p, 0] * (screen.get_width() / 4))
        y = int(screen.get_height() / 2 + positions[p, 1] * (screen.get_height() / 4))
        
        # Only draw if within simulation area
        if 0 <= x < screen.get_width() and 0 <= y < screen.get_height():
            # Semi-transparent white color (RGBA with alpha=180)
            pygame.gfxdraw.pixel(screen, x, y, (255, 255, 225, 180))

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('N-body')
    
    sim = NBody(n=2500, total_mass=4e11, dt=1e-3)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        sim.step()
        
        screen.fill('black')
        draw_particles(screen, sim.pos)        
        pygame.display.flip()

if __name__ == '__main__':
    main()