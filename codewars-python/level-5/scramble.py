#Kata URL: https://www.codewars.com/kata/55c04b4cc56a697bb0000048/

def scramble(s1,s2):
    inpt = []
    correct = 0
    done_before = []
    already = []
    d = 0
    for char in s1:
        inpt += char
        if s2.count(char) != s1.count(char) and len(s1) == len(s2):
            return False
    for char in s1:
        if char not in already:
            no_times = s2.count(char)
            if no_times > 1:
                d += 1
                already.append(char)
        for a in range(no_times):
            if char in s2 and char not in done_before:
                correct += 1
                done_before.append(char)
    if correct == len(s2) - d:
        return True
    else:
        return False
