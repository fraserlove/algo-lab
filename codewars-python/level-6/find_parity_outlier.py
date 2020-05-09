#Kata URL: https://www.codewars.com/kata/5526fc09a1bbd946250002dc

def find_outlier(integers):
    list = []
    for counter in range(len(integers)):
        if integers[counter]%2 == 1:
           list.append(1)
        else:
           list.append(0)
    if list.count(1) == 1:
        position = list.index(1)
    if list.count(0) == 1:
        position = list.index(0)
    return integers[position]  
