from interface import Interface
from storage import Storage
from task import Task
from timer import Timer 
from os import system, name
import time

def clearScreen():
    if name == "posix":
        system("clear")
    elif name == "nt":
        system("cls")

if __name__ == "__main__":
    task = Task()
    timer = Timer()
    storage = Storage()
    menu = Interface(storage,timer)

    states = ("terminated", "at_home_menu" ,"adding_workload", "working", "checking_progress")
    
    isProgramRunning = True

    while isProgramRunning:
        if menu.machineState() == states[0]:
            menu.closeFile()
            isProgramRunning = False
        elif menu.machineState() == states[1]:
            clearScreen()
            menu.atHomeMenu()
        elif menu.machineState() == states[2]:
            clearScreen()
            menu.atAddingWorkLoad()
        elif menu.machineState() == states[3]:
            clearScreen()
            menu.atWorkingProcess()
            time.sleep(5)
        elif menu.machineState() == states[4]:
            clearScreen()
            menu.atCheckingProgress()
            menu.resetStateTransition()
        else:
            clearScreen()
            menu.resetStateTransition()
       