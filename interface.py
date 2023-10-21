from task import Task
#please add a condition to make way for program termination
class Interface:
    def __init__(self, pseudoDB : object, timer : object):
        self.__isAtAddingWorkLoad = True
        self.__isWorking = False
        self.__isCheckingWorkProgress = False
        self.__timer = timer
        self.__pseudoDB = pseudoDB
        self.__currentState = ""
    
    #state checker
    def machineState(self) -> str:
        
        if self.__isAtAddingWorkLoad == True and self.__isWorking == False and self.__isCheckingWorkProgress == False:
            self.__currentState = "adding_workload"
        elif self.__isWorking == True and self.__isAtAddingWorkLoad == False and self.__isCheckingWorkProgress == False:
            self.__currentState = "working"
        elif self.__isCheckingWorkProgress == True and self.__isAtAddingWorkLoad == False and self.__isWorking == False:
            self.__currentState = "checking_progress"
        
        return self.__currentState
    
    #state modifiers
    def resetStateTransition(self) -> str:
        self.__currentState = "adding_workload"
        self.__isAtAddingWorkLoad = True
        self.__isWorking = False
        self.__isCheckingWorkProgress = False

        return self.__currentState

    def atAddingWorkLoad(self) -> bool:
        while self.__isAtAddingWorkLoad == True:
            ask = input("add work [y/n]: ").lower()

            if ask == "n":
                self.__isAtAddingWorkLoad = False
                self.__isWorking = True
            elif ask == "y":
                task = Task()
                task.setTaskName()
                task.setTimeTaken()
                self.__pseudoDB.storePending(task)

        return self.__isAtAddingWorkLoad 
        
  
    def atWorkingProcess(self) -> str:
        somethingToDo = len(self.__pseudoDB.getPending()) > 0

        if somethingToDo:
            print(f"{self.__pseudoDB.displayPending()}")
            taskSelection = input("Select task from the index: ")
            currentTask = self.__pseudoDB.getPending()[int(taskSelection)]
            self.__pseudoDB.setWIP(currentTask)
            self.__timer.countDown(currentTask)

        self.__isWorking = False 
        self.__isCheckingWorkProgress = True
        return self.__isWorking
    
    def atCheckingProgress(self) -> bool:
        somethingToDo = len(self.__pseudoDB.getPending()) > 0

        if somethingToDo:
            currentTask = self.__pseudoDB.getWIP()
            ask = input(f"\nIs {currentTask[0]} done: ")
        
            if ask == "y":
                currentTask[0].changeStatus()
                self.__pseudoDB.markDone(currentTask[0])
                print(self.__pseudoDB.displayDone())
                self.__pseudoDB.clearWIP()
                self.__isCheckingWorkProgress = False

        self.__isAtAddingWorkLoad = True
        
        return self.__isCheckingWorkProgress 