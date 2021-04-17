import copy
import logging
import unittest
from enum import IntEnum
from typing import List, Optional

from PyQt5.QtCore import QPoint, QObject, pyqtSignal
from PyQt5.QtWidgets import QGraphicsPixmapItem

from Presenter.GameArea import Rotation, ShipListItem, Ship


class State(IntEnum):
    FREE = 0
    OCCUPIED = 1
    HIT = 2
    KILLED = 3
    MISS = 4

    def isEndCell(self):
        return self in [State.FREE, State.MISS]

    def __repr__(self):
        return str(self.value)


class GameModel(QObject):
    shipKilled = pyqtSignal(Ship)

    def __init__(self, listOfShips: Optional[List[QGraphicsPixmapItem]] = None):
        super(GameModel, self).__init__()
        if listOfShips is None:
            listOfShips = []
        self.listOfShips: List[QGraphicsPixmapItem] = listOfShips
        self.__matrix = [[State.FREE for _ in range(10)] for __ in range(10)]

        for ship in self.listOfShips:
            r: Rotation = ship.data(0)
            shipItem: ShipListItem = ship.data(1)
            leftCorner: QPoint = ship.data(2)

            for i in range(shipItem.length):
                if r.isVertical():
                    self.setCell(leftCorner.x(), leftCorner.y() + 1, State.OCCUPIED)
                elif r.isHorizontal():
                    self.setCell(leftCorner.x() + 1, leftCorner.y(), State.OCCUPIED)
                else:
                    raise Exception('Unknown rotation')

    def getMatrix(self):
        return copy.deepcopy(self.__matrix)

    def setMatrix(self, matrix: List[List[int]]):
        # for unittest
        for i in range(10):
            for j in range(10):
                self.__matrix[i][j] = State(matrix[i][j])

    def getCell(self, x: int, y: int):
        logger = logging.getLogger(__name__)
        if not (0 <= x < 10 and 0 <= y < 10):
            logger.warning('Coords of get must be in range [0, 10)')
            # thing about it
            return State.FREE
        return self.__matrix[y][x]

    def setCell(self, x: int, y: int, state: State):
        logger = logging.getLogger(__name__)
        if not (0 <= x < 10 and 0 <= y < 10):
            logger.warning('Coords of set must be in range [0, 10)')
            return None
        self.__matrix[y][x] = state

    def hit(self, x: int, y: int) -> bool:
        """
        :param x: coord x
        :param y: coord y
        :return: true if keep current player else false
        """
        logger = logging.getLogger(__name__)

        if self.getCell(x, y) in [State.HIT, State.KILLED, State.MISS]:
            logger.warning('This cell is hit or killed earlier')
            return True

        if self.getCell(x, y) == State.FREE:
            self.setCell(x, y, State.MISS)
            logger.debug('Hit is missed')
            return False

        if self.getCell(x, y) == State.OCCUPIED:
            self.setCell(x, y, State.HIT)
            logger.debug('Hit is on aim')

            killed = False
            vertical = False
            if (
                    self.getCell(x, y + 1).isEndCell() and
                    self.getCell(x, y - 1).isEndCell() and
                    self.getCell(x - 1, y).isEndCell() and
                    self.getCell(x + 1, y).isEndCell()
            ):
                length = 1
                killed = True
            else:
                vertical = False
                tempKilled = True
                length = 1
                a = self.check(x, y, isAdd=True, isRow=True)
                if a > -1:
                    tempKilled &= True
                    length += a
                else:
                    tempKilled &= False
                a = self.check(x, y, isAdd=False, isRow=True)
                if a > -1:
                    tempKilled &= True
                    length += a
                else:
                    tempKilled &= False

                if length > 1:
                    killed = tempKilled

                if length == 1:
                    vertical = True
                    length = 1
                    a = self.check(x, y, isAdd=True, isRow=False)
                    if a > -1:
                        tempKilled &= True
                        length += a
                    else:
                        tempKilled &= False
                    a = self.check(x, y, isAdd=False, isRow=False)
                    if a > -1:
                        tempKilled &= True
                        length += a
                    else:
                        tempKilled &= False
                    if length > 1:
                        killed = tempKilled

            if killed:
                pos = self.findLeftShipCorner(x, y, vertical)
                self.hitAroundCells(pos, length, vertical)
                # TODO: need to check
                # self.shipKilled.emit(Ship(name='killed_ship', length=length, pos=pos, vertical=vertical))

            return True
        else:
            raise Exception(f'Unknown state: {self.getCell(x, y)}')

    def hitAroundCells(self, pos: QPoint, length: int, vertical: bool):
        if vertical:
            for i in range(pos.x() - 1, pos.x() + 2):
                for j in range(pos.y() - 1, pos.y() + length + 1):
                    self.setCell(i, j, State.MISS)
            for j in range(pos.y(), pos.y() + length):
                self.setCell(pos.x(), j, State.KILLED)
        else:
            for i in range(pos.x() - 1, pos.x() + length + 1):
                for j in range(pos.y() - 1, pos.y() + 2):
                    self.setCell(i, j, State.MISS)
            for i in range(pos.x(), pos.x() + length):
                self.setCell(i, pos.y(), State.KILLED)

    def findLeftShipCorner(self, x: int, y: int, isVertical: bool):
        if isVertical:
            for i in range(1, 4):
                cell = self.getCell(x, y - i)
                if cell.isEndCell():
                    return QPoint(x, y - i + 1)
        else:
            for i in range(1, 4):
                cell = self.getCell(x - i, y)
                if cell.isEndCell():
                    return QPoint(x - i + 1, y)
        raise Exception('Unexpected behaviour')

    def check(self, x: int, y: int, isAdd: bool, isRow: bool):
        length = 0
        for i in range(1, 4):
            if isAdd:
                if isRow:
                    cell = self.getCell(x + i, y)
                else:
                    cell = self.getCell(x, y + i)
            else:
                if isRow:
                    cell = self.getCell(x - i, y)
                else:
                    cell = self.getCell(x, y - i)

            if cell.isEndCell():
                return length
            if cell == State.OCCUPIED:
                return -1
            if cell == State.HIT:
                length += 1

        return length


