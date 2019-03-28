"""
Conway's Game Of Life Cellular Automaton
Developed by Fraser Love on 26/09/18
Dependencies: Pygame
Ran on CPU - Reccomended to use on High-Range CPU
"""

import pygame, sys, random
from pygame.locals import *
pygame.init()

session = True
cells_x = 70
cells_y = 40
res = 15
cell_size = 13
start_cells = 1000
frame_rate = 30
cells = [[0 for x in range(cells_y)] for y in range(cells_x)]

display = pygame.display.set_mode((cells_x*res-res+2, cells_y*res-res+2))
pygame.display.set_caption('Conway\'s Game Of Life')
clock = pygame.time.Clock()
display.fill(pygame.Color("black"))
pygame.font.init()

def intro():

    heading = pygame.font.Font('freesansbold.ttf',70)
    TextSurf = heading.render("GAME OF LIFE", True, (255,255,255))
    TextRect = TextSurf.get_rect()
    TextRect.center = ((cells_x*res/2),(cells_y*res/2-100))
    display.blit(TextSurf, TextRect)

    credits = pygame.font.Font('freesansbold.ttf',20)
    TextSurf = credits.render("FRASER LOVE", True, (255,255,255))
    TextRect = TextSurf.get_rect()
    TextRect.center = ((cells_x*res-90),(cells_y*res-25))
    display.blit(TextSurf, TextRect)

    button_rand = pygame.Rect(0, 0, 150, 45)
    button_rand.center = ((cells_x*res/2+100),(cells_y*res/2))
    button_draw = pygame.Rect(0, 0, 150, 45)
    button_draw.center = ((cells_x*res/2-100),(cells_y*res/2))

    button_text = pygame.font.Font("freesansbold.ttf",20)
    rand_TextSurf = button_text.render("RANDOM", True, (0,0,0))
    rand_TextRect = rand_TextSurf.get_rect()
    rand_TextRect.center = ((cells_x*res/2+100),(cells_y*res/2))
    display.blit(rand_TextSurf, rand_TextRect)
    draw_TextSurf = button_text.render("DRAW", True, (0,0,0))
    draw_TextRect = draw_TextSurf.get_rect()
    draw_TextRect.center = ((cells_x*res/2-100),(cells_y*res/2))
    display.blit(draw_TextSurf, draw_TextRect)

    while True:
        rand_colour = (255,255,255)
        draw_colour = (255,255,255)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rand.collidepoint(mouse_pos):
                    sim_rand()
                if button_draw.collidepoint(mouse_pos):
                    sim_draw()

        mouse_pos = pygame.mouse.get_pos()
        if button_rand.collidepoint(mouse_pos):
            rand_colour = (66, 134, 244)
            pygame.draw.rect(display, rand_colour , button_rand)
        if button_draw.collidepoint(mouse_pos):
            draw_colour = (66, 134, 244)
            pygame.draw.rect(display, draw_colour , button_draw)

        pygame.draw.rect(display, draw_colour , button_draw)
        pygame.draw.rect(display, rand_colour , button_rand)
        display.blit(rand_TextSurf, rand_TextRect)
        display.blit(draw_TextSurf, draw_TextRect)

        pygame.display.update()
        clock.tick(frame_rate)

def sim_rand():
    gen = 0

    for c in range(start_cells):
        rand_x = random.randrange(0,cells_x)
        rand_y = random.randrange(0,cells_y)
        cells[rand_x][rand_y] = 1
        pygame.draw.rect(display, (255,255,255), (rand_x*res,rand_y*res,cell_size,cell_size), 0)
    pygame.display.update()

    while session:
        gen += 1
        pygame.display.set_caption('Conway\'s Game Of Life - Generation '+ str(gen))
        clock.tick(frame_rate)
        display.fill(pygame.Color("black"))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();

        new = [[0 for x in range(cells_y)] for y in range(cells_x)]

        for y in range(cells_y-1):
            for x in range(cells_x-1):
                if cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] < 2 and cells[x][y] == 1:
                    new[x][y] = 0
                elif cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] == 2 or cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] == 3 and cells[x][y] == 1:
                    new[x][y] = cells[x][y]
                elif cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] > 3 and cells[x][y] == 1:
                    new[x][y] = 0
                elif cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] == 3 and cells[x][y] == 0:
                    new[x][y] = 1

        for i in range(cells_y):
            for j in range(cells_x):
                cells[j][i] = new[j][i]
                if cells[j][i] == 1:
                    pygame.draw.rect(display, (255,255,255), (j*res+2,i*res+2,cell_size,cell_size), 0)
        pygame.display.update()

