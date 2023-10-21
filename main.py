from interface import Interface, storage
if __name__ == "__main__":
    menu = Interface()
    nothingToDo = len(storage.getPending()) == 0
    isAsking = True
    while isAsking:
        ask = input("load / work").lower()

        if ask == "load":
            while menu.atInputQueueProcess():
                menu.atInputQueue()
        elif ask == "work":
            if nothingToDo:
                print("You have nothing to do...")
            else:
                while menu.atCountdownProcess():
                    menu.countingDown()