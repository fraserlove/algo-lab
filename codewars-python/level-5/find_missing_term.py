#Kata URL: https://www.codewars.com/kata/find-the-missing-term-in-an-arithmetic-progression/python

def find_missing(sequence):
    diff = []
    num = []
    for i in range(0,len(sequence)):
        if i+1 < len(sequence):
            diff.append(sequence[i+1] - sequence[i])
    for j in diff:
        if j not in num:
            num.append(j)
        else:
            seq = j   
    for i in range(0,len(sequence)):
        if sequence[i+1] != sequence[i] + seq and i < len(sequence):
            return(sequence[i] + seq)
