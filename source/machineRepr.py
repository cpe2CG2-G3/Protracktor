from expState import MachineState 
from taskHandlerStates import TaskHandler
from userResponse import UserResponse
from states import State
from rich import print as rprint
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from pyfiglet import figlet_format


class Protracktor(State):
    def __init__(self, taskHandler, pseudoDB, taskGenerator):
        self.__taskGenerator = taskGenerator
        self.__pseudoDB = pseudoDB
        self.__layout = Layout()
        self.__console = Console()
        self.__currentState = MachineState.HOME_MENU
        self.__taskHandler = taskHandler
        self.__choices = {UserResponse.YES : "Yes", UserResponse.NO : "No", UserResponse.BACK : "Back" }
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
            return ask

    #public methods        
    def changeState(self, nextState):
        self.__currentState = nextState
        return self.__currentState

    def machineState(self) -> int:
        return self.__currentState
    
    def resetState(self) -> MachineState:
        self.__currentState = MachineState.HOME_MENU
        return self.__currentState

    def __displayInstruction(self) -> str:
        option_str = ""

        for each in self.__choices:
            option_str += f"{each}: {self.__choices[each]}\n"
        return option_str
    
    def __caveat(self) -> str:
         caveat = """\n[bold]The right panel is still at beta test[/b]...\nTo see the full details of all the pending list, it is located at the [bold green]Work Selection State of the Program[/bold green]
                \nWhile for the full list of completed task, go check the local text file named [bold green]progress.txt[/bold green]
                """
         return caveat
    #iaabstract estetik nito
    def atHomeMenu(self) -> MachineState:

        homeBanner = figlet_format("ProTrackTor", font = "slant")
       
        description = "A [blink][green]text-based user interface (TUI)[/blink][/green] based application helps the client monitor their productivity."
        self.__layout.split_row(Layout(name = "left"), Layout(name = "mid"), Layout(name = "right"))
        
        self.__layout["left"].split_column(Layout(name = "title"), Layout(name = "description"))
        self.__layout["left"]["title"].update(Panel(homeBanner))
        self.__layout["left"]["description"].update(Panel(description))
        
        self.__layout["mid"].update(Panel(f"{self.__caveat()}\nInstructions:\n{self.__displayInstruction()}\n[blink][bold cyan]Wish to proceed?[/bold cyan][/blink]"))

        self.__layout["right"].split_column(Layout(name="pending"), Layout(name="completed"))
        self.__layout["right"]["pending"].update(Panel(f"[blink][bold red]Pending\n[/bold red][/blink]{self.__pseudoDB.displayPending()}"))

        self.__layout["right"]["completed"].update(Panel(f"[blink][bold green]Completed\n[/bold green][/blink]{self.__pseudoDB.displayPending()}"))
  
        self.__console.print(self.__layout)
        self.__binaryQuestion(MachineState.HOME_MENU, "Options: ", MachineState.ADDING_WORKLOAD, MachineState.TERMINATED)
        return self.__currentState
    
    #iaabstract estetik nito
    def atAddingWorkLoad(self) -> MachineState:
        workLoadBanner = figlet_format("Adding Workload")
        self.__layout.split_row(Layout(name = "left"), Layout(name = "mid"), Layout(name = "right"))
        self.__layout["left"].update(Panel(workLoadBanner))
        self.__layout["mid"].update(Panel(f"{self.__caveat()}\nInstructions:\n{self.__displayInstruction()}\n[blink][bold cyan]Wish to proceed?[/bold cyan][/blink]"))
        
        self.__layout["right"].split_column(Layout(name="pending"), Layout(name="completed"))
        self.__layout["right"]["pending"].update(Panel(f"[blink][bold red]Pending\n[/bold red][/blink]{self.__pseudoDB.displayPending()}"))

        self.__layout["right"]["completed"].update(Panel(f"[blink][bold green]Completed\n[/bold green][/blink]{self.__pseudoDB.displayDone()}"))
        self.__console.print(self.__layout)
  
        ask = input(f"Add work: ").lower()
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