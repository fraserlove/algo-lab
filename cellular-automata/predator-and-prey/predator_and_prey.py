"""
Predator and Prey Cellular Automaton
Developed by Fraser Love on 30/09/18
Dependencies: Pygame
Ran on CPU - Reccomended to use on High-Range CPU
"""

import pygame, sys, random, time
from pygame.locals import *

session = True
prey_count = 0
predator_count = 0
cells_x, cells_y = 200, 100         # Sets the size of the grid
spacing = 0                         # Sets space between each cell
cell_size = 4                       # Sets the drawn size of each cell
frame_rate = 30
generation = 0
prey_probability = 0.5              # Probability of Prey reproducing - change for different results (choose 0.5 for spiral)
predator_probability = 0.4          # Probability of Predator reproducing - change for differnent results (chose 0.4 for spiral)
cells = [[0 for x in range(cells_y)] for y in range(cells_x)]
start_time = time.time()

pygame.init()
display = pygame.display.set_mode((cells_x*(cell_size+spacing), cells_y*(cell_size+spacing)))
display.fill(pygame.Color("black"))
clock = pygame.time.Clock()

# Assigning random values to our grid of cells: 0 - dead, 1 - prey, 2 - predator
for x in range(cells_x):
    for y in range(cells_y):
        rand_no = random.randint(0, 100)
        if rand_no >= 0 and rand_no <= 50:
            cells[x][y] = 0
        elif rand_no > 50 and rand_no <= 75:
            cells[x][y] = 1
            pygame.draw.rect(display, (68,255,0), (x*(cell_size+spacing),y*(cell_size+spacing),cell_size,cell_size), 0)
        elif rand_no > 75 and rand_no <= 100:
            cells[x][y] = 2
            pygame.draw.rect(display, (255,22,22), (x*(cell_size+spacing),y*(cell_size+spacing),cell_size,cell_size), 0)

# CA Simulation Loop
while session:
    generation += 1
    pygame.display.set_caption('Predator and Prey: Generation {}  Time: {}  AverageFPS: {}  Prey: {}  Predators: {}'.format(str(generation), round(time.time() - start_time,2), round(generation/round(time.time() - start_time,2),2), prey_count, predator_count))
    display.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();

    # Calaculating Prey Growth
    new = [[0 for x in range(cells_y)] for y in range(cells_x)]
    prey_count = 0
    predator_count = 0
    for x in range(cells_x):
        for y in range(cells_y):
            if cells[x][y] == 1:
                prey_count += 1
                new[x][y] = cells[x][y]
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if x+i < cells_x and y+j < cells_y and cells[x+i][y+j] == 0:
                            chance = random.randint(0,100)
                            if chance < prey_probability*100:
                                new[x+i][y+j] = 1
    for x in range(cells_x):
        for y in range(cells_y):
            if cells[x][y] == 2:
                predator_count += 1
                new[x][y] = cells[x][y]
                die = True
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if x+i < cells_x and y+j < cells_y and new[x+i][y+j] == 1:
                            die = False
                            chance = random.randint(0,100)
                            if chance < predator_probability*100:
                                new[x+i][y+j] = 2
                if die == True:
                    new[x][y] = 0

    # Displaying Growth
    for i in range(cells_x):
        for j in range(cells_y):
            if new[i][j] == 1:
                pygame.draw.rect(display, (68,255,0), (i*(cell_size+spacing),j*(cell_size+spacing),cell_size,cell_size), 0)
            if new[i][j] == 2:
                pygame.draw.rect(display, (255,22,22), (i*(cell_size+spacing),j*(cell_size+spacing),cell_size,cell_size), 0)
            cells[i][j] = new[i][j]
    pygame.display.update()
    clock.tick(frame_rate)
