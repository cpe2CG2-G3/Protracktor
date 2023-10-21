class Storage:
    def __init__(self):
        self.__pending = []
        self.__done = []
        self.__wip = []
    
    def getPending(self):
        return self.__pending
    
    #may problem sa printing dito bakit may nag aappear na none
    def displayPending(self):
        print("Pending:")
        
        if len(self.__pending) > 0:
            for i, each in enumerate(self.__pending):
                print(f"({i}) {each}")
        else:
            print("Congrats!!! No pending")

    def displayDone(self):
        print("Done:") 
        for each in self.__done:
            print(each)
    
    def storePending(self, pendingTask : object) -> None:
        self.__pending.append(pendingTask)
    
    def markDone(self, doneTask : object):
        doneTask.changeStatus()
        self.__done.append(doneTask)
        
        for each in self.__pending:
            if each.getStatus() == True:
                self.__pending.remove(each)

    def setWIP(self, wip : object) -> list:
        return self.__wip.append(wip)

    def getWIP(self):
        return self.__wip
    
    def clearWIP(self):
        self.__wip.pop(0)
        return self.__wip
