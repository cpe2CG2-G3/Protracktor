from enum import Enum,auto

class TimerState(Enum):
    NORMAL_COUNTDOWN = auto()
    HALT = auto()
    EXTENSION_COUNTDOWN = auto()