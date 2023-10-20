class Task:
    def __init__(self):
        self.__taskName = input("Task: ")
        #ett stands for estimated time taken
        self.__ett = input("How long: ")
    
    def getTaskName(self) -> str:
        return self.__taskName
    

    def getTimeTaken(self) -> str:
        return self.__ett