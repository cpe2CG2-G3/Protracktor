from taskGenerator import TaskGenerator
from pseudoDatabase import PseudoDB
from expState import MachineState
from machineRepr import Protracktor
from taskHandling import TaskHandler
from filelogger import FileLogger
from timeHandler import Timer
from screenRefresher import clearScreen
from rich.console import Console
from termcolor import colored

import time

if __name__ == "__main__":
    fileLogger = FileLogger()
    taskGenerator= TaskGenerator()
    pseudoDB = PseudoDB()
    timer = Timer(pseudoDB)
    taskHandler = TaskHandler(fileLogger, timer, pseudoDB)
    protracktor = Protracktor(taskHandler, pseudoDB, taskGenerator)

    console = Console()
    protocol = {
                MachineState.HOME_MENU : lambda: protracktor.atHomeMenu(),
                MachineState.ADDING_WORKLOAD : lambda: protracktor.atAddingWorkLoad(),
                MachineState.WORK_SELECTION : lambda: protracktor.atWorkSelectionProcess(),
                MachineState.WORKING : lambda: protracktor.atWorkingProcess(),
                MachineState.CHECKING_PROGRESS : lambda: protracktor.atCheckingProgress(),
                MachineState.RETRYING_TASK : lambda: protracktor.atRetryingState(),
                MachineState.TERMINATED : lambda: protracktor.atTermination(),
                MachineState.ERROR : lambda: protracktor.resetState()
                }
    
    isProgramRunning = True
    while isProgramRunning:
        protracktorStatus = protracktor.machineState()
        try:
            match protracktorStatus:
                case MachineState.HOME_MENU:
                    protocol[MachineState.HOME_MENU]()
                    clearScreen()
                case MachineState.ADDING_WORKLOAD:
                    protocol[MachineState.ADDING_WORKLOAD]()
                    time.sleep(1)
                    clearScreen()
                case MachineState.WORK_SELECTION:
                    protocol[MachineState.WORK_SELECTION]()
                    time.sleep(1)
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
                    #clearScreen()
                case MachineState.TERMINATED:
                    protocol[MachineState.TERMINATED]()
                    isProgramRunning = False
                case MachineState.ERROR:
                    protocol[MachineState.ERROR]()
        except KeyboardInterrupt:
            protocol[MachineState.ERROR]()
            clearScreen()