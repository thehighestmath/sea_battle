# This Python file uses the following encoding: utf-8
import sys
import os

# use PyQt5
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QSize, QPoint, QEvent, QMimeData, QByteArray, QDataStream, QIODevice
from PyQt5.QtGui import QImage, QPixmap, QTransform, QCursor, QDrag

from Presenter.ui_ShipListWidget import Ui_ShipListWidget

import Environment

DEBUG_RESOURCE = ""

SHIP_MIME_TYPE = "application/x-ship"

class ShipListWidget(QWidget):
    def __init__(self, parent = None):
        super(ShipListWidget, self).__init__(parent)
        self.ui = Ui_ShipListWidget()
        self.ui.setupUi(self)

        self.ships = {
            1: 
                {
                    "name": "boat",
                    "count": 4
                },
            2:
                {
                    "name": "boat",
                    "count": 3
                },
            3:
                {
                    "name": "boat",
                    "count": 2
                },
            4: 
                {
                    "name": "boat",
                    "count": 1
                },
        }
        self.shipNames = {
            1: "boat",
            2: "destroyer",
            3: "cruiser",
            4: "battleship",
        }
        self.shipItems = [QGraphicsPixmapItem() for i in range(0, 4)]
        self.shipImages = [QImage() for i in range(0, 4)]
        self.itemToDrag = None
        self.dragElement = None

        self.loadResources()
        self.createGraphicsView()


    def loadResources(self):
        resourcesPath = Environment.Resources.path()
        for i in range(1, 5):
            srcImage = QImage(os.path.join(resourcesPath, str(i)))
            center = srcImage.rect().center()
            t = QTransform().translate(center.x(), center.y()).rotate(90)
            dstImage = srcImage.transformed(t)
            self.shipImages[i-1] = dstImage


    def createGraphicsView(self):
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.viewport().installEventFilter(self)
        self.ui.graphicsView.viewport().setMouseTracking(True)

        self.tileSize = int(min(self.height(), self.width()/10))
        xPos = 0
        for i in range(4):
            xPos += i
            shipSize = QSize(self.tileSize * (i + 1), self.tileSize)
            xOffset = xPos * self.tileSize

            image = self.shipImages[i]
            item = QGraphicsPixmapItem(QPixmap.fromImage(image).scaled(shipSize))
            item.setPos(xOffset, 0)
            item.setData(0, i + 1)
            
            self.shipItems[i] = item
            self.scene.addItem(item)


    def resizeEvent(self, event):
        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()
        self.scene.setSceneRect(0, 0, width, height)

        self.tileSize = int(min(height, width/10))
        xPos = 0
        for i in range(4):
            xPos += i
            shipSize = QSize(self.tileSize * (i + 1), self.tileSize)
            xOffset = xPos * self.tileSize

            image = self.shipImages[i]
            item = self.shipItems[i]
            item.setPixmap(QPixmap.fromImage(image).scaled(shipSize))
            item.setPos(xOffset, 0)


    def eventFilter(self, obj, event):
        if obj is self.ui.graphicsView.viewport():
            if event.type() == QEvent.MouseButtonPress:
                self.viewportMousePressEvent(event)
            elif event.type() == QEvent.MouseButtonRelease:
                self.viewportMouseReleaseEvent(event)
            elif event.type() == QEvent.MouseMove:
                self.viewportMouseMoveEvent(event)

        return super().eventFilter(obj, event)


    def viewportMousePressEvent(self, event):
        scenePos = self.ui.graphicsView.mapToScene(event.pos())

        if event.button() == Qt.MouseButton.LeftButton:
            item = self.scene.itemAt(scenePos, QTransform())
            if item:
                self.itemToDrag = item
                self.ui.graphicsView.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)

    
    def viewportMouseReleaseEvent(self, event):
        scenePos = self.ui.graphicsView.mapToScene(event.pos())
        itemUnderCursor = self.scene.itemAt(scenePos, QTransform())

        if event.button() == Qt.MouseButton.LeftButton:
            self.itemToDrag = None

        if itemUnderCursor:
            self.ui.graphicsView.viewport().setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            self.ui.graphicsView.viewport().setCursor(Qt.CursorShape.ArrowCursor)


    def viewportMouseMoveEvent(self, event):
        scenePos = self.ui.graphicsView.mapToScene(event.pos())
        itemUnderCursor = self.scene.itemAt(scenePos, QTransform())

        if self.itemToDrag == None:
            if itemUnderCursor:
                self.ui.graphicsView.viewport().setCursor(Qt.CursorShape.OpenHandCursor)
            else:
                self.ui.graphicsView.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        else:
            self.startDrag()


    def startDrag(self):
        item = self.itemToDrag
        self.itemToDrag = None
        shipCode = item.data(0)
        pixmap = item.pixmap()

        itemData = QByteArray()
        dataStream = QDataStream(itemData, QIODevice.OpenModeFlag.WriteOnly)
        dataStream << self.shipImages[shipCode - 1]
        dataStream.writeInt(shipCode)
        dataStream.writeQString(self.shipNames[shipCode])

        mimeData = QMimeData()
        mimeData.setData(SHIP_MIME_TYPE, itemData)

        self.dragElement = QDrag(self)
        self.dragElement.setMimeData(mimeData)
        self.dragElement.setHotSpot(QPoint(pixmap.width()/2, pixmap.height()/2))
        self.dragElement.setPixmap(pixmap)

        self.dragElement.exec(Qt.DropAction.MoveAction)
        self.dragElement = None


if __name__ == "__main__":
    DEBUG_RESOURCE = os.path.join(os.path.dirname(__file__), "res")

    app = QApplication([])
    widget = ShipListWidget()
    widget.show()
    sys.exit(app.exec_())
