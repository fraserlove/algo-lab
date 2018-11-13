"""
Wire World Cellular Automaton
Developed by Fraser Love on 04/10/18
Dependencies: Pygame
Ran on CPU - Reccomended to use on High-Range CPU
Controls:
 - W,A,S,D to move
 - SPACE to select
 - ENTER to confirm
"""
import pygame, sys, time
from pygame.locals import *

session = True
grid_size = (160, 160)              # Sets the size of the grid
spacing = 0                         # Sets space between each cell
cell_size = 8                       # Sets the drawn size of each cell
frame_rate = 100
pointer_size = 0.8                  # Sets the size of mouse pointer

def initialise():
    pygame.init()
    display = pygame.display.set_mode((grid_size[0]*(cell_size+spacing)-spacing, grid_size[1]*(cell_size+spacing)-spacing))
    pygame.display.set_caption('Wire World: Controls - WASD to Move, SPACE to select cells, ENTER to confirm')
    display.fill(pygame.Color("black"))
    clock = pygame.time.Clock()
    cells = [[0 for x in range(grid_size[1])] for y in range(grid_size[0])]
    return display, clock, cells

def key_input(display, cells, pos, selection = True, conductor_selection = True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pos[1] -= 1
    elif keys[pygame.K_s]:
        pos[1] += 1
    elif keys[pygame.K_d]:
        pos[0] += 1
    elif keys[pygame.K_a]:
        pos[0] -= 1
    if keys[pygame.K_RETURN]:
        if conductor_selection:
            selection = False
    if keys[pygame.K_SPACE]:
        if conductor_selection:
            if cells[pos[0]][pos[1]] == 1:
                cells[pos[0]][pos[1]] = 0
            elif cells[pos[0]][pos[1]] == 0:
                cells[pos[0]][pos[1]] = 1
        else:
            cells[pos[0]][pos[1]] = 2
            selection = False
    return selection

def draw_selection(display, cells, spacing, pos, fill_colour, draw_pointer):
    display.fill(fill_colour)
    for i in range(grid_size[1]):
        for j in range(grid_size[0]):
            if cells[j][i] == 1:
                pygame.draw.rect(display, (255,255,255), (j*(cell_size+spacing),i*(cell_size+spacing),cell_size,cell_size), 0)
            if cells[j][i] == 0:
                pygame.draw.rect(display, (0,0,0), (j*(cell_size+spacing),i*(cell_size+spacing),cell_size,cell_size), 0)
            if cells[j][i] == 2:
                pygame.draw.rect(display, (255,0,255), (j*(cell_size+spacing),i*(cell_size+spacing),cell_size,cell_size), 0)
    if draw_pointer == True:
        pygame.draw.rect(display, (255, 43, 74), (pos[0]*(cell_size+spacing)+(cell_size-(pointer_size*cell_size)),pos[1]*(cell_size+spacing)+(cell_size-(pointer_size*cell_size)),cell_size*pointer_size,cell_size*pointer_size), 0)
    pygame.display.update()

def conductor_selection(display, cells, spacing = 2, pos = [0,0], selection = True):
    while selection:
        selection = key_input(display, cells, pos, True, True)
        draw_selection(display, cells, spacing, pos, (0, 0, 255), True)
    return cells

def head_selection(display, cells, spacing = 2, pos = [0,0], selection = True):
    selection = True
    while selection:
        selection = key_input(display, cells, pos, True, False)
        draw_selection(display, cells, spacing, pos, (0, 255, 0), True)
    else:
        draw_selection(display, cells, spacing, pos, (255, 0, 0), False)
        time.sleep(2)
    return cells

def cell_setup(display, cells):
    cells = conductor_selection(display, cells, 2, [0,0], True)
    cells = head_selection(display, cells, 2, [0,0], True)
    return cells

def new_cells(cells):
    new = [[0 for x in range(grid_size[1])] for y in range(grid_size[0])]
    for j in range(grid_size[1]):
        for i in range(grid_size[0]):
            if cells[j][i] == 1:
                count = 0
                new[j][i] = 1
                for k in [-1,0,1]:
                    for l in [-1,0,1]:
                        if cells[j+k][i+l] == 2:
                            count += 1
                if count == 1 or count == 2:
                    new[j][i] = 2
            elif cells[j][i] == 2:
                new[j][i] = 3
            elif cells[j][i] == 3:
                new[j][i] = 1
    return new

def draw(display, new, generation, start_time):
    display.fill(pygame.Color("black"))
    pygame.display.set_caption('Wire World: Generation {}  Time: {}  AverageFPS: {}'.format(str(generation), round(time.time() - start_time,2), round(generation/round(time.time() - start_time,2),2)))
    for j in range(grid_size[1]):
        for i in range(grid_size[0]):
            if new[j][i] == 1:
                pygame.draw.rect(display, (230,239,62), (j*(cell_size+spacing),i*(cell_size+spacing),cell_size,cell_size), 0)
            if new[j][i] == 2:
                pygame.draw.rect(display, (62,174,239), (j*(cell_size+spacing),i*(cell_size+spacing),cell_size,cell_size), 0)
            if new[j][i] == 3:
                pygame.draw.rect(display, (239,62,62), (j*(cell_size+spacing),i*(cell_size+spacing),cell_size,cell_size), 0)
    pygame.display.update()

def update_cells(new, cells):
    for j in range(grid_size[1]):
        for i in range(grid_size[0]):
            cells[j][i] = new[j][i]
    return cells

def game_loop(display, clock, cells):
    start_time = time.time()
    generation = 0
    while True:
        generation += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
        new = new_cells(cells)
        cells = update_cells(new, cells)
        draw(display, new, generation, start_time)
        clock.tick(frame_rate)

def main():
    display, clock, cells = initialise()
    cells = cell_setup(display, cells)
    game_loop(display, clock, cells)

main()
