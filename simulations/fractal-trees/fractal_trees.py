"""
Fractal Trees Generator

Created 14/08/19
Developed by Fraser Love

Generates random fractal trees by creating branch objects which are a line between two position vectors marking the start and end of the branch.
These branches are then stored in an array called tree and shown to the user.
"""
import pygame, branch, math, copy, random

dimensions = (1200, 800)
leaves_colour = (40,140,40)
branch_colour = (0,0,0)
bg_colour = (255,255,255)
show_leaves = False # Choose to reveal leaves on the top layer

branch_size = 130 # The size of the root branch to start scaling down
branch_reduction = 0.8 # The amount to scale down each new branch from the previous branch
top_layer = 12 # The maximum layers to draw

class Display:
    """ A display object to setup and run the program with pygame """
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.display = pygame.display.set_mode(dimensions)
        self.running = True
        self.tree = [] # List storing all of the branches
        self.leaves = []
        self.setup()

    def setup(self):
        """ Setting up the display and storing our initial root branch """
        self.display.fill(bg_colour)
        pygame.display.set_caption("Fractal Tree Generator")
        a = branch.Vector(self.dimensions[0]/2, self.dimensions[1])
        b = branch.Vector(self.dimensions[0]/2, self.dimensions[1] - branch_size)
        self.root = branch.Branch(a, b)
        self.tree.append(self.root)
        self.run()

    def draw(self):
        """ Method to draw all branches and leaves on screen """
        self.display.fill(bg_colour)
        for branch in self.tree:
            branch.show(self.display, branch_colour)
        for leave in self.leaves:
            pygame.draw.circle(self.display, leaves_colour, (int(leave.x), int(leave.y)), 2)
        pygame.display.update()

    def run(self):
        """ Main program loop """
        layer = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if layer < top_layer:
                    for i in range(len(self.tree)):
                        if not self.tree[i].finished:
                            self.tree.append(self.tree[i].branch_off(math.pi / random.randint(4,top_layer-layer+8), branch_reduction))
                            self.tree.append(self.tree[i].branch_off(-math.pi / random.randint(4,top_layer-layer+8), branch_reduction))
                            self.tree[i].finished = True
                            self.draw()
                    layer += 1
                if layer == top_layer:
                    for i in range(len(self.tree)):
                        if not self.tree[i].finished:
                            self.leaves.append(copy.copy(self.tree[i].end))
                            if show_leaves:
                                self.draw()
                    layer += 1

if __name__ == "__main__":
    pygame.init()
    viewer = Display(dimensions)
