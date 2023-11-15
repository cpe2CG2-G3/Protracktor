from pseudoDBInterface import PseudoDBInterface
from rich.table import Table
from rich.console import Console
class PseudoDB(PseudoDBInterface):
    def __init__(self):
        self.__wip = []
        self.__pending = []
        self.__completed = []
        self.__table = Table()
        self.__table.add_column("Index", justify="center")
        self.__table.add_column("Task", justify="left")
        self.__console = Console()
    
    def sendData(self) -> list:
        return self.__pending
    
    def isNotEmpty(self) -> bool:
        return len(self.__pending) > 0

    #needs for fixing tomorrow
    def displayPending(self):        
        if self.isNotEmpty():
            self.__console.print("[bold red]Pending:\n".center(45))
            for i, each in enumerate(self.__pending):
                task_exists = any(row  == str(each) for row in self.__table.rows)
                if not task_exists:
                    self.__table.add_row(str(i), str(each))
            
            self.__console.print(self.__table)
        else:
            print("Congrats!!! No pending")

    def displayDone(self) -> None:
        print("Done:") 
        for each in self.__done:
            print(each)
    
    def readPendingList(self) -> list:
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
