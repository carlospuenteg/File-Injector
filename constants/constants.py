#-------------------------------------------------------
ENCRYPTION_KEYS_PATH = "files/$encryption-keys"

BASE_PATH = "files/base"
BASE_IMAGES_PATH = f"{BASE_PATH}/images"
BASE_AUDIOS_PATH = f"{BASE_PATH}/audios"

INPUT_PATH = "files/input"

MOD_PATH = "files/modified"
MOD_IMAGES_PATH = f"{MOD_PATH}/images"
MOD_AUDIOS_PATH = f"{MOD_PATH}/audios"

OUTPUT_PATH = "files/output"

PATHS = [BASE_IMAGES_PATH, INPUT_PATH, BASE_AUDIOS_PATH, MOD_IMAGES_PATH, MOD_AUDIOS_PATH, OUTPUT_PATH]
#-------------------------------------------------------
IMAGE_EXTS = [".png", ".jpg", ".jpeg"]
AUDIO_EXTS = [".mp3", ".wav"]
#-------------------------------------------------------
# Maximum number used for masking
MAX_MASK = 2**16

# Maximum filename size
MAX_FN_SIZE = 256 # In bytes
MAX_FN_SIZE_BIN = MAX_FN_SIZE * 8 # In bits