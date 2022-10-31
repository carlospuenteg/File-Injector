import os
from pathlib import Path

from constants.constants import IMAGE_EXTS
from utils.ctxt import *

# Create folders if they don't exist
def create_folders(*args:str) -> None:
    folders = args

    for folder in folders:
        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)


def folder2png(folder:str) -> None:
    for file in os.listdir(folder):
        ext = Path(file).suffix
        stem = Path(file).stem
        if ext in IMAGE_EXTS and ext != ".png":
            os.rename(f"{folder}/{file}", f"{folder}/{stem}.png")
            print(ctxt(f"Converted {file} to {stem}.png", Fore.GREEN))