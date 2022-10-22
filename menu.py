import time
from PIL import Image
import binascii
from pathlib import Path
import numpy as np

from classes.Options import Options
from utils.input import get_path, get_bool
from utils.ctxt import *
from utils.cryptography import get_fernet, decrypt_content
from utils.conversor import t2h
from constants.constants import *
from noise_storer import store_file, retrieve_file
from config import MOD_PREFIX, MOD_SUFIX, TEST_MODE

def menu() -> None:
    option = Options(["EXIT", "Store file", "Retrieve file"]).get_choice()
    
    if option == 0: 
        exit()

    elif option == 1: 
        store_file_func()

    elif option == 2:
        retrieve_file_func()



def store_file_func() -> None:
    # Get the inputs
    if TEST_MODE:
        file_path = f"{INPUT_FILES_PATH}/images.zip"
        img_path = f"{BASE_IMAGES_PATH}/0'7MP.png"
    else:
        file_path = get_path(INPUT_FILES_PATH, "File to be stored: ")
        img_path = get_path(BASE_IMAGES_PATH, "Filename of the image to use as a base: ", IMAGE_EXTS)

    do_encryption = get_bool("Encrypt the file?")

    file_filename = Path(file_path).name
    img_stem = Path(img_path).stem
    out_img_path = f"{MOD_IMAGES_PATH}/{MOD_PREFIX}{img_stem}{MOD_SUFIX}.png"

    # Read the file
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Read the image and store it in a an array
    img_arr = np.array(Image.open(img_path))

    # Encrypt the file
    if do_encryption:
        fernet = get_fernet()
        content = fernet.encrypt(content)
        file_filename = fernet.encrypt(file_filename.encode()).decode()

    hex_input = str(binascii.hexlify(content), 'utf-8')
    hex_filename = t2h(file_filename)

    t1 = time.time()
    #--------------------------------------
    try:
        new_img_arr = store_file(hex_filename, hex_input, img_arr)
        Image.fromarray(new_img_arr).save(out_img_path)
        print(ctxt(f"\nModified image saved in {ctxt(out_img_path, Fore.YELLOW)}", Fore.GREEN))
    except Exception as e:
        print(f"\n{ctxt('Error: ', Fore.RED)}{e}")
        return
    #--------------------------------------
    print(f"\nDone in {ctxt(time.time() - t1, Fore.GREEN)} seconds")



def retrieve_file_func() -> None:
    if TEST_MODE:
        base_img_path = f"{BASE_IMAGES_PATH}/0'7MP.png"
        mod_img_path = f"{MOD_IMAGES_PATH}/0'7MP_mod.png"
    else:
        base_img_path = get_path(BASE_IMAGES_PATH, "Filename of the base image: ", IMAGE_EXTS)
        mod_img_path = get_path(MOD_IMAGES_PATH, "Filename of the modified image: ", IMAGE_EXTS)

    t1 = time.time()
    #---------------------------
    # Get the base image array and the modified image array and flatten it
    base_img_arr = np.array(Image.open(base_img_path)).flatten().astype(np.int8)
    mod_img_arr = np.array(Image.open(mod_img_path)).flatten().astype(np.int8)

    output = retrieve_file(base_img_arr, mod_img_arr)
    file_content = output["file_content"]
    filename = output['filename']

    # Decryption
    if file_content.startswith(b"gAAAAA"):
        try:
            output_decrypted = decrypt_content(file_content, filename)
            file_content = output_decrypted["file_content"]
            filename = output_decrypted["filename"]
        except Exception as e:
            print(f"\n{ctxt('Error: ', Fore.RED)}{e}")
            return

    out_path = f"{OUTPUT_FILES_PATH}/{filename}"

    with open(out_path, 'wb') as f:
        f.write(file_content)
        print(ctxt(f"\nOutput file saved in {ctxt(out_path, Fore.YELLOW)}", Fore.GREEN))
    #---------------------------
    print(f"\nDone in {ctxt(time.time() - t1, Fore.GREEN)} seconds")