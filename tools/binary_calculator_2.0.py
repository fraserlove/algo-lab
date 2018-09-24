"""
Created 20/05/18
Developed by Fraser Love
"""
from pynput.keyboard import Key, Listener

def user_input(inpt):
    text = []
    if inpt.isdigit() == False:
        for i in inpt: text.append(ord(i))
    else: text.append(int(inpt))
    calculate(text)

def calculate(text):
    for j in range(0,len(text)): text[j] = bin(text[j])
    display(text)

def display(text):
    for c in text: c = str(c).split("0b"); print(c[1],end="")
    retry = str(input("\n\nPress space to convert again..."))
    if retry == " ": user_input(inpt = str(input("\nWhat would you like to convert: ")))           

user_input(inpt = str(input("\nWhat would you like to convert: ")))
