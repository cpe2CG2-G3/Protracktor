from abc import ABC, abstractmethod

class State(ABC):
    
    @abstractmethod
    def changeState(self, nextState):
        pass