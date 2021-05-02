import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QTransform

# inner project imports
import Environment
from Model.Enums import GameMode
from OffGame.UI_AIChoose import UI_AiChoose
from Model.Enums import AIMode


class AIChooseWidget(QtWidgets.QWidget):
    modeSignal = pyqtSignal(AIMode)

    backSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = UI_AiChoose()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.back)
        self.ui.pushButton_2.clicked.connect(self.easyStart)
        self.ui.pushButton_3.clicked.connect(self.mediumStart)
        self.ui.pushButton_4.clicked.connect(self.hardStart)


    def easyStart(self):
        self.modeSignal.emit(AIMode.EASY)

    def mediumStart(self):
        self.modeSignal.emit(AIMode.MIDDLE)

    def hardStart(self):
        self.modeSignal.emit(AIMode.HARD)

    def back(self):
        self.backSignal.emit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ai = AIChooseWidget()
    ai.show()
    app.exec_()
