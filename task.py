class Task:
    def __init__(self):
        self.__taskName = input("Task: ")
        #ett stands for estimated time taken
        self.__ett = input("How long: ")
    
    def getTaskName(self) -> str:
        return self.__taskName
    
    def getTimeTaken(self) -> str:
        return self.__ett
    
    def __str__(self) -> str:
        return f"Task: {self.__taskName}\nETA: {self.__ett}"