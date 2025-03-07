def smallest_int(arr: list[int]) -> int:
    '''Returns the smallest positive integer, i, not in arr.'''
    arr = set(arr)
    i = 1
    while i in arr:
        i += 1
    return i