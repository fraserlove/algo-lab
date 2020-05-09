import math

class Circle():
    def __init__(self, radius):
        self._radius = radius

    def getRadius(self):
        return self._radius

    def setRadius(self, radius):
        self._radius = radius

    def area(self):
        return math.pi * self._radius**2

class Cone(Circle):
    def __init__(self, radius, height):
        Circle.__init__(self, radius)
        self._height = height

    def setHeight(self, height):
        self._height = height

    def getHeight(self):
        return self._height

    def area(self):
        return math.pi*self._radius*(self._radius+math.sqrt(self._height**2+self._radius**2))

    def volume(self):
        return math.pi*self._radius**2*self._height/3

class Cylinder(Circle):
    def __init__(self, radius, height):
        Circle.__init__(self, radius)
        self._height = height

    def setHeight(self, height):
        self._height = height

    def getHeight(self):
        return self._height

    def area(self):
        return 2*math.pi*self._radius*self._height + 2*math.pi*self._radius**2

    def volume(self):
        return math.pi*self._radius**2*self._height

class Sphere(Circle):
    def __init__(self, radius):
        Circle.__init__(self, radius)

    def area(self):
        return 4*math.pi*self._radius**2

    def volume(self):
        return 4/3*math.pi*self._radius**3

class Square():
    def __init__(self, height):
        self._height = height

    def area(self):
        return self._height**2

class Rectange(Square):
    def __init__(self, height, width):
        Square.__init__(self, height)
        self._width = width

    def area(self):
        return self._height*self._width

class Trapezioid(Square):
    def __init__(self, height, base1, base2):
        Square.__init__(self, height)
        self._base1 = base1
        self._base2 = base2

    def area(self):
        return (self._base1+self._base2)/2*self._height

class Triange(Square):
    def __init__(self, height, base):
        Square.__init__(self, height)
        self._base = base

    def area(self):
        return self._base/2*self._height

square = Square(10)
print(square.area())
rectangle = Rectange(10,6)
print(rectangle.area())
trapezioid = Trapezioid(8,15,20)
print(trapezioid.area())
triange = Triange(10,13)
print(triange.area())
