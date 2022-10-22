from colorama import Fore, init; init()

class Fore:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    LIGHTBLACK_EX = '\033[90m'
    LIGHTRED_EX = '\033[91m'
    LIGHTGREEN_EX = '\033[92m'
    LIGHTYELLOW_EX = '\033[93m'
    LIGHTBLUE_EX = '\033[94m'
    LIGHTMAGENTA_EX = '\033[95m'
    LIGHTCYAN_EX = '\033[96m'
    LIGHTWHITE_EX = '\033[97m'
    RESET = '\033[39m'

def ctxt(text:str, color:str=Fore.WHITE) -> str:
    return f"{color}{text}{Fore.RESET}"