#Kata URL: https://www.codewars.com/kata/5287e858c6b5a9678200083c

def narcissistic( value ):
    total = 0
    lst = [int(d) for d in str(value)]
    for i in range(len(lst)):
        total += lst[i]**len(lst)
    if total == value:
        return True
    else:
        return False
