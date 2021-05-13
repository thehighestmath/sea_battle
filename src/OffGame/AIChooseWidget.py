import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon

# inner project imports
import Environment
from OffGame.UI_AIChoose import Ui_AiChoose
from Model.Enums import GameLevel


class AIChooseWidget(QtWidgets.QWidget):
    modeSignal = pyqtSignal(GameLevel)

    backSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_AiChoose()
        self.ui.setupUi(self)

        resourcePath = Environment.Resources.path()
        iconExit = QIcon(QPixmap(os.path.join(resourcePath, "img", "miscellaneous", "logout.png")))
        self.ui.pushButton.setIcon(iconExit)

        self.ui.pushButton.clicked.connect(self.back)
        self.ui.pushButton_2.clicked.connect(self.easyStart)
        self.ui.pushButton_3.clicked.connect(self.mediumStart)
        self.ui.pushButton_4.clicked.connect(self.hardStart)


    def easyStart(self):
        self.modeSignal.emit(GameLevel.EASY)

    def mediumStart(self):
        self.modeSignal.emit(GameLevel.MEDIUM)

    def hardStart(self):
        self.modeSignal.emit(GameLevel.HARD)

    def back(self):
        self.backSignal.emit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ai = AIChooseWidget()
    ai.show()
    app.exec_()
