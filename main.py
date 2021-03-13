import sys
from PyQt5 import QtWidgets
import InitWindow

class InitWindow(QtWidgets.QMainWindow, InitWindow.Ui_InitWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.PVAI.clicked.connect(self.PvsAI)
        self.PVP.clicked.connect(self.PvsP)
        self.hst.clicked.connect(self.showHST)

    def PvsAI(self):
        print("PVSAI")

    def PvsP(self):
        print("PVSP")

    def showHST(self):
        print("showHST")

if __name__ == '__main__':
    print("Sea Battle!")
    app = QtWidgets.QApplication(sys.argv)
    init = InitWindow()
    init.show()
    app.exec_()