from collections import deque
from random import choice
from typing import Optional, List

from PyQt5.QtCore import QObject, QPoint

from Model.Controller import Controller
from Model.Enums import CellState, GameLevel
from Model.GameModel import GameModel
from Presenter.GameArea import Ship


class AI(QObject):
    SIZE = 10
    
    def __init__(self, parent=None):
        super(AI, self).__init__(parent)
        self.controller: Optional[Controller] = None
        self.cells = [{'x': x, 'y': y} for y in range(0, AI.SIZE) for x in range(0, AI.SIZE)]
        self.model: Optional[GameModel] = None
        self.killedCells = deque()
        self.weight: Optional[List[List[int]]] = None

        self.countMisses = 1

        self.enemyShips = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

    def removeCells(self, ship: Ship):
        self.enemyShips.remove(ship.length)
        shipCells = []
        for i in range(ship.length):
            shipCells.append(ship.pos + (QPoint(0, i) if ship.vertical else QPoint(i, 0)))

        cells = []
        for cell in shipCells:
            arounds = [cell + QPoint(i, j) for i in range(-1, 2) for j in range(-1, 2)]
            for candidate in arounds:
                if 0 <= candidate.x() < AI.SIZE and 0 <= candidate.y() < AI.SIZE:
                    if candidate not in cells:
                        cells.append(candidate)

        for cell in cells:
            if cell not in shipCells:
                dCell = {'x': cell.x(), 'y': cell.y()}
                if dCell in self.cells:
                    self.cells.remove(dCell)

    def setController(self, controller: Controller):
        self.controller = controller
        self.controller.onBot()

    def setModel(self, model):
        if self.model:
            self.model.shipKilled.disconnect()
        self.model = model
        self.model.shipKilled.connect(self.removeCells)

    def recalculateWeightMap(self, gameLevel):
        self.weight = [[1 for _ in range(AI.SIZE)] for _ in range(AI.SIZE)]
        if self.countMisses % gameLevel == 0:
            xOccupied, yOccupied = self.getNextOccupiedCell()
            if xOccupied is not None and yOccupied is not None:
                self.weight[xOccupied][yOccupied] *= 40
                self.countMisses += 1
        for x in range(AI.SIZE):
            for y in range(AI.SIZE):
                if self.model.getCell(x, y) in [CellState.MISS, CellState.KILLED, CellState.HIT]:
                    self.weight[x][y] = 0
                if self.model.getCell(x, y) == CellState.HIT:
                    if x - 1 >= 0:
                        if y - 1 >= 0:
                            self.weight[x - 1][y - 1] = 0
                        self.weight[x - 1][y] *= 50
                        if y + 1 < AI.SIZE:
                            self.weight[x - 1][y + 1] = 0
                    if y - 1 >= 0:
                        self.weight[x][y - 1] *= 50
                    if y + 1 < AI.SIZE:
                        self.weight[x][y + 1] *= 50
                    if x + 1 < AI.SIZE:
                        if y - 1 >= 0:
                            self.weight[x + 1][y - 1] = 0
                        self.weight[x + 1][y] *= 50
                        if y + 1 < AI.SIZE:
                            self.weight[x + 1][y + 1] = 0

        # TO_THINK: Вроде как надо, но в этом случае сложность алгоритма O(n^4) ну её нахер

        # for shipSize in self.enemyShips:
        #     ship = Ship('ship', shipSize, QPoint(0, 0), False)
        #     # вот тут бегаем по всем клеткам поля
        #     for x in range(AI.SIZE):
        #         for y in range(AI.SIZE):
        #             ship.pos = QPoint(x, y)
        #             if (
        #                     self.model.getCell(x, y) in [CellState.MISS, CellState.KILLED, CellState.HIT]
        #                     or self.weight[x][y] == 0
        #             ):
        #                 self.weight[x][y] = 0
        #                 continue
        #             # вот здесь ворочаем корабль и проверяем помещается ли он
        #             for rotation in range(2):
        #                 ship.vertical = bool(rotation)
        #                 if self.checkShipFits(ship, self.model.getMatrix()):
        #                     self.weight[x][y] += 1

    def checkShipFits(self, ship: Ship, field: List[List[CellState]]) -> bool:
        pos = ship.pos
        x = pos.x()
        y = pos.y()
        length = ship.length
        if ship.vertical:
            height = length
            width = 1
        else:
            width = length
            height = 1

        if x + height - 1 >= AI.SIZE or x < 0 or y + width - 1 >= AI.SIZE or y < 0:
            return False

        for pX in range(x, x + height):
            for pY in range(y, y + width):
                if field[pX][pY] == CellState.MISS:
                    return False

        for pX in range(x - 1, x + height + 1):
            for pY in range(y - 1, y + width + 1):
                if pX < 0 or pX >= len(field) or pY < 0 or pY >= len(field):
                    continue
                if field[pX][pY] in [CellState.OCCUPIED, CellState.KILLED]:
                    return False

        return True

    def getMaxWeightCells(self):
        weights = {}
        maxWeight = 0
        for x in range(AI.SIZE):
            for y in range(AI.SIZE):
                if self.weight[x][y] > maxWeight:
                    maxWeight = self.weight[x][y]
                weights.setdefault(self.weight[x][y], []).append((x, y))

        return weights[maxWeight]

    def getNextOccupiedCell(self):
        for x in range(AI.SIZE):
            for y in range(AI.SIZE):
                if self.model.getCell(x, y) == CellState.OCCUPIED:
                    return x, y
        return None, None

    def makeShot(self, gameLevel=GameLevel.HARD):
        self.recalculateWeightMap(gameLevel)
        x, y = choice(self.getMaxWeightCells())
        cell = {'x': x, 'y': y}
        if self.model.getCell(**cell) == CellState.FREE:
            self.countMisses += 1
        self.controller.emitHit(**cell)


if __name__ == '__main__':
    pass
