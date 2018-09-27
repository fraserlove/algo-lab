#Kata URL: https://www.codewars.com/kata/546e2562b03326a88e000020

def square_digits(num):
    ans = []
    lst = [int(d) for d in str(num)]
    for i in range(len(lst)):
        if lst[i] >= 1:
            sqr = lst[i]**2
            ans.append(str(sqr))
    ans = int(''.join(ans))
    return ans
