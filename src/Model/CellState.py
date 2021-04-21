from enum import IntEnum


class CellState(IntEnum):
    FREE = 0
    OCCUPIED = 1
    HIT = 2
    KILLED = 3
    MISS = 4

    def isEndCell(self):
        return self in [CellState.FREE, CellState.MISS]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)
