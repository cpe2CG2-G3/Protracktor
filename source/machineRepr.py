from expState import MachineState 
from taskHandlerStates import TaskHandler
from userResponse import UserResponse
from states import State
from rich import print as rprint
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from pyfiglet import figlet_format
from termcolor import colored

class Protracktor(State):
    def __init__(self, taskHandler, pseudoDB, taskGenerator):
        self.__taskGenerator = taskGenerator
        self.__pseudoDB = pseudoDB
        self.__layout = Layout()
        self.__console = Console()
        self.__currentState = MachineState.HOME_MENU
        self.__taskHandler = taskHandler
        self.__choices = {UserResponse.YES : "Yes", UserResponse.NO : "No", UserResponse.CHECK_COMPLETED : "Check Completed" }
        self.__do = {TaskHandler.ADD_WORKLOAD : lambda: self.__taskHandler.addWork(self.__taskGenerator, self.__pseudoDB),
                     TaskHandler.SELECT_WORK : lambda: self.__taskHandler.selectWork(self.__pseudoDB),
                     TaskHandler.DO_TASK : lambda: self.__taskHandler.doCurrentTask(),
                     TaskHandler.RETRYING : lambda: self.__taskHandler.retryTask(),
                     TaskHandler.LOG_WHEN_DONE : lambda: self.__taskHandler.logWhenDone(self.__pseudoDB),
                     TaskHandler.LOG_WHEN_NOT_DONE : lambda x: self.__taskHandler.logWhenNotDone(x)}
    
    #private methods
    def __binaryQuestion(self, currentState : MachineState, 
                         prompt : str, yesResponse : MachineState, 
                         noResponse : MachineState):
        
        while self.__currentState == currentState:
            table = Table()
            table.add_column("Syntax", justify="center")
            table.add_column("Definition", justify="center")
            for options in self.__choices:
                table.add_row(options, self.__choices[options])
            self.__console.print(table)
            ask = input(prompt).lower()

            match ask:
                case UserResponse.YES:
                    self.changeState(yesResponse)
                    return self.__currentState
                case UserResponse.NO:
                    self.changeState(noResponse)
                    return self.__currentState
                case _:
                    print("[red]Try again...\n")

    #public methods        
    def changeState(self, nextState):
        self.__currentState = nextState
        return self.__currentState

    def machineState(self) -> int:
        return self.__currentState
    
    def resetState(self) -> MachineState:
        self.__currentState = MachineState.HOME_MENU
        return self.__currentState
    
    def atHomeMenu(self) -> MachineState:
        homeBanner = figlet_format("ProTrackTor")
        self.__console.print(Panel(homeBanner))      
        self.__binaryQuestion(MachineState.HOME_MENU, "Options: ", MachineState.ADDING_WORKLOAD, MachineState.TERMINATED)
        return self.__currentState
        
    def atAddingWorkLoad(self) -> MachineState:
        workLoadBanner = figlet_format("Adding Workload")
        ask = input(f"{workLoadBanner}\nAdd work [y/n]: ").lower()
        match ask:
            case UserResponse.YES:
                self.__do[TaskHandler.ADD_WORKLOAD]()
            case UserResponse.NO:
                self.changeState(MachineState.WORK_SELECTION)
        
        return self.__currentState
        
    def atWorkSelectionProcess(self) -> MachineState:
        somethingToDo = self.__pseudoDB.isNotEmpty()

        if somethingToDo:
            self.__do[TaskHandler.SELECT_WORK]()
            self.__currentState = MachineState.WORKING
        else:
            rprint("[red]NO WORK TO SELECT [NO PENDING TASK]\n")
            self.__currentState = MachineState.ADDING_WORKLOAD

        return self.__currentState
    
    def atWorkingProcess(self) -> MachineState:
        somethingToDo = self.__pseudoDB.isNotEmpty()

        if somethingToDo:
            self.__do[TaskHandler.DO_TASK]()
            self.changeState(MachineState.CHECKING_PROGRESS)
        else:
            rprint("[red]", figlet_format("NO PENDING TASK"))
            self.changeState(MachineState.ADDING_WORKLOAD)

        return self.__currentState
    
    def atCheckingProgress(self) -> MachineState:
        somethingToDo = self.__pseudoDB.isNotEmpty()

        if somethingToDo:
            currentTask = self.__pseudoDB.getWIP()
            ask = input(f"Is {currentTask.getTaskName()} done [y/n]: ").lower()

            match ask:
                case UserResponse.YES:
                    self.__do[TaskHandler.LOG_WHEN_DONE]()
                    self.__currentState = MachineState.HOME_MENU

                case UserResponse.NO:    
                    self.__currentState = MachineState.RETRYING_TASK

        return self.__currentState
    
   
    def atRetryingState(self) -> MachineState:
        self.__do[TaskHandler.RETRYING]()
        self.__currentState = MachineState.WORKING
        return self.__currentState
    
    def atTermination(self) -> MachineState:
        if self.__pseudoDB.isNotEmpty():
           for each in self.__pseudoDB.getPendingList():
               self.__do[TaskHandler.LOG_WHEN_NOT_DONE](each)
        return self.__currentState