from constants.constants import *
from utils.folders import create_folders, folder2png
from menu import menu

create_folders(BASE_IMAGES_PATH, MOD_IMAGES_PATH, INPUT_FILES_PATH, OUTPUT_FILES_PATH, ENCRYPTION_KEYS_PATH)
folder2png(BASE_IMAGES_PATH)

menu()