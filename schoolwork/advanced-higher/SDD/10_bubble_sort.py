
array = [53, 42, 2, 98, 9, 34, 95, 67, 4, 81, 55, 12, 27, 64]

def bubbleSort(array):
    passes, swaps = 0, 0
    for outer in range(len(array)-1,0,-1):
        for inner in range(outer):
            if array[inner] > array[inner+1]:
                array[inner], array[inner+1] = array[inner+1], array[inner]
                swaps += 1
        passes += 1
        print('Pass {} Swaps {}: {}'.format(passes, swaps, array))

bubbleSort(array)
