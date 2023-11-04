from enum import Enum

class TimerState(Enum):
    PAUSED = 0
    COUNTING_DOWN = 1
    ERROR = -1