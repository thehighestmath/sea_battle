import logging
import os
import random
import signal
import sys
from typing import Optional

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QGraphicsBlurEffect

# inner project imports
import Environment
from Model.AI import AI
from Model.Emuns import GameState, GameMode
from Model.GameModel import GameModel
from Presenter.GameArea import GameArea
from Presenter.ui_gamewindow import Ui_GameWindow

DEBUG = False


class GameWindow(QtWidgets.QWidget):
    gameOverSignal = pyqtSignal(str)
    toMenuSignal = pyqtSignal()

    def __init__(self, parent=None, gameMode=None):
        super(GameWindow, self).__init__(parent)
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)
        self.gameMode = gameMode

        resourcePath = Environment.Resources.path()
        imagePath = os.path.join(resourcePath, "img", "miscellaneous", "logout.png")
        icon = QIcon(QPixmap(imagePath))
        self.ui.menu.setIcon(icon)
        self.ui.menu.clicked.connect(lambda _: self.toMenuSignal.emit())
        # self.ui.menu.setIconSize()

        self.ui.gameArea_1.controller.hit.connect(self.makeShot)
        self.ui.gameArea_2.controller.hit.connect(self.makeShot)
        if gameMode == GameMode.PVE:
            self.ai: Optional[AI] = AI()
            self.ai.setController(self.ui.gameArea_1.controller)
        else:
            self.ai: Optional[AI] = None
        self.ui.finishSettingShips.clicked.connect(self.next)
        self.ui.shuffleShips.clicked.connect(self.shuffleShips)
        self.currentState: GameState = GameState.INIT
        self.currentPlayer: int = -1
        self.next()
        self.model_1: Optional[GameModel] = None
        self.model_2: Optional[GameModel] = None
        self.gameOverSignal.connect(self.gameOverDummy)

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
        logger = logging.getLogger(__name__)
        logger.debug(f"shot at point ({x}, {y})")
        if self.currentState == GameState.GAME:
            if self.currentPlayer == 2 and controller == self.ui.gameArea_1.controller:
                isKeep, cellType = self.model_1.hit(x, y)
                controller.accept(cellType)
                if self.model_1.isOver():
                    self.gameOver()
                else:
                    self.next(isKeep)
            elif self.currentPlayer == 1 and controller == self.ui.gameArea_2.controller:
                isKeep, cellType = self.model_2.hit(x, y)
                controller.accept(cellType)
                if self.model_2.isOver():
                    self.gameOver()
                else:
                    self.next(isKeep)
            else:
                controller.decline()
        else:
            controller.decline()

    def gameOver(self):
        logger = logging.getLogger(__name__)
        logger.debug(f"Игра окончена. Выиграл игрок {self.currentPlayer}")
        self.currentState = GameState.GAME_OVER
        self.gameOverSignal.emit(f'Player {self.currentPlayer}')

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
        if not DEBUG:
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
            if self.gameMode == GameMode.PVE:
                self.ui.labelPlayer_2.setText('Bot')
                self.shuffleShips()
                self.next()
        else:
            raise Exception(f'Player {player} does not supported')

    def movePlayer(self, player: int):
        self.ui.wigdetPlayer_1.show()
        self.ui.wigdetPlayer_2.show()
        if player == 1:
            isFirst = False
            if self.gameMode == GameMode.PVP:
                effectWidget_1 = QGraphicsBlurEffect()
                effectWidget_2 = None
        elif player == 2:
            isFirst = True
            if self.gameMode == GameMode.PVP:
                effectWidget_1 = None
                effectWidget_2 = QGraphicsBlurEffect()
            if self.gameMode == GameMode.PVE:
                QTimer.singleShot(500, self.ai.makeShot)
                isFirst = False
        else:
            raise Exception(f'Player {player} does not supported')
        self.setWidgetsOnOff(isFirst=isFirst)
        if self.gameMode == GameMode.PVP:
            self.ui.wigdetPlayer_1.setGraphicsEffect(effectWidget_1)
            self.ui.wigdetPlayer_2.setGraphicsEffect(effectWidget_2)

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
            if self.gameMode == GameMode.PVE:
                self.ai.setModel(self.model_1)
        elif player == 2:
            self.model_2 = GameModel(player, gameArea.getPlacedShips())
            gameArea.serviceModel(self.model_2)
        else:
            raise Exception(f'Player {player} does not supported')
        return True

    def initCurrentPlayer(self):
        if self.gameMode == GameMode.PVP:
            self.currentPlayer = random.randint(1, 2)
        elif self.gameMode == GameMode.PVE:
            self.currentPlayer = 1
        else:
            raise Exception(f'Unknown type of game mode {self.gameMode}')

    def next(self, keepPlayer: bool = False):
        if keepPlayer and self.currentState in [GameState.INIT, GameState.FIRST_PREPARE, GameState.SECOND_PREPARE]:
            raise Exception(f'Impossible use [keep_player=True] while state is {self.currentState}')

        if self.currentState == GameState.INIT:
            self.currentState = GameState.FIRST_PREPARE
            self.initCurrentPlayer()
            self.preparePlayer(self.currentPlayer)

        elif self.currentState == GameState.FIRST_PREPARE:
            if not self.checkCountShips(self.currentPlayer):
                return
            self.currentState = GameState.SECOND_PREPARE
            self.currentPlayer = 2 if self.currentPlayer == 1 else 1
            self.preparePlayer(self.currentPlayer)

        elif self.currentState == GameState.SECOND_PREPARE:
            if not self.checkCountShips(self.currentPlayer):
                return
            self.ui.statusbar.showMessage("")
            self.currentState = GameState.GAME
            self.initCurrentPlayer()
            self.hideShipsAndButton()
            self.movePlayer(self.currentPlayer)

        elif self.currentState == GameState.GAME:
            if not keepPlayer:
                self.currentPlayer = 2 if self.currentPlayer == 1 else 1
            self.movePlayer(self.currentPlayer)

        else:
            raise Exception(f'Unknown type: {self.currentState}')

    def gameOverDummy(self, player):
        self.ui.statusbar.showMessage(f'Выиграл {player}')


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
