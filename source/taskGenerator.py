from task import Task

class TaskGenerator:
    def __init__(self):
        self.__tasks = []
    
    def listDownTasks(self) -> list:
        toDo = Task()
        toDo.setTaskName()
        toDo.setHour()
        toDo.setMinute()
        toDo.setSecond()

        self.__tasks.append(toDo)
    
    def popTask(self, index : int) -> list:
        self.__tasks.pop(index)
        return self.__tasks

    def getTasks(self) -> list:
        return self.__tasks