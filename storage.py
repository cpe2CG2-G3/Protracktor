class Storage:
    def __init__(self):
        self.__pending = []
        self.__done = []
    
    def displayPending(self):
        print("Pending:")
        for each in self.__pending:
            print(each)

    def displayDone(self):
        print("Done:") 
        for each in self.__done:
            print(each)
    
    def storePending(self, pendingTask : object) -> None:
        self.__pending.append(pendingTask)
    
    def markDone(self, doneTask : object) -> None:
        self.__done.append(doneTask)

        for each in self.__pending:
            if each in self.__done:
                self.__pending.remove(each)
    
    def __str__(self):
        return f"{self.__pending}\n{self.__done}"


