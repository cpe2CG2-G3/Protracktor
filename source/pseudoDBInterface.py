from abc import ABC, abstractmethod

class PseudoDBInterface(ABC):
    @abstractmethod
    def retrieveData(self, taskGenerator : object) -> list:
        pass
    
    @abstractmethod
    def sendData(self) -> list:
        pass