from enum import IntEnum

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, QEvent, Qt, QCoreApplication
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
        self.setStyleSheet('''
            background-color: #b3e6ff;
        ''')

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.menu = InitWidget()
        self.gameWindow = GameWindow()
        self.currentWidget = DisplayedWidget.MENU

        self.menu.PvAISignal.connect(self.goToGameWindow)
        self.menu.PvPSignal.connect(self.goToGameWindow)

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.menu)
        self.Stack.addWidget(self.gameWindow)
        self.setCentralWidget(self.Stack)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Морской бой')

        self.mLastMousePosition = None
        self.mMoving = None
        self.gameOverWidget = None

    @pyqtSlot()
    def goToMenu(self):
        self.currentWidget = DisplayedWidget.MENU
        self.display()

    @pyqtSlot()
    def goToGameWindow(self):
        self.currentWidget = DisplayedWidget.GAME

        self.gameWindow = GameWindow()
        self.gameWindow.gameOverSignal.connect(self.showGameOver)
        self.gameWindow.toMenuSignal.connect(self.goToMenu)
        self.Stack.insertWidget(DisplayedWidget.GAME, self.gameWindow)
        
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

    def quit(self):
        QCoreApplication.quit()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.mMoving = True
            self.mLastMousePosition = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.mMoving:
            self.move(self.pos() + event.pos() - self.mLastMousePosition)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.mMoving = False
