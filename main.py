from interface import Interface
from storage import Storage
from task import Task
from timer import Timer 
from states import MachineState
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

    isProgramRunning = True

    while isProgramRunning:
        menuStatus = menu.machineState()
        if menuStatus == MachineState.HOME_MENU:
            menu.atHomeMenu()
            clearScreen()
        elif menuStatus == MachineState.ADDING_WORKLOAD:
            menu.atAddingWorkLoad()
            clearScreen()
        elif menuStatus == MachineState.WORK_SELECTION:
            menu.atWorkSelectionProcess()
        elif menuStatus == MachineState.WORKING:
            menu.atWorkingProcess()
            time.sleep(5)
            clearScreen()
        elif menuStatus == MachineState.CHECKING_PROGRESS:
            menu.atCheckingProgress()
            clearScreen()
        elif menuStatus == MachineState.RETRYING_TASK:
            menu.atRetryingState()
        elif menuStatus == MachineState.TERMINATED:
            menu.cleanUp()
            menu.closeFile()
            isProgramRunning = False
        else:
            menu.resetState()
            clearScreen()
        