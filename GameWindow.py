# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import QtWidgets

from gamewindow_ui import Ui_GameWindow


class GameWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)
        self.ui = Ui_GameWindow()
        self.ui.setupUi(self)
        self.ui.actionHide.triggered.connect(self.hide_)
        self.ui.actionShow.triggered.connect(self.show_)

    def hide_(self):
        print('Switch')
        self.ui.ships_player_1.hide()
        self.ui.ships_player_2.hide()

    def show_(self):
        print('Show')
        self.ui.ships_player_1.show()
        self.ui.ships_player_2.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gameWindow = GameWindow()
    gameWindow.show()
    app.exec_()
