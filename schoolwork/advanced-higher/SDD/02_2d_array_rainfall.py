import csv

rows = 52
cols = 7

def initArray():
    newArray =[[None for x in range(cols)] for y in range(rows)]
    return newArray

def populateArray(array):
    with open('data/input/rainfall.csv') as file:
        for i, row in enumerate(csv.reader(file, delimiter=',')):
            for j, day in enumerate(row):
                array[i][j] = int(day)

def findTotal(array):
    total = 0
    for x in range(len(array)):
        for y in range(len(array[x])):
            total += array[x][y]
    return total

def weeklyStats(array):
    for x in range(len(array)):
        total = 0
        least, most = array[x][0], array[x][0]
        for y in range(len(array[x])):
            total += array[x][y]
            if array[x][y] < least:
                least = array[x][y]
            if array[x][y] > most:
                most = array[x][y]
        yield least, most, total

array = initArray()
populateArray(array)
print(findTotal(array))
for week in weeklyStats(array):
    print('Least:{} Most:{} Total:{}'.format(week[0],week[1],week[2]))
