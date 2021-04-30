from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, Qt, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from Model.Enums import DisplayedWidget, GameMode
from OffGame.GameOverWidget import GameOverWidget
from OffGame.InitWidget import InitWidget
from Presenter.GameWindow import GameWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet('''
            background-color: #b3e6ff;
        ''')

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.menu = InitWidget()
        self.gameWindow = GameWindow(gameMode=GameMode.PVP)
        self.currentWidget = DisplayedWidget.MENU

        self.menu.PvAISignal.connect(self.goToPVEGame)
        self.menu.PvPSignal.connect(self.goToPVPGame)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.gameWindow)
        self.setCentralWidget(self.stack)

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
    def goToPVPGame(self):
        self.goToGameWindow(GameMode.PVP)

    @pyqtSlot()
    def goToPVEGame(self):
        self.goToGameWindow(GameMode.PVE)

    def goToGameWindow(self, gameMode):
        self.currentWidget = DisplayedWidget.GAME

        self.gameWindow = GameWindow(gameMode=gameMode)
        self.gameWindow.gameOverSignal.connect(self.showGameOver)
        self.gameWindow.toMenuSignal.connect(self.goToMenu)
        self.stack.insertWidget(DisplayedWidget.GAME, self.gameWindow)

        self.display()

    @pyqtSlot(str)
    def showGameOver(self, player):
        self.gameOverWidget = GameOverWidget(player)
        self.gameOverWidget.ui.menuButton.clicked.connect(self.goToMenu)
        self.gameOverWidget.ui.newGameButton.clicked.connect(self.goToGameWindow)
        self.stack.addWidget(self.gameOverWidget)
        self.stack.setCurrentWidget(self.gameOverWidget)

    def display(self):
        self.stack.setCurrentIndex(self.currentWidget)

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