class TestModel(unittest.TestCase):
    initField = [
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def testKillLongShip(self):
        model = GameModel()
        model.setMatrix(TestModel.initField)
        model.hit(3, 2)
        model.hit(1, 2)
        model.hit(0, 2)
        model.hit(2, 2)
        self.assertEqual(
            model.getMatrix(),
            [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
             [4, 4, 4, 4, 4, 1, 0, 1, 0, 1],
             [4, 3, 3, 3, 4, 1, 0, 1, 0, 0],
             [4, 4, 4, 4, 4, 1, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        )

    def testKeepPlayer(self):
        model = GameModel()
        model.setMatrix(TestModel.initField)
        self.assertEqual(model.hit(0, 0), True)
        self.assertEqual(model.hit(0, 0), True)
        self.assertEqual(model.hit(1, 1), False)
        self.assertEqual(model.hit(1, 1), True)
        self.assertEqual(model.hit(0, 9), True)
        # prev hot kill ship that's why (1, 9) was marked as hooted
        self.assertEqual(model.hit(1, 9), True)
        self.assertEqual(model.hit(3, 9), False)
        self.assertEqual(model.hit(3, 9), True)

    def testLongShip(self):
        model = GameModel()
        model.setMatrix(TestModel.initField)
        model.hit(0, 0)
        model.hit(2, 0)
        model.hit(3, 0)
        self.assertEqual(
            model.getMatrix(),
            [[2, 1, 2, 2, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
             [0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        )
        model = GameModel()
        model.setMatrix(TestModel.initField)
        model.hit(0, 0)
        model.hit(2, 0)
        model.hit(3, 0)
        model.hit(1, 0)
        self.assertEqual(
            model.getMatrix(),
            [[3, 3, 3, 3, 4, 0, 0, 0, 0, 0],
             [4, 4, 4, 4, 4, 1, 0, 1, 0, 1],
             [0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        )

    def testMissShot(self):
        model = GameModel()
        model.setMatrix(TestModel.initField)
        model.hit(1, 1)
        model.hit(9, 9)
        model.hit(8, 8)
        self.assertEqual(
            model.getMatrix(),
            [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
             [0, 4, 0, 0, 0, 1, 0, 1, 0, 1],
             [0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 4, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 4]]
        )

    def testHitInside(self):
        model = GameModel()
        model.setMatrix(TestModel.initField)
        model.hit(0, 7)
        model.hit(1, 7)
        self.assertEqual(
            model.getMatrix(),
            [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
             [0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [4, 4, 4, 1, 0, 0, 1, 1, 0, 0],
             [4, 3, 4, 0, 0, 0, 0, 0, 0, 0],
             [4, 4, 4, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        )

    def testHitOnBorders(self):
        model = GameModel()
        model.setMatrix(TestModel.initField)
        model.hit(0, 9)
        self.assertEqual(
            model.getMatrix(),
            [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
             [0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [4, 4, 0, 1, 0, 0, 0, 0, 0, 0],
             [3, 4, 0, 0, 0, 0, 0, 0, 0, 0]]
        )
        model = GameModel()
        model.setMatrix(TestModel.initField)
        model.hit(0, 5)
        self.assertEqual(
            model.getMatrix(),
            [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
             [0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             [4, 4, 1, 1, 0, 0, 0, 0, 0, 0],
             [3, 4, 0, 0, 0, 0, 0, 0, 0, 0],
             [4, 4, 0, 1, 0, 0, 1, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        )


if __name__ == '__main__':
    # model = GameModel()
    # model.setMatrix(TestModel.initField)
    # model.hit(1, 7)

    unittest.main()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
