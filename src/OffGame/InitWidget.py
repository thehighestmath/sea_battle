import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QTransform

# inner project imports
import Environment
from OffGame.UI_InitWidget import Ui_InitWidget
from OffGame.PlayerNamesWidget import WidgetType


class InitWidget(QtWidgets.QWidget):
    PvAISignal = pyqtSignal(WidgetType)
    PvPSignal = pyqtSignal(WidgetType)

    showHSTSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_InitWidget()
        self.ui.setupUi(self)

        resourcePath = Environment.Resources.path()
        imagePath = os.path.join(resourcePath, "img", "miscellaneous", "logo.png")
        pixmap = QPixmap(imagePath).transformed(QTransform().scale(0.7, 0.7),
                                                Qt.TransformationMode.SmoothTransformation)
        self.ui.label.setPixmap(pixmap)

        self.ui.PVE.clicked.connect(self.PvsAI)
        self.ui.PVP.clicked.connect(self.PvsP)
        self.ui.highscoreTable.clicked.connect(self.showHST)
        self.ui.exit.clicked.connect(lambda _: QCoreApplication.quit())

    def PvsAI(self):
        self.PvAISignal.emit(WidgetType.PvE)

    def PvsP(self):
        self.PvPSignal.emit(WidgetType.PvP)

    def showHST(self):
        self.showHSTSignal.emit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    init = InitWidget()
    init.show()
    app.exec_()
