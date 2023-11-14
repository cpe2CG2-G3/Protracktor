from os import system, name

def clearScreen():
    if name == "posix":
        system("clear")
    elif name == "nt":
        system("cls")