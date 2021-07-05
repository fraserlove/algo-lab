"""
Fractal Trees Generator

Created 14/08/19
Developed by Fraser Love

Generates random fractal trees by creating branch objects which are a line between two position vectors marking the start and end of the branch.
These branches are then stored in an array called tree and shown to the user.
"""
import pygame, branch, math, copy, random

dimensions = (3000, 1000)
leaves_colour = (40,140,40)
branch_colour = "white"
bg_colour = "black"
show_leaves = False # Choose to reveal leaves on the top layer
forest_size = 20

min_branch_size = 130 # The minimum size of the root branch to start scaling down
max_branch_size = 260 # The maximum size of the root branch to start scaling down
branch_reduction = 0.75 # The amount to scale down each new branch from the previous branch
top_layer = 10 # The maximum layers to draw

class Display:
    """ A display object to setup and run the program with pygame """
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.display = pygame.display.set_mode(dimensions)
        self.running = True
        self.forest = [] # List storing all of the trees
        self.tree = [] # List storing all of the branches
        self.leaves = []
        self.setup()

    def setup(self):
        """ Setting up the display and storing our initial root branch """
        self.display.fill(bg_colour)
        pygame.display.set_caption("Fractal Tree Generator")
        for i in range(forest_size):
            branch_size = random.randint(min_branch_size, max_branch_size)
            x = random.randint(0, self.dimensions[0])
            a = branch.Vector(x, self.dimensions[1])
            b = branch.Vector(x, self.dimensions[1] - branch_size)
            root = branch.Branch(a, b)
            self.tree.append(root)
            self.forest.append(self.tree)
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
                for tree in self.forest:
                    if layer < top_layer:
                        for i in range(len(tree)):
                            if not tree[i].finished:
                                tree.append(tree[i].branch_off(math.pi / random.randint(4,top_layer-layer+8), branch_reduction))
                                tree.append(tree[i].branch_off(-math.pi / random.randint(4,top_layer-layer+8), branch_reduction))
                                tree[i].finished = True
                        layer += 1
                    if layer == top_layer:
                        for i in range(len(tree)):
                            if not tree[i].finished:
                                if show_leaves:
                                    self.leaves.append(copy.copy(tree[i].end))
                    self.draw()

if __name__ == "__main__":
    pygame.init()
    viewer = Display(dimensions)
