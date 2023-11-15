from  timeHandlerState import TimerState

class TaskHandler:
    def __init__(self, fileLogger, timer, pseudoDB):
        self.__timer = timer 
        self.__fileLogger = fileLogger
        self.__pseudoDB = pseudoDB

        self.__checkTime = {TimerState.NORMAL_COUNTDOWN : lambda: self.__timer.countDown(),
                            TimerState.EXTENSION_COUNTDOWN : lambda: self.__timer.countDown()}

    def addWork(self, taskGenerator : object, pseudoDB : object) -> None:
        taskGenerator.listDownTasks()
        pseudoDB.retrieveData(taskGenerator)
        
    
    def selectWork(self, pseudoDB : object):
        pseudoDB.displayPending()
        taskSelection = int(input("Select task from the index: "))
        currentTask = pseudoDB.readPendingList()[taskSelection]
        pseudoDB.setWIP(currentTask)
            
    
    def doCurrentTask(self):
        self.__checkTime[TimerState.NORMAL_COUNTDOWN]()
        print("Time's up!\n")

    def logWhenDone(self, pseudoDB : object):
        currentTask = pseudoDB.getWIP()   
        currentTask.changeStatus()
        self.__fileLogger.log(currentTask)
        pseudoDB.markDone()

    def logWhenNotDone(self, task : object):
        self.__fileLogger.log(task)
    
   
    def retryTask(self):
        currentTask = self.__pseudoDB.getWIP()
        print(f"You didn\'t finished {currentTask.getTaskName()}\nFor how long you would like to try again?\n")

        self.__timer.changeState(TimerState.EXTENSION_COUNTDOWN)
        self.__checkTime[TimerState.EXTENSION_COUNTDOWN]