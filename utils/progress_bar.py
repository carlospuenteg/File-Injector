from utils.ctxt import *

def progress_bar(percent:float, text:str="", bar_len:int=30) -> None:
    SYMBOL = "━"
    percent_done = round(percent*100,2)
    done_len = round(percent*bar_len)
    left_len = bar_len - done_len

    print(f"   {ctxt(text,Fore.MAGENTA)} {ctxt(SYMBOL*done_len,Fore.GREEN)}{SYMBOL*left_len} {f'[{percent_done}%]'.ljust(8)}", end='\r')
    if percent == 1: 
        print("✅")