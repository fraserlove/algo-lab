import csv

def importData():
    array = []
    with open('data/input/router.csv', 'r') as file:
        for row in csv.reader(file, delimiter=','):
            array.append(row)
    return array

def bubbleSort(array):
    for i in range(len(array)-1,0,-1):
        for j in range(i):
            if int(array[j][0].split('.')[3]) > int(array[j+1][0].split('.')[3]):
                array[j], array[j+1] = array[j+1], array[j]

def outputResults(array):
    for i in range(len(array)-1):
        print('{}\t{}\t{}'.format(array[i][0], array[i][1], array[i][2]))

array = importData()
bubbleSort(array)
outputResults(array)
