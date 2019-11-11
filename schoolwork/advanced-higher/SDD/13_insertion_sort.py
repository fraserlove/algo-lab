import random

def genRandArray(length):
    array = random.sample(range(length), length)
    return array

def genReverseArray(length):
    array = [i for i in range(length-1,-1,-1)]
    return array

def genSortedArray(length):
    array = [i for i in range(0,length)]
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

sorted_array = genSortedArray(18)
reverse_array = genReverseArray(18)
random_array = genRandArray(18)
print('Best: ',end='')
insertionSort(sorted_array)
print('Worst: ',end='')
insertionSort(reverse_array)
print('Random: ',end='')
insertionSort(random_array)
