from screenRefresher import clearScreen
from timeHandlerState import TimerState
from extensionTime import ExtensionTime
from pyfiglet import print_figlet, figlet_format
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
import time
class Timer:
    def __init__(self, pseudoDB):
        self.__conversion = {"minuteToSecond" : 60, "hourToSecond" : 3600 }
        self.__pseudoDB = pseudoDB
        self.__currentState = TimerState.NORMAL_COUNTDOWN
        self.__extension = ExtensionTime()
        self.__console = Console()
        self.__layout = Layout()

    def changeState(self, nextState) -> TimerState:
        self.__currentState = nextState

    def countDown(self) -> TimerState:
        workingBanner = figlet_format("WORKING PROCESS")
        self.__layout.split_column(Layout(name = "header"), Layout(name = "watch"))
    
        self.__layout["header"].update(Panel(f"[bold green3]{workingBanner}"))


      
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

                    timer = figlet_format(f"{hour:02}:{minute:02}:{second:02}")
                    self.__layout["watch"].update(Panel(f"[blink][bright_green]Work In Progress[/blink][/bright_green]: {currentTask.getTaskName()}\n\n[magenta3]{timer}".center(45, " ")))
                    self.__console.print(self.__layout)
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

            timer = figlet_format(f"{hour:02}:{minute:02}:{second:02}")
            self.__layout["body"]["mid"].update(f"""\t\t\t\t\t\t\t[blink][bright_green]Work In Progress[/blink][/bright_green]: {currentTask.getTaskName()}\n\n
                                                {timer}""")
            time.sleep(1)
            clearScreen()