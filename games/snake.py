"""
Python Implementation of Snake
Developed by Fraser Love on 28/03/19
Dependencies: Pygame
Ran on CPU - Reccomended to use on High-Range CPU
W,A,S,D to move
"""

import pygame, time, sys, random

grid_size = (80, 50)
cell_size = 12
snake_size = 1
tail = [[1,1]]
spacing = 2
frame_rate = 15

def initialise():
    pygame.init()
    display = pygame.display.set_mode((grid_size[0]*(cell_size+spacing)-spacing, grid_size[1]*(cell_size+spacing)-spacing))
    display.fill(pygame.Color("black"))
    cells = [[0 for y in range(grid_size[1])] for x in range(grid_size[0])]
    cells[random.randrange(0,grid_size[0])][random.randrange(0,grid_size[1])] = 1
    snake_vec = 2
    snake_pos = [1, 1]
    clock = pygame.time.Clock()
    return display, cells, snake_vec, clock, snake_pos

def key_input(snake_vec, snake_size):
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] and snake_vec != 2 and snake_size > 1) or keys[pygame.K_w] and snake_size == 1:
        snake_vec = 0
    elif (keys[pygame.K_s] and snake_vec != 0 and snake_size > 1) or keys[pygame.K_s] and snake_size == 1:
        snake_vec = 2
    elif (keys[pygame.K_d] and snake_vec != 3 and snake_size > 1) or keys[pygame.K_d] and snake_size == 1:
        snake_vec = 1
    elif (keys[pygame.K_a] and snake_vec != 1 and snake_size > 1 or keys[pygame.K_a] and snake_size == 1):
        snake_vec = 3
    return snake_vec

def draw_cells(display, cells, tail):
    display.fill((0,0,0))
    for i in range(grid_size[1]):
        for j in range(grid_size[0]):
            if cells[j][i] == 0:
                pygame.draw.rect(display, (255,255,255), (j*(cell_size+spacing),i*(cell_size+spacing),cell_size,cell_size), 0)
            if cells[j][i] == 1:
                pygame.draw.rect(display, (0,0,255), (j*(cell_size+spacing),i*(cell_size+spacing),cell_size,cell_size), 0)
    for node in tail:
        pygame.draw.rect(display, (255,0,0), (node[0]*(cell_size+spacing),node[1]*(cell_size+spacing),cell_size,cell_size), 0)
    pygame.display.update()

def check_collision(cells, snake_pos, snake_size, tail):
    collision = False
    if cells[snake_pos[0]][snake_pos[1]] == 1:
        snake_size += 5
        cells[snake_pos[0]][snake_pos[1]] = 0
        cells[random.randrange(0,grid_size[0])][random.randrange(0,grid_size[1])] = 1
    for node in range(1, len(tail)-1):
        if snake_pos[0] == tail[node][0] and snake_pos[1] == tail[node][1]:
            collision = True
            break
    return cells, snake_size, collision

def move_snake(snake_vec, snake_pos):
    out_of_bounds = False
    if snake_vec == 0:
        snake_pos = [snake_pos[0], snake_pos[1]-1]
    if snake_vec == 1:
        snake_pos = [snake_pos[0]+1, snake_pos[1]]
    if snake_vec == 2:
        snake_pos = [snake_pos[0], snake_pos[1]+1]
    if snake_vec == 3:
        snake_pos = [snake_pos[0]-1, snake_pos[1]]
    if snake_pos[0] >= grid_size[0] or snake_pos[0] < 0 or snake_pos[1] >= grid_size[1] or snake_pos[1] < 0:
        out_of_bounds = True
    return snake_pos, out_of_bounds

def game_loop(display, cells, snake_vec, clock, snake_pos, snake_size, tail):
    while True:
        pygame.display.set_caption('Python Snake - Length: '+ str(snake_size-1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
        snake_vec = key_input(snake_vec, snake_size)
        snake_pos, out_of_bounds = move_snake(snake_vec, snake_pos)
        tail.append(snake_pos)
        tail = tail[1:]
        cells, snake_size, collision = check_collision(cells, snake_pos, snake_size, tail)
        if collision == True or out_of_bounds == True:
            break
        while len(tail) < snake_size-1:
            tail.append(snake_pos)
        draw_cells(display, cells, tail)
        clock.tick(frame_rate)

display, cells, snake_vec, clock , snake_pos = initialise()
game_loop(display, cells, snake_vec, clock, snake_pos, snake_size, tail)
