class Task:
    def __init__(self):
        self.__taskName = ""
        self.__timeTaken = ""
        self.__isDone = False
    
    #read only
    def getTaskName(self) -> str:
        return self.__taskName
    
    def getTimeTaken(self) -> str:
        return self.__timeTaken
    
    def getStatus(self) -> bool:
        return self.__isDone
    
    #write only
    def setTaskName(self) -> str:
        taskName = input("Task name: ")
        self.__taskName = taskName
        return self.__taskName
    
    def setTimeTaken(self) -> str:
        timeTaken = input("How long: ")
        self.__timeTaken = timeTaken
    
    def changeStatus(self) -> bool:
        self.__isDone = True
        return self.__isDone
    
    #misc
    def __str__(self) -> str:
        return f"Task: {self.__taskName}\nETA: {self.__timeTaken}\nDone?: {self.__isDone}"
    