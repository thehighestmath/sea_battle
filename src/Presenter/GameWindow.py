import logging
import random
import signal
import sys
from enum import Enum
from typing import Optional

import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QGraphicsBlurEffect
from PyQt5.QtWidgets import QStackedWidget

from Model.GameModel import GameModel
from Presenter.GameArea import GameArea
from Presenter.ui_gamewindow import Ui_GameWindow


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
        self.ui.gameArea_1.controller.hit.connect(self.makeShot)
        self.ui.gameArea_2.controller.hit.connect(self.makeShot)
        self.ui.finishSettingShips.clicked.connect(self.next)
        self.ui.shuffleShips.clicked.connect(self.shuffleShips)
        self.currentState: States = States.INIT
        self.currentPlayer: int = -1
        self.next()
        self.model_1: Optional[GameModel] = None
        self.model_2: Optional[GameModel] = None

        self.ui.buttonMyField.pressed.connect(self.myFieldPressed)
        self.ui.buttonMyField.released.connect(self.myFieldReleased)


    def shuffleShips(self):
        gameArea: Optional[GameArea] = None
        if self.currentPlayer == 1:
            gameArea = self.ui.gameArea_1

        elif self.currentPlayer == 2:
            gameArea = self.ui.gameArea_2

        else:
            raise Exception(f'Player {player} does not supported')

        gameArea.shuffleShips()

    def makeShot(self, controller, x, y):
        log = logging.getLogger(__name__)
        log.debug(f"{x}, {y}")
        if self.currentState == States.GAME:
            if self.currentPlayer == 2 and controller == self.ui.gameArea_1.controller:
                isKeep, cellType = self.model_1.hit(x, y)
                controller.accept(cellType)
                self.next(isKeep)
                self.ui.statusbar.showMessage(f'Стреляет игрок {self.currentPlayer} | Prev hot - {cellType.name}')
                return
            elif self.currentPlayer == 1 and controller == self.ui.gameArea_2.controller:
                isKeep, cellType = self.model_2.hit(x, y)
                controller.accept(cellType)
                self.next(isKeep)
                self.ui.statusbar.showMessage(f'Стреляет игрок {self.currentPlayer} | Prev hot - {cellType.name}')
                return
        controller.decline()


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

    def showPlayer(self, player, label):
        self.ui.stackedWidget.setCurrentIndex(player - 1)
        self.ui.labelPlayer.setText(label)

    def myFieldPressed(self):
        self.showPlayer(player=self.currentPlayer, label="Your field")

    def myFieldReleased(self):
        if self.currentPlayer == 1:
            self.showPlayer(player=2, label=f"Player {self.currentPlayer} attacks")
        elif self.currentPlayer == 2:
            self.showPlayer(player=1, label=f"Player {self.currentPlayer} attacks")
        else:
            raise Exception(f'Player {self.currentPlayer} does not supported')

    def preparePlayer(self, player: int):
        self.showPlayer(player, f"Prepares player {player}")
        if player not in [1, 2]:
            raise Exception(f'Player {player} does not supported')

    def movePlayer(self):
        self.ui.buttonMyField.setEnabled(True)
        self.myFieldReleased()

    def checkCountShips(self, player: int):
        gameArea: Optional[GameArea] = None
        model: Optional[GameModel] = None
        if player == 1:
            model = self.model_1
            gameArea = self.ui.gameArea_1

        elif player == 2:
            model = self.model_2
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

        if player == 1:
            self.model_1 = GameModel(player, gameArea.getPlacedShips())
            gameArea.serviceModel(self.model_1)
        elif player == 2:
            self.model_2 = GameModel(player, gameArea.getPlacedShips())
            gameArea.serviceModel(self.model_2)
        else:
            raise Exception(f'Player {player} does not supported')
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
            self.hideShipsAndButton()
            self.movePlayer()
            self.ui.statusbar.showMessage(f'Стреляет игрок {self.currentPlayer}')

        elif self.currentState == States.GAME:
            self.ui.stackedWidget.currentWidget().setEnabled(False)
            if not keepPlayer:
                self.currentPlayer = 2 if self.currentPlayer == 1 else 1
                QTimer.singleShot(500, Qt.PreciseTimer, self.movePlayer)
            self.ui.stackedWidget.currentWidget().setEnabled(True)
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
