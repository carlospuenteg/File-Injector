import os
from pathlib import Path

import pydub

from constants.constants import *
from utils.ctxt import *

# Create folders if they don't exist
def create_folders(*args:str) -> None:
    folders = args

    for folder in folders:
        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)


def folder_convert(folder:str, extension:str, valid_exts:list) -> None:
    for file in os.listdir(folder):
        ext = Path(file).suffix
        stem = Path(file).stem
        if ext in valid_exts and ext != extension:
            os.rename(f"{folder}/{file}", f"{folder}/{stem}{extension}")
            print(ctxt(f"Converted {file} to {stem}{extension}", Fore.GREEN))


def folder2mp3(folder:str) -> None:
    for file in os.listdir(folder):
        ext = Path(file).suffix
        stem = Path(file).stem
        if ext in AUDIO_EXTS and ext != ".mp3":
            sound = pydub.AudioSegment.from_wav(f"{folder}/{file}")
            sound.export(f"{folder}/{stem}.mp3", format="mp3")
            os.remove(f"{folder}/{file}")
            print(ctxt(f"Converted {file} to {stem}.mp3", Fore.GREEN))