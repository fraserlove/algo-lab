import csv

rows = 6
cols = 15

def initArray():
    newArray =[[None for x in range(cols)] for y in range(rows)]
    return newArray

def populateArray(array):
    with open('data/input/test_scores.csv') as file:
        for i, row in enumerate(csv.reader(file, delimiter=',')):
            for j, element in enumerate(row):
                array[i][j] = element

def calcAvg(row):
    count = 0
    for val in row:
        count += int(val)
    return int(count/len(row)*10)

def displayResults(array):
    for x in range(1,len(array)):
        print(array[x][0], end='\t')
        for y in range(1,len(array[x])):
            print('{}%'.format(int(int(array[x][y])/int(array[0][y])*100)), end=' ')
        avg = calcAvg(array[x][1:len(array[x])])
        print('Total: {}%'.format(avg))

array = initArray()
populateArray(array)
displayResults(array)
