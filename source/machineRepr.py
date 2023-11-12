from expState import MachineState 
from taskHandlerStates import TaskHandler
from userResponse import UserResponse

class Protracktor:
    def __init__(self, taskHandler, pseudoDB, taskGenerator):
        self.__taskGenerator = taskGenerator
        self.__pseudoDB = pseudoDB

        self.__currentState = MachineState.HOME_MENU
        self.__taskHandler = taskHandler
        self.__do = {TaskHandler.ADD_WORKLOAD : lambda: self.__taskHandler.addWork(self.__taskGenerator, self.__pseudoDB),
                     TaskHandler.SELECT_WORK : lambda: self.__taskHandler.selectWork(self.__pseudoDB),
                     TaskHandler.DO_TASK : lambda: self.__taskHandler.doCurrentTask(),
                     TaskHandler.LOG_WHEN_DONE : lambda: self.__taskHandler.logWhenDone(self.__pseudoDB),
                     TaskHandler.LOG_WHEN_NOT_DONE : lambda: self.__taskHandler.logWhenNotDone(self.__pseudoDB)}
    
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
                    self.__currentState = yesResponse
                    return self.__currentState
                case UserResponse.NO:
                    self.__currentState = noResponse
                    return self.__currentState
                case _:
                    print("Try again...\n")
            
    def resetState(self) -> MachineState:
        self.__currentState = MachineState.HOME_MENU
        return self.__currentState
    
    def atHomeMenu(self) -> MachineState:
        self.__sequenceHandle(MachineState.HOME_MENU, "Want to be productive [y/n]: ", MachineState.ADDING_WORKLOAD, MachineState.TERMINATED)
        return self.__currentState
        
    def atAddingWorkLoad(self) -> MachineState:
        ask = input("Add work [y/n]: ").lower()
        match ask:
            case UserResponse.YES:
                self.__do[TaskHandler.ADD_WORKLOAD]()
            case UserResponse.NO:
                self.__currentState = MachineState.WORK_SELECTION
        
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
            self.__currentState = MachineState.CHECKING_PROGRESS
        else:
            print("Timer will not start ticking... [NO PENDING TASKS]\n")
            self.__currentState = MachineState.ADDING_WORKLOAD

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
                    self.__do[TaskHandler.LOG_WHEN_NOT_DONE]()
                    self.__currentState = MachineState.RETRYING_TASK

        return self.__currentState
    
   
    def atRetryingState(self) -> MachineState:
        currentTask = self.__pseudoDB.getWIP()
        print(f"You didn\'t finished {currentTask.getTaskName()}\nFor how long you would like to try again?\n")

        currentTask.setEstimatedTimeTaken()

        self.__currentState = MachineState.WORKING

        return self.__currentState
    
    def atTermination(self) -> MachineState:
        if self.__pseudoDB.isNotEmpty():
           for each in self.__pseudoDB.getPendingList():
               self.__do[TaskHandler.LOG_WHEN_NOT_DONE]()
        return self.__currentState