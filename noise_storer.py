import numpy as np

from utils.conversor import quat
from utils.progress_bar import progress_bar
from utils.ctxt import ctxt, Fore
from constants.constants import MAX_BIN_FN_SIZE
from config import STORE_RANDOM



def store_bits(channel_val, to_store):
    if to_store == 0:
        return channel_val
    sum = channel_val + to_store
    sign = -1 if sum > 255 else 1
    channel_val += (to_store * sign)
    return channel_val


def store_file(hex_filename, hex_input, img_arr, store_random=STORE_RANDOM) -> np.ndarray:
    print(ctxt("\nPreparing...\n", Fore.MAGENTA))

    # Get image array and flatten it
    img_arr_flat = img_arr.flatten()

    # Get the number of available pixels and the relation between avail_pix and hex_input
    avail_pix = len(img_arr_flat) - 1 - MAX_BIN_FN_SIZE
    div = avail_pix // len(hex_input)

    # Depending on the relation between avail_pix and hex_input, choose the base
    if div >= 4:
        base = 2
        hex_input2hide = bin(int(hex_input, 16))[2:]
        hex_filename = bin(int(hex_filename, 16))[2:]
    elif div >= 3:
        base = 4
        hex_input2hide = quat(int(hex_input,16))
        hex_filename = quat(int(hex_filename, 16))
    elif div >= 2:
        base = 8
        hex_input2hide = oct(int(hex_input, 16))[2:]
        hex_filename = oct(int(hex_filename, 16))[2:]
    elif div >= 1:
        base = 16
        hex_input2hide = hex(int(hex_input, 16))[2:]
        hex_filename = hex(int(hex_filename, 16))[2:]
    else:
        raise Exception("Image is too small to store the file")
    
    print(f"Added/Subtracted bpp (bits per pixel): {3*base}")

    # Store the base-1 on the first pixel
    idx = 0
    img_arr_flat[idx] = store_bits(img_arr_flat[idx], base-1)
    idx += 1

    # Store the filename
    for i,h in enumerate(hex_filename):
        img_arr_flat[idx+i] = store_bits(img_arr_flat[idx+i], int(h, base))

    # Put a divider between the filename and the input file
    idx = len(hex_filename) + 1
    img_arr_flat[idx] = store_bits(img_arr_flat[idx], base)
    idx += 1

    # Store the input file
    for i in range(len(hex_input2hide)):
        if i % 10000 == 0 or i == len(hex_input2hide)-1:
            progress_bar(i/(len(hex_input2hide)-1), ctxt("Storing...", Fore.GREEN))
        img_arr_flat[idx+i] = store_bits(img_arr_flat[idx+i], int(hex_input2hide[i], base))
    
    # Put a divider at the end of the input file
    idx += len(hex_input2hide)
    img_arr_flat[idx] = store_bits(img_arr_flat[idx], base)
    idx += 1

    # Store random values on the rest of the pixels
    if store_random:
        print(ctxt("\nGenerating random values...", Fore.MAGENTA))
        rands = list(np.random.randint(low = 0, high=base, size=len(img_arr_flat[idx:])))
        print(ctxt("\nStoring random values...", Fore.MAGENTA))
        img_arr_flat[idx:] = np.array(
            [x + rands[i]*(-1 if x + rands[i] > 255 else 1) 
            for i,x in enumerate(img_arr_flat[idx:].tolist())])

    # Return flat_img to original shape
    print(ctxt("\nReshaping...", Fore.MAGENTA))
    new_img_arr = img_arr_flat.reshape(img_arr.shape)

    return new_img_arr



def retrieve_file(base_img_arr, mod_img_arr) -> dict:
    print(ctxt("\nPreparing...", Fore.MAGENTA))

    # Get the difference between the two images
    diff = np.absolute(np.subtract(mod_img_arr, base_img_arr))

    # Get the base
    base = diff[0]+1
    idx = 1

    # Find the dividers between the filename and the input file and between the input file and the end
    dividers = np.where(diff == base)[0]

    # Get the filename
    print(ctxt("\nRetrieving filename...", Fore.MAGENTA))
    fn_str = ''.join([f'{n:x}' for n in diff[idx:dividers[0]]])
    idx = dividers[0] + 1

    # Get the input file
    print(ctxt("\nRetrieving input file...", Fore.MAGENTA))
    fn_file = ''.join([f'{n:x}' for n in diff[idx:dividers[1]]])
    idx = dividers[1] + 1

    print(ctxt("\nConverting filename to hex...", Fore.MAGENTA))
    fn_hex = f"{int(fn_str, base):x}"

    print(ctxt("\nConverting input file to hex...", Fore.MAGENTA))
    file_hex = f"{int(fn_file, base):x}"
    
    # Return the filename and the input file
    return {
        "filename": bytes.fromhex(fn_hex).decode("utf-8"),
        "file_content": bytes.fromhex(file_hex)
    }