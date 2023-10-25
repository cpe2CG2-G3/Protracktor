class Timer:
    def __init__(self) -> int:
        self.__hour = 0
        self.__minute = 0
        self.__second = 0
    
    #leave as it is na lang 'to matagal to gawin kasi may math involved
    def countDown(self, currentTask):
        timeLimit = currentTask.getTimeTaken().split(":")
        print(f"Doing {currentTask.getTaskName()}\n")
        print("Assume that the timer algorithm is running\nTime\'s up\n")
