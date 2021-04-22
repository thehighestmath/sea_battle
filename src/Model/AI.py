from random import choice
from typing import Optional

from PyQt5.QtCore import QObject, QPoint

from Model.Controller import Controller
from Model.GameModel import GameModel
from Presenter.GameArea import Ship


class AI(QObject):
    def __init__(self, parent=None):
        super(AI, self).__init__(parent)
        self.controller: Optional[Controller] = None
        self.cells = [{'x': x, 'y': y} for y in range(0, 10) for x in range(0, 10)]
        self.model: Optional[GameModel] = None

    def f(self, ship: Ship):
        shipCells = []
        for i in range(ship.length):
            shipCells.append(ship.pos + (QPoint(0, i) if ship.vertical else QPoint(i, 0)))
        cells = []

        for cell in shipCells:
            arounds = [cell + QPoint(i, j) for i in range(-1, 2) for j in range(-1, 2)]
            for candidate in arounds:
                if 0 <= candidate.x() < 10 and 0 <= candidate.y() < 10:
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
        self.model.shipKilled.connect(self.f)

    def randomShot(self):
        cell = choice(self.cells)
        self.cells.remove(cell)
        self.controller.emitHit(**cell)


if __name__ == '__main__':
    pass
