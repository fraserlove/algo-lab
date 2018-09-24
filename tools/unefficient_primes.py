"""
Created 18/04/18
Developed by Fraser Love
"""
import time

int_lst = [1]
primes = []
passes = 0
start_time = time.time()

while passes < 1000:
    in_list = False
    if int_lst[0] == 1:
        int_lst[0] = 2
    for i in int_lst:
        if i > int_lst[-1]/2:
            break
        for j in int_lst:
            if j > int_lst[-1]/2 or j > i:
                break
            if (int_lst[-1]) == i * j:
                in_list = True
    if in_list == False:
        primes.append(int_lst[-1])
        print(int_lst[-1])
    int_lst.append(int_lst[-1] + 1)
    passes += 1
print(primes)
print("Completed In: %.5s seconds" % (time.time() - start_time))
