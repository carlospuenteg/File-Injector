import os
import re
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

from constants.constants import ENCRYPTION_KEYS_PATH
from classes.Options import Options
from utils.ctxt import *
from utils.input import get_path, get_valid_filename


# Generate a key with Fernet.generate_key(), save it to a file and return the path
def gen_key(new_filename:str=None) -> str:
    key = Fernet.generate_key()

    if new_filename:
        stem = Path(new_filename).stem
        path = f"{ENCRYPTION_KEYS_PATH}/{stem}.key"

    else:
        idxs = [0]
        for file in os.listdir(ENCRYPTION_KEYS_PATH):
            if re.match(r"key\d+\.key", file):
                idxs.append(int(file[3:-4]))
        new_idx = max(idxs) + 1
        path = f"{ENCRYPTION_KEYS_PATH}/key{new_idx}.key"

    with open(path, 'wb') as f:
        f.write(key)
    
    print(f"Key generated and saved to {ctxt(path, Fore.GREEN)}")
    return path



# Load the key from the path
def load_key(path:str) -> bytes:
    stem = Path(path).stem

    with open(path, 'rb') as f:
        key = f.read()

    return key



# Choose or generate a key from a menu, validate it and return the Fernet object
def get_fernet() -> Fernet:
    print("\nDo you want to use an existing key or generate a new one?")
    option = Options(["Existing key", "New key"]).get_choice()
    
    if option == 0:
        key_path = get_path([ENCRYPTION_KEYS_PATH], "Filename of the key file: ", [".key"])

    if option == 1:
        key_filename = get_valid_filename("Filename of the new key file (blank for default): ", [".key"], allow_blank=True)
        key_path = gen_key(key_filename)

    return Fernet(load_key(key_path))



# Choose the path of the key file and return the Fernet object
def choose_fernet() -> Fernet:
    key_path = get_path([ENCRYPTION_KEYS_PATH], "\nFilename of the key file: ", [".key"])

    return Fernet(load_key(key_path))



# Return a list of all the paths of the key files
def get_key_paths() -> list:
    keys_paths = []
    for file in os.listdir(ENCRYPTION_KEYS_PATH):
        if file.endswith(".key"):
            keys_paths.append(f"{ENCRYPTION_KEYS_PATH}/{file}")
    return keys_paths



# Decrypt the content of the file and filename trying with all the key files
def decrypt_content(file:bytes, filename:bytes)  -> dict:
    for key_path in get_key_paths():
        fernet = Fernet(load_key(key_path))
        try:
            file = fernet.decrypt(file)
            filename = fernet.decrypt(filename)
            print(ctxt(f'Decrypted with "{key_path}"', Fore.GREEN))
            return {
                "file": file,
                "filename": filename
            }
        except InvalidToken:
            continue

    # If the file couldn't be decrypted with any key, raise an Exception
    raise Exception(f'Decryption key for the file not found in "{ENCRYPTION_KEYS_PATH}"')