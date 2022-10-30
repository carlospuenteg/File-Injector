from colorama import Fore, init; init()

def ctxt(text:str, color:str=Fore.WHITE) -> str:
    return f"{color}{text}{Fore.RESET}"