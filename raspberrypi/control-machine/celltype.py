from enum import Enum

class CellType(Enum):
    WALL = "W"
    EMPTY = " "
    START = "S"
    END = "E"
    PATH = "P"