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

        # self.menuButton = QPushButton("Вернуться в меню")
        # self.menuButton.clicked.connect(self.goToMenu)
        # self.menuButton.setVisible(False)

        self.menuButton = QAction()
        self.menuButton.setText('Вернуться в меню')
        self.menuButton.triggered.connect(self.goToMenu)
        self.menuButton.setVisible(False)

        self.quitButton = QAction()
        self.quitButton.setText('Выйти')
        self.quitButton.triggered.connect(self.quit)
        self.quitButton.setVisible(True)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(self.menuButton)
        self.toolbar.addAction(self.quitButton)
        self.toolbar.setMovable(False)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Морской бой')
        self.show()

        self.mLastMousePosition = None
        self.mMoving = None
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
