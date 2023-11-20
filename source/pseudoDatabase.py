from pseudoDBInterface import PseudoDBInterface

class PseudoDB(PseudoDBInterface):
    def __init__(self):
        self.__wip = []
        self.__pending = []
        self.__completed = []
    
    def sendData(self) -> list:
        return self.__pending
    
    def isNotEmpty(self) -> bool:
        return len(self.__pending) > 0

    def isCompletedNotEmpty(self) -> bool:
        return len(self.__completed) > 0

    def displayPending(self) -> str:
        display = ""        
        if self.isNotEmpty():
            for i, each in enumerate(self.__pending):
               display += f"Index: ({i})\n{each}\n"
        else:
           display = "[blink][red]No Pending..."

        return display
    
    def displayDone(self) -> None:
        display = ""        
        if self.isCompletedNotEmpty():
            for i, each in enumerate(self.__completed):
               display += f"Index: ({i})\n{each}\n"
            return display
        else:
           display = "[blink][blue]No Completed..."
        
        return display
    
    def readPendingList(self) -> list:
        return self.__pending

    def getCompletedList(self) -> list:
        return self.__completed
    
    def retrieveData(self, taskGenerator : object) -> list:
        pendingTask = taskGenerator.getTasks()
    
        for i, each in enumerate(pendingTask):
            self.__pending.append(each)
            taskGenerator.popTask(i)

        return self.__pending
    

    def setWIP(self, wip : object) -> object:
        self.__wip.append(wip)
        return self.__wip 

    def getWIP(self) -> list:
        return self.__wip[0]
    
    def clearWIP(self) -> list:
        self.__wip.clear()
        return self.__wip

    def markDone(self) -> list:
        self.getWIP().changeStatus()

        for each in self.__pending:
            if each == self.getWIP():
                self.__completed.append(each)
                self.__pending.remove(each)
        
        self.clearWIP()
        return self.__completed
    
    def clearPending(self) -> list:
        self.__pending.clear()
        return self.__pending
    
    def pop(self) -> list:
        self.__pending.pop()
        return self.__pending
