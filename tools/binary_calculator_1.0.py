"""
Created 12/08/17
Developed by Fraser Love
"""

import time

def calculate (number, length):
    global c
    c = []
    n = -1
    if number < 2 ** 8:
        n += 8
    elif number < 2 ** 16:
        n += 16
    elif number < 2 ** 32:
        n += 32
    elif number < 2 ** 64:
        n += 64
    elif number < 2 ** 128:
        n += 128
    while length > 0:
        length -= 1
        while number >= 0 and n > -1:
           if number >= 2 ** n:
               c.append("1")
               number -= 2 ** n
               n -= 1
           else:
              c.append ("0")
              n -= 1

    for counter in c:
        print (counter,end=' ')

def details ():
    global length
    choice = str(input ("\nWould you like to convert a number or text: "))
    while choice == "number" or choice == "text":
        if choice == "number":
            number = int (input("\nWhat number would you like to convert: "))
            length = 1
            print ("\nConverted into binary: ")
            calculate (number, length)
            choice = "retry"
        elif choice == "text":
            textinput = str(input ("\nWhat text would you like to convert: "))
            format = str (input ("\nType 1 to output as a collum or Type 2 to output as a string: "))
            length = 0
            print ("\nSucessfully converted", textinput, "into binary: ")
            while length != len (textinput):
                letter = textinput[length]
                length += 1
                if letter == " ":
                   number = 32
                elif letter == "!":
                    number = 33
                elif letter == "\"":
                    number = 34
                elif letter == "#":
                    number = 35
                elif letter == "$":
                    number = 36
                elif letter == "%":
                    number = 37
                elif letter == "&":
                    number = 38
                elif letter == "\'":
                    number = 39
                elif letter == "(":
                    number = 40
                elif letter == ")":
                    number = 41
                elif letter == "*":
                    number = 42
                elif letter == "+":
                    number = 43
                elif letter == ",":
                    number = 44
                elif letter == "-":
                    number = 45
                elif letter == ".":
                    number = 46
                elif letter == "/":
                    number = 47
                elif letter == "0":
                    number = 48
                elif letter == "1":
                    number = 49
                elif letter == "2":
                    number = 50
                elif letter == "3":
                    number = 51
                elif letter == "4":
                    number = 52
                elif letter == "5":
                    number = 53
                elif letter == "6":
                    number = 54
                elif letter == "7":
                    number = 55
                elif letter == "8":
                    number = 56
                elif letter == "9":
                    number = 57
                elif letter == ":":
                    number = 58
                elif letter == ";":
                    number = 59
                elif letter == "<":
                    number = 60
                elif letter == "=":
                    number = 61
                elif letter == ">":
                    number = 62
                elif letter == "?":
                    number = 63
                elif letter == "@":
                    number = 64
                elif letter == "A":
                    number = 65
                elif letter == "B":
                    number = 66
                elif letter == "C":
                    number = 67
                elif letter == "D":
                    number = 68
                elif letter == "E":
                    number = 69
                elif letter == "F":
                    number = 70
                elif letter == "G":
                    number = 71
                elif letter == "H":
                    number = 72
                elif letter == "I":
                    number = 73
                elif letter == "J":
                    number = 74
                elif letter == "K":
                    number = 75
                elif letter == "L":
                    number = 76
                elif letter == "M":
                    number = 77
                elif letter == "N":
                    number = 78
                elif letter == "O":
                    number = 79
                elif letter == "P":
                    number = 80
                elif letter == "Q":
                    number = 81
                elif letter == "R":
                    number = 82
                elif letter == "S":
                    number = 83
                elif letter == "T":
                    number = 84
                elif letter == "U":
                    number = 85
                elif letter == "V":
                    number = 86
                elif letter == "W":
                    number = 87
                elif letter == "X":
                    number = 88
                elif letter == "Y":
                    number = 89
                elif letter == "Z":
                    number = 90
                elif letter == "[":
                    number = 91
                elif letter == "\\":
                    number = 92
                elif letter == "]":
                    number = 93
                elif letter == "^":
                    number = 94
                elif letter == "_":
                    number = 95
                elif letter == "`":
                    number = 96
                elif letter == "a":
                    number = 97
                elif letter == "b":
                    number = 98
                elif letter == "c":
                    number = 99
                elif letter == "d":
                    number = 100
                elif letter == "e":
                    number = 101
                elif letter == "f":
                    number = 102
                elif letter == "g":
                    number = 103
                elif letter == "h":
                    number = 104
                elif letter == "i":
                    number = 105
                elif letter == "j":
                    number = 106
                elif letter == "k":
                    number = 107
                elif letter == "l":
                    number = 108
                elif letter == "m":
                    number = 109
                elif letter == "n":
                    number = 110
                elif letter == "o":
                    number = 111
                elif letter == "p":
                    number = 112
                elif letter == "q":
                    number = 113
                elif letter == "r":
                    number = 114
                elif letter == "s":
                    number = 115
                elif letter == "t":
                    number = 116
                elif letter == "u":
                    number = 117
                elif letter == "v":
                    number = 118
                elif letter == "w":
                    number = 119
                elif letter == "x":
                    number = 120
                elif letter == "y":
                    number = 121
                elif letter == "z":
                    number = 122
                elif letter == "{":
                    number = 123
                elif letter == "|":
                    number = 124
                elif letter == "}":
                    number = 125
                elif letter == "~":
                    number = 126
                elif letter == "DEL":
                    number = 127
                if format == "1":
                    print("")
                calculate (number, length)
                choice = "retry"
    if choice != "retry":
        print ("\nError:",choice,"is not an option, please try again")
        time.sleep (1)
        details ()
        choice = "retry"
    else:
        print ("\n")
        time.sleep(2)
        retry = str (input("Type retry to calculate more: "))
        if retry == "retry":
            details ()
        while retry != "retry":
            print("Error:", retry, "is an invalid statement, please try again")
            retry = str (input("Type retry to calculate more: "))
            if retry == "retry":
                details ()

print ("\nBinary Calculator by Fraser Love")
time.sleep (1)
details ()
