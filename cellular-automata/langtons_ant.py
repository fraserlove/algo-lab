"""
Langtons Ant Cellular Automaton
Developed by Fraser Love on 12/11/18
Dependencies: Pygame

Improvements
- Modulus wrapping added to allow ant to travel across the edges of the plane
- Ant class added making code more modular
- Fixed loop with calculations per second added to decrease display updates and improve performance - can be varied for preference
- Rect drawing now added into next_gen() to drastically improve performance as now only the one ant rectangle is being drawn per calulation instead of all the cells
"""
import pygame, sys, time
from pygame.locals import *

grid_size = (920, 480)              # Sets the size of the grid
cell_size = 2                       # Sets the drawn size of each cell
frame_rate = 60
calc_per_frame = 1000               # Sets the calculations done between each frame - higher is faster

class Ant():
    def __init__(self):
        self.x = int(grid_size[0]/2)
        self.y = int(grid_size[1]/2)
        self.dir = 0

    def turn_right(self):
        self.dir += 1
        self.dir = self.dir % 4

    def turn_left(self):
        self.dir -= 1
        self.dir = self.dir % 4

    def move_forward(self):
        if self.dir == 0:
            self.y -= 1
        elif self.dir == 1:
            self.x += 1
        elif self.dir == 2:
            self.y += 1
        elif self.dir == 3:
            self.x -= 1
        self.x = self.x % grid_size[0]
        self.y = self.y % grid_size[1]

def initialise():
    pygame.init()
    display = pygame.display.set_mode((grid_size[0]*cell_size, grid_size[1]*cell_size))
    display.fill(pygame.Color("black"))
    clock = pygame.time.Clock()
    cells = [[0 for y in range(grid_size[1])] for x in range(grid_size[0])]
    ant = Ant()
    return display, clock, cells, ant

def next_gen(cells, ant, display):
    if cells[ant.x][ant.y] == 1:
        ant.turn_right()
        cells[ant.x][ant.y] = 0
        pygame.draw.rect(display, (0,0,0), (ant.x*(cell_size),ant.y*(cell_size),cell_size,cell_size), 0)
    elif cells[ant.x][ant.y] == 0:
        ant.turn_left()
        cells[ant.x][ant.y] = 1
        pygame.draw.rect(display, (255,255,255), (ant.x*(cell_size),ant.y*(cell_size),cell_size,cell_size), 0)
    ant.move_forward()

def update(display, generation, start_time):
    pygame.display.set_caption('Langtons Ant: Generation {}  Time: {}  MeanGensPerSecond: {}'.format(str(generation), round(time.time() - start_time,2), round(generation/round(time.time() - start_time,2),2)))
    pygame.display.update()

def game_loop(display, clock, cells, ant):
    start_time = time.time()
    time.sleep(0.1)
    generation = 0
    while True:
        for i in range(calc_per_frame):
            generation += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
            next_gen(cells, ant, display)
        update(display, generation, start_time)
        clock.tick(frame_rate)

def main():
    display, clock, cells, ant = initialise()
    game_loop(display, clock, cells, ant)

main()
