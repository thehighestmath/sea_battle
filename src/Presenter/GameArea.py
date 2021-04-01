import sys, os
import enum

#use PyQt5
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem, QSizePolicy
from PyQt5.QtGui import QImage, QFont, QPixmap, QTransform, QPainter
from PyQt5.QtCore import QSize, QMargins

# inner project imports
import Environment

# ui
from Presenter.ui_GameArea import Ui_GameArea

DEBUG_RESOURCE = ""


class ShipItem:
    def __init__(self, length, count):
        self.length         = length
        self.image          = None
        self.graphicsItem   = QGraphicsPixmapItem()
        self.count          = count



class GameArea(QWidget):
    #constants of widget
    RATIO = 11/14
    EPS = 0.3

    def __init__(self, parent = None):
        super(GameArea, self).__init__(parent)
        self.ui = Ui_GameArea()
        self.ui.setupUi(self)

        self.ships = {
            "boat":         ShipItem(length=1, count=4),
            "destroyer":    ShipItem(length=2, count=3),
            "cruiser":      ShipItem(length=3, count=2),
            "battleship":   ShipItem(length=4, count=1),
        }

        # resources
        self.cellImages = {
            "intact":       None,
            "hit":          None,
            "miss":         None
        }

        # self.shipImages = {
        #     "boat":         None,
        #     "destroyer":    None,
        #     "cruiser":      None,
        #     "battleship":   None,
        # }

        self.shipListImage = QImage()

        # ship list counter
        # self.shipListResiduals = {
        #     "boat":         4,
        #     "destroyer":    3,
        #     "cruiser":      2,
        #     "battleship":   1,
        # }

        # drawing items
        self.field = [QGraphicsPixmapItem() for _ in range(100)]
        self.letters = [QGraphicsTextItem() for _ in range(10)]
        self.numbers = [QGraphicsTextItem() for _ in range(10)]
        # self.shipItems = {
        #     "boat":         QGraphicsPixmapItem(),
        #     "destroyer":    QGraphicsPixmapItem(),
        #     "cruiser":      QGraphicsPixmapItem(),
        #     "battleship":   QGraphicsPixmapItem(),
        # }
        self.shipListItem = QGraphicsPixmapItem()
        self.ghostShip = QGraphicsPixmapItem()

        # prepare Qt objects
        self.scene = QGraphicsScene()
        self.loadResources()
        self.initGraphicsView()
        self.adjustedToSize = 0

    def loadResources(self):
        if DEBUG_RESOURCE:
            resourcesPath = os.path.join(os.path.dirname(__file__), DEBUG_RESOURCE)
        else:
            resourcesPath = Environment.Resources.path()

        for key in self.cellImages:
            self.cellImages[key] = QImage(os.path.join(resourcesPath, "cells", f"{key}.png"))

        for key, item in self.ships.items():
            item.image = QImage(os.path.join(resourcesPath, "ships", f"{key}.png"))

        self.shipListImage = QImage(os.path.join(resourcesPath, "backgrounds", "shiplist.png"))


    def initGraphicsView(self):
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.viewport().installEventFilter(self)
        self.ui.graphicsView.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        
        for item in self.field:
            item.setData(0, "intact")
            self.scene.addItem(item)

        ca_letters = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]
        # ca_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        ca_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        for i in range(10):
            self.letters[i].setPlainText(ca_letters[i])
            self.numbers[i].setPlainText(ca_numbers[i])
            self.scene.addItem(self.letters[i])
            self.scene.addItem(self.numbers[i])

        self.scene.addItem(self.shipListItem)

        for key, item in self.ships.items():
            item.graphicsItem.setData(0, key)
            self.scene.addItem(item.graphicsItem)

        self.scene.addItem(self.ghostShip)



    def heightForWidth(self, width):
        return width / self.RATIO


    def resizeEvent(self, event):
        size = event.size()
        if size == self.adjustedToSize:
            return

        self.adjustedToSize = size

        nowWidth = size.width()
        nowHeight = size.height()

        width = min(nowWidth, nowHeight * self.RATIO)
        height = min(nowHeight, nowWidth / self.RATIO)

        h_margin = round((nowWidth - width) / 2)
        v_margin = round((nowHeight - height) / 2)

        self.setContentsMargins(QMargins(h_margin, v_margin, h_margin, v_margin))
        self.resizeScene()


    def resizeScene(self):
        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()
        self.scene.setSceneRect(0, 0, width, height)

        self.tileSize = min(width // 11, height // 14)

        for i, item in enumerate(self.field):
            x = i % 10
            y = i // 10
            cellType = item.data(0)
            pixmap = QPixmap.fromImage(self.cellImages[cellType])
            item.setPixmap(pixmap.scaled(QSize(self.tileSize, self.tileSize)))
            item.setPos((x+1)*self.tileSize, (y+1)*self.tileSize)

        for i in range(10):
            font = QFont("Roboto")
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

        xPos = 0
        for key, item in self.ships.items():
            xPos += (item.length - 1)
            xOffset = xPos * self.tileSize
            t = QTransform().rotate(90)
            pixmap = QPixmap.fromImage(item.image).transformed(t)
            item.graphicsItem.setPixmap(pixmap.scaled(self.tileSize * item.length, self.tileSize))
            item.graphicsItem.setPos(self.tileSize + xOffset, self.tileSize * (12 + self.EPS))

        shipListX = self.tileSize
        shipListY = self.tileSize * (11 + self.EPS)
        shipListPixmap = QPixmap.fromImage(self.shipListImage)
        shipListRatio = self.shipListImage.width() / self.shipListImage.height()
        self.shipListItem.setPixmap(shipListPixmap.scaled(QSize(self.tileSize * 10, self.tileSize * 10 / shipListRatio)))
        self.shipListItem.setPos(shipListX, shipListY)
        

if __name__ == "__main__":
    app = QApplication([])
    QFontDatabase.addApplicationFont(os.path.join(Environment.Resources.path(), "fonts", "Roboto", "Roboto-Bold.ttf"))
    
    widget = GameArea()
    widget.show()
    sys.exit(app.exec_())