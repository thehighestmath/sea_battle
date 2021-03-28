# This Python file uses the following encoding: utf-8
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
        self.setStyleSheet('''#centralWidget{
        border-image: url(ship.jpg) 0 0 0 0 stretch stretch;
        }
        QLabel{
        color: #FFA500;
        font-weight: bold;
        }
        ''')

        self.ui.actionPreparePlayer_1.triggered.connect(self.prepare_player_1)
        self.ui.actionPreparePlayer_2.triggered.connect(self.prepare_player_2)
        self.ui.actionPlayer_1.triggered.connect(self.move_player_1)
        self.ui.actionPlayer_2.triggered.connect(self.move_player_2)

        self.current_state: States = States.INIT
        self.current_player: int = -1

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Q:
            logging.debug(f'State: {self.current_state} | current_player: {self.current_player} | keep_player: False')
            self.state_machine_next(keep_player=False)
        if event.key() == QtCore.Qt.Key.Key_W:
            logging.debug(f'State: {self.current_state} | current_player: {self.current_player} | keep_player: True')
            self.state_machine_next(keep_player=True)
        event.accept()

    def mousePressEvent(self, event):
        # вдруг пригодится
        # logging.debug("Game window mouse press")
        super(GameWindow, self).mousePressEvent(event)

    def set_widgets_on_off(self, is_first: bool = True):
        self.ui.wigdet_player_1.setEnabled(is_first)
        self.ui.wigdet_player_2.setEnabled(not is_first)

    def hide_ships(self):
        self.ui.ships_list_1.hide()
        self.ui.ships_list_2.hide()

    def prepare_player_1(self):
        logger = logging.getLogger(__name__)
        logger.debug('prepare_player_1')

        self.ui.label_player_1.setText('[Prepare player 1]')
        self.ui.label_player_2.setText('Prepare player 2')

        self.set_widgets_on_off(is_first=True)

    def prepare_player_2(self):
        logger = logging.getLogger(__name__)
        logger.debug('prepare_player_2')
        self.ui.label_player_1.setText('Prepare player 1')
        self.ui.label_player_2.setText('[Prepare player 2]')

        self.set_widgets_on_off(is_first=False)

    def move_player_1(self):
        logger = logging.getLogger(__name__)
        logger.debug('player_1')

        self.ui.label_player_1.setText('[Player 1]')
        self.ui.label_player_2.setText('Player 2')

        self.hide_ships()

        self.set_widgets_on_off(is_first=True)
        self.ui.wigdet_player_1.setGraphicsEffect(None)
        self.ui.wigdet_player_2.setGraphicsEffect(QGraphicsBlurEffect())

    def move_player_2(self):
        logger = logging.getLogger(__name__)
        logger.debug('player_2')

        self.ui.label_player_1.setText('Player 1')
        self.ui.label_player_2.setText('[Player 2]')

        self.hide_ships()

        self.set_widgets_on_off(is_first=False)
        self.ui.wigdet_player_1.setGraphicsEffect(QGraphicsBlurEffect())
        self.ui.wigdet_player_2.setGraphicsEffect(None)

    def prepare_player(self, player: int):
        if player == 1:
            self.prepare_player_1()
        elif player == 2:
            self.prepare_player_2()
        else:
            raise Exception(f'Player {player} does not supported')

    def move_player(self, player: int):
        if player == 1:
            self.move_player_1()
        elif player == 2:
            self.move_player_2()
        else:
            raise Exception(f'Player {player} does not supported')

    def state_machine_next(self, keep_player: bool = False):
        if keep_player and self.current_state in [States.INIT, States.FIRST_PREPARE, States.SECOND_PREPARE]:
            raise Exception(f'Impossible use [keep_player=True] while state is {self.current_state}')

        if self.current_state == States.INIT:
            self.current_state = States.FIRST_PREPARE
            self.current_player = random.randint(1, 2)
            self.prepare_player(self.current_player)

        elif self.current_state == States.FIRST_PREPARE:
            self.current_state = States.SECOND_PREPARE
            self.current_player = 2 if self.current_player == 1 else 1
            self.prepare_player(self.current_player)

        elif self.current_state == States.SECOND_PREPARE:
            self.current_state = States.GAME
            self.current_player = random.randint(1, 2)
            self.move_player(self.current_player)

        elif self.current_state == States.GAME:
            if not keep_player:
                self.current_player = 2 if self.current_player == 1 else 1
            self.move_player(self.current_player)

        else:
            raise Exception(f'Unknown type: {self.current_state}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app = QtWidgets.QApplication(sys.argv)
    gameWindow = GameWindow()
    gameWindow.show()
    app.exec_()
