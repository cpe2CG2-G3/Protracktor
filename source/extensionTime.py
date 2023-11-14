class ExtensionTime:
    def __init__(self):
        self.hour = 0
        self.minute = 0
        self.second = 0
    
    def setHour(self) -> int:
        settingHour = True
        while settingHour:
            try:
                self.hour = int(input("HH: "))
                assert 0 <= self.hour
            except ValueError as ve:
                print(f"Error: {ve}")
            except AssertionError:
                print("The input must be a positive number") 
            else:
                settingHour = False    
        return self.hour
    
    def setMinute(self) -> int:
        settingMinute = True
        while settingMinute:
            try:
                self.minute = int(input("mm: "))
                assert 0 <= self.minute < 60
            except ValueError as ve:
                print(f"Error: {ve}")
            except AssertionError:
                print("The input must be within 0 - 59 minutes")
            else:
                settingMinute = False
        return self.minute
        
    def setSecond(self) -> int:
        settingSecond = True
        
        while settingSecond:
            try:
                self.second = int(input("ss: "))
                if not(0 <= self.second < 60):
                    raise ValueError("Must be 0 - 60")
            except ValueError as ve:
                print(f"Error: {ve}")
            else:
                settingSecond = False 
        
        return self.second