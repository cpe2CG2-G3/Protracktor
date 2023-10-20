class Storage:
    def __init__(self):
        self.__pending = []
        self.__done = []
    
    def getPending(self):
        return self.__pending
    
    def getDone(self):
        return self.__done
    
    def storePending(self, pendingTask : object) -> None:
        self.__pending.append(pendingTask)
    
    def markDone(self, doneTask : object) -> None:
        self.__done.append(doneTask)

        for each in self.__pending:
            if each in self.__done:
                self.__pending.remove(each)
    


