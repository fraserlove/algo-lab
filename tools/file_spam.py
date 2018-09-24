"""
Created 23/03/18
Developed by Fraser Love
"""

import os
import random

sl = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
hl=[]
num = ["0","1","2","3","4","5","6","7","8","9"]
choice = [sl, hl, num]
r=[]
out =[]
for i in sl:
    hl.append(i.upper())
for i in range (0,1000):          #Amount of documents
    r = []
    for i in range (0, random.randint(5,25)):
        c = 0
        c = random.choice(choice)
        r.append(random.choice(c[random.randint(0, len(c) - 1)]))
    f = open("".join(r) +".txt","w+")
    for j in range(0,100):      #No of lines
        out =[]
        for a in range(0, random.randint(20,200)):      #Number of char in lines
            c = 0
            c = random.choice(choice)
            out.append(random.choice(c[random.randint(0, len(c) - 1)]))
        f.write("".join(out)+ "\n")
    f.close()
print("DONE")