def sim_draw():
    gen = 0
    selection = True
    rect_obj = []
    display.fill((145, 145, 145))

    for i in range(cells_y):
        for j in range(cells_x):
            cells[j][i] = 0
            rect_obj.append(pygame.draw.rect(display, (0,0,0), (j*res+2,i*res+2,cell_size,cell_size), 0))
    pygame.display.update()
    xpos = 0
    ypos = 0

    while selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                pygame.draw.rect(display, (0, 0, 0), (xpos*res+2,ypos*res+2,cell_size,cell_size), 0)
                ypos -= 1
            if pressed[pygame.K_s]:
                pygame.draw.rect(display, (0, 0, 0), (xpos*res+2,ypos*res+2,cell_size,cell_size), 0)
                ypos += 1
            if pressed[pygame.K_d]:
                pygame.draw.rect(display, (0, 0, 0), (xpos*res+2,ypos*res+2,cell_size,cell_size), 0)
                xpos += 1
            if pressed[pygame.K_a]:
                pygame.draw.rect(display, (0, 0, 0), (xpos*res+2,ypos*res+2,cell_size,cell_size), 0)
                xpos -= 1
            if pressed[pygame.K_SPACE]:
                if cells[xpos][ypos] == 1:
                    cells[xpos][ypos] = 0
                elif cells[xpos][ypos] == 0:
                    cells[xpos][ypos] = 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for rect in rect_obj:
                    if rect.collidepoint(mouse_pos):
                        x_sel = int((rect.left-2)/res)
                        y_sel = int((rect.top-2)/res)
                        cells[x_sel][y_sel] = 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pos = event.pos
                for rect in rect_obj:
                    if rect.collidepoint(mouse_pos):
                        x_sel = int((rect.left-2)/res)
                        y_sel = int((rect.top-2)/res)
                        cells[x_sel][y_sel] = 0
            if pressed[pygame.K_RETURN]:
                selection = False
            for i in range(cells_y):
                for j in range(cells_x):
                    if cells[j][i] == 1:
                        pygame.draw.rect(display, (255,255,255), (j*res+2,i*res+2,cell_size,cell_size), 0)
                    if cells[j][i] == 0:
                        rect_obj.append(pygame.draw.rect(display, (0,0,0), (j*res+2,i*res+2,cell_size,cell_size), 0))
            pygame.draw.rect(display, Color(255, 43, 74), (xpos*res+2,ypos*res+2,cell_size,cell_size), 0)
            pygame.display.update()


    while session:
        gen += 1
        pygame.display.set_caption('Conway\'s Game Of Life - Generation '+ str(gen))
        clock.tick(frame_rate)
        display.fill(pygame.Color("black"))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();

        new = [[0 for x in range(cells_y)] for y in range(cells_x)]

        for y in range(cells_y-1):
            for x in range(cells_x-1):
                if cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] < 2 and cells[x][y] == 1:
                    new[x][y] = 0
                elif cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] == 2 or cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] == 3 and cells[x][y] == 1:
                    new[x][y] = cells[x][y]
                elif cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] > 3 and cells[x][y] == 1:
                    new[x][y] = 0
                elif cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] == 3 and cells[x][y] == 0:
                    new[x][y] = 1

        for i in range(cells_y):
            for j in range(cells_x):
                cells[j][i] = new[j][i]
                if cells[j][i] == 1:
                    pygame.draw.rect(display, (255,255,255), (j*res+2,i*res+2,cell_size,cell_size), 0)
        pygame.display.update()

intro()
