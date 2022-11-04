import numpy as np

from constants.constants import *
from utils.bit_storing import store_bits, retrieve_bits
from utils.conversor import conv
from utils.ctxt import *
from utils.progress_bar import progress_bar

def inject_file(img_arr:np.ndarray, file:str, filename:str, store_random:bool) -> np.ndarray:
    print(ctxt("\nPreparing...\n", Fore.MAGENTA))

    img_arr_flat = img_arr.flatten()
    
    #-------------------------------------------------------
    # Get the maximum size the file can have
    max_file_size = len(img_arr_flat) - MAX_FN_SIZE_BIN - 1
    # Get the length of the maximum size in binary
    max_file_size_len = len(conv(max_file_size, 2))
    # Get the available pixels for storing the file
    available_channels = max_file_size - max_file_size_len
    #-------------------------------------------------------
    # Get the base to use and the mask
    times = available_channels // len(file)
    if times < 1: 
        needed_img_size = (len(file) + MAX_FN_SIZE_BIN + 1 + 50)/3 # 50 is a really big image size ((2^50)/3 pixels)
        raise Exception(f"Image is too small to store the file. Needed size: {ctxt(f'{round(needed_img_size/1000000,4)} MP', Fore.YELLOW)}")
    times = times if times <= 4 else 4
    base_exp = 5-times
    base = 2**base_exp
    mask = 256 - base
    #-------------------------------------------------------
    # Convert the filename to base 2 and fill it left with 0s
    filename_conv = conv(int(filename,16), 2).zfill(MAX_FN_SIZE_BIN)

    # Convert the file to base {base}
    file_conv = conv(int(file,16), base)

    # Get the file size and convert it to base 2
    file_size = len(file_conv)
    file_size_conv = conv(file_size, 2).zfill(max_file_size_len) # image resolution in pixels
    #-------------------------------------------------------
    print(f"Modified bits per channel: {ctxt(base_exp, Fore.YELLOW)}")
    print(f"Image modification: {ctxt(f'{round(base/256*100, 2)}%', Fore.YELLOW)}\n")
    #-------------------------------------------------------
    # (1) Store the (base exponent) in idx 0 (e.g. 3 = 2^3 = 8)
    img_arr_flat[0] = store_bits(img_arr_flat[0], base_exp, MAX_BASE_EXP_MASK)
    idx = 1
    # Store the file size in the next {max_file_size_len} pixels
    for i,h in enumerate(file_size_conv):
        img_arr_flat[idx+i] = store_bits(img_arr_flat[idx+i], int(h, 2), 256 - 2)
    idx += len(file_size_conv)
    #-------------------------------------------------------
    # Store the filename
    for i,h in enumerate(filename_conv):
        img_arr_flat[idx+i] = store_bits(img_arr_flat[idx+i], int(h, 2), 256 - 2)
    idx += len(filename_conv)

    # Store the input file
    for i in range(len(file_conv)):
        if i % 10000 == 0 or i == len(file_conv)-1:
            progress_bar(i/(len(file_conv)-1), ctxt("Storing...", Fore.GREEN))
        img_arr_flat[idx+i] = store_bits(img_arr_flat[idx+i], int(file_conv[i], base), mask)
    idx += len(file_conv)
    #-------------------------------------------------------
    # Store random values on the rest of the pixels
    if store_random:
        print(ctxt("\nGenerating random values...", Fore.MAGENTA))
        rands = list(np.random.randint(low = 0, high=base, size=len(img_arr_flat[idx:])))
        print(ctxt("\nStoring random values...", Fore.MAGENTA))
        img_arr_flat[idx:] = np.array([store_bits(x, rands[i], mask) for i,x in enumerate(img_arr_flat[idx:].tolist())])
    #-------------------------------------------------------
    # Return flat_img to original shape
    print(ctxt("\nReshaping...", Fore.MAGENTA))
    img_arr = img_arr_flat.reshape(img_arr.shape)
    
    return img_arr



def extract_file(mod_img_arr_flat:np.ndarray) -> str:
    print(ctxt("\nPreparing...", Fore.MAGENTA))

    # Get the maximum size the file can have
    max_file_size = len(mod_img_arr_flat) - MAX_FN_SIZE_BIN - 1
    # Get the length of the maximum size in binary
    max_file_size_len = len(conv(max_file_size, 2))

    # Get the base
    base_exp = retrieve_bits(mod_img_arr_flat[0], MAX_BASE_EXP_BASE)
    base = 2**base_exp
    idx = 1

    # Get the file size
    file_size_str = "".join([f'{retrieve_bits(x, 2):b}' for x in mod_img_arr_flat[idx:idx+max_file_size_len]])
    file_size = int(file_size_str, 2)
    idx += max_file_size_len

    # Get the filename
    print(ctxt("\nRetrieving filename...", Fore.MAGENTA))
    filename_str = "".join([f'{retrieve_bits(x, 2):b}' for x in mod_img_arr_flat[idx:idx+MAX_FN_SIZE_BIN]])
    filename_hex = f"{int(filename_str, 2):x}"
    idx += MAX_FN_SIZE_BIN

    # Get the file
    print(ctxt("\nRetrieving input file...", Fore.MAGENTA))
    file_str = "".join([f'{retrieve_bits(x, base):x}' for x in mod_img_arr_flat[idx:idx+file_size]])
    file_hex = f"{int(file_str, base):x}"

    # Return the filename and the input file
    return {
        "filename": bytes.fromhex(filename_hex),
        "file": bytes.fromhex(file_hex)
    }