class Storage:
    def __init__(self):
        self.__pending = []
        self.__done = []
    

    def getPending(self):
        return self.__pending
    
    def displayPending(self):
        print("Pending:")
        
        if len(self.__pending) > 0:
            for i, each in enumerate(self.__pending):
                print(f"({i + 1}) {each}")
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



