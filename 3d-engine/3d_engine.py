"""
3D Engine in Python

Created 16/08/19
Developed by Fraser Love

A Simple 3D Engine to display a wire mesh and provide user controls to move and rotate around it.
Use WASD to move forward, backward and to the side. Use Q and E to move up and down.
Rotate around the cube with the mouse ESC to exit.
"""

import os, sys, math
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

dimensions = (1200, 800)
bg_colour = (40,40,40)
caption = "3D Engine"

class Display():
    """ A display object to setup pygame and draw nodes and edges on screen """
    def __init__(self, dimensions, bg_colour, caption):
        self.display = pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.dimensions = dimensions
        self.cx, self.cy = dimensions[0]//2, dimensions[1]//2
        self.bg_colour = bg_colour
        self.caption = caption
        self.engine = Engine3D()
        self.camera = Camera((0,0,-5))
        self.setup()

    def setup(self):
        pygame.event.get(); pygame.mouse.get_rel()
        pygame.mouse.set_visible(0), pygame.event.set_grab(1)
        pygame.display.set_caption(self.caption)
        self.display.fill(self.bg_colour)
        self.engine.add_nodes(Node((x, y, z)) for x in range(-1,2,2) for y in range(-1,2,2) for z in range(-1,2,2))
        self.engine.add_edges(((0,1), (2,3), (4,5), (6,7), (0,2), (1,3), (4,6), (5,7), (0,4), (1,5), (2,6), (3,7)))
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                self.camera.events(event)
            self.display.fill(self.bg_colour)
            self.draw_edges()
            pygame.display.flip()
            dt = self.clock.tick()/1000
            key = pygame.key.get_pressed()
            self.camera.translate(dt, key)

    def draw_nodes(self):
        for node in self.engine.nodes:
            x_pos = node.x - self.camera.pos[0]
            y_pos = node.y - self.camera.pos[1]
            z_pos = node.z - self.camera.pos[2]
            pygame.draw.circle(self.display, (255,255,255), (int(x_pos*self.dimensions[0]/2/z_pos)+self.cx, int(y_pos*self.dimensions[0]/2/z_pos)+self.cy), 6)

    def draw_edges(self):
        for edge in self.engine.edges:
            edge_nodes = []
            for node in (self.engine.nodes[edge[0]], self.engine.nodes[edge[1]]):
                x_pos = node.x - self.camera.pos[0]
                y_pos = node.y - self.camera.pos[1]
                z_pos = node.z - self.camera.pos[2]
                x_pos,z_pos = self.engine.rotate2D((x_pos,z_pos),self.camera.rotation[1])
                y_pos,z_pos = self.engine.rotate2D((y_pos,z_pos),self.camera.rotation[0])
                edge_nodes += [(int(x_pos*self.dimensions[0]/2/z_pos)+self.cx, int(y_pos*self.dimensions[0]/2/z_pos)+self.cy)]
            pygame.draw.aaline(self.display, (255,255,255), edge_nodes[0], edge_nodes[1], 1)

class Engine3D():
    """ An object storing all the engine calculations """
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_nodes(self, new_nodes):
        self.nodes += new_nodes

    def add_edges(self, new_edges):
        self.edges += new_edges

    def rotate2D(self, pos, theta):
        x, y = pos
        return x*math.cos(theta)-y*math.sin(theta), y*math.cos(theta)+x*math.sin(theta)

    """ Functions for debugging """
    def print_nodes(self):
        for i, node in enumerate(self.nodes):
            print("Node {}: x={} y={} z={}".format(i,node.x, node.y, node.z))

class Camera():
    """ A camera object to provide camera movement by recieving user input """
    def __init__(self, position=(0,0,0), rotation=(0,0)):
        self.pos = list(position)
        self.rotation = list(rotation)

    def translate(self, dt, key):
        s = dt*5
        if key[pygame.K_q]: self.pos[1] += s
        if key[pygame.K_e]: self.pos[1] -= s
        x,y = s*math.sin(self.rotation[1]), s*math.cos(self.rotation[0])
        if key[pygame.K_w]: self.pos[0] += x; self.pos[2] += y;
        if key[pygame.K_s]: self.pos[0] -= x; self.pos[2] -= y;
        if key[pygame.K_a]: self.pos[0] -= y; self.pos[2] += x;
        if key[pygame.K_d]: self.pos[0] += y; self.pos[2] -= x;

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            x,y = event.rel
            x /= 200
            y /= 200
            self.rotation[0] += y
            self.rotation[1] += x

class Node():
    """ A simple 3D point object """
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]

if __name__ == "__main__":
    pygame.init()
    display = Display(dimensions, bg_colour, caption)
