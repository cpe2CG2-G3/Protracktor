from interface import Interface
from storage import Storage
from task import Task
from timer import Timer 
from enum import Enum


if __name__ == "__main__":
    task = Task()
    timer = Timer()
    storage = Storage()
    menu = Interface(storage,timer)

    states = ("terminated", "at_home_menu" ,"adding_workload", "working", "checking_progress")
    #dagdag ka ng termination sa states para mag terminate ang program
    #start ka na mag implement ng file handling
    while True:
        if menu.machineState() == states[0]:
            break
        elif menu.machineState() == states[1]:
            menu.atHomeMenu()
       