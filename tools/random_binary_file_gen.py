"""
Created 23/03/18
Developed by Fraser Love
"""
import os
import random

binary = ["0","1"]
out = []
f = open("binary" +".txt","w+")
for a in range(0,100000000):      #Number of char in lines
    out.append(random.choice(binary[random.randint(0,1)]))
f.write("".join(out))
f.close()
print("DONE")
