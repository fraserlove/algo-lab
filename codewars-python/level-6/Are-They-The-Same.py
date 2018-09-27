#Kata URL: https://www.codewars.com/kata/550498447451fbbd7600041c

def comp(a1, a2):
    correct = 0
    list = []
    copy = a2
    if a1 == None or a2 ==  None:
        return False
    for i in a1:
        done = []
        for j in copy:
            if j**.5 == i and j not in done:
                done.append(j)
                correct += 1
                to_del = a2.index(j)
                del a2[to_del]
    if correct == len(a1):
        return True
    else:
        return False
