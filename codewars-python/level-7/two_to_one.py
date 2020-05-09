#Kata URL: https://www.codewars.com/kata/5656b6906de340bd1b0000ac

def longest(s1, s2):
    sort = sorted(s1 + s2)
    lst = []
    for i in range(len(sort)):
        if sort[i] not in lst:
            lst.append(sort[i])
    output = "".join(lst)
    return output
