"""
Brian's Brain Cellular Automaton
Developed by Fraser Love on 13/11/18
Dependencies: Pygame

Improvements
- Modulus wrapping added to allow ant to travel across the edges of the plane
"""
import pygame, sys, random, time
from pygame.locals import *

grid_size = (200, 100)              # Sets the size of the grid
cell_size = 9                       # Sets the drawn size of each cell
frame_rate = 30

def randomise(cells):
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            cells[i][j] = random.randrange(0,3)
    return cells

def initialise():
    pygame.init()
    display = pygame.display.set_mode((grid_size[0]*cell_size, grid_size[1]*cell_size))
    display.fill(pygame.Color("black"))
    clock = pygame.time.Clock()
    cells = [[0 for y in range(grid_size[1])] for x in range(grid_size[0])]
    cells = randomise(cells)
    return display, clock, cells

def next_gen(cells):
    new = [[0 for y in range(grid_size[1])] for x in range(grid_size[0])]
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            if cells[i][j] == 0:
                alive = 0
                for k in range(-1,2):
                    for l in range(-1,2):
                        if cells[(i+k) % grid_size[0]][(j+l)% grid_size[1]] == 1:
                            alive += 1
                if alive == 2:
                    new[i][j] = 1
            elif cells[i][j] == 1:
                new[i][j] = 2
            elif cells[i][j] == 2:
                new[i][j] = 0
    return new

def update_cells(new, cells):
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            cells[i][j] = new[i][j]
    return cells

def draw(display, generation, start_time, cells):
    display.fill(pygame.Color("black"))
    pygame.display.set_caption('Brians Brain: Generation {}  Time: {}  MeanGensPerSecond: {}'.format(str(generation), round(time.time() - start_time,2), round(generation/round(time.time() - start_time,2),2)))
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            if cells[i][j] == 1:
                pygame.draw.rect(display, (255,255,255), (i*cell_size,j*cell_size,cell_size,cell_size), 0)
            elif cells[i][j] == 2:
                pygame.draw.rect(display, (239,62,62), (i*cell_size,j*cell_size,cell_size,cell_size), 0)
    pygame.display.update()

def game_loop(display, clock, cells):
    start_time = time.time()
    time.sleep(0.1)
    generation = 0
    while True:
        generation += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
        new = next_gen(cells)
        cells = update_cells(new, cells)
        draw(display, generation, start_time, cells)
        clock.tick(frame_rate)

def main():
    display, clock, cells = initialise()
    game_loop(display, clock, cells)

if __name__ == "__main__":
    main()
