import logging
import random
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsBlurEffect

from gamewindow_ui import Ui_GameWindow
from states import States


class GameWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)

        self.currentState: States = States.INIT
        self.currentPlayer: int = -1

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Q:
            logging.debug(f'State: {self.currentState} | currentPlayer: {self.currentPlayer} | keepPlayer: False')
            self.next(keepPlayer=False)
        if event.key() == QtCore.Qt.Key.Key_W:
            logging.debug(f'State: {self.currentState} | currentPlayer: {self.currentPlayer} | keepPlayer: True')
            self.next(keepPlayer=True)
        event.accept()

    def mousePressEvent(self, event):
        # вдруг пригодится
        # logging.debug("Game window mouse press")
        super(GameWindow, self).mousePressEvent(event)

    def setWidgetsOnOff(self, isFirst: bool = True):
        self.ui.wigdetPlayer_1.setEnabled(isFirst)
        self.ui.wigdetPlayer_2.setEnabled(not isFirst)

    def hideShips(self):
        self.ui.shipsList_1.hide()
        self.ui.shipsList_2.hide()

    def preparePlayer_1(self):
        logger = logging.getLogger(__name__)
        logger.debug('prepare_player_1')

        self.ui.labelPlayer_1.setText('[Prepare player 1]')
        self.ui.labelPlayer_2.setText('Prepare player 2')

        self.setWidgetsOnOff(isFirst=True)

    def preparePlayer_2(self):
        logger = logging.getLogger(__name__)
        logger.debug('prepare_player_2')
        self.ui.labelPlayer_1.setText('Prepare player 1')
        self.ui.labelPlayer_2.setText('[Prepare player 2]')

        self.setWidgetsOnOff(isFirst=False)

    def movePlayer_1(self):
        logger = logging.getLogger(__name__)
        logger.debug('player_1')

        self.ui.labelPlayer_1.setText('[Player 1]')
        self.ui.labelPlayer_2.setText('Player 2')

        self.hideShips()

        self.setWidgetsOnOff(isFirst=True)
        self.ui.wigdetPlayer_1.setGraphicsEffect(None)
        self.ui.wigdetPlayer_2.setGraphicsEffect(QGraphicsBlurEffect())

    def movePlayer_2(self):
        logger = logging.getLogger(__name__)
        logger.debug('player_2')

        self.ui.labelPlayer_1.setText('Player 1')
        self.ui.labelPlayer_2.setText('[Player 2]')

        self.hideShips()

        self.setWidgetsOnOff(isFirst=False)
        self.ui.wigdetPlayer_1.setGraphicsEffect(QGraphicsBlurEffect())
        self.ui.wigdetPlayer_2.setGraphicsEffect(None)

    def preparePlayer(self, player: int):
        if player == 1:
            self.preparePlayer_1()
        elif player == 2:
            self.preparePlayer_2()
        else:
            raise Exception(f'Player {player} does not supported')

    def movePlayer(self, player: int):
        if player == 1:
            self.movePlayer_1()
        elif player == 2:
            self.movePlayer_2()
        else:
            raise Exception(f'Player {player} does not supported')

    def next(self, keepPlayer: bool = False):
        if keepPlayer and self.currentState in [States.INIT, States.FIRST_PREPARE, States.SECOND_PREPARE]:
            raise Exception(f'Impossible use [keep_player=True] while state is {self.currentState}')

        if self.currentState == States.INIT:
            self.currentState = States.FIRST_PREPARE
            self.currentPlayer = random.randint(1, 2)
            self.preparePlayer(self.currentPlayer)

        elif self.currentState == States.FIRST_PREPARE:
            self.currentState = States.SECOND_PREPARE
            self.currentPlayer = 2 if self.currentPlayer == 1 else 1
            self.preparePlayer(self.currentPlayer)

        elif self.currentState == States.SECOND_PREPARE:
            self.currentState = States.GAME
            self.currentPlayer = random.randint(1, 2)
            self.movePlayer(self.currentPlayer)

        elif self.currentState == States.GAME:
            if not keepPlayer:
                self.currentPlayer = 2 if self.currentPlayer == 1 else 1
            self.movePlayer(self.currentPlayer)

        else:
            raise Exception(f'Unknown type: {self.currentState}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app = QtWidgets.QApplication(sys.argv)
    gameWindow = GameWindow()
    gameWindow.show()
    app.exec_()
