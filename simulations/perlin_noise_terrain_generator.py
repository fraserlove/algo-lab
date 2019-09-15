"""
Perlin Noise Terrain Generation

Created 01/08/19
Developed by Fraser Love

An dynamic terrain generator using perlin noise.
"""
import math, random, noise, os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Display Variables
scale = 25
dimensions = (1200, 700)
x_padding = -20
y_padding = -250
rows = 95
cols = 50
camera_rotation = 1.32

#Perlin Noise Variables
flying = 0
flying_rate = 0.1 # Controls the speed of terrain generation
noise_res = 0.08 # Controls the resolution of the perlin noise
octaves = 2 # Controls the roughness of the perlin noise
height = 8 # Coefficient of the height of perlin noise

class Display:
    """ Object to generate a pygame window and terrain and update display"""
    def __init__(self):
        self.display = pygame.display.set_mode(dimensions)
        self.terrain = Terrain()
        self.run()

    def display_lines(self):
        """ Draws lines between nodes on screen to show terrain """
        for line in self.terrain.lines:
            line = pygame.draw.aaline(self.display, (255,255,255), (int(line[0][0]*scale)+x_padding, int(line[0][1]*scale)+y_padding), (int(line[1][0]*scale)+x_padding, int(line[1][1]*scale)+y_padding), 1)

    def gen_terrain(self):
        """ Generates terrain using perlin noise """
        global flying, flying_rate
        self.terrain.nodes = []
        self.terrain.lines = []
        flying -= flying_rate
        new_nodes = []
        y_off = flying
        for y in range(rows):
            x_off = 0
            for x in range(cols):
                z = noise.pnoise2(x_off,y_off,octaves)*height
                new_nodes.append(Node((x,y,z)))
                x_off += noise_res
            y_off += noise_res
        self.terrain.nodes += new_nodes

    def run(self):
        """ Main program loop to control generation and display of terrain """
        running = True
        while running:
            pygame.display.set_caption("Perlin Noise Terrain Generation")
            self.display.fill((20,20,20))
            self.gen_terrain()
            self.terrain.rotate_x(camera_rotation)
            self.terrain.gen_lines()
            self.display_lines()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_ESCAPE:
                       pygame.quit()
            pygame.display.update()

class Node():
    """ A point object to represent a 3D coordinate """
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]

class Terrain():
    """ Object that stores data on nodes, generates lines and rotates all nodes """
    def __init__(self):
        self.nodes = []
        self.lines = []

    def gen_lines(self):
        """ Generates lines to show triangle between 3 points """
        for i in range(len(self.nodes)-1):
            if i % cols != cols-1:
                self.lines.append([(self.nodes[i].x, self.nodes[i].y), (self.nodes[i+1].x, self.nodes[i+1].y)])
            if i+cols < len(self.nodes):
                self.lines.append([(self.nodes[i].x,self.nodes[i].y), (self.nodes[i+cols].x, self.nodes[i+cols].y)])
            if i % cols != cols-1 and i+cols < len(self.nodes):
                self.lines.append([(self.nodes[i+cols].x, self.nodes[i+cols].y), (self.nodes[i+1].x, self.nodes[i+1].y)])

    def rotate_x(self, cx=rows/2, cy=cols/2, cz=0, radians=camera_rotation):
        """ Rotates all nodes along the x axis by x radians """
        for node in self.nodes:
            y = node.y - cy
            z = node.z - cz
            d = math.hypot(y, z)
            theta = math.atan2(y, z) + radians
            node.z = cz + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)

    def print_nodes(self):
        for i, node in enumerate(self.nodes):
            print("Node:", i, node.x, node.y, node.z)

    def print_lines(self):
        for i, line in enumerate(self.lines):
            print("Line:", i, line[0], line[1])

pygame.init()
window = Display()
