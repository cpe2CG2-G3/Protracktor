from rich.console import Console

class ExtensionTime:
    def __init__(self):
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.console = Console()

    def setHour(self) -> int:
        settingHour = True
        while settingHour:
            try:
                self.hour = int(input("Type and Enter the hour/s to extend [0 - 8 hour/s only]: "))
                assert 0 <= self.hour <= 8
            except ValueError as ve:
                self.console.print(f"[bright_red]Error: {ve}")
            except AssertionError:
                self.console.print("[bright_red]Error: Invalid Time") 
            else:
                settingHour = False    
        return self.hour
    
    def setMinute(self) -> int:
        settingMinute = True
        while settingMinute:
            try:
                self.minute = int(input("Type and Enter the minute/s to extend [0 - 59 minute/s only]: "))
                assert 0 <= self.minute < 60
            except ValueError as ve:
                self.console.print(f"[bright_red]Error: {ve}")
            except AssertionError:
                self.console.print("[bright_red]Invalid TIme")
            else:
                settingMinute = False
        return self.minute
        
    def setSecond(self) -> int:
        settingSecond = True
        
        while settingSecond:
            try:
                self.second = int(input("Type and Enter the second/s to extend [0 - 59 seconds only]: "))
                assert 0 <= self.second < 60
                if self.hour == 0 and self.minute == 0 and self.second == 0:
                    raise ValueError("Impossible to Track")
            except ValueError as ve:
                self.console.print(f"[bright_red]Error: {ve}")
            except AssertionError:
                self.console.print("[bright_red]Invalid Time")
            else:
                settingSecond = False 
        
        return self.second