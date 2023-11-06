from taskGenerator import TaskGenerator
from pseudoDatabase import PseudoDB
from timer import Timer 
from expState import MachineState
from machineRepr import Protracktor
from os import system, name
import time

def clearScreen():
    if name == "posix":
        system("clear")
    elif name == "nt":
        system("cls")

if __name__ == "__main__":
    taskGenerator= TaskGenerator()
    timer = Timer()
    storage = PseudoDB()
    protracktor = Protracktor()
                
    protocol = {
                MachineState.HOME_MENU : lambda: protracktor.atHomeMenu(),
                MachineState.ADDING_WORKLOAD : lambda: protracktor.atAddingWorkLoad(taskGenerator, storage),
                MachineState.WORK_SELECTION : lambda: protracktor.atWorkSelectionProcess(storage),
                MachineState.WORKING : lambda: protracktor.atWorkingProcess(storage),
                MachineState.CHECKING_PROGRESS : lambda: protracktor.atCheckingProgress(storage),
                MachineState.RETRYING_TASK : lambda: protracktor.atRetryingState(storage),
                MachineState.TERMINATED : lambda: protracktor.atTermination(storage),
                MachineState.ERROR : lambda: protracktor.resetState()
                }

    isProgramRunning = True
    while isProgramRunning:
        protracktorStatus = protracktor.machineState()

        match protracktorStatus:
            case MachineState.HOME_MENU:
                protocol[MachineState.HOME_MENU]()
                clearScreen()
            case MachineState.ADDING_WORKLOAD:
                protocol[MachineState.ADDING_WORKLOAD]()
                clearScreen()
            case MachineState.WORK_SELECTION:
                protocol[MachineState.WORK_SELECTION]()
                clearScreen()
            case MachineState.WORKING:
                protocol[MachineState.WORKING]()
                time.sleep(1)
                clearScreen()
            case MachineState.CHECKING_PROGRESS:
                protocol[MachineState.CHECKING_PROGRESS]()
                clearScreen()
            case MachineState.RETRYING_TASK:
                protocol[MachineState.RETRYING_TASK]()
                clearScreen()
            case MachineState.TERMINATED:
                protocol[MachineState.TERMINATED]()
                isProgramRunning = False
            case MachineState.ERROR:
                protocol[MachineState.ERROR]()
        