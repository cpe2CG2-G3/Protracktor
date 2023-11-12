from filelogger import FileLogger

class TaskHandler:
    def __init__(self):
        #self.__timer = timer // sa susunod na lang
        self.__fileLogger = FileLogger()


    def addWork(self, taskGenerator : object, pseudoDB : object) -> None:
        taskGenerator.listDownTasks()
        pseudoDB.retrieveData(taskGenerator)
        
    
    def selectWork(self, pseudoDB : object):
        pseudoDB.displayPending()
        taskSelection = int(input("Select task from the index: "))
        currentTask = pseudoDB.getPendingList()[taskSelection]
        pseudoDB.setWIP(currentTask)
            
    
    def doCurrentTask(self):
        print("Assume that there is a timer")

    
    def logWhenDone(self, pseudoDB : object):
        currentTask = pseudoDB.getWIP()   
        currentTask.changeStatus()
        self.__fileLogger.log(currentTask)
        pseudoDB.markDone()

    def logWhenNotDone(self, pseudoDB):
        currentTask = pseudoDB.getWIP()
        self.__fileLogger.log(currentTask)
    
   
    def retryTask(self, pseudoDB : object):
        currentTask = pseudoDB.getWIP()
        print(f"You didn\'t finished {currentTask.getTaskName()}\nFor how long you would like to try again?\n")

        currentTask.setEstimatedTimeTaken()

        return self.__currentState
    
    def terminate(self, pseudoDB : object):
        if pseudoDB.isNotEmpty():
           for each in pseudoDB.getPendingList():
               self.__fileLogger.log(each)
        return self.__currentState