import sys
import os
from enum import IntEnum
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform

# inner project imports
import Environment

from OffGame.UI_PlayerNames import UI_PlayerNames


class WidgetType(IntEnum):
    PvP = 0
    PvE = 1


class PlayerNamesWidget(QtWidgets.QWidget):

    StartSignal = pyqtSignal()
    MenuSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = UI_PlayerNames()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.start)
        self.ui.pushButton_2.clicked.connect(self.menu)

    def prepareWidget(self, mode: IntEnum):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()

        if mode == WidgetType.PvP:
            self.ui.label_3.setVisible(True)
            self.ui.lineEdit_2.setVisible(True)
            self.ui.label.setText("Введите имена игроков")
            self.ui.label_2.setText("Игрок 1:")
        if mode == WidgetType.PvE:
            self.ui.label_3.setVisible(False)
            self.ui.lineEdit_2.setVisible(False)
            self.ui.label.setText("Введите имя игрока")
            self.ui.label_2.setText("Игрок:")

    def start(self, mode: IntEnum):
        if mode == WidgetType.PvP and self.ui.lineEdit_2.text() == '' or \
                self.ui.lineEdit.text() == '':
            return
        self.StartSignal.emit()

    def menu(self):
        self.MenuSignal.emit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = PlayerNamesWidget()
#    widget.prepareWidget(WidgetType.PvE)
    widget.prepareWidget(WidgetType.PvP)
    widget.show()
    app.exec_()
