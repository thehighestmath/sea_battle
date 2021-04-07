import sys
from PyQt5 import QtWidgets
from OffGame.UI_InitWidget import Ui_InitWidget
from PyQt5.QtCore import pyqtSignal


class InitWidget(QtWidgets.QWidget, Ui_InitWidget):

    PvAISignal = pyqtSignal()
    PvPSignal = pyqtSignal()
    showHSTSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.PVAI.clicked.connect(self.PvsAI)
        self.PVP.clicked.connect(self.PvsP)
        self.hst.clicked.connect(self.showHST)

    def PvsAI(self):
        self.PvAISignal.emit()

    def PvsP(self):
        self.PvPSignal.emit()

    def showHST(self):
        self.showHSTSignal.emit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    init = InitWidget()
    init.show()
    app.exec_()