class Key():
    value: str

    def __init__(self, value: str) -> None:
        if len(value) != 64:
            raise Exception
        self.value = value

def addKey(key1: Key, key2: Key) -> Key: 
    newvalue = int(key1.value, 16) + int(key2.value, 16)
    if len(hex(newvalue)[2:]) > 64:
        newvalue = newvalue - int("".ljust(64, "f"), 16) - 1
    return Key(hex(newvalue)[2:].zfill(64))

def isBetween(start: Key, end: Key, target: Key) -> bool:
    if start.value < end.value:
        return start.value < target.value <= end.value
    else: # start.value >= end.value
        return start.value < target.value or target.value <= end.value
