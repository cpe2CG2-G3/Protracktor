from task import Task
from storage import Storage

storage = Storage()

class Interface:
    def __init__(self) -> bool:
        self.__isAtInputQueue = False
        self.__isTimerRunning = False
    
    def atInputQueueProcess(self) -> bool:
        self.__isAtInputQueue = True
        return self.__isAtInputQueue
    
    def atInputQueue(self):
       self.__isTimerRunning = False
       
       isInputting = True
       while True:
            option = ("y", "n")

            #tuloy mo dito ayusin mo bakit ayaw mag terminate
            addTask = input("add task? [y/n]: ").lower()
          
            if addTask == option[1]:
                break
            elif addTask == option[0]:
                task = Task()
                task.setTaskName()
                task.setTimeTaken()

                storage.storePending(task)
            else:
                print("Wrong input")

    def atCountdownProcess(self) -> bool:
        self.__isTimerRunning = True
        return self.__isTimerRunning
    
    def countingDown(self):
        print("Timer counts down... Implementation bukas")