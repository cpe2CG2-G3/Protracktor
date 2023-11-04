from expState import MachineState 
from filelogger import FileLogger
#this needs abstraction at baka imigrate na lang 'to into another module para mas abstracted
class Protracktor:
    def __init__(self):
        #self.__timer = timer // sa susunod na lang
        self.__fileLogger = FileLogger()
        self.__currentState = MachineState.HOME_MENU

    
    def machineState(self) -> int:
        return self.__currentState
    
    #user yes or no response handler may problem need ng executioner
    def __sequenceHandle(self, currentState : MachineState, 
                         prompt : str, yesResponse : MachineState, 
                         noResponse : MachineState) -> str:
        
        while self.__currentState == currentState:
            ask = input(prompt).lower()

            match ask:
                case "y":
                    self.__currentState = yesResponse
                    return self.__currentState
                case "n":
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
        
    def atAddingWorkLoad(self, taskGenerator : object, pseudoDB : object) -> MachineState:
        ask = input("Add work [y/n]: ").lower()

        match ask:
            case "y":
                taskGenerator.listDownTasks()
                pseudoDB.retrieveData(taskGenerator)
            case "n":
                self.__currentState = MachineState.WORK_SELECTION
            
        return self.__currentState
        
    
    def atWorkSelectionProcess(self, pseudoDB : object) -> MachineState:
        somethingToDo = pseudoDB.isNotEmpty()

        if somethingToDo:
            pseudoDB.displayPending()
            taskSelection = int(input("Select task from the index: "))
            currentTask = pseudoDB.getPendingList()[taskSelection]
            pseudoDB.setWIP(currentTask)
            self.__currentState = MachineState.WORKING
        else:
            print("NO WORK TO SELECT [NO PENDING TASK]\n")
            self.__currentState = MachineState.ADDING_WORKLOAD

        return self.__currentState
    
    def atWorkingProcess(self, pseudoDB : object) -> MachineState:
        somethingToDo = pseudoDB.isNotEmpty()

        if somethingToDo:
            print("Assume that there is a timer")
            self.__currentState = MachineState.CHECKING_PROGRESS
        else:
            print("Timer will not start ticking... [NO PENDING TASKS]\n")
            self.__currentState = MachineState.ADDING_WORKLOAD

        return self.__currentState
    
    def atCheckingProgress(self, pseudoDB : object) -> MachineState:
        somethingToDo = pseudoDB.isNotEmpty()

        if somethingToDo:
            currentTask = pseudoDB.getWIP()
            ask = input(f"Is {currentTask.getTaskName()} done [y/n]: ").lower()

            match ask:
                case "y":
                    currentTask.changeStatus()
                    self.__fileLogger.log(currentTask)
                    pseudoDB.markDone()
                    self.__currentState = MachineState.HOME_MENU

                case "n":    
                    self.__currentState = MachineState.RETRYING_TASK

        return self.__currentState
    
    #still untouched please fix
    def atRetryingState(self, pseudoDB : object) -> MachineState:
        currentTask = pseudoDB.getWIP()
        print(f"You didn\'t finished {currentTask.getTaskName()}\nFor how long you would like to try again?\n")

        currentTask.setEstimatedTimeTaken()

        self.__currentState = MachineState.WORKING

        return self.__currentState
    
    def atTermination(self, pseudoDB : object) -> MachineState:
        if pseudoDB.isNotEmpty():
            for each in pseudoDB.getPendingList():
                self.__fileLogger.log(each)
        
        return self.__currentState