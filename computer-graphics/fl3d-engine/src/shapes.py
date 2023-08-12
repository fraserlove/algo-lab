# Third party modules
import math

# Project-specific modules
from structures import Object3D, Matrix
import data_handling

class Cube(Object3D):
    def __init__(self, name, position, size, colour = 'grey'):
        Object3D.__init__(self, name, colour, position, 'Cube')
        self.size = size
        self.create(position)

    def get_size(self):
        return self.size

    def create(self, position = None):
        if position == None:
            position = self.position
        cx, cy, cz = position
        self.add_points(Matrix([[x,y,z] for x in (cx, cx + self.size) for y in (cy, cy + self.size) for z in (cz, cz + self.size)]))
        self.add_lines([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
        self.add_surfaces([(0,2,6,4), (1,3,7,5), (0,1,3,2), (5,4,6,7), (0,1,5,4), (3,2,6,7)])
        self.projected = self.points

    def set_size(self, size):
        self.clear_object_data()
        self.size = size
        self.create()

class Quad(Object3D):
    def __init__(self, name, position, length, width, height, colour = 'grey'):
        Object3D.__init__(self, name, colour, position, 'Quad')
        self.length, self.width, self.height = length, width, height
        self.create(position)

    def create(self, position = None):
        if position == None:
            position = self.position
        cx, cy, cz = position
        self.add_points(Matrix([[x,y,z] for x in (cx, cx + self.length) for y in (cy, cy + self.width) for z in (cz, cz + self.height)]))
        self.add_lines([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
        self.add_surfaces([(0,2,6,4), (1,3,7,5), (0,1,3,2), (5,4,6,7), (0,1,5,4), (3,2,6,7)])
        self.projected = self.points

    def get_length(self):
        return self.length
    
    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_length(self, length):
        self.clear_object_data()
        self.length = length
        self.create()

    def set_width(self, width):
        self.clear_object_data()
        self.width = width
        self.create()

    def set_height(self, height):
        self.clear_object_data()
        self.height = height
        self.create()

    def set_dimensions(self, length, width, height):
        self.set_length(length)
        self.set_width(width)
        self.set_height(height)

class Plane(Object3D):
    def __init__(self, name, position, length, width, colour = 'grey'):
        Object3D.__init__(self, name, colour, position, 'Plane', True)
        self.length, self.width = length, width
        self.create(position)

    def create(self, position = None):
        if position == None:
            position = self.position
        cx, cy, cz = position
        self.add_points(Matrix([[x,y,0] for x in (cx, cx + self.length) for y in (cy, cy + self.width)]))
        self.add_lines([(0,1), (1,3), (2,3), (0,2)])
        self.add_surfaces([(0,1,3,2)])
        self.projected = self.points

    def get_length(self):
        return self.length
    
    def get_width(self):
        return self.width

    def set_length(self, length):
        self.clear_object_data()
        self.length = length
        self.create()

    def set_width(self, width):
        self.clear_object_data()
        self.width = width
        self.create()

class Polygon(Object3D):
    def __init__(self, name, position, size, no_points, colour = 'grey'):
        Object3D.__init__(self, name, colour, position, 'Polygon', True)
        self.no_points, self.size = no_points, size
        self.create(position)

    def create(self, position = None):
        if position == None:
            position = self.position
        cx, cy, cz = position
        points = []
        for i in range(1,self.no_points + 1):
            x = (math.cos(2*math.pi / self.no_points * i) * self.size / self.no_points) + cx
            y = (math.sin(2*math.pi / self.no_points * i) * self.size / self.no_points) + cy
            cx, cy = x, y
            points.append([x,y,0])
        self.add_points(Matrix(points))
        self.add_lines([(n, (n + 1) % self.no_points) for n in range(0,self.no_points)])
        surfaces = []
        for i in range(0, self.no_points):
            surfaces.append(i)
        self.add_surfaces([surfaces])
        self.projected = self.points

    def get_no_points(self):
        return self.no_points

    def get_size(self):
        return self.size

    def set_no_points(self, no_points):
        self.clear_object_data()
        self.no_points = no_points
        self.create()

    def set_size(self, size):
        self.clear_object_data()
        self.size = size
        self.create()

class Sphere(Object3D):
    def __init__(self, name, position, radius, verts_res, colour = 'grey'):
        Object3D.__init__(self, name, colour, position, 'Sphere')
        self.radius, self.verts_res = radius, verts_res
        self.create(position)

    def create(self, position = None):
        if position == None:
            position = self.position
        cx, cy, cz = position
        points, lines, surfaces = [], [], []
        k = -1
        for i in range(self.verts_res):
            lat = data_handling.map(i, 0, self.verts_res, 0, math.pi)
            c = 0
            for j in range(self.verts_res):
                lon = data_handling.map(j, 0, self.verts_res, 0, 2 * math.pi)
                x = self.radius * math.sin(lon) * math.cos(lat) + cx
                y = self.radius * math.sin(lon) * math.sin(lat) + cy
                z = self.radius * math.cos(lon) + cz
                points.append([x,y,z])
                lines.append((j+k,j+k+1))
                if i + c + self.verts_res < self.verts_res ** 2:
                    lines.append((i+c, i + c + self.verts_res))
                else:
                    if i + c + self.verts_res == 0:
                        lines.append((i+c, 0))
                    else:
                        lines.append((i+c, self.verts_res ** 2 % (i+c)))
                if i + c + self.verts_res < self.verts_res ** 2:
                    surfaces.append((i+c, i+1+c, (i + self.verts_res+1+c) % self.verts_res ** 2, i + self.verts_res + c))
                else:
                    surfaces.append((i+c, (i+1+c) % self.verts_res ** 2, self.verts_res ** 2 % (i+c+1), self.verts_res ** 2 % (i+c)))
                c += self.verts_res
            k += self.verts_res
        self.add_points(Matrix(points))
        self.add_lines(lines)
        self.add_surfaces(surfaces)
        self.projected = self.points

    def get_radius(self):
        return self.radius

    def get_verts_res(self):
        return self.verts_res

    def set_radius(self, radius):
        self.clear_object_data()
        self.radius = radius
        self.create()

    def set_verts_res(self, verts_res):
        self.clear_object_data()
        self.verts_res = verts_res
        self.create()

class Line2D(Object3D):
    def __init__(self, name, position, degrees, magnitude, colour = 'grey'):
        Object3D.__init__(self, name, colour, position, 'Line2D')
        self.degrees, self.magnitude = degrees, magnitude
        self.create(position)

    def create(self, position = None):
        if position == None:
            position = self.position
        cx, cy, cz = position
        angle = math.radians(self.degrees)
        nx, ny = cx + (math.cos(angle) * self.magnitude), cy - (math.sin(angle) * self.magnitude)
        self.add_points(Matrix([[cx, cy, cz], [nx, ny, cz]]))
        self.add_lines([(0,1)])
        self.projected = self.points

    def get_angle(self):
        return self.degrees
    
    def get_magnitude(self):
        return self.magnitude

    def set_angle(self, angle):
        self.clear_object_data()
        self.degrees = angle
        self.create()

    def set_magnitude(self, magnitude):
        self.clear_object_data()
        self.magnitude = magnitude
        self.create()

class Line3D(Object3D):
    def __init__(self, name, position_1, position_2, colour = 'grey'):
        Object3D.__init__(self, name, colour, position_1, 'Line3D')
        self.position_1, self.position_2 = position_1, position_2

    def create(self, position = None):
        if position == None:
            position = self.position_1
        self.add_points(Matrix([[*position], [*self.position_2]]))
        self.add_lines([(0,1)])
        self.projected = self.points

    def get_start_point(self):
        return self.position_1

    def get_end_point(self):
        return self.position_2

    def set_start_point(self, start_point):
        self.clear_object_data()
        self.position_1 = start_point
        self.create()

    def set_end_point(self, end_point):
        self.clear_object_data()
        self.position_2 = end_point
        self.create()

class GUILines(Object3D):
    def __init__(self, position, length, colour = 'grey'):
        Object3D.__init__(self, name = 'GUI_Line', colour = colour)
        self.add_points(Matrix([[position[0], position[1], position[2]], [position[0] + length, position[1], position[2]],
                                [position[0], position[1] + length, position[2]]]))
        self.add_lines([(0,1), (0,2)])