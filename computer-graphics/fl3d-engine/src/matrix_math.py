# Third party modules
import math

# Project-specific modules
import structures

''' Provides mathematical functions for used in math structures '''

''' Multiplies two matrices together if they are conformable '''
def multiply(matrix_1, matrix_2):
    if matrix_1.no_cols() != matrix_2.no_rows():
        print("ERROR: Matrix 1's {} columns do not match Matrix 2's {} rows".format(matrix_1.no_cols(), matrix_2.no_rows()))
        return None
    result = structures.Matrix(matrix_1.no_rows(), matrix_2.no_cols())

    # Finding the dot product of the row of matrix 1 and the column of matrix 2 for each element in the new matrix
    for y in range(matrix_1.no_rows()):
        for x in range(matrix_2.no_cols()):
            sum = 0
            for i in range(matrix_1.no_cols()):
                sum += matrix_1.access_index(y, i) * matrix_2.access_index(i, x)
            result.set_index(y, x, sum)
    return result

def h_stack(matrix_1, matrix_2):
    ''' Adds matrix_2 to the right columns of matrix_1 '''
    result = structures.Matrix(matrix_1.no_rows(), matrix_1.no_cols() + matrix_2.no_cols())
    for y in range(matrix_1.no_rows()):
        result.set_row(y, matrix_1.access_row(y) + matrix_2.access_row(y))
    return result       

def add_vector(matrix, vector):
    if isinstance(matrix, list):
        matrix = structures.Matrix([matrix])
    result = structures.Matrix(matrix.no_rows(), matrix.no_cols())
    for y in range(matrix.no_rows()):
        for x in range(matrix.no_cols()):
            result.set_index(y, x, matrix.access_index(y, x) + vector[x])
    return result

def inverse_vector(vector):
    new_vector = []
    for y in range(len(vector)):
        new_vector.append(- vector[y])
    return new_vector

def orthographic_projection_matrix():
    ''' Returns a matrix used in projection to provide depth '''
    return structures.Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

def perspective_projection_matrix(dz):
    ''' Returns a matrix used in projection to provide depth '''
    if (10 - dz) == 0:
        z = 0
    else:
        z = 1 / (10 - dz)
    return structures.Matrix([
        [z, 0, 0, 0],
        [0, z, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

def translation_matrix(dx = 0, dy = 0, dz = 0):
    ''' Returns a matrix for a translation of (dx, dy, dz) '''
    return structures.Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1],
    ])

def scale_matrix(kx, ky, kz):
    ''' Returns a matrix for scaling by (kx, ky, kz) '''
    return structures.Matrix([
        [kx, 0, 0, 0],
        [0, ky, 0, 0],
        [0, 0, kz, 0],
        [0, 0, 0, 1],
    ])

def rotate_x_matrix(rx):
    ''' Returns a matrix for rotation about the x-axis by rx radians '''
    cos = math.cos(rx)
    sin = math.sin(rx)
    return structures.Matrix([
        [1, 0, 0, 0],
        [0, cos, -sin, 0],
        [0, sin, cos, 0],
        [0, 0, 0, 1],
    ])

def rotate_y_matrix(ry):
    ''' Returns a matrix for rotation about the x=y-axis by ry radians '''
    cos = math.cos(ry)
    sin = math.sin(ry)
    return structures.Matrix([
        [cos, 0, sin, 0],
        [0, 1, 0, 0],
        [-sin, 0, cos, 0],
        [0, 0, 0, 1],
    ])

def rotate_z_matrix(rz):
    ''' Returns a matrix for rotation about the z-axis by rz radians '''
    cos = math.cos(rz)
    sin = math.sin(rz)
    return structures.Matrix([
        [cos, -sin, 0, 0],
        [sin, cos, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

def convert_to_int_matrix(matrix):
    result = structures.Matrix(matrix.no_rows(), matrix.no_cols())
    for y in range(matrix.no_rows()): 
         for x in range(matrix.no_cols()):
             result.set_index(y, x, int(matrix.access_index(y, x)))
    return result