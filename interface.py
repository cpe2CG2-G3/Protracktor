from task import Task
#please add a condition to make way for program termination
class Interface:
    def __init__(self, pseudoDB : object, timer : object):
        self.__isTerminated = False
        self.__isAtHomeMenu = True
        self.__isAtAddingWorkLoad = False
        self.__isWorking = False
        self.__isCheckingWorkProgress = False
        self.__timer = timer
        self.__pseudoDB = pseudoDB
        self.__currentState = ""
    
    #state checker
    def machineState(self) -> str:
        stateSignals = { (True, False, False, False, False) : "terminated",
                         (False, True, False, False, False) : "at_home_menu",
                         (False, False, True, False, False) : "adding_work",
                         (False, False, False, True, False) : "working",
                         (False, False, False, False, True) : "checking_progress"
                       }
        
        for signals, state in stateSignals.items():
            if signals == (self.__isTerminated, self.__isAtHomeMenu, self.__isAtAddingWorkLoad, self.__isWorking, self.__isCheckingWorkProgress):
                self.__currentState = state
                break
        return self.__currentState
    
    #state modifiers
    def resetStateTransition(self) -> bool:
        self.__isTerminated = False
        self.__isAtHomeMenu = True
        self.__isAtAddingWorkLoad = False
        self.__isWorking = False
        self.__isCheckingWorkProgress = False

        return self.__isAtHomeMenu

    def atHomeMenu(self):
        while self.__isAtHomeMenu == True:
            ask = input("wanna be productive [y/n]: ").lower()
            
            if ask == "n":
                self.__isAtHomeMenu = False
                self.__isTerminated = True
            elif ask == "y":
                self.__isAtAddingWorkLoad = True

        return self.__isAtHomeMenu 
        
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
        
  
    def atWorkingProcess(self) -> bool:
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