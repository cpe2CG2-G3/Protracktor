from expState import MachineState 
from taskHandlerStates import TaskHandler
from userResponse import UserResponse
from states import State
from rich import print
from pyfiglet import figlet_format

class Protracktor(State):
    def __init__(self, taskHandler, pseudoDB, taskGenerator):
        self.__taskGenerator = taskGenerator
        self.__pseudoDB = pseudoDB

        self.__currentState = MachineState.HOME_MENU
        self.__taskHandler = taskHandler
        self.__do = {TaskHandler.ADD_WORKLOAD : lambda: self.__taskHandler.addWork(self.__taskGenerator, self.__pseudoDB),
                     TaskHandler.SELECT_WORK : lambda: self.__taskHandler.selectWork(self.__pseudoDB),
                     TaskHandler.DO_TASK : lambda: self.__taskHandler.doCurrentTask(),
                     TaskHandler.RETRYING : lambda: self.__taskHandler.retryTask(),
                     TaskHandler.LOG_WHEN_DONE : lambda: self.__taskHandler.logWhenDone(self.__pseudoDB),
                     TaskHandler.LOG_WHEN_NOT_DONE : lambda x: self.__taskHandler.logWhenNotDone(x)}
    
    def changeState(self, nextState):
        self.__currentState = nextState
        return self.__currentState

    def machineState(self) -> int:
        return self.__currentState
    
    #user yes or no response handler may problem need ng executioner
    def __sequenceHandle(self, currentState : MachineState, 
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
            
    def resetState(self) -> MachineState:
        self.__currentState = MachineState.HOME_MENU
        return self.__currentState
    
    def atHomeMenu(self) -> MachineState:
        homeBanner = figlet_format("ProTrackTor", font = "slant")
        print(homeBanner)
        self.__sequenceHandle(MachineState.HOME_MENU, "Want to be productive [y/n]: ", MachineState.ADDING_WORKLOAD, MachineState.TERMINATED)
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
            print("NO WORK TO SELECT [NO PENDING TASK]\n")
            self.__currentState = MachineState.ADDING_WORKLOAD

        return self.__currentState
    
    def atWorkingProcess(self) -> MachineState:
        somethingToDo = self.__pseudoDB.isNotEmpty()

        if somethingToDo:
            self.__do[TaskHandler.DO_TASK]()
            self.changeState(MachineState.CHECKING_PROGRESS)
        else:
            print("Timer will not start ticking... [NO PENDING TASKS]\n")
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