import csv

class Driver():
    def __init__(self, args, time):
        self.name = args[0]
        self.team = args[1]
        self.time = time
        self.points = 0

def importData():
    array = []
    with open('data/input/grandprix.csv', 'r') as file:
        for row in csv.reader(file, delimiter=','):
            time = input('Enter the race time for {}: '.format(row[0]))
            array.append(Driver(row, time))
    return array

def bubbleSort(array):
    for i in range(len(array)-1,0,-1):
        for j in range(i):
            if array[j].time > array[j+1].time:
                array[j], array[j+1] = array[j+1], array[j]

def assignPoints(array):
    array[0].points = 25
    array[1].points = 18
    array[2].points = 15

def outputResults(array):
    print('Driver\t\t\tTeam\t\tTime\tPoints')
    for i in range(len(array)):
        print('{}\t{}\t{}\t{}'.format(array[i].name, array[i].team, array[i].time, array[i].points))

array = importData()
bubbleSort(array)
assignPoints(array)
outputResults(array)
