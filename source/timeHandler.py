from screenRefresher import clearScreen
from timeHandlerState import TimerState
from extensionTime import ExtensionTime
from pyfiglet import figlet_format, print_figlet
from rich import print as rprint
import time
class Timer:
    def __init__(self, pseudoDB):
        self.__conversion = {"minuteToSecond" : 60, "hourToSecond" : 3600 }
        self.__pseudoDB = pseudoDB
        self.__currentState = TimerState.NORMAL_COUNTDOWN
        self.__extension = ExtensionTime()


    def changeState(self, nextState) -> TimerState:
        self.__currentState = nextState

    def countDown(self) -> TimerState:
        match self.__currentState:
            case TimerState.NORMAL_COUNTDOWN:
                currentTask = self.__pseudoDB.getWIP()

                hour = currentTask.getHour()
                minute = currentTask.getMinute()
                second = currentTask.getSecond()

                duration = (hour * self.__conversion["hourToSecond"]) + (minute * self.__conversion["minuteToSecond"]) + (second % self.__conversion["minuteToSecond"]) 
        
                for elapsed in range(duration, 0, -1):
                    hour = int(elapsed / self.__conversion["hourToSecond"])
                    minute = int((elapsed / self.__conversion["minuteToSecond"]) % self.__conversion["minuteToSecond"])
                    second = int(elapsed % self.__conversion["minuteToSecond"])

                    rprint("\t\t\t\t\t\t\t[green]Work In Progress: ",currentTask.getTaskName())
                    print_figlet(f"{hour:02}:{minute:02}:{second:02}")
                    time.sleep(1)
                    clearScreen()
            case TimerState.EXTENSION_COUNTDOWN:
                currentTask = self.__pseudoDB.getWIP()
                self.__countDownExtension()

                currentTask.extendHour(self.__extension.hour)
                currentTask.extendMinute(self.__extension.minute)
                currentTask.extendSecond(self.__extension.second)
                
                
        return self.__currentState

    def __countDownExtension(self):
        currentTask = self.__pseudoDB.getWIP()

        self.__extension.setHour()
        self.__extension.setMinute()
        self.__extension.setSecond()

        duration = (self.__extension.hour * self.__conversion["hourToSecond"]) + (self.__extension.minute * self.__conversion["minuteToSecond"]) + (self.__extension.second % self.__conversion["minuteToSecond"]) 

        for elapsed in range(duration, 0, -1):
            hour = int(elapsed / self.__conversion["hourToSecond"])
            minute = int((elapsed / self.__conversion["minuteToSecond"]) % self.__conversion["minuteToSecond"])
            second = int(elapsed % self.__conversion["minuteToSecond"])

            print(f"\t\t\t\t\t\t\tWork In Progress: {currentTask.getTaskName()}")
            print(f"\t\t\t\t\t\t\t{hour:02}:{minute:02}:{second:02}")
            time.sleep(0.0000000000000000005)
            clearScreen()
