
array = [53, 42, 2, 98, 9, 34, 95, 67, 4, 81, 55, 12, 27, 64]

def bubbleSortConditional(array):
    passes = 0
    swaps = True
    outer = len(array)-1
    while outer >= 0 and swaps == True:
        swaps = False
        for inner in range(outer):
            if array[inner] > array[inner+1]:
                array[inner], array[inner+1] = array[inner+1], array[inner]
                swaps = True
        outer -= 1
        passes += 1
        print('Pass {}: {}'.format(passes, array))

bubbleSortConditional(array)
