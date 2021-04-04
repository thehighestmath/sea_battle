import logging
import random
import signal
import sys
from enum import Enum
from typing import Optional

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QGraphicsBlurEffect

from Presenter.GameArea import GameArea
from Presenter.gamewindow_ui import Ui_GameWindow


class States(Enum):
    INIT = 0
    FIRST_PREPARE = 1
    SECOND_PREPARE = 2
    GAME = 3


class GameWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)
        # self.ui.gameArea_1.shipPlaced.connect(self.foo)
        # self.ui.gameArea_2.shipPlaced.connect(self.foo)
        self.ui.finishSettingShips.clicked.connect(self.next)
        self.currentState: States = States.INIT
        self.currentPlayer: int = -1
        self.next()

    def foo(self, val):
        print(val)

    def mousePressEvent(self, event: QMouseEvent):
        logger = logging.getLogger(__name__)
        # вдруг пригодится
        # logging.debug("Game window mouse press")
        super(GameWindow, self).mousePressEvent(event)

    def setWidgetsOnOff(self, isFirst: bool = True):
        self.ui.wigdetPlayer_1.setEnabled(isFirst)
        self.ui.wigdetPlayer_2.setEnabled(not isFirst)

    def hideShipsAndButton(self):
        self.ui.gameArea_1.hideShipList()
        self.ui.gameArea_2.hideShipList()
        self.ui.gameArea_1.hideShips()
        self.ui.gameArea_2.hideShips()
        self.ui.buttonWidget.hide()

    def preparePlayer(self, player: int):
        if player == 1:
            self.setWidgetsOnOff(isFirst=True)
            self.ui.wigdetPlayer_2.hide()
            self.ui.wigdetPlayer_1.show()

        elif player == 2:
            self.setWidgetsOnOff(isFirst=False)
            self.ui.wigdetPlayer_1.hide()
            self.ui.wigdetPlayer_2.show()

        else:
            raise Exception(f'Player {player} does not supported')

    def movePlayer(self, player: int):
        self.ui.wigdetPlayer_1.show()
        self.ui.wigdetPlayer_2.show()
        self.hideShipsAndButton()
        if player == 1:
            isFirst = False
            effectWidget_1 = QGraphicsBlurEffect()
            effectWidget_2 = None
        elif player == 2:
            isFirst = True
            effectWidget_1 = None
            effectWidget_2 = QGraphicsBlurEffect()
        else:
            raise Exception(f'Player {player} does not supported')
        self.setWidgetsOnOff(isFirst=isFirst)
        self.ui.wigdetPlayer_1.setGraphicsEffect(effectWidget_1)
        self.ui.wigdetPlayer_2.setGraphicsEffect(effectWidget_2)

    def checkCountShips(self, player: int):
        gameArea: Optional[GameArea] = None
        if player == 1:
            gameArea = self.ui.gameArea_1

        elif player == 2:
            gameArea = self.ui.gameArea_2

        else:
            raise Exception(f'Player {player} does not supported')

        placedShipsCount = gameArea.placedShipsCount()

        if placedShipsCount != 10:
            self.ui.statusbar.showMessage(
                f'Расставляет корабли игрок {self.currentPlayer} | '
                f'Вы поставили {placedShipsCount} кораблей, осталось {10 - placedShipsCount} кораблей'
            )
            return False

        return True

    def next(self, keepPlayer: bool = False):
        if keepPlayer and self.currentState in [States.INIT, States.FIRST_PREPARE, States.SECOND_PREPARE]:
            raise Exception(f'Impossible use [keep_player=True] while state is {self.currentState}')

        if self.currentState == States.INIT:
            self.currentState = States.FIRST_PREPARE
            self.currentPlayer = random.randint(1, 2)
            self.preparePlayer(self.currentPlayer)
            self.ui.statusbar.showMessage(f'Расставляет корабли игрок {self.currentPlayer}')

        elif self.currentState == States.FIRST_PREPARE:
            if not self.checkCountShips(self.currentPlayer):
                return
            self.currentState = States.SECOND_PREPARE
            self.currentPlayer = 2 if self.currentPlayer == 1 else 1
            self.preparePlayer(self.currentPlayer)
            self.ui.statusbar.showMessage(f'Расставляет корабли игрок {self.currentPlayer}')

        elif self.currentState == States.SECOND_PREPARE:
            if not self.checkCountShips(self.currentPlayer):
                return
            self.currentState = States.GAME
            self.currentPlayer = random.randint(1, 2)
            self.movePlayer(self.currentPlayer)
            self.ui.statusbar.showMessage(f'Стреляет игрок {self.currentPlayer}')

        elif self.currentState == States.GAME:
            if not keepPlayer:
                self.currentPlayer = 2 if self.currentPlayer == 1 else 1
            self.movePlayer(self.currentPlayer)
            self.ui.statusbar.showMessage(f'Стреляет игрок {self.currentPlayer}')

        else:
            raise Exception(f'Unknown type: {self.currentState}')


if __name__ == '__main__':
    def sigint_handler(*args):
        QtWidgets.QApplication.quit()


    signal.signal(signal.SIGINT, sigint_handler)
    app = QtWidgets.QApplication(sys.argv)
    timer = QtCore.QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    gameWindow = GameWindow()
    gameWindow.show()
    sys.exit(app.exec_())
