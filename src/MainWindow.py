import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QStackedWidget, QAction

# for example
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, QLabel


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.menu = QWidget()
        self.gameWindow = QWidget()
        self.currentWidget = 0

        self.stack1UI()
        self.stack2UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.menu)
        self.Stack.addWidget(self.gameWindow)
        self.setCentralWidget(self.Stack)

        self.menuButton = QPushButton("Вернуться в меню")
        self.menuButton.clicked.connect(self.goToMenu)
        self.menuButton.setVisible(False)

        self.gameButton = QAction()
        self.gameButton.setText('Начать игру')
        self.gameButton.triggered.connect(self.goToGameWindow)

        self.menuButton = QAction()
        self.menuButton.setText('Вернуться в меню')
        self.menuButton.triggered.connect(self.goToMenu)
        self.menuButton.setVisible(False)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(self.menuButton)
        self.toolbar.addAction(self.gameButton)
        self.toolbar.setMovable(False)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Морской бой')
        self.show()

    @pyqtSlot()
    def goToMenu(self):
        self.currentWidget = 0
        self.menuButton.setVisible(False)
        self.gameButton.setVisible(True)
        self.display()

    @pyqtSlot()
    def goToGameWindow(self):
        self.currentWidget = 1
        self.gameButton.setVisible(False)
        self.menuButton.setVisible(True)
        self.display()

    def display(self):
        self.Stack.setCurrentIndex(self.currentWidget)

    # this for example
    def stack1UI(self):
        layout = QFormLayout()
        layout.addRow("COOL GAME", QLineEdit("yea"))
        self.menu.setLayout(layout)

    def stack2UI(self):
        layout = QFormLayout()
        result = QHBoxLayout()
        result.addWidget(QRadioButton("Win"))
        result.addWidget(QRadioButton("Lose"))
        layout.addRow(QLabel("?"), result)
        self.gameWindow.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
