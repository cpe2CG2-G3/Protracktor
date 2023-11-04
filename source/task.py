from datetime import date

class Task:
    def __init__(self):
        self.__date = date.today()
        self.__taskName = ""
        self.__estimatedTimeTaken = ""
        self.__actualTimeTaken = "Assumed"
        self.__isDone = False
        self.__wip = False
    
    #read only
    def getTaskName(self) -> str:
        return self.__taskName
    
    def __getDate(self) -> str:
        return self.__date.isoformat()
    def getEstimatedTimeTaken(self) -> str:
        return self.__estimatedTimeTaken
    
    def getActualTimeTaken(self) -> str:
        return self.__actualTimeTaken
    
    def getStatus(self) -> bool:
        return self.__isDone
    
    #write only
    def setTaskName(self) -> str:
        taskName = input("Task name: ")
        self.__taskName = taskName
        return self.__taskName
    
    def setEstimatedTimeTaken(self) -> str:
        estimatedTimeTaken = input("How long: ")
        self.__estimatedTimeTaken = estimatedTimeTaken
    
    def changeStatus(self) -> bool:
        self.__isDone = True
        return self.__isDone
    
    def currentlyWorking(self) -> bool:
        self.__wip = True
        return self.__wip 

    def __str__(self):
        return f"Task: {self.__taskName}\nDate: {self.__getDate()}\nEstimated Time Taken: {self.__estimatedTimeTaken}\nActual Time Taken: {self.__actualTimeTaken}\nDone: {self.__isDone}\n"