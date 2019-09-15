import random

rows = 4
cols = 5

search_value = 6

def initArray():
    newArray =[[None for x in range(cols)] for y in range(rows)]
    return newArray

def search2DArray(array, value):
    for x in range(len(array)):
        for y in range(len(array[x])):
            if array[x][y] == search_value:
                print('({},{})'.format(x,y))

def populateArray(array):
    for x in range(rows):
        for y in range(cols):
            random_value = random.randint(0,25)
            array[x][y] = random_value
    return array

def print2DArray(array):
    row = ''
    for x in range(len(array)):
        for y in range(len(array[x])):
            row += str(array[x][y]) + ' '
        print(row)
        row = ''
    print()

array = initArray()
array = populateArray(array)
print2DArray(array)
search2DArray(array, search_value)
