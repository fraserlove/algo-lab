#Kata URL: https://www.codewars.com/kata/578553c3a1b8d5c40300037c

def binary_array_to_number(arr):
    total = 0
    for i in range(len(arr)):
        if arr[i] == 1:
            total += arr[i] * (2**(len(arr) - i - 1))
    return total
