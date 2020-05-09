
def importData():
    names, gears, types, prices = [], [], [], []
    with open('data/input/bikes.txt', 'r') as file:
        for row in file:
            row = row.rstrip().split(',')
            names.append(row[0])
            gears.append(row[1])
            types.append(row[2])
            prices.append(row[3])
    return names, gears, types, prices

def bubbleSort(arr, arr1, arr2, arr3):
    for outer in range(len(arr)-1,0,-1):
        for inner in range(outer):
            if arr[inner] > arr[inner+1]:
                arr[inner], arr[inner+1] = arr[inner+1], arr[inner]
                arr1[inner], arr1[inner+1] = arr1[inner+1], arr1[inner]
                arr2[inner], arr2[inner+1] = arr2[inner+1], arr2[inner]
                arr3[inner], arr3[inner+1] = arr3[inner+1], arr3[inner]

def insertionSort(arr, arr1, arr2, arr3):
    for i in range(0,len(arr)-1):
        cur = arr[i]
        cur1 = arr1[i]
        cur2 = arr2[i]
        cur3 = arr3[i]
        index = i
        while index > 0 and arr[index-1] > cur:
            arr[index] = arr[index-1]
            arr1[index] = arr1[index-1]
            arr2[index] = arr2[index-1]
            arr3[index] = arr3[index-1]
            index -= 1
        arr[index] = cur
        arr1[index] = cur1
        arr2[index] = cur2
        arr3[index] = cur3

def outputArrays(arr, arr1, arr2, arr3):
    print('\nName\tGears\tType\tPrice')
    for i in range(0,len(arr)-1):
        print('{}\t{}\t{}\t{}'.format(arr[i], arr1[i], arr2[i], arr3[i]))

names, gears, types, prices = importData()
insertionSort(prices, names, gears, types)
outputArrays(names, gears, types, prices)
