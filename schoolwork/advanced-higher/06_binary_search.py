
array = [3, 7, 9, 12, 15, 20, 25, 35, 67, 78]

def binarySearch(array, val):
    compares = 0
    start, end = 0, len(array)-1
    while start <= end:
        compares += 1
        mid = (start+end)//2
        if array[mid] == val:
            return mid, compares
        elif array[mid] < val:
            start = mid + 1
        else:
            end = mid - 1
    return -1, compares

result, compares = binarySearch(array, 15)
if result != -1:
    print('The value was found at position {}'.format(result))
else:
    print('The value was not found in the array')
print ('\n{} comparisons were made'.format(compares))
