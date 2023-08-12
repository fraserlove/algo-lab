# Third party modules
import math

# Project-specific modules
import matrix_math
import data_handling

class Matrix():
    ''' A matrix object that has zero based indexing'''
    def __init__(self, *args):
        ''' Overloading to create a new matrix with specified dimension or initialise with a 2d array '''
        if len(args) > 1:
            self.rows = args[0]
            self.cols = args[1]
            if len(args) > 2:
                self.matrix = [[args[2] for x in range(self.cols)] for y in range(self.rows)]
            else:
                self.matrix = [[0 for x in range(self.cols)] for y in range(self.rows)]
        elif len(args) == 1:
            self.rows = len(args[0])
            self.cols = len(args[0][0])
            self.matrix = args[0]
        else:
            print('ERROR: Invalid arguments provided when initialising matrix: ', args)

    def __iter__(self):
        for y in range(self.rows):
            yield self.matrix[y]

    def __len__(self):
        return self.rows

    def show(self):
        ''' Displays the entire matrix and its dimension '''
        print("Matrix: ", self.rows, "x", self.cols)
        for y in range(self.rows):
            for x in range(self.cols):
                print(self.matrix[y][x], " ", end="")
            print("")
    
    def copy(self):
        new_matrix = Matrix(self.rows, self.cols)
        for y in range(self.rows):
            for x in range(self.cols): 
                new_matrix.set_index(y, x, self.matrix[y][x])
        return new_matrix
    
    def no_rows(self):
        return self.rows
    
    def no_cols(self):
        return self.cols
    
    def access_index(self, y, x):
        return self.matrix[y][x]
    
    def set_index(self, y, x, value):
        self.matrix[y][x] = value
    
    def access_row(self, y):
        return self.matrix[y]
    
    def set_row(self, y, values):
        self.matrix[y] = values

    def sum_column(self, y):
        return sum([point[y] for point in self.matrix])

    def access_matrix(self):
        return self.matrix
    
