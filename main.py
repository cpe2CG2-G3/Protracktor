from interface import Interface
from storage import Storage
from task import Task
from timer import Timer 

if __name__ == "__main__":
    states = ("adding_workload", "working", "checking_progress")
    task = Task()
    timer = Timer()
    storage = Storage()
    menu = Interface(storage,timer)

    #dagdag ka ng termination sa states para mag terminate ang program
    #start ka na mag implement ng file handling
    while True:
        if menu.machineState() == states[0]:
            menu.atAddingWorkLoad()
        elif menu.machineState() == states[1]:
            menu.atWorkingProcess()
        elif menu.machineState() == states[2]:
            menu.atCheckingProgress()
            menu.resetStateTransition()
        
        