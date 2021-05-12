import sys
from typing import Optional

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from Model.Enums import GameMode
from OffGame.UI_PlayerNames import UI_PlayerNames


class PlayerNamesWidget(QtWidgets.QWidget):
    startSignal = pyqtSignal(str, str)
    menuSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = UI_PlayerNames()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.start)
        self.ui.pushButton_2.clicked.connect(self.menu)
        self.mode: Optional[GameMode] = None

    def prepareWidget(self, mode: GameMode):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.mode = mode

        if mode == GameMode.PVP:
            self.ui.label_3.setVisible(True)
            self.ui.lineEdit_2.setVisible(True)
            self.ui.label.setText("Введите имена игроков")
            self.ui.label_2.setText("Игрок 1:")

        if mode == GameMode.PVE:
            self.ui.label_3.setVisible(False)
            self.ui.lineEdit_2.setVisible(False)
            self.ui.label.setText("Введите имя игрока")
            self.ui.label_2.setText("Игрок:")

    def start(self):
        if self.mode == GameMode.PVP:
            if self.ui.lineEdit_2.text() == '' or self.ui.lineEdit.text() == '':
                return
            self.startSignal.emit(self.ui.lineEdit.text(), self.ui.lineEdit_2.text())
        elif self.mode == GameMode.PVE:
            if self.ui.lineEdit.text() == '':
                return
            self.startSignal.emit(self.ui.lineEdit.text(), 'OpenAI')

    def menu(self):
        self.menuSignal.emit()

    def getPlayer1(self):
        return self.ui.lineEdit.text()

    def getPlayer2(self):
        return self.ui.lineEdit_2.text()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = PlayerNamesWidget()
    # widget.prepareWidget(WidgetType.PvE)
    widget.prepareWidget(GameMode.PVP)
    widget.show()
    app.exec_()
