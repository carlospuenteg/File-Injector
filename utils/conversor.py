from constants.constants import *
from utils.ctxt import *

# Convert from text to hexadecimal
def t2h(txt:str) -> str:
    return txt.encode('utf-8').hex()


# Convert hexadecimal to utf-8
def h2t(hex:str)-> str:
    return bytes.fromhex(hex).decode('utf-8')


# Convert a number to an array of numbers
def numberToArr(n, base) -> list:
    if n == 0: return [0]
    digits = []
    while n:
        digits.append(n % base)
        n //= base
    return digits[::-1]


def quat(n) -> int:
    b = bin(n)[2:]

    if len(b) % 2 != 0:
        b = "0" + b

    quaternary_n = ""
    for i in range(0, len(b), 2):
        quaternary_n += str(int(b[i:i+2], 2))

    return quaternary_n