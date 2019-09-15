import csv

rows = 8
cols = 8

def initArray():
    newArray =[[None for x in range(cols)] for y in range(rows)]
    return newArray

def populateArray(array):
    with open('data/input/bitmap.csv') as file:
        for i, row in enumerate(csv.reader(file, delimiter=',')):
            for j, pixel in enumerate(row):
                array[i][j] = str(pixel)

def incrementBrightness(array):
    to_bright = False
    for x in range(len(array)):
        for y in range(len(array[x])):
            if int(array[x][y]) < 255:
                array[x][y] = str(round(int(array[x][y]) * 1.1))
            if int(array[x][y]) > 255:
                to_bright = True
    return to_bright

def outputToCSV(array, to_bright):#
    if to_bright == False:
        with open('data/output/new_bitmap.csv', 'w') as file:
            for x in range(len(array)):
                file.write(','.join(array[x])+'\n')

array = initArray()
populateArray(array)
to_bright = incrementBrightness(array)
outputToCSV(array, to_bright)
