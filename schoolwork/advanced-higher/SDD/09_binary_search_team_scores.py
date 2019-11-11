import csv

def importData():
    with open('data/input/teamscores.csv', 'r') as file:
        array =[[None for x in range(5)] for y in range(0,250)]
        for i, row in enumerate( csv.reader(file, delimiter=',')):
            for j, item in enumerate(row):
                array[i][j] = str(item)
        return array

def binarySearch(array, val):
    start, end = 0, len(array)-1
    while start <= end:
        mid = (start+end)//2
        if array[mid][0].lower() == val:
            return mid
        elif array[mid][0].lower() < val:
            start = mid + 1
        else:
            end = mid - 1
    return -1


array = importData()
val = input('Enter Team Name: ').lower()
result = binarySearch(array, val)
if result != -1:
    print('Round Scores: {}'.format(' '.join(array[result][1:5])))
    print('Total Score: {}'.format(sum(map(int,map(str, array[result][1:5])))))
else:
    print('No matches found!')
