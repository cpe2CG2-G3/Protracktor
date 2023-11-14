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

    def displayPending(self):
        print("Pending:")
        
        if self.isNotEmpty():
            for i, each in enumerate(self.__pending):
                print(f"({i}) {each}")
        else:
            print("Congrats!!! No pending")

    def displayDone(self) -> None:
        print("Done:") 
        for each in self.__done:
            print(each)
    
    def getPendingList(self) -> list:
        return self.__pending

    def getCompletedList(self) -> list:
        return self.__completed
    
    def retrieveData(self, taskGenerator : object) -> list:
        pendingTask = taskGenerator.getTasks()
        index = 0

        for i, each in enumerate(pendingTask):
            self.__pending.append(each)
            taskGenerator.popTask(index)
            index += 1

        return self.__pending
    

    def setWIP(self, wip : object) -> object:
        self.__wip.append(wip)
        return self.__wip 

    def getWIP(self) -> list:
        return self.__wip[0]
    
    def __clearWIP(self) -> list:
        self.__wip.clear()
        return self.__wip

    def markDone(self) -> list:
        self.getWIP().changeStatus()

        for each in self.__pending:
            if each == self.getWIP():
                self.__completed.append(each)
                self.__pending.remove(each)
        
        self.__clearWIP()
        return self.__completed
