from  timeHandlerState import TimerState
from rich.console import Console
from screenRefresher import clearScreen
from pyfiglet import figlet_format
from rich.panel import Panel
from expState import MachineState
import time 

class TaskHandler:
    def __init__(self, fileLogger, timer):
        self.__timer = timer 
        self.__fileLogger = fileLogger
        self.__console = Console()

        self.__checkTime = {TimerState.NORMAL_COUNTDOWN : lambda: self.__timer.countDownNormally(),
                            TimerState.EXTENSION_COUNTDOWN : lambda: self.__timer.countDownExtended()}
    
    def addWork(self, taskGenerator : object, pseudoDB : object) -> None:
        taskGenerator.listDownTasks()
        pseudoDB.retrieveData(taskGenerator)
        
    
    def selectWork(self, pseudoDB : object):
        selecting = True
        while selecting:
            try:
                workSelectionBanner = figlet_format("WORK SELECTION")

                workSelectionBanner.center(len(workSelectionBanner))
                self.__console.print(Panel(f"[bright_magenta]{workSelectionBanner}"))
                self.__console.print(f"[bold bright_red][blink]Pending:[/bold bright_red][/blink]\n\n{pseudoDB.displayPending()}")
                taskSelection = int(input("Select task from the index: "))
                currentTask = pseudoDB.readPendingList()[taskSelection]
                pseudoDB.setWIP(currentTask)
                self.__console.print(f"[bold][blink]Work to be accomplished[/blink]: [bright_yellow]{currentTask.getTaskName()}")
            except ValueError as ve:
                self.__console.print("[bold red]Error: ", ve)
                time.sleep(1)
                clearScreen()
            except IndexError as ie:
                self.__console.print("[bold red]Error: ", ie)
                time.sleep(1)
                clearScreen()
            else:
                selecting = False

    def doCurrentTask(self):
        self.__checkTime[TimerState.NORMAL_COUNTDOWN]()
        timesOverBanner = figlet_format("Time's Up")
        self.__console.print(Panel(f"[bright_red]{timesOverBanner}"))
        time.sleep(0.5)
        
    def logWhenDone(self, pseudoDB : object):
        currentTask = pseudoDB.getWIP()   
        currentTask.changeStatus()
        self.__fileLogger.log(currentTask)
        pseudoDB.markDone()

    def logWhenNotDone(self, task : object):
        self.__fileLogger.log(task)
       
    def retryTask(self) -> MachineState:
        self.__timer.changeState(TimerState.EXTENSION_COUNTDOWN)
        self.__checkTime[TimerState.EXTENSION_COUNTDOWN]()
        timesOverBanner = figlet_format("Time's Up")
        self.__console.print(Panel(f"[bright_red]{timesOverBanner}"))
        time.sleep(0.5)
        
    def redoWorkAdding(self, pseudoDB : object) -> object:
        if not pseudoDB.isNotEmpty():
            pseudoDB.clearPending()
        else:
            pseudoDB.pop()
        return pseudoDB
    
    def redoWorkSelection(self, pseudoDB : object) -> object:
        pseudoDB.pop()
        return pseudoDB