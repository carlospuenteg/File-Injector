import os
from pathlib import Path

from utils.ctxt import *

def check_path(path:str) -> bool:
    return os.path.isfile(path)

def get_valid_filename(msg:str, exts:list=None, allow_blank:bool=False) -> str:
    while True:
        filename = input(msg).strip()
        ext = Path(filename).suffix
        fn = Path(filename).stem

        if not fn:
            if allow_blank:
                if ext: 
                    print(ctxt("Can't have just an extension", Fore.RED))
                    continue
                else:
                    return filename
            else:
                print(ctxt("Filename can't be blank", Fore.RED))
                continue
        if exts:
            if ext:
                if ext in exts:
                    return filename
                else:
                    print(ctxt("Invalid extension", Fore.RED))
            else:
                return f"{filename}{exts[0]}"
        else:
            return filename


def get_path(folder_paths:str, msg:str, exts:list=None) -> str:
    # Concatenate exts lists into a single list
    if exts and len(exts) > 1:
        exts = [ext for ext_list in exts for ext in ext_list] if exts else None
    while True:
        filename = input(msg).strip()
        for folder_path in folder_paths:
            path = f"{folder_path}/{filename}"
            ext = Path(path).suffix
            stem = Path(path).stem
            if ext:
                if check_path(path) and (not exts or ext in exts):
                    return path
            # If the file doesn't have extension or if that file with that extension doesn't exist
            if exts:
                for e in exts:
                    path = f"{folder_path}/{stem}{e}"
                    if check_path(path):
                        return path
            else:
                for file in os.listdir(folder_path):
                    if stem == Path(file).stem and check_path(f"{folder_path}/{file}"):
                        return f"{folder_path}/{file}"

        print(ctxt("Invalid file", Fore.RED))
    

def get_bool(msg:str) -> bool:
    while True:
        choice = input(f"{msg} (y/n): ")
        if choice.strip().lower() == 'y': 
            return True
        elif choice.strip().lower() == 'n': 
            return False
        else:
            print(ctxt("Invalid input", Fore.RED))