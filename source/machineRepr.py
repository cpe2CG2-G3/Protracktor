from expState import MachineState 
from taskHandlerStates import TaskHandler
from userResponse import UserResponse
from states import State
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from pyfiglet import figlet_format
from screenRefresher import clearScreen
import time

class Protracktor(State):
    def __init__(self, taskHandler, pseudoDB, taskGenerator):
        self.__taskGenerator = taskGenerator
        self.__pseudoDB = pseudoDB
        self.__layout = Layout()
        self.__console = Console()
        self.__currentState = MachineState.HOME_MENU
        self.__taskHandler = taskHandler
        self.__choices = {
                          UserResponse.YES : "Yes", 
                          UserResponse.NO : "No", 
                          UserResponse.BACK : "Back",
                          UserResponse.CHECK_PENDING : "Check Pending", 
                          UserResponse.CHECK_COMPLETED : "Check Completed"
                          }
        self.__do = {
                     TaskHandler.ADD_WORKLOAD : lambda taskGenerator, pseudoDB: self.__taskHandler.addWork(taskGenerator, pseudoDB),
                     TaskHandler.SELECT_WORK : lambda pseudoDB: self.__taskHandler.selectWork(pseudoDB),
                     TaskHandler.DO_TASK : lambda: self.__taskHandler.doCurrentTask(),
                     TaskHandler.RETRYING : lambda: self.__taskHandler.retryTask(),
                     TaskHandler.LOG_WHEN_DONE : lambda pseudoDB: self.__taskHandler.logWhenDone(pseudoDB),
                     TaskHandler.LOG_WHEN_NOT_DONE : lambda pseudoDB: self.__taskHandler.logWhenNotDone(pseudoDB),
                     TaskHandler.REDO_WORKLOAD_ADDING : lambda pseudoDB: self.__taskHandler.redoWorkAdding(pseudoDB),
                     TaskHandler.REDO_WORK_SELECTION : lambda pseudoDB: self.__taskHandler.redoWorkSelection(pseudoDB)
                     }
    

    #private methods
    def __doubleChecking(self, yesResponse : MachineState) -> None:
        try:
            askAgain = input("Are you sure? [y] [n]: ")
            match askAgain:
                case UserResponse.YES:
                    self.changeState(yesResponse)
                case UserResponse.NO:
                    match self.__currentState:
                        case MachineState.ADDING_WORKLOAD:
                            self.__do[TaskHandler.REDO_WORKLOAD_ADDING](self.__pseudoDB)
                case _:
                    self.__console.print("[bright_red]Error: invalid input[/bright_red]")
                    match self.__currentState:
                        case MachineState.ADDING_WORKLOAD:
                            self.__do[TaskHandler.REDO_WORKLOAD_ADDING](self.__pseudoDB)
                    time.sleep(1)
        except KeyboardInterrupt:
            self.changeState(MachineState.ERROR)
            
    
    def __query(self, currentState : MachineState, 
                prompt : str, yesResponse : MachineState, 
                noResponse : MachineState, previousState : MachineState) -> None:
        try:
            while self.__currentState == currentState:
                ask = input(prompt).lower()

                match ask:
                    case UserResponse.YES:
                        self.changeState(yesResponse)
                    case UserResponse.NO:
                        self.changeState(noResponse)
                    case UserResponse.BACK:
                        self.changeState(previousState)
                    case UserResponse.CHECK_PENDING:
                        clearScreen()
                        pendingBanner = figlet_format("Pending")
                        self.__console.print(Panel(f"[bright_red]{pendingBanner}"))
                        self.__console.print(f"{self.__pseudoDB.displayPending()}")
                        time.sleep(5)
                        self.changeState(currentState)
                        clearScreen()
                        self.__console.print(self.__layout)
                    case UserResponse.CHECK_COMPLETED:
                        clearScreen()
                        completedBanner = figlet_format("Completed")
                        self.__console.print(Panel(f"[green2]{completedBanner}"))
                        self.__console.print(f"{self.__pseudoDB.displayDone()}")
                        time.sleep(5)
                        self.changeState(currentState)
                        clearScreen()
                        self.__console.print(self.__layout)
                    case _:
                        self.__console.print("[bright_red]Try again...\n")
                        time.sleep(1)
                        clearScreen()
                        self.__console.print(self.__layout)
        except KeyboardInterrupt:
            self.changeState(MachineState.ERROR)
                

    def __displayInstruction(self) -> str:
        option_str = "[bold][bright_yellow]Instructions:[/bright_yellow][/bold] Type and enter the specified string from the string options below to interact with the program...\n\n"

        for each in self.__choices:
            option_str += f" [ {each} ]: {self.__choices[each]}\n"
        return option_str
    
    
    def __caveat(self) -> str:
         caveat = """[bold]The right panel is still at alpha test[/bold]...To see the full details of the pending or the completed task.
         \nPlease type and enter the specific command to invoke that functionality.
         \nSee the [bright_yellow]Instruction[/bright_yellow] label below...\n
                """
         return caveat
    
    def __noPendingWarning(self) -> None:
        warningBanner =  figlet_format("NO PENDING TASK")
        self.__console.print(Panel(f"[bright_red]{warningBanner}"))
    
    def __isUserSlacking(self) -> MachineState:
        conscienceBanner = figlet_format("EMERGENCY???")
        clearScreen()
        self.__console.print(Panel(f"[blink][bright_red]{conscienceBanner}[/blink][/bright_red]"))
        self.__console.print(f"[bold] Make sure you are not being unproductive...")
        self.changeState(MachineState.TERMINATED)

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
        try:
            homeBanner = figlet_format("ProTrackTor")
        
            description = """A [blink][green]text-based user interface (TUI)[/green][/blink] based application that helps the client monitor their productivity. Thus, it figuratively acts as the client's second brain as they keep working on their pending tasks. 
                             \nThe concept is a melded version of a note-taking and timer program, powered by file-handling functionality that acts as a makeshift database."""
            
            self.__layout.split_row(Layout(name = "left"), Layout(name = "mid"), Layout(name = "right"))
            self.__layout["left"].split_column(Layout(name = "title"), Layout(name = "description"))
            self.__layout["left"].ratio = 2
            self.__layout["left"]["title"].update(Panel(f"[cyan2]{homeBanner}"))
            self.__layout["left"]["description"].update(Panel(description))
            
            self.__layout["mid"].update(Panel(f"{self.__caveat()}\n{self.__displayInstruction()}\n[blink][bold cyan]Wish to proceed?[/bold cyan][/blink]"))
            self.__layout["right"].split_column(Layout(name="pending"), Layout(name="completed"))
            self.__layout["right"]["pending"].update(Panel(f"[blink][bold bright_red]Pending:\n\n[/bold bright_red][/blink]{self.__pseudoDB.displayPending()}"))

            self.__layout["right"]["completed"].update(Panel(f"[blink][bold bright_green]Completed:\n\n[/bold bright_green][/blink]{self.__pseudoDB.displayDone()}"))
    
            self.__console.print(self.__layout)
            self.__query(MachineState.HOME_MENU, "Options [y] [n] [b] [cp] [cc]: ", MachineState.ADDING_WORKLOAD, MachineState.TERMINATED, MachineState.HOME_MENU)
            return self.__currentState
        except KeyboardInterrupt:
            self.change(MachineState.ERROR)

    def atAddingWorkLoad(self) -> MachineState:
        try:
            workLoadBanner = figlet_format("Adding Workload")
            
            self.__layout.split_row(Layout(name = "left"), Layout(name = "mid"), Layout(name = "right"))
            self.__layout["left"].ratio = 2
            self.__layout["left"].update(Panel(workLoadBanner))
            self.__layout["mid"].update(Panel(f"{self.__caveat()}\n\n{self.__displayInstruction()}\n[blink][bold cyan]Wish to proceed?[/bold cyan][/blink]"))

            self.__layout["right"].split_column(Layout(name="pending"), Layout(name="completed"))
            self.__layout["right"]["pending"].update(Panel(f"[blink][bold bright_red]Pending:\n\n[/bold bright_red][/blink]{self.__pseudoDB.displayPending()}"))

            self.__layout["right"]["completed"].update(Panel(f"[blink][bold bright_green]Completed:\n\n[/bold bright_green][/blink]{self.__pseudoDB.displayDone()}"))
            self.__console.print(self.__layout)
        
            ask = input("Add workload [y] [n] [b] [cp] [cc]: ").lower()
            match ask:
                case UserResponse.YES:
                    self.__do[TaskHandler.ADD_WORKLOAD](self.__taskGenerator, self.__pseudoDB)  
                    self.__doubleChecking(MachineState.ADDING_WORKLOAD)  
                case UserResponse.NO:
                    self.__query(MachineState.ADDING_WORKLOAD,"Continue Adding? [y] [n] [b]: ", MachineState.ADDING_WORKLOAD, MachineState.WORK_SELECTION, MachineState.HOME_MENU)
                case UserResponse.BACK:
                    self.changeState(MachineState.HOME_MENU)
                case UserResponse.CHECK_PENDING:
                        clearScreen()
                        pendingBanner = figlet_format("Pending")
                        self.__console.print(Panel(f"[bright_red]{pendingBanner}"))
                        self.__console.print(f"{self.__pseudoDB.displayPending()}")
                        time.sleep(5)
                        self.changeState(MachineState.ADDING_WORKLOAD)
                        clearScreen()
                        self.__console.print(self.__layout)
                case UserResponse.CHECK_COMPLETED:
                    clearScreen()
                    completedBanner = figlet_format("Completed")
                    self.__console.print(Panel(f"[green2]{completedBanner}"))
                    self.__console.print(f"{self.__pseudoDB.displayDone()}")
                    time.sleep(5)
                    self.changeState(MachineState.ADDING_WORKLOAD)
                    clearScreen()
                    self.__console.print(self.__layout)
                case _:
                    self.__console.print("[bright_red]Try again...\n")
                    time.sleep(2)
        

            return self.__currentState
        except KeyboardInterrupt:
            self.changeState(MachineState.ERROR)
        
    def atWorkSelectionProcess(self) -> MachineState:
        try:
            somethingToDo = self.__pseudoDB.isNotEmpty()
            
            if somethingToDo:
                self.__do[TaskHandler.SELECT_WORK](self.__pseudoDB)
                self.__doubleChecking(MachineState.WORKING)

            else:
                self.__noPendingWarning()
                self.changeState(MachineState.ADDING_WORKLOAD)
                time.sleep(2)

            return self.__currentState
        except KeyboardInterrupt:
            self.changeState(MachineState.ADDING_WORKLOAD)
    
    def atWorkingProcess(self) -> MachineState:
        try:
            somethingToDo = self.__pseudoDB.isNotEmpty()
            if somethingToDo:
                self.__do[TaskHandler.DO_TASK]()
                self.changeState(MachineState.CHECKING_PROGRESS)
            else:
                self.__noPendingWarning()
                self.changeState(MachineState.ADDING_WORKLOAD)
                time.sleep(2)

            return self.__currentState
        except KeyboardInterrupt:
            self.__isUserSlacking()
        
    def atCheckingProgress(self) -> MachineState:
        try:
            somethingToDo = self.__pseudoDB.isNotEmpty()
            checkingProgressBanner = figlet_format("Checking Progress")
            self.__console.print(Panel(f"[cyan2]{checkingProgressBanner}"))

            if somethingToDo:
                currentTask = self.__pseudoDB.getWIP()
                ask = input(f"Is {currentTask.getTaskName()} done [y] [n]: ").lower()

                match ask:
                    case UserResponse.YES:
                        self.__do[TaskHandler.LOG_WHEN_DONE](self.__pseudoDB)
                        self.changeState(MachineState.HOME_MENU)
                    case UserResponse.NO:    
                        self.changeState(MachineState.RETRYING_TASK)
                    case _:
                        self.__console.print("[bright_red]Error: Invalid Input")
                        time.sleep(1)
                        
            return self.__currentState
        except KeyboardInterrupt:
            self.changeState(MachineState.TERMINATED)
        
    def atRetryingState(self) -> MachineState:
        try:
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
                    self.changeState(MachineState.HOME_MENU)
                case _:
                    self.__console.print("[bright_red]Error: Invalid Input")
                    time.sleep(1)
                    clearScreen()
    
            return self.__currentState
        except KeyboardInterrupt:
             self.__isUserSlacking()
    
    def atTermination(self) -> MachineState:
        if self.__pseudoDB.isNotEmpty():
            for each in self.__pseudoDB.readPendingList():
                self.__do[TaskHandler.LOG_WHEN_NOT_DONE](each)
        return self.__currentState