from pathlib import Path

import pydub
from PIL import Image
import numpy as np

from constants.constants import *


#-------------------------------------------------------
# Read the file
def read_file(path: str) -> bytes:
    with open(path, 'rb') as f: 
        return f.read()
    
# Read audio file into a numpy array
def read_audio(path:str) -> dict[np.ndarray,int,int]:
    # Get the audio object
    audio = pydub.AudioSegment.from_mp3(path)

    # Convert the audio object to a numpy array
    audio_arr = np.array(audio.get_array_of_samples())

    # Return the audio array, frame rate and number of channels
    return {
        "arr": audio_arr,
        "frame_rate": audio.frame_rate, 
        "num_channels": audio.channels
    }

# Read audio file into a numpy array
def read_image(path:str) -> np.ndarray:
    return np.array(Image.open(path))


# Read the base file
def read_base_file(path: str) -> np.ndarray:
    # If the file has a valid image extension
    if Path(path).suffix in IMAGE_EXTS:
        return {
            "file_type": "image",
            "arr": read_image(path)
        }

    # If the file has a valid audio extension
    elif Path(path).suffix in AUDIO_EXTS:
        audio_dict = read_audio(path)
        return {
            "file_type": "audio",
            "arr": audio_dict["arr"],
            "frame_rate": audio_dict["frame_rate"],
            "num_channels": audio_dict["num_channels"]
        }

    # If the file doesn't have a valid extension, raise an exception
    else:
        raise Exception("Invalid base file type")

#-------------------------------------------------------

# Write file in a path
def write_file(file: bytes, path: str) -> None:
    with open(path, 'wb') as f: 
        f.write(file)

# Write audio array to a file
def write_audio(arr, frame_rate, num_channels, path):
    song = pydub.AudioSegment(arr.tobytes(), frame_rate=frame_rate, sample_width=2, channels=num_channels)
    song.export(path, format=Path(path).suffix[1:], bitrate="320k")

# Write image array to a file
def write_image(arr, path):
    Image.fromarray(arr).save(path)