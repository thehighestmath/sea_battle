from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, Qt, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from Model.Enums import DisplayedWidget, GameMode, GameLevel
from OffGame.GameOverWidget import GameOverWidget
from OffGame.InitWidget import InitWidget
from OffGame.PlayerNamesWidget import PlayerNamesWidget
from OffGame.AIChooseWidget import AIChooseWidget

from Presenter.GameWindow import GameWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet('''
            background-color: #b3e6ff;
        ''')

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.menu = InitWidget()
        self.gameWindow = GameWindow('', '', gameMode=GameMode.PVP)
        self.currentWidget = DisplayedWidget.MENU
        self.mode = GameMode.PVP

        # self.menu.PvAISignal.connect(self.goToNames)
        # self.menu.PvPSignal.connect(self.goToNames)

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
        self.playerNamesWidget = None
        self.AIChooseWidget = None

    def goToNames(self, mode=GameMode.PVE):
        self.playerNamesWidget = PlayerNamesWidget()
        self.playerNamesWidget.prepareWidget(mode)

        if mode == GameMode.PVE:
            self.AIChooseWidget = AIChooseWidget()
            self.playerNamesWidget.startSignal.connect(self.choosePvEMode)
            self.AIChooseWidget.modeSignal.connect(self.goToGameWindow)
        else:
            self.playerNamesWidget.startSignal.connect(self.goToGameWindow1)

        self.playerNamesWidget.menuSignal.connect(self.goToMenu)
        self.stack.addWidget(self.playerNamesWidget)
        self.stack.setCurrentWidget(self.playerNamesWidget)



    @pyqtSlot()
    def goToMenu(self):
        self.currentWidget = DisplayedWidget.MENU
        self.display()

    @pyqtSlot()
    def goToPVPGame(self):
        self.mode = GameMode.PVP
        self.goToNames(GameMode.PVP)

    @pyqtSlot()
    def goToPVEGame(self):
        self.mode = GameMode.PVE
        self.goToNames(GameMode.PVE)

    @pyqtSlot()
    def choosePvEMode(self):
        self.stack.addWidget(self.AIChooseWidget)
        self.stack.setCurrentWidget(self.AIChooseWidget)
        self.AIChooseWidget.backSignal.connect(self.goToNames)

    @pyqtSlot(str, str)
    def goToGameWindow1(self, player_1, player_2):
        self.currentWidget = DisplayedWidget.GAME
        self.gameWindow = GameWindow(player_1, player_2, self.mode)
        self.gameWindow.gameOverSignal.connect(self.showGameOver)
        self.gameWindow.toMenuSignal.connect(self.goToMenu)
        self.stack.insertWidget(DisplayedWidget.GAME, self.gameWindow)

        self.display()

    @pyqtSlot(GameLevel)
    def goToGameWindow(self, mode):
        self.currentWidget = DisplayedWidget.GAME
        player_1 = self.playerNamesWidget.getPlayer1()
        self.gameWindow = GameWindow(player_1, "OpenAI", GameMode.PVE, mode)
        self.gameWindow.gameOverSignal.connect(self.showGameOver)
        self.gameWindow.toMenuSignal.connect(self.goToMenu)
        self.stack.insertWidget(DisplayedWidget.GAME, self.gameWindow)

        self.display()

    # def goToGameWindow_(self, gameMode):
    #     self.currentWidget = DisplayedWidget.GAME
    #     self.gameWindow = GameWindow(gameMode=gameMode)
    #     self.gameWindow.gameOverSignal.connect(self.showGameOver)
    #     self.gameWindow.toMenuSignal.connect(self.goToMenu)
    #     self.stack.insertWidget(DisplayedWidget.GAME, self.gameWindow)
    #
    #     self.display()

    @pyqtSlot(str)
    def showGameOver(self, player):
        self.gameOverWidget = GameOverWidget(player)
        self.gameOverWidget.ui.menuButton.clicked.connect(self.goToMenu)
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
