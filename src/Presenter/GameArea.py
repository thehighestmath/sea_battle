import sys, os
from enum import Enum

#use PyQt5
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsItem, QSizePolicy
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsTextItem, QGraphicsRectItem

from PyQt5.QtGui import QImage, QFont, QPixmap, QTransform, QPainter, QResizeEvent, QPen
from PyQt5.QtCore import Qt, QSize, QMargins, QEvent, QRectF, QPoint, QPointF

# inner project imports
import Environment

# ui
from Presenter.ui_GameArea import Ui_GameArea

DEBUG_RESOURCE = ""


class ShipItem():
    def __init__(self, length, count):
        self.length         = length
        
        self.image          = None
        self.shipItem       = QGraphicsPixmapItem()
        
        self.count          = count
        self.counterItem    = QGraphicsPixmapItem()
        self.counterText    = QGraphicsTextItem()


class Rotation(Enum):
    RIGHT   = 0
    DOWN    = 1
    LEFT    = 2
    UP      = 3


class GameArea(QWidget):
    #constants of widget
    RATIO_WITH_SHIPLIST = 11/14
    RATIO_WITHOUT_SHIPLIST = 1
    EPS = 0.3

    def __init__(self, parent = None):
        super(GameArea, self).__init__(parent)
        self.ui = Ui_GameArea()
        self.ui.setupUi(self)

        self.ratio = self.RATIO_WITH_SHIPLIST

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
        self.originalTileSize = 0

        self.shipListImage = QImage()
        self.counterImage = QImage()

        # drawing items
        self.field = [QGraphicsPixmapItem() for _ in range(100)]
        self.letters = [QGraphicsTextItem() for _ in range(10)]
        self.numbers = [QGraphicsTextItem() for _ in range(10)]
     
        self.shipListItem = QGraphicsPixmapItem()
        self.ghostShip = QGraphicsPixmapItem()
        self.placer = QGraphicsRectItem()
        self.dragShip = False

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


        first = True
        for key in self.cellImages:
            image = QImage(os.path.join(resourcesPath, "img", "cells", f"{key}.png"))
            if first:
                first = False
                self.originalTileSize = min(image.width(), image.height())
            else:
                self.originalTileSize = min(self.originalTileSize, image.width(), image.height())
            self.cellImages[key] = image


        for key, item in self.ships.items():
            item.image = QImage(os.path.join(resourcesPath, "img", "ships", f"{key}.png"))

        self.shipListImage = QImage(os.path.join(resourcesPath, "img", "backgrounds", "shiplist.png"))
        self.counterImage = QImage(os.path.join(resourcesPath, "img", "miscellaneous", "shipcounter.png"))


    def initGraphicsView(self):
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.viewport().installEventFilter(self)
        self.ui.graphicsView.setRenderHints(
            QPainter.RenderHint.HighQualityAntialiasing |
            QPainter.RenderHint.TextAntialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        
        for cell in self.field:
            cell.setData(0, "intact")
            pixmap = QPixmap.fromImage(self.cellImages["intact"])
            cell.setPixmap(pixmap)
            cell.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
            self.scene.addItem(cell)

        ca_letters = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]
        # ca_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        ca_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        font = QFont("Roboto")
        font.setPixelSize(int(self.originalTileSize * 0.8))
        for i in range(10):
            self.letters[i].setPlainText(ca_letters[i])
            self.letters[i].setFont(font)
            self.numbers[i].setPlainText(ca_numbers[i])
            self.numbers[i].setFont(font)
            self.scene.addItem(self.letters[i])
            self.scene.addItem(self.numbers[i])

        self.shipListItem.setPixmap(QPixmap.fromImage(self.shipListImage))
        self.shipListItem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.scene.addItem(self.shipListItem)

        font.setPixelSize(self.originalTileSize * 0.3)
        for key, item in self.ships.items():
            t = QTransform().rotate(90)
            item.shipItem.setPixmap(QPixmap.fromImage(item.image).transformed(t))
            item.shipItem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
            item.counterItem.setPixmap(QPixmap.fromImage(self.counterImage))
            item.counterText.setPlainText(str(item.count))
            item.counterText.setFont(font)
            self.scene.addItem(item.shipItem)
            self.scene.addItem(item.counterItem)
            self.scene.addItem(item.counterText)

        self.ghostShip.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.ghostShip.setOpacity(0.7)
        
        pen = QPen()
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.placer.setPen(pen)


    def hasHeightForWidth(self):
        return True


    def heightForWidth(self, width):
        return width / self.ratio


    def hideShipList(self):
        self.ratio = self.RATIO_WITHOUT_SHIPLIST
        self.scene.removeItem(self.shipListItem)
        for key, ship in self.ships.items():
            self.scene.removeItem(ship.shipItem)

        self.adjustedToSize = None
        resize = QResizeEvent(self.size(), self.size())
        QApplication.postEvent(self, resize)


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

        self.setContentsMargins(QMargins(h_margin, v_margin, h_margin, v_margin))
        self.resizeScene()


    def resizeScene(self):
        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()
        self.scene.setSceneRect(0, 0, width, height)

        self.tileSize = min(width / 11, height / (11 / self.ratio))
        self.scaleFactor = self.tileSize / self.originalTileSize

        for i, item in enumerate(self.field):
            x = i % 10
            y = i // 10
            item.setScale(self.scaleFactor)
            item.setPos((x+1)*self.tileSize, (y+1)*self.tileSize)

        for i in range(10):
            letter = self.letters[i]
            letter.setScale(self.scaleFactor)
            offsetX = (self.tileSize - letter.boundingRect().width() * self.scaleFactor) / 2 
            offsetY = (self.tileSize - letter.boundingRect().height() * self.scaleFactor) / 2
            letter.setPos((i + 1) * self.tileSize + offsetX, offsetY)

            number = self.numbers[i]
            number.setScale(self.scaleFactor)
            offsetX = (self.tileSize - number.boundingRect().width() * self.scaleFactor) / 2
            offsetY = (self.tileSize - number.boundingRect().height() * self.scaleFactor) / 2
            number.setPos(offsetX, (i + 1) * self.tileSize + offsetY)

        xPos = 0

        for key, item in self.ships.items():
            xPos += (item.length - 1)
            xOffset = xPos * self.tileSize
            
            item.shipItem.setScale(self.scaleFactor)
            item.shipItem.setPos(self.tileSize + xOffset, self.tileSize * (12 + self.EPS))
            
            item.counterItem.setScale(self.scaleFactor)
            item.counterItem.setPos(self.tileSize + xOffset, self.tileSize * (12.65 + self.EPS))
            
            textX = item.counterItem.pos().x() + (item.counterItem.boundingRect().width() - item.counterText.boundingRect().width()) * self.scaleFactor / 2
            textY = item.counterItem.pos().y() + (item.counterItem.boundingRect().height() - item.counterText.boundingRect().height()) * self.scaleFactor / 2
            item.counterText.setScale(self.scaleFactor)
            item.counterText.setPos(textX, textY)

        shipListX = self.tileSize
        shipListY = self.tileSize * (11 + self.EPS)
        self.shipListItem.setScale(self.scaleFactor)
        self.shipListItem.setPos(shipListX, shipListY)
        self.ghostShip.setScale(self.scaleFactor)


    def eventFilter(self, obj, event):
        if obj is self.ui.graphicsView.viewport():
            if event.type() == QEvent.MouseButtonPress:
                self.viewportMousePressEvent(event)
            elif event.type() == QEvent.MouseButtonRelease:
                self.viewportMouseReleaseEvent(event)
            elif event.type() == QEvent.MouseMove:
                self.viewportMouseMoveEvent(event)

        return super().eventFilter(obj, event)


    def initGhostShip(self, ship, pos):
        self.ghostShip.setPixmap(QPixmap.fromImage(ship.image))
        self.ghostShip.setPos(pos)
        self.ghostShip.setRotation(0)
            
        width = self.ghostShip.boundingRect().width()
        height = self.ghostShip.boundingRect().height()
        self.ghostShip.setOffset(-width / 2, -height / 2)
        self.ghostShip.setData(0, Rotation.UP)
        self.ghostShip.setData(1, ship.length)

        self.placer.setRect(0, 0, self.tileSize, self.tileSize * ship.length)
        self.placer.setZValue(50)
        pen = self.placer.pen()
        pen.setColor(Qt.GlobalColor.red)
        self.placer.setPen(pen)

        self.scene.addItem(self.ghostShip)
        self.ghostShip.setZValue(100)

    def rotateGhostShip(self):
        old_rot = self.ghostShip.data(0)
        new_rot = Rotation((old_rot.value + 1) % len(Rotation))
        self.ghostShip.setData(0, new_rot)
        self.ghostShip.setRotation((new_rot.value + 1) * 90)

        placerRect = self.placer.rect()
        self.placer.setRect(0, 0, placerRect.height(), placerRect.width())


    def ghostShipLongSurface(self):
        pos = self.ghostShip.pos()
        x = pos.x()
        y = pos.y()
        rot = self.ghostShip.data(0)
        length = self.ghostShip.data(1)
        if rot == Rotation.LEFT or rot == Rotation.RIGHT:
            x -= self.tileSize * length / 2
            return x, y

        if rot == Rotation.UP or rot == Rotation.DOWN:
            y -= self.tileSize * length / 2
            return x, y


    def sceneToMap(self, x, y):
        x -= self.tileSize
        y -= self.tileSize
        x //= self.tileSize
        y //= self.tileSize
        return x, y


    def viewportMousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            shipUnderMouse = None
            for key, ship in self.ships.items():
                if ship.shipItem.isUnderMouse():
                    shipUnderMouse = ship
                    break

            if(shipUnderMouse):
                self.initGhostShip(shipUnderMouse, event.pos())
                # self.rotateGhostShip()
                self.dragShip = True

        if event.button() == Qt.MouseButton.RightButton:
            if self.dragShip:
                self.rotateGhostShip()

    
    def viewportMouseReleaseEvent(self, event):
        if(event.button() == Qt.MouseButton.LeftButton):
            if self.dragShip:
                self.scene.removeItem(self.ghostShip)
                self.dragShip = False
        

    def viewportMouseMoveEvent(self, event):
        if self.dragShip:
            self.ghostShip.setPos(event.pos())

            permittedArea = QRectF(self.ui.graphicsView.viewport().geometry())
            permittedArea.setTopLeft(QPointF(self.tileSize, self.tileSize))

            if not permittedArea.contains(event.pos()):
                self.scene.removeItem(self.ghostShip)
                self.dragShip = False

            permittedArea.setBottomRight(QPointF(self.tileSize * 12, self.tileSize * 12))
            sceneX, sceneY = self.ghostShipLongSurface()
            placerRect = QRectF(sceneX, sceneY, self.placer.boundingRect().width(), self.placer.boundingRect().height())
            
            if permittedArea.contains(event.pos()) and permittedArea == permittedArea.united(placerRect):
                if self.placer.scene() == None:
                    self.scene.addItem(self.placer)
                x, y = self.sceneToMap(sceneX, sceneY)
                self.placer.setPos((x + 1) * self.tileSize, (y + 1) * self.tileSize)
                
            else:
                if self.placer.scene() == self.scene:
                    self.scene.removeItem(self.placer)


if __name__ == "__main__":
    app = QApplication([])
    QFontDatabase.addApplicationFont(os.path.join(Environment.Resources.path(), "fonts", "Roboto", "Roboto-Bold.ttf"))
    
    widget = GameArea()
    widget.show()

    # widget.hideShipList()
    sys.exit(app.exec_())