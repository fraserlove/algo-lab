import csv

class Pupil():
    def __init__(self, args):
        self.name = args[0]
        self.form = args[1]
        self.prelim = int(args[2])
        self.coursework = int(args[3])
        self.total = round(((self.prelim + self.coursework)/160)*100,1)

def importData():
    array = []
    with open('data/input/marks.csv', 'r') as file:
        for row in csv.reader(file, delimiter=','):
            array.append(Pupil(row))
    return array

def bubbleSort(array, order):
    for i in range(len(array)-1,0,-1):
        for j in range(i):
            if array[j].total < array[j+1].total and order == 0:
                array[j], array[j+1] = array[j+1], array[j]
            if array[j].total > array[j+1].total and order == 1:
                array[j], array[j+1] = array[j+1], array[j]

def displayResults(array):
    print('Results')
    for i in range(0,3):
        print('{}\t{}%'.format(array[i].name, array[i].total))

array = importData()
bubbleSort(array, 0)
displayResults(array)
