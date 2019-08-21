#Kata URL: https://www.codewars.com/kata/554b4ac871d6813a03000035

def high_and_low(numbers):
    list = numbers.split()
    highest_num = int(list[0])
    lowest_num = int(list[0])
    i = 0
    while i < len(list):
        if int(list[i]) > highest_num:
            highest_num = int(list[i])
        if int(list[i]) < lowest_num:
            lowest_num = int(list[i])
        i += 1 
    return str(highest_num) + " " + str(lowest_num)
