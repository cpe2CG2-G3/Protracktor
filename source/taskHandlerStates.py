from enum import Enum, auto

class TaskHandler(Enum):
    ADD_WORKLOAD = auto()
    SELECT_WORK = auto()
    DO_TASK = auto()
    LOG_WHEN_DONE = auto()
    LOG_WHEN_NOT_DONE = auto()
    RETRYING = auto()
    REDO_WORKLOAD_ADDING = auto()
    REDO_WORK_SELECTION = auto()