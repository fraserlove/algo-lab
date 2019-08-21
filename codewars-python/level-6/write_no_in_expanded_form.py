#Kata URL: https://www.codewars.com/kata/5842df8ccbd22792a4000245

def expanded_form(num):
    digits = [int(x) for x in str(num)]
    ans = []
    for i in range(len(digits)):
        if digits[i] != 0:
            if i != len(digits) - 1:
                size = digits[i] * 10**(len(digits) - 1 - i)
                ans.append(size)
            else:
                ans.append(digits[len(digits) - 1])
    return ' + '.join(map(str, ans))
