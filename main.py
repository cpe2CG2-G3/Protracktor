from task import Task
from storage import Storage

if __name__ == "__main__":
    taskOne = Task()
    storage = Storage()

    storage.storePending(taskOne)
    storage.displayPending()
    storage.markDone(taskOne)
    #storage.displayDone()
    storage.displayPending()