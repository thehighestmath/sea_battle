from enum import IntEnum


class DisplayedWidget(IntEnum):
    MENU = 0
    GAME = 1


class GameState(IntEnum):
    INIT = 0
    FIRST_PREPARE = 1
    SECOND_PREPARE = 2
    GAME = 3
    GAME_OVER = 4


class GameMode(IntEnum):
    PVP = 0
    PVE = 1


class AIMode(IntEnum):
    EASY = 0
    MIDDLE = 1
    HARD = 2


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


class GameLevel(IntEnum):
    """
    every N turns AI will found you occupied cell
    """
    EASY = 20
    MEDIUM = 10
    HARD = 3

