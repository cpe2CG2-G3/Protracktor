from enum import Enum, auto

class MachineState(Enum):
    TERMINATED = auto()
    HOME_MENU = auto()
    ADDING_WORKLOAD = auto()
    WORK_SELECTION = auto()
    WORKING = auto()
    CHECKING_PROGRESS = auto()
    RETRYING_TASK = auto()
    ERROR = auto()