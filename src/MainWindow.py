from enum import IntEnum
from PyQt5.QtCore import pyqtSlot, QEvent
from PyQt5.QtWidgets import QMainWindow, QPushButton, QStackedWidget, QAction

from Presenter.GameWindow import GameWindow
from OffGame.InitWidget import InitWidget
from OffGame.GameOverWidget import GameOverWidget


class DisplayedWidget(IntEnum):
    MENU = 0
    GAME = 1


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.menu = InitWidget()
        self.gameWindow = GameWindow()
        self.currentWidget = DisplayedWidget.MENU

        self.menu.PvAISignal.connect(self.goToGameWindow)
        self.menu.PvPSignal.connect(self.goToGameWindow)

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.menu)
        self.Stack.addWidget(self.gameWindow)
        self.setCentralWidget(self.Stack)

        self.menuButton = QPushButton("Вернуться в меню")
        self.menuButton.clicked.connect(self.goToMenu)
        self.menuButton.setVisible(False)

        self.menuButton = QAction()
        self.menuButton.setText('Вернуться в меню')
        self.menuButton.triggered.connect(self.goToMenu)
        self.menuButton.setVisible(False)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(self.menuButton)
        self.toolbar.setMovable(False)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Морской бой')
        self.show()

        self.gameOverWidget = None

    @pyqtSlot()
    def goToMenu(self):
        self.currentWidget = DisplayedWidget.MENU
        self.menuButton.setVisible(False)
        self.display()

    @pyqtSlot()
    def goToGameWindow(self):
        self.currentWidget = DisplayedWidget.GAME

        self.gameWindow = GameWindow()
        self.gameWindow.gameOverSignal.connect(self.showGameOver)
        self.Stack.insertWidget(DisplayedWidget.GAME, self.gameWindow)
        
        self.menuButton.setVisible(True)
        self.display()

    @pyqtSlot(str)
    def showGameOver(self, player):
        print("WHAT WOT?")
        self.gameOverWidget = GameOverWidget(player)
        self.gameOverWidget.ui.menuButton.clicked.connect(self.goToMenu)
        self.gameOverWidget.ui.newGameButton.clicked.connect(self.goToGameWindow)
        self.Stack.addWidget(self.gameOverWidget)
        self.Stack.setCurrentWidget(self.gameOverWidget)


    def display(self):
        self.Stack.setCurrentIndex(self.currentWidget)
