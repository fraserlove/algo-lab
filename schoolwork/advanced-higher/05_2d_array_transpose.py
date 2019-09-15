import csv

def initArray(rows, cols):
    newArray =[[0 for x in range(cols)] for y in range(rows)]
    return newArray

def transposeArray(array):
    # Creating a new Array with length of rows and cols switched
    newArray = initArray(len(array[0]), len(array))
    for x in range(len(array)):
        for y in range(len(array[0])):
            newArray[y][x] = array[x][y]
    return newArray

def print2DArray(array):
    row = ''
    for x in range(len(array)):
        for y in range(len(array[x])):
            row += str(array[x][y]) + ' '
        print(row)
        row = ''
    print()

array = initArray(6, 2)
print2DArray(array)
newArray = transposeArray(array)
print2DArray(newArray)
