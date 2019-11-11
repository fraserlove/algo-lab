import csv

words = []
meanings = []

def importData():
    with open('data/input/dictionary.csv', 'r') as file:
        for row in csv.reader(file, delimiter=','):
            words.append(row[0])
            meanings.append(row[1])


def binarySearch(array, val):
    start, end = 0, len(array)-1
    while start <= end:
        mid = (start+end)//2
        if array[mid].lower() == val:
            return mid
        elif array[mid] < val:
            start = mid + 1
        else:
            end = mid - 1
    return -1

importData()
val = input('Enter a word: ').lower()
result = binarySearch(words, val)
if result != -1:
    print('Definition of {}: {}'.format(words[result].lower(), meanings[result].lower()))
else:
    print('No matches found!')
