from taskGenerator import TaskGenerator
from pseudoDatabase import PseudoDB
from expState import MachineState
from machineRepr import Protracktor
from taskHandling import TaskHandler
from filelogger import FileLogger
from timeHandler import Timer
from screenRefresher import clearScreen
import time

if __name__ == "__main__":
    fileLogger = FileLogger()
    taskGenerator= TaskGenerator()
    pseudoDB = PseudoDB()
    timer = Timer(pseudoDB)
    taskHandler = TaskHandler(fileLogger, timer)
    protracktor = Protracktor(taskHandler, pseudoDB, taskGenerator)

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
            case MachineState.CHECKING_PROGRESS:
                protocol[MachineState.CHECKING_PROGRESS]()
                clearScreen()
            case MachineState.RETRYING_TASK:
                protocol[MachineState.RETRYING_TASK]()
            case MachineState.TERMINATED:
                protocol[MachineState.TERMINATED]()
                isProgramRunning = False
            case MachineState.ERROR:
                protocol[MachineState.ERROR]()