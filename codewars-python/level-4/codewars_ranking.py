#Kata URL: https://www.codewars.com/kata/51fda2d95d6efda45e00004e

class User(object):
    def __init__(self):
        self.rank = -8        
        self.progress = 0
        
    def inc_progress(self, rank):
        if rank < -8 or rank > 8 or rank == 0:
            return error
        if rank == self.rank:
            self.progress += 3
        elif rank < self.rank - 2:
            return
        elif rank < self.rank:
            self.progress += 1
        elif rank > self.rank and self.rank:
            if rank > 0 and self.rank < 0:
                d = rank - self.rank -1
            else:
                d = rank - self.rank
            self.progress += (10 * d * d)
        while self.progress >= 100 and self.rank < 8:
            if self.rank == -1:
                self.rank = 1
                self.progress -= 100
            else:
                self.rank += 1
                self.progress -= 100
        if self.rank == 8:
            self.progress = 0          