class Object3D():
    def __init__(self, name, colour, position = None, _type = None, is_2d = False):
        self.name = name
        self.type = _type
        self.position = position
        self.points = Matrix(0, 0)
        self.projected = Matrix(0, 0)
        self.surfaces = []
        self.lines = []
        self.is_2d = is_2d

        self.colour = colour

    def surface_mean_y(self, surface):
        sum = 0
        for point in surface:
            sum += self.projected.access_row(point)[1]
        return data_handling.div_non_zero(sum, len(surface))

    def surface_mean_z(self, surface):
        sum = 0
        for point in surface:
            sum += self.projected.access_row(point)[2]
        return data_handling.div_non_zero(sum, len(surface))

    def order_surfaces(self):
        ''' Surfaces must be ordered so that the closest surfaces are drawn first to remove display errors where surfaces furhter behind are drawn over closer surfaces '''
        ''' Uses insertion sort '''
        for i in range(len(self.surfaces)):
            current = self.surfaces[i]
            index = i
            while index > 0 and self.surface_mean_z(self.surfaces[index-1]) > self.surface_mean_z(current):
                self.surfaces[index] = self.surfaces[index-1]
                index -= 1
            self.surfaces[index] = current
        return self.surfaces
        
    def find_points(self, surface):
        ''' Returns a list of coordinates in a given surface '''
        points = []
        for point in surface:
            points.append([int(self.projected.access_row(point)[0]), int(self.projected.access_row(point)[1])])
        return points

    def hue(self, surface, lighting_factor):
        return int(data_handling.map(-(self.surface_mean_y(surface) - self.find_centre()[1]), data_handling.div_non_zero(- self.surface_mean_y(surface), lighting_factor), data_handling.div_non_zero(self.surface_mean_y(surface), lighting_factor), 0, 255))

    def map_colour(self, surface, lighting_factor):
        colours = {'red': (255, self.hue(surface, lighting_factor), self.hue(surface, lighting_factor)), 'magenta': (255, self.hue(surface, lighting_factor), 255), 'green': (self.hue(surface, lighting_factor), 255, self.hue(surface, lighting_factor)),
                   'blue': (self.hue(surface, lighting_factor), self.hue(surface, lighting_factor), 255), 'yellow': (255, 255, self.hue(surface, lighting_factor)), 'cyan': (self.hue(surface, lighting_factor), 255, 255),
                   'grey': (self.hue(surface, lighting_factor), self.hue(surface, lighting_factor), self.hue(surface, lighting_factor))
                    }
        if self.colour in colours:
            return colours[self.colour]
        else:
            print ('ERROR: Choose a colour from: \'red\', \'magenta\', \'green\', \'blue\', \'yellow\', \'cyan\', \'grey\'')

    def viewer_relativity(self, viewer_width, viewer_height):
        ''' Returns an array of the directions to which the object is off the screen '''
        x, y = self.find_centre()[0], self.find_centre()[1]
        directions = []
        if x < 0:
            directions.append('W')
        if x > viewer_width:
            directions.append('E')
        if y < 0:
            directions.append('N')
        if y > viewer_height:
            directions.append('S')
        return directions

    def check_render_distance(self, max_render_distance, min_render_distance):
        # If the shape is 2D, automatically return true
        render = False
        if self.is_2d:
            render = True
        if abs(self.find_centre()[2]) < data_handling.div_non_zero(1, max_render_distance) or abs(self.find_centre()[2]) < data_handling.div_non_zero(1, min_render_distance):
            render = True
        return render

    def is_visible(self, viewer_width, viewer_height):
        return True if (len(self.viewer_relativity(viewer_width, viewer_height)) == 0) else False

    def add_points(self, points):
        new_column = Matrix(len(points), 1, 1)
        new_matrix = matrix_math.h_stack(points, new_column)
        self.points = new_matrix
        
    def add_lines(self, lines):
        self.lines += lines
    
    def add_surfaces(self, surfaces):
        self.surfaces += surfaces

    def show_points(self):
        for i, (x, y, z) in enumerate(self.points):
            print('{}: ({}, {}, {})'.format(i, x, y, z))

    def show_lines(self):
        for i, (node_1, node_2) in enumerate(self.lines):
            print('{}: {} to {}'.format(i, node_1, node_2))

    def project(self, projection_type, projection_anchor):
        self.projected = self.points.copy()
        for i, point in enumerate(self.projected):
            if projection_type == 'orthographic':
                projection_matrix = matrix_math.orthographic_projection_matrix()
            elif projection_type == 'perspective':
                projection_matrix = matrix_math.perspective_projection_matrix(point[2])
            else:
                print('ERROR: Invaild projection type entered: {}'.format(projection_type))
            self.projected.set_row(i, matrix_math.add_vector(matrix_math.multiply(matrix_math.add_vector(point, matrix_math.inverse_vector(projection_anchor)), projection_matrix), projection_anchor).access_row(0))
    
    def translate(self, translation):
        translation_matrix = matrix_math.translation_matrix(*translation)
        self.points = matrix_math.multiply(self.points, translation_matrix)

    def scale(self, scale_factor, anchor = None): # Anchor is a point object which stores the point to scale from
        ''' Scales the object from an arbetrary point '''
        if anchor == None:  # If no anchor is provided, scale from objects centre
            anchor = self.find_centre()
        scale_matrix = matrix_math.scale_matrix(*scale_factor)
        self.points = matrix_math.add_vector(matrix_math.multiply(matrix_math.add_vector(self.points, matrix_math.inverse_vector(anchor)), scale_matrix), anchor) # Equivalent to self.points = scale_factor * (self.points - anchor) + anchor

    def find_centre(self):
        cx = data_handling.div_non_zero(self.points.sum_column(0), len(self.points))
        cy = data_handling.div_non_zero(self.points.sum_column(1), len(self.points))
        cz = data_handling.div_non_zero(self.points.sum_column(2), len(self.points))
        return (cx, cy, cz, 0)
    
    def no_points(self):
        return len(self.points)

    def sum_x(self):
        return self.points.sum_column(0)

    def sum_y(self):
        return self.points.sum_column(1)

    def sum_z(self):
        return self.points.sum_column(2)

    def _rotate_z(self, anchor, z_rotation):      
        rotate_z_matrix = matrix_math.rotate_z_matrix(z_rotation)  
        self.points = matrix_math.add_vector(matrix_math.multiply(matrix_math.add_vector(self.points, matrix_math.inverse_vector(anchor)), rotate_z_matrix), anchor)

    def _rotate_x(self, anchor, x_rotation):
        rotate_x_matrix = matrix_math.rotate_x_matrix(x_rotation)        
        self.points = matrix_math.add_vector(matrix_math.multiply(matrix_math.add_vector(self.points, matrix_math.inverse_vector(anchor)), rotate_x_matrix), anchor)

    def _rotate_y(self, anchor, y_rotation):
        rotate_y_matrix = matrix_math.rotate_y_matrix(y_rotation)      
        self.points = matrix_math.add_vector(matrix_math.multiply(matrix_math.add_vector(self.points, matrix_math.inverse_vector(anchor)), rotate_y_matrix), anchor)

    def rotate(self, rotation, anchor):
        rx, ry, rz = rotation
        self._rotate_x(anchor, rx)
        self._rotate_y(anchor, ry)
        self._rotate_z(anchor, rz)

    def get_type(self):
        return self.type

    def get_colour(self):
        return self.colour

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def point_count(self):
        return len(self.points)

    def line_count(self):
        return len(self.lines)
    
    def surface_count(self):
        return len(self.surfaces)

    def update_position(self):
        self.position = self.points.access_row(0)[:3]

    def set_position(self, position):
        self.position = position
        current_position = self.points.access_row(0)
        # d_vector is a vector to calculate and store the difference between the new and current first points, which can then be applied to the whole points matrix
        self.d_vector = current_position[0] - position[0], current_position[1] - position[1], current_position[2] - position[2], current_position[3]
        self.projected = self.points = matrix_math.add_vector(self.points, matrix_math.inverse_vector(self.d_vector))

    def set_name(self, name):
        self.name = name
    
    def set_colour(self, colour):
        self.colour = colour

    def clear_object_data(self):
        self.points, self.projected = Matrix(0, 0), Matrix(0, 0)
        self.surfaces, self.lines = [], []

    def get_surfaces(self):
        return self.surfaces

    def get_points(self):
        return self.points.matrix