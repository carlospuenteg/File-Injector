import math

import numpy as np

from constants.constants import *
from utils.bit_storing import store_bits, retrieve_bits
from utils.conversor import conv, bin2Arr, arr2int
from utils.ctxt import *

# Inyect a file and a filename into an array
def inject_file(arr:np.ndarray, file:bytes, filename:bytes, store_random:bool) -> np.ndarray:
    #-------------------------------------------------------
    print(ctxt("\nPreparing...\n", Fore.MAGENTA))
    #-------------------------------------------------------
    # Convert file and filename to binary
    file_bin = conv(int(file.hex(), 16), 2)
    filename_bin = conv(int(filename.hex(), 16), 2)
    #-------------------------------------------------------
    # Flatten the array
    arr_flat = arr.flatten()
    #-------------------------------------------------------
    # Get the maximum number of bits that can be modified in each channel and its base and mask
    channel_bits = np.iinfo(arr.dtype).bits
    max_mod_bits_base = 2**channel_bits
    max_mod_bits_mask = max_mod_bits_base
    #-------------------------------------------------------
    # Maximum size the file can have
    max_file_size = arr.size - MAX_FN_SIZE_BIN - 1

    # Length of max_file_size in base 2
    max_file_size_len = len(conv(max_file_size, 2))

    # Available pixels that can be used to store the file
    available_channels = max_file_size - max_file_size_len
    #-------------------------------------------------------
    # Times the file_len_b2 is bigger than the available channels (rounded up)
    file_len_b2 = len(file_bin)
    times = math.ceil(file_len_b2 / available_channels)

    # If times > channel_bits
    if times > channel_bits:
        raise Exception(f"Base file is too small to store the file")

    # times must be between 1 and max_mod_bits (maximum modification of bits you can do to a channel)
    times = times if times <= channel_bits else channel_bits

    mod_bits = times                    # The number of bits that will be modified
    base = 2**mod_bits                  # Base that will be used to store the information
    mask = max_mod_bits_base - base     # Mask that will be used to store the information
    #-------------------------------------------------------
    # Convert the filename to base 2 and fill it left with 0s
    filename_conv = bin2Arr(filename_bin.zfill(MAX_FN_SIZE_BIN), 2)

    # Convert the file to base {base}
    file_conv = bin2Arr(file_bin, base)

    # Get the file size and convert it to base 2
    file_size = len(file_conv)
    file_size_conv = bin2Arr(conv(file_size, 2).zfill(max_file_size_len),2)
    #-------------------------------------------------------
    print(f"Modified bits per channel: {ctxt(mod_bits, Fore.YELLOW)}")
    print(f"Base file modification: {ctxt(f'{round(base/(2**channel_bits)*100, 2)}%', Fore.YELLOW)}")
    #-------------------------------------------------------
    # (1) Store mod_bits at idx 0
    arr_flat[0] = store_bits(arr_flat[0], mod_bits, max_mod_bits_mask)

    # Generate random values
    print(ctxt("\nGenerating random values...", Fore.MAGENTA))
    end_idx = 1 + len(file_size_conv) + len(filename_conv) + len(file_conv)
    if store_random: 
        rands = np.random.randint(low = 0, high=base, size=arr_flat.size - end_idx)
    else:
        rands = np.zeros(arr_flat.size - end_idx, dtype=arr.dtype)

    # Use zip to inject information in channels
    print(ctxt("\nInjecting information...", Fore.MAGENTA))
    arr_flat[1:] = [
        store_bits(channel, val, mask) for channel, val in zip(
            arr_flat[1:],
            np.concatenate((file_size_conv, filename_conv, file_conv, rands)),
        )
    ]
    #-------------------------------------------------------
    # Return flat_img to original shape if needed
    if arr.shape != arr_flat.shape:
        print(ctxt("\nReshaping...", Fore.MAGENTA))
        return arr_flat.reshape(arr.shape)

    else: # If the array was already flat
        return arr_flat



# Extract the file from the array
def extract_file(mod_arr:np.ndarray) -> dict[bytes, bytes]:
    #-------------------------------------------------------
    print(ctxt("\nPreparing...", Fore.MAGENTA))
    #-------------------------------------------------------
    # Get the maximum number of bits that can be modified in each channel and its base
    channel_bits = np.iinfo(mod_arr.dtype).bits
    max_mod_bits_base = 2**channel_bits
    #-------------------------------------------------------
    # Flatten the array
    mod_arr_flat = mod_arr.flatten()
    #-------------------------------------------------------
    # Maximum size the file can have
    max_file_size = len(mod_arr_flat) - MAX_FN_SIZE_BIN - 1
    # Length of the maximum size in binary
    max_file_size_len = len(conv(max_file_size, 2))
    #-------------------------------------------------------
    # Modified bits per channel and Base
    mod_bits = retrieve_bits(mod_arr_flat[0], max_mod_bits_base)
    base = 2**mod_bits
    idx = 1
    #-------------------------------------------------------
    # Get the file size
    file_size_arr = [retrieve_bits(x, 2) for x in mod_arr_flat[idx:idx+max_file_size_len]]
    file_size = arr2int(file_size_arr, 2)
    idx += max_file_size_len

    # Get the filename
    print(ctxt("\nRetrieving filename...", Fore.MAGENTA))
    filename_arr = [retrieve_bits(x, 2) for x in mod_arr_flat[idx:idx+MAX_FN_SIZE_BIN]]
    filename_hex = conv(arr2int(filename_arr, 2), 16)
    idx += MAX_FN_SIZE_BIN

    # Get the file
    print(ctxt("\nRetrieving input file...", Fore.MAGENTA))
    file_arr = [retrieve_bits(x, base) for x in mod_arr_flat[idx:idx+file_size]]
    file_hex = conv(arr2int(file_arr, base), 16)
    #-------------------------------------------------------
    # Return the filename and the input file in bytes
    return {
        "filename": bytes.fromhex(filename_hex),
        "file": bytes.fromhex(file_hex)
    }