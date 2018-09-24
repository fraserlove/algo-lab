"""
Developed by Fraser Love
"""
step = 100000
session = True
increment = 0
while session:
    if increment >= step:
        print("Number: " + str(increment))
        step += 100000
    increment = str(increment)
    increment = list(increment)
    lst = list(increment)
    for j in range(0,len(lst)-1):
        c = lst[j]
        lst[j] = lst[-1]
        lst[-1] = c
    lst = "".join(lst)
    increment = "".join(increment)
    if int(increment) == int(lst)*2:
        print(increment)
    increment = int(increment)
    increment += 1
