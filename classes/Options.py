from utils.ctxt import *

class Options:
    def __init__(self, options:list, first_idx:int=0):
        self.options = options
        self.first_idx = first_idx


    def get_choice(self) -> int:
        self.__str__()
        choice = input("Option: ")

        if self.check_input(choice): return int(choice)

        print(ctxt("\nInvalid choice.\n", Fore.RED))
        return self.get_choice()


    def check_input(self, choice:str) -> bool:
        return choice.strip().isdigit() and \
               int(choice) in range(self.first_idx, self.first_idx + len(self.options))


    def __str__(self) -> str:
        print("".join(
            [f"[{self.first_idx+i}] {opt}\n" 
            for i,opt in enumerate(self.options)]))