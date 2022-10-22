import os
from pathlib import Path

from utils.ctxt import *
from constants.constants import IMAGE_EXTS

def create_folders(*args) -> None:
    folders = args

    for folder in folders:
        if not os.path.isdir(folder):
            os.makedirs(folder, exist_ok=True)


def folder2png(folder) -> None:
    for file in os.listdir(folder):
        ext = Path(file).suffix
        stem = Path(file).stem
        if ext in IMAGE_EXTS and ext != ".png":
            os.rename(f"{folder}/{file}", f"{folder}/{stem}.png")
            print(ctxt(f"Converted {file} to {stem}.png", Fore.GREEN))