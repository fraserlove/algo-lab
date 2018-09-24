"""
Created 23/03/18
Developed by Fraser Love
"""
import smtplib, time, datetime
import random

def func1():
    global message
    email = 'your_email.com'
    password = 'yourpassword'
    send_to_email = 'target_email.com'
    message = []


    sl = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    hl=[]
    num = ["0","1","2","3","4","5","6","7","8","9"]
    choice = [sl, hl, num]
    r=[]
    out =[]
    for i in sl:
        hl.append(i.upper())
    for a in range(0,100):      #Number of char in lines
        c = 0
        c = random.choice(choice)
        out.append(random.choice(c[random.randint(0, len(c) - 1)]))
    for i in range(0,10):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, send_to_email , out)
        server.quit()
        print(sending)
        message = []


