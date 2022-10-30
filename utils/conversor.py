import binascii

from constants.constants import *
from utils.ctxt import *

# Convert from text to hexadecimal
def t2h(txt:str) -> str:
    return txt.encode('utf-8').hex()

# Convert from bytes to hexadecimal
def b2h(txt:bytes) -> str:
    return str(binascii.hexlify(txt), 'utf-8')


# Convert hexadecimal to bytes (utf-8)
def h2b(hex:str)-> bytes:
    return bytes.fromhex(hex).decode('utf-8')


# Convert a number to an array of numbers
def numberToArr(n, base) -> list:
    if n == 0: return [0]
    digits = []
    while n:
        digits.append(n % base)
        n //= base
    return digits[::-1]


# Convert from base 10 to base 4
def quat(n) -> int:
    b = bin(n)[2:]

    if len(b) % 2 != 0:
        b = "0" + b

    quaternary_n = ""
    for i in range(0, len(b), 2):
        quaternary_n += str(int(b[i:i+2], 2))

    return quaternary_n

# Convert from int to base 2,4,8 or 16
def conv(x, base):
    if base == 2:
        return bin(x)[2:]
    elif base == 4:
        return quat(x)
    elif base == 8:
        return oct(x)[2:]
    elif base == 16:
        return hex(x)[2:]
    else:
        raise Exception("Invalid base")