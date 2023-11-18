import os

class FileLogger:
    def log(self, currentTask : object) -> None:
        logsDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        logsFile =   os.path.join(logsDirectory, "progress.txt")
        try:
            with open(logsFile, "a") as log:
                log.write(f"{str(currentTask)}\n")
        except Exception as e:
            print(f"Error cannot write {e}")    