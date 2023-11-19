from expState import MachineState 
from taskHandlerStates import TaskHandler
from userResponse import UserResponse
from states import State
from rich import print as rprint
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from pyfiglet import figlet_format
import time

class Protracktor(State):
    def __init__(self, taskHandler, pseudoDB, taskGenerator):
        self.__taskGenerator = taskGenerator
        self.__pseudoDB = pseudoDB
        self.__layout = Layout()
        self.__console = Console()
        self.__currentState = MachineState.HOME_MENU
        self.__taskHandler = taskHandler
        self.__choices = {UserResponse.YES : "Yes", UserResponse.NO : "No", UserResponse.BACK : "Back" }
        self.__do = {TaskHandler.ADD_WORKLOAD : lambda taskGenerator, pseudoDB: self.__taskHandler.addWork(taskGenerator, pseudoDB),
                     TaskHandler.SELECT_WORK : lambda pseudoDB: self.__taskHandler.selectWork(pseudoDB),
                     TaskHandler.DO_TASK : lambda: self.__taskHandler.doCurrentTask(),
                     TaskHandler.RETRYING : lambda: self.__taskHandler.retryTask(),
                     TaskHandler.LOG_WHEN_DONE : lambda pseudoDB: self.__taskHandler.logWhenDone(pseudoDB),
                     TaskHandler.LOG_WHEN_NOT_DONE : lambda pseudoDB: self.__taskHandler.logWhenNotDone(pseudoDB),
                     TaskHandler.REDO_WORKLOAD_ADDING : lambda pseudoDB: self.__taskHandler.redoWorkAdding(pseudoDB),
                     TaskHandler.REDO_WORK_SELECTION : lambda pseudoDB: self.__taskHandler.redoWorkSelection(pseudoDB)}
    

    #private methods
    def __doubleChecking(self, yesResponse : MachineState) -> None:
        askAgain = input("Are you sure? [y/n]: ")
        match askAgain:
            case UserResponse.YES:
                self.changeState(yesResponse)
            case UserResponse.NO:
                match self.__currentState:
                    case MachineState.ADDING_WORKLOAD:
                        self.__do[TaskHandler.REDO_WORKLOAD_ADDING](self.__pseudoDB)
                    case MachineState.WORK_SELECTION:
                        self.__do[TaskHandler.REDO_WORK_SELECTION](self.__pseudoDB)
        
    

    def __query(self, currentState : MachineState, 
                         prompt : str, yesResponse : MachineState, 
                         noResponse : MachineState, previousState : MachineState) -> None:
        while self.__currentState == currentState:
            ask = input(prompt).lower()

            match ask:
                case UserResponse.YES:
                    self.changeState(yesResponse)
                case UserResponse.NO:
                    self.changeState(noResponse)
                case UserResponse.BACK:
                    self.changeState(previousState)
                case _:
                    print("[red]Try again...\n")
            return ask

    def __displayInstruction(self) -> str:
        option_str = "Instructions: Type and enter the specified string from the string options below to interact with the program...\n\n"

        for each in self.__choices:
            option_str += f" [ {each} ]: {self.__choices[each]}\n"
        return option_str
    
    
    def __caveat(self) -> str:
         caveat = """\n[bold]The right panel is still at alpha test[/b]...\nTo see the full details of all the pending list, it is located at the [bold green]Work Selection State of the Program[/bold green]
                \nWhile for the full list of completed task, go check the local text file named [bold green]progress.txt[/bold green]
                """
         return caveat
    
    def __noPendingWarning(self) -> None:
        warningBanner =  figlet_format("NO PENDING TASK")
        self.__console.print(Panel(f"[bright_red]{warningBanner}"))



    #public methods        
    def changeState(self, nextState):
        self.__currentState = nextState
        return self.__currentState

    def machineState(self) -> int:
        return self.__currentState
    
    def resetState(self) -> MachineState:
        self.__currentState = MachineState.HOME_MENU
        return self.__currentState
    
    #iaabstract estetik nito
    def atHomeMenu(self) -> MachineState:

        homeBanner = figlet_format("ProTrackTor")
       
        description = "A [blink][green]text-based user interface (TUI)[/blink][/green] based application helps the client monitor their productivity."
        self.__layout.split_row(Layout(name = "left"), Layout(name = "mid"), Layout(name = "right"))
        self.__layout["left"].split_column(Layout(name = "title"), Layout(name = "description"))
        self.__layout["left"].ratio = 2
        self.__layout["left"]["title"].update(Panel(f"[cyan2]{homeBanner}"))
        self.__layout["left"]["description"].update(Panel(description))
        
        self.__layout["mid"].update(Panel(f"{self.__caveat()}\n{self.__displayInstruction()}\n[blink][bold cyan]Wish to proceed?[/bold cyan][/blink]"))
        self.__layout["right"].split_column(Layout(name="pending"), Layout(name="completed"))
        self.__layout["right"]["pending"].update(Panel(f"[blink][bold bright_red]Pending\n[/bold bright_red][/blink]{self.__pseudoDB.displayPending()}"))

        self.__layout["right"]["completed"].update(Panel(f"[blink][bold bright_green]Completed\n[/bold bright_green][/blink]{self.__pseudoDB.displayDone()}"))
  
        self.__console.print(self.__layout)
        self.__query(MachineState.HOME_MENU, "Options: ", MachineState.ADDING_WORKLOAD, MachineState.TERMINATED, MachineState.HOME_MENU)
        
        return self.__currentState
    
    #iaabstract estetik nito
    def atAddingWorkLoad(self) -> MachineState:
        workLoadBanner = figlet_format("Adding Workload")
        self.__layout.split_row(Layout(name = "left"), Layout(name = "mid"), Layout(name = "right"))
        self.__layout["left"].update(Panel(workLoadBanner))
        self.__layout["mid"].update(Panel(f"{self.__caveat()}\n\n{self.__displayInstruction()}\n[blink][bold cyan]Wish to proceed?[/bold cyan][/blink]"))
        
        self.__layout["right"].split_column(Layout(name="pending"), Layout(name="completed"))
        self.__layout["right"]["pending"].update(Panel(f"[blink][bold bright_red]Pending\n[/bold bright_red][/blink]{self.__pseudoDB.displayPending()}"))

        self.__layout["right"]["completed"].update(Panel(f"[blink][bold bright_green]Completed\n[/bold bright_green][/blink]{self.__pseudoDB.displayDone()}"))
        self.__console.print(self.__layout)
       
        ask = input("Add workload [y] [n] [b]: ").lower()
        match ask:
            case UserResponse.YES:
                self.__do[TaskHandler.ADD_WORKLOAD](self.__taskGenerator, self.__pseudoDB)  
                self.__doubleChecking(MachineState.ADDING_WORKLOAD)  
            case UserResponse.NO:
                self.__query(MachineState.ADDING_WORKLOAD,"Continue Adding? [y] [n] [b]: ", MachineState.ADDING_WORKLOAD, MachineState.WORK_SELECTION, MachineState.HOME_MENU)
            case UserResponse.BACK:
                self.changeState(MachineState.HOME_MENU)

        return self.__currentState
        
    def atWorkSelectionProcess(self) -> MachineState:
        somethingToDo = self.__pseudoDB.isNotEmpty()
        
        workSelectionBanner = figlet_format("WORK SELECTION")

        workSelectionBanner.center(len(workSelectionBanner))
        self.__console.print(Panel(f"[bright_magenta]{workSelectionBanner}"))

        if somethingToDo:
            self.__do[TaskHandler.SELECT_WORK](self.__pseudoDB)
            self.__doubleChecking(MachineState.WORKING)

        else:
            self.__noPendingWarning()
            self.changeState(MachineState.ADDING_WORKLOAD)
            time.sleep(2)

        return self.__currentState
    
    def atWorkingProcess(self) -> MachineState:
        somethingToDo = self.__pseudoDB.isNotEmpty()
        if somethingToDo:
            self.__do[TaskHandler.DO_TASK]()
            self.changeState(MachineState.CHECKING_PROGRESS)
        else:
            self.__noPendingWarning()
            self.changeState(MachineState.ADDING_WORKLOAD)
            time.sleep(2)

        return self.__currentState
    
    def atCheckingProgress(self) -> MachineState:
        somethingToDo = self.__pseudoDB.isNotEmpty()
        checkingProgressBanner = figlet_format("Checking Progress")
        self.__console.print(Panel(f"[cyan2]{checkingProgressBanner}"))

        if somethingToDo:
            currentTask = self.__pseudoDB.getWIP()
            ask = input(f"Is {currentTask.getTaskName()} done [y/n]: ").lower()

            match ask:
                case UserResponse.YES:
                    self.__do[TaskHandler.LOG_WHEN_DONE](self.__pseudoDB)
                    self.changeState(MachineState.HOME_MENU)

                case UserResponse.NO:    
                    self.changeState(MachineState.RETRYING_TASK)

        return self.__currentState
    
    def atRetryingState(self) -> MachineState:
        currentTask = self.__pseudoDB.getWIP()
        warningBanner = figlet_format("Oh No!\n")

        self.__console.print(Panel(f"[bright_red][blink]{warningBanner}[/bright_red][/blink]"))
        self.__console.print(f"You didn\'t finished [bright_red]{currentTask.getTaskName()}[/bright_red]\n")
        response = input("Would you to like to extend your time? [y] [n]: ").lower()
        
        match response:
            case UserResponse.YES:
                self.__do[TaskHandler.RETRYING]()
                self.changeState(MachineState.CHECKING_PROGRESS)
            case UserResponse.NO:
                #self.__do[TaskHandler.LOG_WHEN_NOT_DONE](self.__pseudoDB)
                self.changeState(MachineState.HOME_MENU)
  
        return self.__currentState
    
    def atTermination(self) -> MachineState:
        if self.__pseudoDB.isNotEmpty():
            for each in self.__pseudoDB.readPendingList():
                self.__do[TaskHandler.LOG_WHEN_NOT_DONE](each)
        return self.__currentState