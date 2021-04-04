import sys, os
import logging
from enum import Enum

#use PyQt5
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsItem, QSizePolicy
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsTextItem, QGraphicsRectItem

from PyQt5.QtGui import QImage, QFont, QPixmap, QTransform, QPainter, QResizeEvent, QPen
from PyQt5.QtCore import Qt, QSize, QMargins, QEvent, QRectF, QPoint, QPointF
from PyQt5.QtCore import pyqtSignal

# inner project imports
import Environment

# ui
from Presenter.ui_GameArea import Ui_GameArea

DEBUG_RESOURCE = ""
log = logging.getLogger("GameArea")


class ShipListItem():
    def __init__(self, length, name, count):
        self.length         = length
        self.name           = name
        
        self.image          = None
        self.shipItem       = QGraphicsPixmapItem()
        
        self.count          = count
        self.counterItem    = QGraphicsPixmapItem()
        self.counterText    = QGraphicsTextItem()


class Ship():
    def __init__(self, name, length, pos, vertical):
        self.name   = name
        self.length = length
        self.pos    = pos
        self.vert   = vertical


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


    #signals
    shipPlaced = pyqtSignal(Ship)


    def __init__(self, parent = None):
        super(GameArea, self).__init__(parent)
        self.ui = Ui_GameArea()
        self.ui.setupUi(self)

        self.ratio = self.RATIO_WITH_SHIPLIST

        self.shipList = {
            "boat":         ShipListItem(length=1, name="boat",       count=4),
            "destroyer":    ShipListItem(length=2, name="destroyer",  count=3),
            "cruiser":      ShipListItem(length=3, name="cruiser",    count=2),
            "battleship":   ShipListItem(length=4, name="battleship", count=1),
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
        self.placedShips = []
        self.field       = [QGraphicsPixmapItem() for _ in range(100)]
        self.letters     = [QGraphicsTextItem()   for _ in range(10) ]
        self.numbers     = [QGraphicsTextItem()   for _ in range(10) ]
     
        self.shipListItem = QGraphicsPixmapItem()
        self.ghostShip = QGraphicsPixmapItem() # data: 0 - rotation; 1 - ShipListItem
        self.placer = QGraphicsRectItem()
        self.dragShip = False

        # prepare Qt objects
        self.scene = QGraphicsScene()
        self.__loadResources()
        self.__initGraphicsView()
        self.adjustedToSize = 0


    def __loadResources(self):
        if DEBUG_RESOURCE:
            resourcesPath = os.path.join(os.path.dirname(__file__), DEBUG_RESOURCE)
        else:
            resourcesPath = Environment.Resources.path()

        first = True
        for imageName in self.cellImages:
            image = QImage(os.path.join(resourcesPath, "img", "cells", f"{imageName}.png"))
            if first:
                first = False
                self.originalTileSize = min(image.width(), image.height())
            else:
                self.originalTileSize = min(self.originalTileSize, image.width(), image.height())
            self.cellImages[imageName] = image

        for shipName, ship in self.shipList.items():
            ship.image = QImage(os.path.join(resourcesPath, "img", "ships", f"{shipName}.png"))

        self.shipListImage = QImage(os.path.join(
            resourcesPath,
            "img",
            "backgrounds",
            "shiplist.png"
        ))
        self.counterImage = QImage(os.path.join(
            resourcesPath,
            "img",
            "miscellaneous",
            "shipcounter.png"
        ))


    def __initGraphicsView(self):
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.viewport().installEventFilter(self)
        self.ui.graphicsView.setRenderHints(
            QPainter.RenderHint.HighQualityAntialiasing |
            QPainter.RenderHint.TextAntialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        self.ui.graphicsView.horizontalScrollBar().blockSignals(True)
        self.ui.graphicsView.verticalScrollBar().blockSignals(True)
        
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

        font.setPixelSize(int(self.originalTileSize * 0.3))
        for _, ship in self.shipList.items():
            t = QTransform().rotate(90)
            ship.shipItem.setPixmap(QPixmap.fromImage(ship.image).transformed(t))
            ship.shipItem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
            ship.counterItem.setPixmap(QPixmap.fromImage(self.counterImage))
            ship.counterText.setPlainText(str(ship.count))
            ship.counterText.setFont(font)
            self.scene.addItem(ship.shipItem)
            self.scene.addItem(ship.counterItem)
            self.scene.addItem(ship.counterText)

        self.ghostShip.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.ghostShip.setOpacity(0.7)
        
        pen = QPen()
        pen.setWidth(2)
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
        for _, ship in self.ships.items():
            self.scene.removeItem(ship.shipItem)

        self.adjustedToSize = None
        resize = QResizeEvent(self.size(), self.size())
        QApplication.postEvent(self, resize)


    def placedShipsCount(self):
        return self.placedShips.count()


    def hideShips(self):
        for ship in self.placedShips:
            self.scene.removeItem(ship)


    def resizeEvent(self, event):
        size = event.size()
        if size == self.adjustedToSize:
            return

        self.adjustedToSize = size

        nowWidth = size.width()
        nowHeight = size.height()

        width = min(nowWidth, nowHeight * self.ratio)
        height = min(nowHeight, nowWidth / self.ratio)

        h_margin = round((nowWidth - width) / 2) - 2
        v_margin = round((nowHeight - height) / 2) - 2

        self.setContentsMargins(QMargins(h_margin, v_margin, h_margin, v_margin))
        self.__resizeScene()


    def __resizeScene(self):
        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()
        self.scene.setSceneRect(0, 0, width, height)

        self.tileSize = min(width / 11, height / (11 / self.ratio))
        self.scaleFactor = self.tileSize / self.originalTileSize

        for i, cell in enumerate(self.field):
            x = i % 10
            y = i // 10
            cell.setScale(self.scaleFactor)
            cell.setPos((x+1)*self.tileSize, (y + 1) * self.tileSize)

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
        for _, ship in self.shipList.items():
            xPos += (ship.length - 1)
            xOffset = xPos * self.tileSize
            
            ship.shipItem.setScale(self.scaleFactor)
            ship.shipItem.setPos(self.tileSize + xOffset, self.tileSize * (12 + self.EPS))
            
            ship.counterItem.setScale(self.scaleFactor)
            ship.counterItem.setPos(self.tileSize + xOffset, self.tileSize * (12.65 + self.EPS))
            
            counterSize = ship.counterItem.boundingRect()
            textSize = ship.counterText.boundingRect()
            textXOffset = (counterSize.width() - textSize.width()) * self.scaleFactor / 2
            textYOffset = (counterSize.height() - textSize.height()) * self.scaleFactor / 2
            textX = ship.counterItem.pos().x() + textXOffset
            textY = ship.counterItem.pos().y() + textYOffset
            ship.counterText.setScale(self.scaleFactor)
            ship.counterText.setPos(textX, textY)

        for ship in self.placedShips:
            mapPos = ship.data(2)
            ship.setPos(
                (mapPos.x() + 1) * self.tileSize,
                (mapPos.y() + 1) * self.tileSize
            )
            ship.setScale(self.scaleFactor)

        shipListX = self.tileSize
        shipListY = self.tileSize * (11 + self.EPS)
        self.shipListItem.setScale(self.scaleFactor)
        self.shipListItem.setPos(shipListX, shipListY)
        self.ghostShip.setScale(self.scaleFactor)


    def eventFilter(self, obj, event):
        if obj is self.ui.graphicsView.viewport():
            if event.type() == QEvent.MouseButtonPress:
                self.__viewportMousePressEvent(event)
            elif event.type() == QEvent.MouseButtonRelease:
                self.__viewportMouseReleaseEvent(event)
            elif event.type() == QEvent.MouseMove:
                self.__viewportMouseMoveEvent(event)

        return super().eventFilter(obj, event)


    def sceneToMap(self, x, y):
        x -= self.tileSize
        y -= self.tileSize
        x //= self.tileSize
        y //= self.tileSize
        return int(x), int(y)


    def __initGhostShip(self, ship, pos):
        self.ghostShip.setPixmap(QPixmap.fromImage(ship.image))
        self.ghostShip.setPos(pos)
        self.ghostShip.setRotation(0)
            
        width = self.ghostShip.boundingRect().width()
        height = self.ghostShip.boundingRect().height()
        self.ghostShip.setOffset(-width / 2, -height / 2)
        self.ghostShip.setData(0, Rotation.UP)
        self.ghostShip.setData(1, ship)

        self.placer.setRect(0, 0, self.tileSize, self.tileSize * ship.length)
        self.placer.setZValue(50)

        self.scene.addItem(self.ghostShip)
        self.ghostShip.setZValue(100)


    def __rotateGhostShip(self, rotation = None):
        if rotation:
            new_rot = rotation
        else:
            old_rot = self.ghostShip.data(0)
            new_rot = Rotation((old_rot.value + 1) % len(Rotation))
        self.ghostShip.setData(0, new_rot)
        self.ghostShip.setRotation((new_rot.value + 1) * 90)

        placerRect = self.placer.rect()
        self.placer.setRect(0, 0, placerRect.height(), placerRect.width())
        self.__validatePlacer()


    def __ghostShipLongSurface(self):
        pos = self.ghostShip.pos()
        x = pos.x()
        y = pos.y()
        rot = self.ghostShip.data(0)
        length = self.ghostShip.data(1).length
        if rot == Rotation.LEFT or rot == Rotation.RIGHT:
            x -= self.tileSize * length / 2
            return x, y

        if rot == Rotation.UP or rot == Rotation.DOWN:
            y -= self.tileSize * length / 2
            return x, y


    def __validatePlacer(self):
        sceneX, sceneY = self.__ghostShipLongSurface()
        x, y = self.sceneToMap(sceneX, sceneY)
        self.placer.setPos((x + 1) * self.tileSize, (y + 1) * self.tileSize)

        permittedArea = QRectF(self.ui.graphicsView.viewport().geometry())
        permittedArea.setTopLeft(QPointF(self.tileSize, self.tileSize))
        permittedArea.setBottomRight(QPointF(self.tileSize * 12, self.tileSize * 12))
        placerSize = self.placer.boundingRect()
        placerRect = QRectF(sceneX, sceneY, placerSize.width(), placerSize.height())

        isPlacerValid = False
        # first validation - ship can be placed inside game field
        if permittedArea.contains(self.ghostShip.pos()) and permittedArea == permittedArea.united(placerRect):
            if self.placer.scene() == None:
                self.scene.addItem(self.placer)
            x, y = self.sceneToMap(sceneX, sceneY)
            self.placer.setPos((x + 1) * self.tileSize, (y + 1) * self.tileSize)
            isPlacerValid = True
            
        else:
            if self.placer.scene() == self.scene:
                self.scene.removeItem(self.placer)

        # second validation - placer does not intersect with other ships
        if isPlacerValid:
            for ship in self.placedShips:
                shipRect = ship.mapRectToScene(ship.boundingRect())
                placerRect = self.placer.mapRectToScene(self.placer.boundingRect())
                isPlacerValid = not placerRect.intersects(shipRect)
                if not isPlacerValid: break

        # set color of placer
        pen = self.placer.pen()
        if isPlacerValid:
            pen.setColor(Qt.GlobalColor.darkGreen)
        else:
            pen.setColor(Qt.GlobalColor.red)
        self.placer.setPen(pen)
        self.placer.setData(0, isPlacerValid)


    def __placeShip(self):
        isPlacingPermitted = self.placer.data(0)
        if isPlacingPermitted:
            sceneX = self.placer.pos().x() + self.tileSize / 2
            sceneY = self.placer.pos().y() + self.tileSize / 2
            mapX, mapY = self.sceneToMap(sceneX, sceneY)
            rotation = self.ghostShip.data(0)
            if rotation == Rotation.RIGHT or rotation == Rotation.LEFT:
                vertical = True
            else: vertical = False

            shipListItem = self.ghostShip.data(1)
            shipListItem.count -= 1
            shipListItem.counterText.setPlainText(str(shipListItem.count))
                        
            angle = (rotation.value + 1) * 90
            pixmap = QPixmap(shipListItem.image).transformed(QTransform().rotate((angle)))
            placedShip = QGraphicsPixmapItem(pixmap)
            placedShip.setData(0, self.ghostShip.data(0))
            placedShip.setData(1, shipListItem)
            placedShip.setData(2, QPoint(mapX, mapY))  # position in map coordinates

            placedShip.setPos(self.placer.pos())
            placedShip.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
            placedShip.setScale(self.scaleFactor)

            self.placedShips.append(placedShip)
            self.scene.addItem(placedShip)

            self.shipPlaced.emit(Ship(
                name=shipListItem.name,
                length=shipListItem.length,
                pos=QPoint(mapX, mapY),
                vertical=vertical
            ))


    def __viewportMousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.shipListItem.scene():
                # check press on shiplist
                shipUnderMouse = None
                for _, ship in self.shipList.items():
                    if ship.shipItem.isUnderMouse():
                        shipUnderMouse = ship
                        break

                # check pres on field
                rotation = Rotation.RIGHT
                if shipUnderMouse == None:
                    for ship in self.placedShips:
                        if ship.isUnderMouse():
                            rotation = ship.data(0)
                            shipListItem = ship.data(1)
                            shipListItem.count += 1
                            shipListItem.counterText.setPlainText(str(shipListItem.count))
                            shipUnderMouse = shipListItem
                            self.placedShips.remove(ship)
                            self.scene.removeItem(ship)
                            break

            # if ship grabbed
            if shipUnderMouse and shipUnderMouse.count > 0:
                self.__initGhostShip(shipUnderMouse, event.pos())
                self.__rotateGhostShip()
                self.dragShip = True

        if event.button() == Qt.MouseButton.RightButton:
            if self.dragShip:
                self.__rotateGhostShip()

 
    def __viewportMouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.dragShip:
                self.scene.removeItem(self.ghostShip)
                self.dragShip = False
            if self.placer.scene() != None:
                self.scene.removeItem(self.placer)

            self.__placeShip()
            self.placer.setData(0, False)
        

    def __viewportMouseMoveEvent(self, event):
        if self.dragShip:
            self.ghostShip.setPos(event.pos())

            permittedArea = QRectF(self.ui.graphicsView.viewport().geometry())
            permittedArea.setTopLeft(QPointF(self.tileSize, self.tileSize))

            if not permittedArea.contains(event.pos()):
                self.scene.removeItem(self.ghostShip)
                self.dragShip = False

            self.__validatePlacer()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(os.path.join(Environment.Resources.path(), "fonts", "Roboto", "Roboto-Bold.ttf"))
    
    widget = GameArea()
    widget.show()

    sys.exit(app.exec_())