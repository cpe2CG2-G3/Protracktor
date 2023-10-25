from task import Task
from states import MachineState 

class Interface:
    def __init__(self, pseudoDB : object, timer : object):
        self.__timer = timer
        self.__pseudoDB = pseudoDB
        self.__currentState = MachineState.HOME_MENU
        self.__receipt = open("progress.txt", "a")

    #state checker
    def machineState(self) -> int:
        return self.__currentState
    
    #state handlers
    
    def resetState(self) -> int:
        self.__currentState = MachineState.HOME_MENU
        return self.__currentState
    
    def atHomeMenu(self) -> int:
        while self.__currentState == MachineState.HOME_MENU:
            ask = input("wanna be productive [y/n]: ").lower()
            
            if ask == "n":
                self.__currentState = MachineState.TERMINATED
            elif ask == "y":
                self.__currentState = MachineState.ADDING_WORKLOAD

        return self.__currentState
        
    def atAddingWorkLoad(self) -> int:
        while self.__currentState == MachineState.ADDING_WORKLOAD:
            ask = input("add work [y/n]: ").lower()

            if ask == "n":
                self.__currentState = MachineState.WORK_SELECTION
            elif ask == "y":
                task = Task()
                task.setTaskName()
                task.setTimeTaken()
                self.__pseudoDB.storePending(task)

        return self.__currentState
        
    
    def atWorkSelectionProcess(self) -> int:
        somethingToDo = len(self.__pseudoDB.getPending()) > 0

        if somethingToDo:
            self.__pseudoDB.displayPending()
            taskSelection = input("Select task from the index: ")
            currentTask = self.__pseudoDB.getPending()[int(taskSelection)]
            self.__pseudoDB.setWIP(currentTask)
            self.__currentState = MachineState.WORKING
        else:
            print("NO WORK TO SELECT [NO PENDING TASK]\n")
            self.__currentState = MachineState.ADDING_WORKLOAD

        return self.__currentState
    
    def atWorkingProcess(self) -> int:
        somethingToDo = len(self.__pseudoDB.getPending()) > 0

        if somethingToDo:
            currentTask = self.__pseudoDB.getWIP()
            self.__timer.countDown(currentTask[0])
            self.__currentState = MachineState.CHECKING_PROGRESS
        else:
            print("Timer will not start ticking... [NO PENDING TASKS]\n")
            self.__currentState = MachineState.ADDING_WORKLOAD

        return self.__currentState
    
    def atCheckingProgress(self) -> bool:
        somethingToDo = len(self.__pseudoDB.getPending()) > 0

        if somethingToDo:
            currentTask = self.__pseudoDB.getWIP()
            ask = input(f"\nIs {currentTask[0].getTaskName()} done [y/n]: ").lower()
        
            if ask == "y":
                currentTask[0].changeStatus()
                self.__receipt.write(f"Task: {currentTask[0].getTaskName()}\n")
                self.__receipt.write(f"Time to take: {currentTask[0].getTimeTaken()}\n")
                self.__receipt.write(f"Done: {str(currentTask[0].getStatus())}\n\n")
                
                self.__pseudoDB.markDone(currentTask[0])

                self.__currentState = MachineState.HOME_MENU
                self.__pseudoDB.clearWIP()

            elif ask == "n":
                self.__receipt.write(f"Task: {currentTask[0].getTaskName()}\n")
                self.__receipt.write(f"Time to take: {currentTask[0].getTimeTaken()}\n")
                self.__receipt.write(f"Done: {str(currentTask[0].getStatus())}\n\n")

                
                self.__currentState = MachineState.RETRYING_TASK

        return self.__currentState
    
    def atRetryingState(self) -> int:
        currentTask = self.__pseudoDB.getWIP()
        print(f"You didn\'t finished {currentTask[0].getTaskName()}\nFor how long you would like to try again?\n")

        currentTask[0].setTimeTaken()

        self.__currentState = MachineState.WORKING

        return self.__currentState
    
    def cleanUp(self) -> None:
        self.__pseudoDB.clearPending()
    
    def closeFile(self) -> None:
        self.__receipt.close() 