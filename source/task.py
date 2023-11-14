from datetime import date

class Task:
    def __init__(self):
        self.__date = date.today()
        self.__taskName = ""
        self.__hourToTake = 0
        self.__minuteToTake = 0
        self.__secondToTake = 0
        self.__isDone = False
    
    #read only
    def getTaskName(self) -> str:
        return self.__taskName
    
    def __getDate(self) -> str:
        return self.__date.isoformat()
    
    def getHour(self) -> int:
        return self.__hourToTake
    
    def getMinute(self) -> int:
        return self.__minuteToTake
    
    def getSecond(self) -> int:
        return self.__secondToTake

    
    def getStatus(self) -> bool:
        return self.__isDone
    
    #write only
    def setTaskName(self) -> str:
        taskName = input("Task name: ")
        self.__taskName = taskName
        return self.__taskName
    
    def setHour(self) -> int:
        settingHour = True
        while settingHour:
            try:
                self.__hourToTake = int(input("HH: "))
                assert 0 <= self.__hourToTake
            except ValueError as ve:
                print(f"Error: {ve}")
            except AssertionError:
                print("The input must be a positive number") 
            else:
                settingHour = False    
        return self.__hourToTake
    
    def setMinute(self) -> int:
        settingMinute = True
        while settingMinute:
            try:
                self.__minuteToTake = int(input("mm: "))
                assert 0 <= self.__minuteToTake < 60
            except ValueError as ve:
                print(f"Error: {ve}")
            except AssertionError:
                print("The input must be within 0 - 59 minutes")
            else:
                settingMinute = False
        return self.__minuteToTake
        
    def setSecond(self) -> int:
        settingSecond = True
        
        while settingSecond:
            try:
                self.__secondToTake = int(input("ss: "))
                if not(0 <= self.__secondToTake < 60):
                    raise ValueError("Must be 0 - 60")
            except ValueError as ve:
                print(f"Error: {ve}")
            else:
                settingSecond = False 
        
        return self.__secondToTake

    def extendHour(self, extension):
        self.__hourToTake += extension
        return self.__hourToTake

    def extendMinute(self, extension):
        self.__minuteToTake += extension

        while self.__minuteToTake > 59:
            self.__minuteToTake -= 60
            self.__hourToTake += 1

        return self.__minuteToTake

    def extendSecond(self, extension):
        self.__secondToTake += extension

        while self.__secondToTake > 59:
            self.__secondToTake -= 60
            self.__minuteToTake += 1

        return self.__secondToTake
    
    def changeStatus(self) -> bool:
        self.__isDone = True
        return self.__isDone
    
    def __str__(self):
        timeFormat = f"{str(self.__hourToTake).zfill(2)}:{str(self.__minuteToTake).zfill(2)}:{str(self.__secondToTake).zfill(2)}"
        return f"Task: {self.__taskName}\nDate: {self.__getDate()}\nTime Taken: {timeFormat}\nDone: {self.__isDone}\n"