"""
Created 05/07/19
Developed by Fraser Love

Notes:
This program is an base64 to ASCII decoder. I implemented the program to use as little pre defined functions as possible to simulate
how a lower level encoder would work and to help me understand the algorithm behind this program. ASCII functions like ord() and chr()
are used as this makes the program code more easier to understand as it excludes extra code behind the ASCII to text functions. A ASCII
to base64 encoder is avaliable on my Github aswell.
"""

def get_input():
    base64 = list(str(input("Enter Base64: ")))
    return base64

def strip_base64(base64):
    base64 = [char for char in base64 if char != "="]
    return base64

def char_search(search_char):
    for i in range(0, len(b64_char_set)):
        if b64_char_set[i] == search_char:
            return i

def base64_to_den(base64):
    denary = []
    for char in base64:
        denary.append(char_search(char))
    return denary

def den_to_bin(denary):
    binary = []
    count = 0
    for num in denary:
        binary.append([])
        for i in range(5,-1,-1):
            if num >= 2**i:
                num -= 2**i
                binary[count].append("1")
            else:
                binary[count].append("0")
        binary[count] = "".join(binary[count])
        count += 1
    binary = "".join(binary)
    return binary

def forming_bytes(binary):
    bytes = []
    count = 0
    for i in range (0, len(binary), 8):
        bytes.append(binary[i:i+8])
        if i+8 > len(binary):
            while len(bytes[count]) < 8:
                bytes[count] = list(bytes[count])
                bytes[count].append("0")
                bytes[count] = "".join(bytes[count])
        count += 1
    return bytes

def bytes_to_ascii(bytes):
    ascii = []
    for byte in bytes:
        exp = 7
        value = 0
        for bit in byte:
            value += int(bit)*2**exp
            exp -= 1
        if value != 0:
            ascii.append("".join(chr(value)))
    return ascii

def display_output(ascii):
    print("".join(ascii))

b64_char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
display_output(bytes_to_ascii(forming_bytes(den_to_bin(base64_to_den(strip_base64(get_input()))))))
