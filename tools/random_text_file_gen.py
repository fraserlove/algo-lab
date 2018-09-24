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
f = open("".join(r) +".txt","w+")
for a in range(0,1000000):      #Number of char in lines
    c = 0
    c = random.choice(choice)
    out.append(random.choice(c[random.randint(0, len(c) - 1)]))
f.write("".join(out))
f.close()
print("DONE")
