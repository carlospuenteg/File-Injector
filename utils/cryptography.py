import os
from pathlib import Path
import re
from cryptography.fernet import Fernet, InvalidToken

from utils.ctxt import *
from utils.input import get_path, get_valid_filename
from constants.constants import ENCRYPTION_KEYS_PATH
from classes.Options import Options

def gen_key(new_filename=None) -> str:
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



def load_key(path) -> bytes:
    stem = Path(path).stem

    with open(path, 'rb') as f:
        key = f.read()

    return key




def get_fernet() -> Fernet:
    print("\nDo you want to use an existing key or generate a new one?")
    option = Options(["Existing key", "New key"]).get_choice()
    
    if option == 0:
        # Filename of the key file (the input can be empty)
        key_path = get_path(ENCRYPTION_KEYS_PATH, "Filename of the key file: ", [".key"])

    if option == 1:
        key_filename = get_valid_filename("Filename of the new key file (blank for default): ", [".key"], allow_blank=True)
        key_path = gen_key(key_filename)

    return Fernet(load_key(key_path))




def choose_fernet() -> Fernet:
    key_path = get_path(ENCRYPTION_KEYS_PATH, "\nFilename of the key file: ", [".key"])

    return Fernet(load_key(key_path))




def get_key_paths() -> list:
    keys_paths = []
    for file in os.listdir(ENCRYPTION_KEYS_PATH):
        if file.endswith(".key"):
            keys_paths.append(f"{ENCRYPTION_KEYS_PATH}/{file}")
    return keys_paths




def decrypt_content(file_content, filename)  -> dict:
    was_successful = False
    for key_path in get_key_paths():
        fernet = Fernet(load_key(key_path))
        try:
            file_content = fernet.decrypt(file_content)
            filename = fernet.decrypt(filename.encode()).decode()
            print(ctxt(f'Decrypted with "{key_path}"', Fore.GREEN))
            was_successful = True
            break
        except InvalidToken:
            continue
    if not was_successful:
        raise Exception(f'Decryption key for the file not found in "{ENCRYPTION_KEYS_PATH}"')

    return {
        "file_content": file_content,
        "filename": filename
    }