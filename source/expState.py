from enum import Enum

class MachineState(Enum):
    TERMINATED = 0
    HOME_MENU = 1
    ADDING_WORKLOAD = 2
    WORK_SELECTION = 3
    WORKING = 4
    CHECKING_PROGRESS = 5
    RETRYING_TASK = 6
    ERROR = -1