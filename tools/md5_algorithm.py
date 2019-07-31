"""
MD5 Hashing Algorithm Implementation in Python

Created 18/07/19
Developed by Fraser Love

This implementation of the MD5 algorithm is modeled from the RFC design avaliable at https://www.ietf.org/rfc/rfc1321.txt. I also used another
python implementation of the algorithm at https://rosettacode.org/wiki/MD5/Implementation#Python to help with implementation.
This implementation only works for integral numbers of bytes as it uses the bytearray object to simplify the code.
"""
import math

rotations = 4*[7, 12, 17, 22] + \
            4*[5, 9, 14, 20] + \
            4*[4, 11, 16, 23] + \
            4*[6, 10, 15, 21]

consts = [int(abs(math.sin(i+1)) * 2**32) for i in range(64)]

init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

functions = 16*[lambda b, c, d: (b & c) | (~b & d)] + \
            16*[lambda b, c, d: (d & b) | (~d & c)] + \
            16*[lambda b, c, d: b ^ c ^ d] + \
            16*[lambda b, c, d: c ^ (b | ~d)]

i_functions = 16*[lambda i: i] + \
              16*[lambda i: (5*i + 1)%16] + \
              16*[lambda i: (3*i + 5)%16] + \
              16*[lambda i: (7*i)%16]

def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF

def md5(message):
    message = bytearray(message)
    msg_length = (8 * len(message))
    message.append(0x80)
    while (len(message)*8) % 512 != 448:
        message.append(0)
    message += msg_length.to_bytes(8, byteorder='little')

    hash_pieces = init_values[:]

    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:chunk_ofst+64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = i_functions[i](i)
            to_rotate = a + f + consts[i] + int.from_bytes(chunk[4*g:4*g+4], byteorder="little")
            new_b = (b + left_rotate(to_rotate, rotations[i]))
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF
    return sum(x<<(32*i) for i, x in enumerate(hash_pieces))

def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

def user_input():
    string = str(input("Enter a string to hash: "))
    bytes_input = string.encode()
    print("Hex: {}".format(md5_to_hex(md5(bytes_input))))

user_input()
