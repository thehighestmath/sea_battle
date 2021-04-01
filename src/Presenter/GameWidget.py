# This Python file uses the following encoding: utf-8
import sys
import os

# use PyQt5
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem, QGraphicsSceneDragDropEvent
from PyQt5.QtGui import QImage, QPixmap, QTransform, QDragMoveEvent, QDropEvent, QMouseEvent
from PyQt5.QtCore import QEvent, QDataStream, QIODevice, pyqtSignal
from PyQt5 import QtCore, QtGui
from enum import Enum

# use ui
from Presenter.ui_GameWidget import Ui_GameWidget

# inner imports
from Presenter.ShipListWidget import SHIP_MIME_TYPE
import Environment

DEBUG_RESOURCE = ""

class DropStatus(Enum):
    DROP_ABSENT = 0
    DROP_STARTED = 1
    DROP_FINISHED = 2


class GameWidget(QWidget):
    shipPlaced = pyqtSignal(int, name="shipPlaced")    
    def __init__(self, parent = None):
        super(GameWidget, self).__init__(parent)
        self.ui = Ui_GameWidget()
        self.ui.setupUi(self)

        # properties
        self.dropStatus = DropStatus.DROP_ABSENT
        self.shipListWidget = None
        self.currentShip = 0
        self.bringedShip = QGraphicsPixmapItem()

        # constants of widget
        self.ratio = 1  # ratio of widget size

        # create drawing field
        self.field = [QGraphicsPixmapItem() for i in range(100)]
        self.letters = [QGraphicsTextItem() for i in range(10)]
        self.numbers = [QGraphicsTextItem() for i in range(10)]

        # prepare Qt objects
        self.loadResources()
        self.createGraphicsView()
        self.setAcceptDrops(True)
        self.adjustedToSize = 0


    def loadResources(self):
        if DEBUG_RESOURCE:
            resourcesPath = os.path.join(os.path.dirname(__file__), DEBUG_RESOURCE)
        else:
            resourcesPath = Environment.Resources.path()

        self.waterImage = QImage(os.path.join(resourcesPath, "water.png"))
        self.hitImage = QImage(os.path.join(resourcesPath, "hit.png"))


    def createGraphicsView(self):
        self.scene = QGraphicsScene()
        self.scene.dragMoveEvent = self.dragMoveEvent
        self.scene.dropEvent = self.dropEvent
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setAcceptDrops(True)
        self.ui.graphicsView.dragEnterEvent = self.dragEnterEvent
        self.ui.graphicsView.viewport().installEventFilter(self)

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

        self.scene.addItem(self.bringedShip)


    def bindShipList(self, shipListWidget):
        self.shipListWidget = shipListWidget

    
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
        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()
        self.scene.setSceneRect(0, 0, width, height)

        self.tileSize = min(width, height) // 11

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
        if event.mimeData().hasFormat(SHIP_MIME_TYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)


    def dragMoveEvent(self, event):
        event.accept()
        
        if type(event) == QDragMoveEvent:
            return

        dropEvent = QDropEvent(
            event.pos(),
            QtCore.Qt.DropAction.MoveAction,
            event.mimeData(),
            event.buttons(),
            event.modifiers(),
            QEvent.Type.Drop
        )

        QApplication.sendEvent(self, dropEvent)


    def dropEvent(self, event):
        if event.mimeData().hasFormat(SHIP_MIME_TYPE):
            event.acceptProposedAction()

            data = event.mimeData().data(SHIP_MIME_TYPE)
            dataStream = QDataStream(data, QIODevice.OpenModeFlag.ReadOnly)
            image = QImage()
            dataStream >> image
            shipCode = dataStream.readInt()
            shipName = dataStream.readQString()

            self.bringedShip.setPixmap(QPixmap().fromImage(image).scaled(
                QtCore.QSize(
                    self.tileSize * shipCode,
                    self.tileSize
                )
            ))
            self.bringedShip.setData(0, shipCode)

            self.shipListWidget.dragElement.cancel()
            self.shipListWidget.dragElement.deleteLater()
            self.dropStatus = DropStatus.DROP_STARTED
        else:
            event.ignore()


    def eventFilter(self, obj, event):
        print(event)
        if obj is self.ui.graphicsView.viewport():
            if event.type() == QEvent.MouseButtonPress:
                self.viewportMousePressEvent(event)
            elif event.type() == QEvent.MouseButtonRelease:
                self.viewportMouseReleaseEvent(event)
            elif event.type() == QEvent.MouseMove:
                self.viewportMouseMoveEvent(event)

        return super().eventFilter(obj, event)


    def viewportMousePressEvent(self, event):
        if self.dropStatus != DropStatus.DROP_ABSENT:
            return

        # do other press event things

    
    def viewportMouseReleaseEvent(self, event):
        if self.dropStatus == DropStatus.DROP_STARTED:
            self.dropStatus = DropStatus.DROP_FINISHED
            return
        
        if self.dropStatus == DropStatus.DROP_FINISHED:
            self.dropStatus = DropStatus.DROP_ABSENT
            self.ui.graphicsView.viewport().releaseMouse()

        # do other release event things
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if not self.bringedShip.pixmap().isNull():
                self.bringedShip.setPixmap(QPixmap())
                self.shipPlaced.emit(self.bringedShip.data(0))


    def rotateBringedShip(self):
        oldPixmap = self.bringedShip.pixmap()
        t = QTransform().rotate(90)
        newPixmap = oldPixmap.transformed(t)
        self.bringedShip.setPixmap(newPixmap)
        

    def viewportMouseMoveEvent(self, event):
        if self.dropStatus == DropStatus.DROP_STARTED:
            self.ui.graphicsView.viewport().grabMouse()
            return

        # do other move event things
        item = self.bringedShip 
        if item:
            item.setPos(event.pos().x(), event.pos().y())
            item.setOffset(-item.boundingRect().width()/2, -item.boundingRect().height()/2)


if __name__ == "__main__":
    DEBUG_RESOURCE = os.path.join(os.path.dirname(__file__), "res")

    app = QApplication([])
    QtGui.QFontDatabase.addApplicationFont(os.path.join(DEBUG_RESOURCE, "fonts", "Roboto", "Roboto-Bold.ttf"))
    
    widget = GameWidget()
    widget.show()
    sys.exit(app.exec_())
