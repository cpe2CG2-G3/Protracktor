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

        match menuStatus:
            case MachineState.HOME_MENU:
                menu.atHomeMenu()
                clearScreen()
                break
            case MachineState.ADDING_WORKLOAD:
                menu.atAddingWorkLoad()
                clearScreen()
                break
            case MachineState.WORK_SELECTION:
                menu.atWorkSelectionProcess()
                clearScreen()
                break
            case MachineState.WORKING:
                menu.atWorkingProcess()
                time.sleep(5)
                clearScreen()
                break
            case MachineState.CHECKING_PROGRESS:
                menu.atCheckingProgress()
                clearScreen()
                break
            case MachineState.TERMINATED:
                menu.cleanUp()
                menu.closeFile()
                isProgramRunning = False
                break

        