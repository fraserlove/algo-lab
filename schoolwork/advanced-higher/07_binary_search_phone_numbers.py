import csv

numbers = []
names = []

def importData():
    with open('data/input/phonenumbers.csv', 'r') as file:
        for row in csv.reader(file, delimiter=','):
            numbers.append(int(row[0]))
            names.append(row[1])


def binarySearch(array, val):
    start, end = 0, len(array)-1
    while start <= end:
        mid = (start+end)//2
        if array[mid] == val:
            return mid
        elif array[mid] < val:
            start = mid + 1
        else:
            end = mid - 1
    return -1

importData()
val = int(input('Enter a phone extension to search for: '))
result = binarySearch(numbers, val)
if result != -1:
    print('{} has the extension {}'.format(names[result], numbers[result]))
else:
    print('No matches found!')
