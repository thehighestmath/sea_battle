# This Python file uses the following encoding: utf-8
import logging
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsBlurEffect

from gamewindow_ui import Ui_GameWindow


class GameWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)
        self.setStyleSheet('''QMainWindow{
        border-image: url(ship.jpg) 0 0 0 0 stretch stretch;
        }
        QLabel{
        color: #FFA500;
        font-weight: bold;
        }
        ''')

        self.ui.actionPreparePlayer_1.triggered.connect(self.prepare_player_1)
        self.ui.actionPreparePlayer_2.triggered.connect(self.prepare_player_2)
        self.ui.actionPlayer_1.triggered.connect(self.player_1)
        self.ui.actionPlayer_2.triggered.connect(self.player_2)

    def mousePressEvent(self, event):
        logging.debug("Main Mouse Press")
        super(GameWindow, self).mousePressEvent(event)

    def set_widgets_on_off(self, is_first: bool = True):
        self.ui.wigdet_player_1.setEnabled(is_first)
        self.ui.wigdet_player_2.setEnabled(not is_first)

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

    def player_1(self):
        logger = logging.getLogger(__name__)
        logger.debug('player_1')

        self.ui.label_player_1.setText('[Player 1]')
        self.ui.label_player_2.setText('Player 2')

        self.ui.ships_list_1.hide()
        self.ui.ships_list_2.hide()

        self.set_widgets_on_off(is_first=True)
        self.ui.wigdet_player_1.setGraphicsEffect(None)
        self.ui.wigdet_player_2.setGraphicsEffect(QGraphicsBlurEffect())

    def player_2(self):
        logger = logging.getLogger(__name__)
        logger.debug('player_2')

        self.ui.label_player_1.setText('Player 1')
        self.ui.label_player_2.setText('[Player 2]')

        self.ui.ships_list_1.hide()
        self.ui.ships_list_2.hide()

        self.set_widgets_on_off(is_first=False)
        self.ui.wigdet_player_1.setGraphicsEffect(QGraphicsBlurEffect())
        self.ui.wigdet_player_2.setGraphicsEffect(None)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app = QtWidgets.QApplication(sys.argv)
    gameWindow = GameWindow()
    gameWindow.show()
    app.exec_()
