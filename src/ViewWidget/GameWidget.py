# This Python file uses the following encoding: utf-8
import sys
import os

# use PyQt5
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui

# use ui
from ui_GameWidget import Ui_GameWidget

# inner imports
from ShipListWidget import ShipMimeType

DEBUG_RESOURCE = ""

class GameWidget(QWidget):
    def __init__(self, parent = None):
        super(GameWidget, self).__init__(parent)
        self.ui = Ui_GameWidget()
        self.ui.setupUi(self)

        # constants of widget
        self.ratio = 1  # ratio of widget size

        # create drawing field
        self.field = [QGraphicsPixmapItem() for i in range(100)]
        self.letters = [QGraphicsTextItem() for i in range(10)]
        self.numbers = [QGraphicsTextItem() for i in range(10)]

        # prepare Qt objects
        self.LoadResources()
        self.CreateGraphicsView()
        self.setAcceptDrops(True)
        self.adjustedToSize = 0


    def LoadResources(self):
        if(DEBUG_RESOURCE):
            resourcesPath = os.path.join(os.path.dirname(__file__), DEBUG_RESOURCE)

        self.waterImage = QImage(os.path.join(resourcesPath, "water.png"))
        self.hitImage = QImage(os.path.join(resourcesPath, "hit.png"))


    def CreateGraphicsView(self):
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.ui.graphicsView.setScene(self.scene)

        self.tileSize = min(self.width(), self.height()) // 11

        for i in range(0, 100):
            x = i % 10
            y = i // 10
            item = QGraphicsPixmapItem(QPixmap.fromImage(self.waterImage).scaled(QtCore.QSize(self.tileSize, self.tileSize)))
            item.setPos((x+1)*self.tileSize, (y+1)*self.tileSize)
            self.field[i] = item
            self.scene.addItem(item)

        letters = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        for i in range (0, 10):
            font = QtGui.QFont("Roboto")
            font.setPixelSize(int(self.tileSize * 0.8))

            letter = QGraphicsTextItem(letters[i])
            letter.setFont(font)
            offsetX = (self.tileSize - letter.boundingRect().width()) // 2 
            offsetY = (self.tileSize - letter.boundingRect().height()) // 2
            letter.setPos((i + 1) * self.tileSize + offsetX, offsetY)

            number = QGraphicsTextItem(numbers[i])
            number.setFont(font)
            offsetX = (self.tileSize - number.boundingRect().width()) // 2
            offsetY = (self.tileSize - number.boundingRect().height()) // 2
            number.setPos(offsetX, (i + 1) * self.tileSize + offsetY)

            self.letters[i] = letter
            self.numbers[i] = number

            self.scene.addItem(letter)
            self.scene.addItem(number)

    
    def heightForWidth(self, w):
        return w / ratio

    #handle events
    def resizeEvent(self, event):
        size = event.size()
        if size == self.adjustedToSize:
            return

        self.adjustedToSize = size

        nowWidth = size.width()
        nowHeight = size.height()

        width = min(nowWidth, nowHeight * self.ratio)
        height = min(nowHeight, nowWidth / self.ratio)

        h_margin = round((nowWidth - width) / 2)
        v_margin = round((nowHeight - height) / 2)

        self.setContentsMargins(QtCore.QMargins(h_margin, v_margin, h_margin, v_margin))
        self.resizeScene()


    def resizeScene(self):
        self.scene.setSceneRect(0, 0, self.width(), self.height())

        self.tileSize = min(self.width(), self.height()) // 11

        for i in range(0, 100):
            x = i % 10
            y = i // 10
            item = self.field[i]
            item.setPixmap(QPixmap.fromImage(self.waterImage).scaled(QtCore.QSize(self.tileSize, self.tileSize)))
            item.setPos((x+1)*self.tileSize, (y+1)*self.tileSize)

        for i in range (0, 10):
            font = QtGui.QFont("Roboto")
            font.setPixelSize(int(self.tileSize * 0.8))

            letter = self.letters[i]
            letter.setFont(font)
            offsetX = (self.tileSize - letter.boundingRect().width()) // 2 
            offsetY = (self.tileSize - letter.boundingRect().height()) // 2
            letter.setPos((i + 1) * self.tileSize + offsetX, offsetY)

            number = self.numbers[i]
            number.setFont(font)
            offsetX = (self.tileSize - number.boundingRect().width()) // 2
            offsetY = (self.tileSize - number.boundingRect().height()) // 2
            number.setPos(offsetX, (i + 1) * self.tileSize + offsetY)


    def dragEnterEvent(self, event):
            if event.mimeData().hasFormat(ShipMimeType()):
                event.accept()

            else:
                event.ignore()


    def dragLeaveEvent(self, event):
            event.accept()


    def dragMoveEvent(self, event):
            print(event.position().x(), event.position().y())
            if event.mimeData().hasFormat(ShipMimeType()):
                event.accept()
            else:
                event.ignore()
            

    def dropEvent(self, event):
            if event.mimeData().hasFormat(ShipMimeType()):
                event.accept()
            else:
                event.ignore()


if __name__ == "__main__":
    DEBUG_RESOURCE = os.path.join(os.path.dirname(__file__), "res")

    app = QApplication([])
    QtGui.QFontDatabase.addApplicationFont(os.path.join(DEBUG_RESOURCE, "fonts", "Roboto", "Roboto-Bold.ttf"))
    
    widget = GameWidget()
    widget.show()
    sys.exit(app.exec_())
