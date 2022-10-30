import math

BASE_IMAGES_PATH = "files/base-images"
MOD_IMAGES_PATH = "files/modified-images"
INPUT_FILES_PATH = "files/input-files"
OUTPUT_FILES_PATH = "files/output-files"
ENCRYPTION_KEYS_PATH = "files/$encryption-keys"

IMAGE_EXTS = [".png", ".jpg", ".jpeg"]

# Maximum filename size
MAX_FN_SIZE = 256 # In bytes
MAX_FN_SIZE_BIN = MAX_FN_SIZE * 4 # In bits

# Max base exponent
MAX_BASE_EXP = 4 # 2^4 = 16
MAX_BASE_EXP_BASE = 2**int(math.log2(MAX_BASE_EXP)+1)
MAX_BASE_EXP_MASK = 256 - MAX_BASE_EXP_BASE