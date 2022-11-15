import math

import numpy as np

from constants.constants import *
from utils.ctxt import *

# Get the length a number will have in a given base, given the number of digits of that number in base 2
def binLen2BaseLen(bin_len:int, base:int) -> int:
    base_exp = int(math.log(base, 2))
    return bin_len // base_exp + (bin_len % base_exp != 0)

# Convert from base 2 to array of base X
def bin2Arr(n:str, base:int) -> list:
    base_exp = int(math.log(base, 2))
    # fill n with 0s to the left
    n = n.zfill(len(n) + (base_exp - len(n) % base_exp) % base_exp)
    # convert n to array of base
    n = [int(n[i:i+base_exp], 2) for i in range(0, len(n), base_exp)]
    return np.array(n)

# Convert from an array of base 64 to an integer
def arr2int(arr:np.ndarray, base:int) -> int:
    base_exp = int(math.log(base, 2))
    arr = [conv(x, 2).zfill(base_exp) for x in arr]
    arr = "".join(arr)
    return int(arr, 2)

# Convert from base 10 to base 4
def quat(n:int) -> int:
    b = bin(n)[2:]

    if len(b) % 2 != 0:
        b = "0" + b

    quaternary_n = ""
    for i in range(0, len(b), 2):
        quaternary_n += str(int(b[i:i+2], 2))

    return quaternary_n

# Convert from int to base 2,4,8 or 16
def conv(x:int, base:int) -> str:
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