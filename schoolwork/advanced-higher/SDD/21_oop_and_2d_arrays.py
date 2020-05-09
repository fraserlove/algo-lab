import random

class Grid():
    def __init__(self, grid_size):
        self._grid = [['_' for i in range(grid_size[0])] for j in range(grid_size[1])]
        self._points = [(random.randint(0,grid_size[1]-1),random.randint(0,grid_size[0]-1)) for i in range(50)]
        self._correct = []
        self._incorrect = []
        self._choice = []
        self._answers = 0
        self.play()

    def enterLocation(self):
        choice = input('Enter a location: ').split(',')
        self._choice = (int(choice[0])-1, int(choice[1])-1)
        self._answers += 1
        if self._choice in self._points:
            self._correct.append(self._choice)
        else:
            self._incorrect.append(self._choice)
        self.display()

    def display(self):
        for i in range(len(self._grid)):
            for j in range(len(self._grid[i])):
                if (i,j) in self._correct:
                    print('f', end='')
                elif (i,j) in self._incorrect:
                    print('x', end='')
                else:
                    print(self._grid[i][j], end='')
            print('')

    def play(self):
        while self._answers < 10 and len(self._correct) < 5:
            self.enterLocation()
        if len(self._correct) >= 5:
            print('\nWell Done!')
        else:
            print('\nSorry you have lost!')

grid = Grid((20,10))
