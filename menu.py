from pathlib import Path
import time

import numpy as np
from PIL import Image

from config import *
from constants.constants import *
from classes.Options import Options
from utils.conversor import b2h, t2h
from utils.cryptography import get_fernet, decrypt_content
from utils.ctxt import *
from utils.injection import inject_file, extract_file
from utils.input import get_path, get_bool

def menu() -> None:
    option = Options(["EXIT", "Inject file", "Extract file"]).get_choice()

    if option == 0: 
        exit()

    elif option == 1: 
        inject_file_func()

    elif option == 2:
        extract_file_func()



def inject_file_func() -> None:
    # Get the inputs
    if TEST_MODE:
        file_path = f"{INPUT_FILES_PATH}/images.zip"
        img_path = f"{BASE_IMAGES_PATH}/0'7MP.png"
    else:
        file_path = get_path(INPUT_FILES_PATH, "File to be stored: ")
        img_path = get_path(BASE_IMAGES_PATH, "Filename of the base image: ", IMAGE_EXTS)

    do_encryption = get_bool("Encrypt the file?")

    # Get filename, extension and output path
    filename = Path(file_path).name
    img_stem = Path(img_path).stem
    out_img_path = f"{MOD_IMAGES_PATH}/{MOD_PREFIX}{img_stem}{MOD_SUFIX}.png"

    # Read the file
    with open(file_path, 'rb') as f: 
        file = f.read()
    
    # Read the image and store it in a an array
    img_arr = np.array(Image.open(img_path))

    # Encrypt the file
    if do_encryption:
        fernet = get_fernet()
        file = fernet.encrypt(file)
        filename = fernet.encrypt(filename.encode()).decode()

    hex_file = b2h(file)
    hex_filename = t2h(filename)

    t1 = time.time()
    #--------------------------------------
    try:
        new_img_arr = inject_file(img_arr, hex_file, hex_filename, STORE_RANDOM)
        Image.fromarray(new_img_arr).save(out_img_path)
        print(ctxt(f"\nModified image saved in {ctxt(out_img_path, Fore.YELLOW)}", Fore.GREEN))
    except Exception as e:
        print(f"\n{ctxt('Error: ', Fore.RED)}{e}")
        return
    #--------------------------------------
    print(f"\nDone in {ctxt(round(time.time() - t1, 4), Fore.GREEN)} seconds")



def extract_file_func() -> None:
    if TEST_MODE:
        mod_img_path = f"{MOD_IMAGES_PATH}/0'7MP_mod.png"
    else:
        mod_img_path = get_path(MOD_IMAGES_PATH, "Filename of the modified image: ", IMAGE_EXTS)

    t1 = time.time()
    #---------------------------
    # Get the modified image array and flatten it
    mod_img_arr_flat = np.array(Image.open(mod_img_path)).flatten().astype(np.int8)

    output = extract_file(mod_img_arr_flat)

    file = output["file"]
    filename = output['filename']

    # Decryption
    if file.startswith(b"gAAAAA") and filename.startswith(b"gAAAAA"):
        try:
            output_decrypted = decrypt_content(file, filename)
            file = output_decrypted["file"]
            filename = output_decrypted["filename"]
        except Exception as e:
            print(f"\n{ctxt('Error: ', Fore.RED)}{e}")
            return

    filename = filename.decode("utf-8")
    out_path = f"{OUTPUT_FILES_PATH}/{filename}"

    with open(out_path, 'wb') as f:
        f.write(file)
        print(ctxt(f"\nOutput file saved in {ctxt(out_path, Fore.YELLOW)}", Fore.GREEN))
    #---------------------------
    print(f"\nDone in {ctxt(round(time.time() - t1, 4), Fore.GREEN)} seconds")