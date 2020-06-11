"""
Created 05/07/19
Developed by Fraser Love

Notes:
This program is an ASCII to base64 encoder. I implemented the program to use as little pre defined functions as possible to simulate
how a lower level encoder would work and to help me understand the algorithm behind this program. ASCII functions like ord() and chr()
are used as this makes the program code more easier to understand as it excludes extra code behind the ASCII to text functions. A base64
to ASCII decoder is avaliable on my Github aswell.
"""

def get_input():
    text = str(input("Enter ASCII text: "))
    return text

def ascii_to_bin(text):
    binary = []
    for chr in text:
        binary.append('{:08b}'.format(ord(chr)))
    return binary

def forming_sixes(binary):
    count = 0
    sixes = [[]]
    for byte in binary:
        for bit in byte:
            bit = int(bit)
            if len(sixes[count]) == 6:
                count += 1
                sixes.append([])
            if len(sixes[count]) < 6:
                sixes[count].append(bit)
    return sixes, count

def padding_bin(sixes, count):
    while len(sixes[count]) < 6:
        sixes[count].append(0)
    return sixes

def bin_to_den(sixes):
    denary = []
    for byte in sixes:
        value = byte[0]*2**5 + byte[1]*2**4 + byte[2]*2**3 + byte[3]*2**2 + byte[4]*2**1 + byte[5]*2**0
        denary.append(value)
    return denary

def den_to_base64(denary):
    base64 = []
    for integer in denary:
        base64.append(b64_char_set[integer])
    return base64

def padding_base64(base64):
    while len(base64) % 4 != 0:
        base64.append("=")
    return base64

def display_output(base64):
    print("".join(base64))

b64_char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
sixes, count = forming_sixes(ascii_to_bin(get_input()))
display_output(padding_base64(den_to_base64(bin_to_den(padding_bin(sixes, count)))))
