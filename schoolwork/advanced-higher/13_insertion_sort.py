import random

def initArray(length):
    array = random.sample(range(length), length)
    return array

def insertionSort(array):
    passes, swaps = 0, 0
    for i in range(0,len(array)-1):
        passes += 1
        cur = array[i]
        index = i
        while index > 0 and array[index-1] > cur:
            array[index] = array[index-1]
            index -= 1
            swaps += 1
        array[index] = cur
        print('Passes: {} Swaps: {} {}'.format(passes, swaps, array))

array = initArray(18)
insertionSort(array)
