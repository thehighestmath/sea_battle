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
from Model.Controller import Controller

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
        self.name     = name
        self.length   = length
        self.pos      = pos
        self.vertical = vertical


class Rotation(Enum):
    RIGHT   = 90
    DOWN    = 180
    LEFT    = 270
    UP      = 0


    def next(self):
        value = self.value + 90
        if value > 270:
            value = 0
        return Rotation(value)


    def prev(self):
        value = self.value - 90
        if value < 0:
            value = 270
        return Rotation[self]


    def isVertical(self):
        return self == Rotation.UP or self == Rotation.DOWN

    
    def isHorizontal(self):
        return self == Rotation.LEFT or self == Rotation.RIGHT


class GameArea(QWidget):
    #constants of widget
    RATIO_WITH_SHIPLIST = 11 / 14
    RATIO_WITHOUT_SHIPLIST = 1
    EPS = 0.3

    #signals
    shipPlaced = pyqtSignal(Ship)

    def __init__(self, parent = None):
        super(GameArea, self).__init__(parent)
        # super().__init__(self, parent)
        self.__ui = Ui_GameArea()
        self.__ui.setupUi(self)

        self.__ratio = self.RATIO_WITH_SHIPLIST
        self.__scaleFactor = 1

        self.controller = Controller()
        self.controller._accept = self.__accept
        self.controller._decline = self.__decline

        self.__shipList = {
            "boat":         ShipListItem(length=1, name="boat",       count=4),
            "destroyer":    ShipListItem(length=2, name="destroyer",  count=3),
            "cruiser":      ShipListItem(length=3, name="cruiser",    count=2),
            "battleship":   ShipListItem(length=4, name="battleship", count=1),
        }

        # resources
        self.__cellImages = {
            "intact":       None,
            "hit":          None,
            "miss":         None
        }
        self.__originalTileSize = 0
        self.tileSize = 0

        self.__shipListImage = QImage()
        self.__counterImage = QImage()

        # drawing items
        self.__placedShips = []
        self.__field       = [QGraphicsPixmapItem() for _ in range(100)]
        self.__letters     = [QGraphicsTextItem()   for _ in range(10) ]
        self.__numbers     = [QGraphicsTextItem()   for _ in range(10) ]
     
        self.__shipListItem = QGraphicsPixmapItem()
        self.__ghostShip = QGraphicsPixmapItem() # data: 0 - rotation; 1 - ShipListItem
        self.__placer = QGraphicsRectItem()
        self.__dragShip = False

        # prepare Qt objects
        self.__scene = QGraphicsScene()
        self.__loadResources()
        self.__initGraphicsView()
        self.__adjustedToSize = 0

        self.shuffleShips()


    def __loadResources(self):
        if DEBUG_RESOURCE:
            resourcesPath = os.path.join(os.path.dirname(__file__), DEBUG_RESOURCE)
        else:
            resourcesPath = Environment.Resources.path()

        first = True
        for imageName in self.__cellImages:
            image = QImage(os.path.join(resourcesPath, "img", "cells", f"{imageName}.png"))
            if first:
                first = False
                self.__originalTileSize = min(image.width(), image.height())
            else:
                self.__originalTileSize = min(self.__originalTileSize, image.width(), image.height())
            self.__cellImages[imageName] = image

        for shipName, ship in self.__shipList.items():
            ship.image = QImage(os.path.join(resourcesPath, "img", "ships", f"{shipName}.png"))

        self.__shipListImage = QImage(os.path.join(
            resourcesPath,
            "img",
            "backgrounds",
            "shiplist.png"
        ))
        self.__counterImage = QImage(os.path.join(
            resourcesPath,
            "img",
            "miscellaneous",
            "shipcounter.png"
        ))


    def __initGraphicsView(self):
        self.__ui.graphicsView.setScene(self.__scene)
        self.__ui.graphicsView.viewport().installEventFilter(self)
        self.__ui.graphicsView.setRenderHints(
            QPainter.RenderHint.HighQualityAntialiasing |
            QPainter.RenderHint.TextAntialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        self.__ui.graphicsView.horizontalScrollBar().blockSignals(True)
        self.__ui.graphicsView.verticalScrollBar().blockSignals(True)
        
        for cell in self.__field:
            cell.setData(0, "intact")
            pixmap = QPixmap.fromImage(self.__cellImages["intact"])
            cell.setPixmap(pixmap)
            cell.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
            self.__scene.addItem(cell)

        ca_letters = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]
        # ca_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        ca_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        font = QFont("Roboto")
        font.setPixelSize(int(self.__originalTileSize * 0.8))
        for i in range(10):
            self.__letters[i].setPlainText(ca_letters[i])
            self.__letters[i].setFont(font)
            self.__numbers[i].setPlainText(ca_numbers[i])
            self.__numbers[i].setFont(font)
            self.__scene.addItem(self.__letters[i])
            self.__scene.addItem(self.__numbers[i])

        self.__shipListItem.setPixmap(QPixmap.fromImage(self.__shipListImage))
        self.__shipListItem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.__scene.addItem(self.__shipListItem)

        font.setPixelSize(int(self.__originalTileSize * 0.3))
        for _, ship in self.__shipList.items():
            t = QTransform().rotate(90)
            ship.shipItem.setPixmap(QPixmap.fromImage(ship.image).transformed(t))
            ship.shipItem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
            ship.counterItem.setPixmap(QPixmap.fromImage(self.__counterImage))
            ship.counterText.setPlainText(str(ship.count))
            ship.counterText.setFont(font)
            self.__scene.addItem(ship.shipItem)
            self.__scene.addItem(ship.counterItem)
            self.__scene.addItem(ship.counterText)

        self.__ghostShip.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.__ghostShip.setOpacity(0.7)
        
        pen = QPen()
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.__placer.setPen(pen)


    def hasHeightForWidth(self):
        return True


    def heightForWidth(self, width):
        return width / self.__ratio


    def hideShipList(self):
        self.__ratio = self.RATIO_WITHOUT_SHIPLIST
        self.__scene.removeItem(self.__shipListItem)
        for _, ship in self.__shipList.items():
            self.__scene.removeItem(ship.shipItem)

        self.__adjustedToSize = None
        resize = QResizeEvent(self.size(), self.size())
        QApplication.postEvent(self, resize)


    def placedShipsCount(self):
        return len(self.__placedShips)


    def hideShips(self):
        for ship in self.__placedShips:
            self.__scene.removeItem(ship)


    def removePlacedShips(self):
        if self.__shipListItem.scene() is None:
            return
        
        for ship in self.placedShipsCount:
            shipListItem = ship.data(1)
            shipListItem.count += 1 
            shipListItem.counterText.setPlainText(str(shipListItem.count))
            self.__placedShips.remove(ship)
            self.__scene.removeItem(ship)

       
    def shuffleShips(self):
        if self.__shipListItem.scene() is None:
            return

        # static placing
        for i in range(4):
            x = i*2
            y = 0
            rotation = Rotation.DOWN
            shipListItem = self.__shipList["boat"]
            self.__placeShip(shipListItem, x, y, rotation)

        for i in range(3):
            x = i*2
            y = 2
            rotation = Rotation.DOWN
            shipListItem = self.__shipList["destroyer"]
            self.__placeShip(shipListItem, x, y, rotation)

        for i in range(2):
            x = i*2
            y = 5
            rotation = Rotation.DOWN
            shipListItem = self.__shipList["cruiser"]
            self.__placeShip(shipListItem, x, y, rotation)

        for i in range(1):
            x = i*2
            y = 9
            rotation = Rotation.RIGHT
            shipListItem = self.__shipList["battleship"]
            self.__placeShip(shipListItem, x, y, rotation)

        # TODO: SHUFFLE
        pass


    def resizeEvent(self, event):
        size = event.size()
        if size == self.__adjustedToSize:
            return

        self.__adjustedToSize = size

        nowWidth = size.width()
        nowHeight = size.height()

        width = min(nowWidth, nowHeight * self.__ratio)
        height = min(nowHeight, nowWidth / self.__ratio)

        h_margin = round((nowWidth - width) / 2) - 2
        v_margin = round((nowHeight - height) / 2) - 2

        self.setContentsMargins(QMargins(h_margin, v_margin, h_margin, v_margin))
        self.__resizeScene()


    def __resizeScene(self):
        width = self.__ui.graphicsView.width()
        height = self.__ui.graphicsView.height()
        self.__scene.setSceneRect(0, 0, width, height)

        self.tileSize = min(width / 11, height / (11 / self.__ratio))
        self.__scaleFactor = self.tileSize / self.__originalTileSize

        for i, cell in enumerate(self.__field):
            x = i % 10
            y = i // 10
            cell.setScale(self.__scaleFactor)
            cell.setPos((x + 1) * self.tileSize, (y + 1) * self.tileSize)

        for i in range(10):
            letter = self.__letters[i]
            letter.setScale(self.__scaleFactor)
            offsetX = (self.tileSize - letter.boundingRect().width() * self.__scaleFactor) / 2 
            offsetY = (self.tileSize - letter.boundingRect().height() * self.__scaleFactor) / 2
            letter.setPos((i + 1) * self.tileSize + offsetX, offsetY)

            number = self.__numbers[i]
            number.setScale(self.__scaleFactor)
            offsetX = (self.tileSize - number.boundingRect().width() * self.__scaleFactor) / 2
            offsetY = (self.tileSize - number.boundingRect().height() * self.__scaleFactor) / 2
            number.setPos(offsetX, (i + 1) * self.tileSize + offsetY)

        xPos = 0
        for _, ship in self.__shipList.items():
            xPos += (ship.length - 1)
            xOffset = xPos * self.tileSize
            
            ship.shipItem.setScale(self.__scaleFactor)
            ship.shipItem.setPos(self.tileSize + xOffset, self.tileSize * (12 + self.EPS))
            
            ship.counterItem.setScale(self.__scaleFactor)
            ship.counterItem.setPos(self.tileSize + xOffset, self.tileSize * (12.65 + self.EPS))
            
            counterSize = ship.counterItem.boundingRect()
            textSize = ship.counterText.boundingRect()
            textXOffset = (counterSize.width() - textSize.width()) * self.__scaleFactor / 2
            textYOffset = (counterSize.height() - textSize.height()) * self.__scaleFactor / 2
            textX = ship.counterItem.pos().x() + textXOffset
            textY = ship.counterItem.pos().y() + textYOffset
            ship.counterText.setScale(self.__scaleFactor)
            ship.counterText.setPos(textX, textY)

        for ship in self.__placedShips:
            mapPos = ship.data(2)
            ship.setPos(
                (mapPos.x() + 1) * self.tileSize,
                (mapPos.y() + 1) * self.tileSize
            )
            ship.setScale(self.__scaleFactor)

        shipListX = self.tileSize
        shipListY = self.tileSize * (11 + self.EPS)
        self.__shipListItem.setScale(self.__scaleFactor)
        self.__shipListItem.setPos(shipListX, shipListY)
        self.__ghostShip.setScale(self.__scaleFactor)


    def eventFilter(self, obj, event):
        if obj is self.__ui.graphicsView.viewport():
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
        self.__ghostShip.setPixmap(QPixmap.fromImage(ship.image))
        self.__ghostShip.setPos(pos)
        self.__ghostShip.setRotation(0)
            
        width = self.__ghostShip.boundingRect().width()
        height = self.__ghostShip.boundingRect().height()
        self.__ghostShip.setOffset(-width / 2, -height / 2)
        self.__ghostShip.setData(0, Rotation.UP)
        self.__ghostShip.setData(1, ship)

        self.__placer.setRect(0, 0, self.tileSize, self.tileSize * ship.length)
        self.__placer.setZValue(50)

        self.__scene.addItem(self.__ghostShip)
        self.__ghostShip.setZValue(100)


    def __rotateGhostShip(self, rotation=None):
        rotation = rotation if rotation else self.__ghostShip.data(0).next()
        self.__ghostShip.setData(0, rotation)
        self.__ghostShip.setRotation(rotation.value)

        placerRect = self.__placer.rect()
        maxSide = max(placerRect.width(), placerRect.height())
        minSide = min(placerRect.width(), placerRect.height())

        if rotation.isHorizontal():
            self.__placer.setRect(0, 0, maxSide, minSide)
        elif rotation.isVertical():
            self.__placer.setRect(0, 0, minSide, maxSide)
        else:
            raise Exception("Unknown state! Rotation is not horizontal and not vertical.")  # wtf
        self.__validatePlacer()


    def __ghostShipLongSurface(self):
        pos = self.__ghostShip.pos()
        x = pos.x()
        y = pos.y()
        rot = self.__ghostShip.data(0)
        length = self.__ghostShip.data(1).length
        if rot == Rotation.LEFT or rot == Rotation.RIGHT:
            x -= self.tileSize * length / 2
            return x, y

        if rot == Rotation.UP or rot == Rotation.DOWN:
            y -= self.tileSize * length / 2
            return x, y

    def __validatePosition(self, x, y):
        isPlacerValid = True
        for ship in self.__placedShips:
            shipRect = ship.mapRectToScene(ship.boundingRect())
            positionRect = QRectF((x + 1) * self.tileSize, (y + 1) * self.tileSize, self.tileSize, self.tileSize)
            isPlacerValid = not positionRect.intersects(shipRect)
            if not isPlacerValid:
                break
        return isPlacerValid


    def __validatePlacer(self):
        sceneX, sceneY = self.__ghostShipLongSurface()
        x, y = self.sceneToMap(sceneX, sceneY)
        self.__placer.setPos((x + 1) * self.tileSize, (y + 1) * self.tileSize)

        permittedArea = QRectF(self.__ui.graphicsView.viewport().geometry())
        permittedArea.setTopLeft(QPointF(self.tileSize, self.tileSize))
        permittedArea.setBottomRight(QPointF(self.tileSize * 12, self.tileSize * 12))
        placerSize = self.__placer.boundingRect()
        placerRect = QRectF(sceneX, sceneY, placerSize.width(), placerSize.height())

        isPlacerValid = False
        # first validation - ship can be placed inside game field
        if permittedArea.contains(self.__ghostShip.pos()) and permittedArea == permittedArea.united(placerRect):
            if self.__placer.scene() == None:
                self.__scene.addItem(self.__placer)
            x, y = self.sceneToMap(sceneX, sceneY)
            self.__placer.setPos((x + 1) * self.tileSize, (y + 1) * self.tileSize)
            isPlacerValid = True
            
        else:
            if self.__placer.scene() == self.__scene:
                self.__scene.removeItem(self.__placer)

        # second validation - placer does not intersect with other ships
        if isPlacerValid:
            x, y = self.__placer.pos().x(), self.__placer.pos().y()
            x, y = self.sceneToMap(x, y)
            isPlacerValid = self.__validatePosition(x, y)

        # set color of placer
        pen = self.__placer.pen()
        if isPlacerValid:
            pen.setColor(Qt.GlobalColor.darkGreen)
        else:
            pen.setColor(Qt.GlobalColor.red)
        self.__placer.setPen(pen)
        self.__placer.setData(0, isPlacerValid)


    def __placeShip(self, shipListItem, x, y, rotation):
        sceneX, sceneY = (x + 1) * self.tileSize, (y + 1) * self.tileSize

        shipListItem.count -= 1
        shipListItem.counterText.setPlainText(str(shipListItem.count))

        pixmap = QPixmap(shipListItem.image).transformed(QTransform().rotate((rotation.value)))
        placedShip = QGraphicsPixmapItem(pixmap)
        placedShip.setData(0, rotation)
        placedShip.setData(1, shipListItem)
        placedShip.setData(2, QPoint(x, y))  # position in map coordinates

        placedShip.setPos(sceneX, sceneY)
        placedShip.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        placedShip.setScale(self.__scaleFactor)

        self.__placedShips.append(placedShip)
        self.__scene.addItem(placedShip)


    def __placeGhostShip(self):
        isPlacingPermitted = self.__placer.data(0)
        if isPlacingPermitted:
            sceneX = self.__placer.pos().x() + self.tileSize / 2
            sceneY = self.__placer.pos().y() + self.tileSize / 2
            mapX, mapY = self.sceneToMap(sceneX, sceneY)
            rotation = self.__ghostShip.data(0)
            if rotation.isVertical():
                vertical = True
            elif rotation.isHorizontal():
                vertical = False
            else:
                raise Exception("Unknown state! Rotation is not horizontal and not vertical.")  # wtf

            shipListItem = self.__ghostShip.data(1)
            self.__placeShip(shipListItem, mapX, mapY, rotation)

            log.debug(
                f"ship \"{shipListItem.name}\"; "
                f"position ({mapX}, {mapY}); "
                f"oriented {'vertically' if vertical else 'horizontally'}"
            )

            self.shipPlaced.emit(Ship(
                name=shipListItem.name,
                length=shipListItem.length,
                pos=QPoint(mapX, mapY),
                vertical=vertical
            ))


    def __viewportMousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.__shipListItem.scene():
                # check press on shiplist
                shipUnderMouse = None
                for _, ship in self.__shipList.items():
                    if ship.shipItem.isUnderMouse():
                        shipUnderMouse = ship
                        break

                # check press on field
                rotation = Rotation.RIGHT
                if shipUnderMouse == None:
                    for ship in self.__placedShips:
                        if ship.isUnderMouse():
                            rotation = ship.data(0)
                            shipListItem = ship.data(1)
                            shipListItem.count += 1
                            shipListItem.counterText.setPlainText(str(shipListItem.count))
                            shipUnderMouse = shipListItem
                            self.__placedShips.remove(ship)
                            self.__scene.removeItem(ship)
                            break

                # if ship grabbed
                if shipUnderMouse and shipUnderMouse.count > 0:
                    self.__initGhostShip(shipUnderMouse, event.pos())
                    self.__rotateGhostShip(rotation)
                    self.__dragShip = True

            x, y = self.sceneToMap(event.pos().x(), event.pos().y())
            if x >= 0 and x < 10 and y >= 0 and y < 10:
                self.controller.emitHit(x, y)

        if event.button() == Qt.MouseButton.RightButton:
            if self.__dragShip:
                self.__rotateGhostShip()

 
    def __viewportMouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.__dragShip:
                self.__scene.removeItem(self.__ghostShip)
                self.__dragShip = False
            if self.__placer.scene() != None:
                self.__scene.removeItem(self.__placer)

            # self.__placeShip()
            self.__placeGhostShip()
            self.__placer.setData(0, False)
        

    def __viewportMouseMoveEvent(self, event):
        if self.__dragShip:
            self.__ghostShip.setPos(event.pos())

            permittedArea = QRectF(self.__ui.graphicsView.viewport().geometry())
            permittedArea.setTopLeft(QPointF(self.tileSize, self.tileSize))

            if not permittedArea.contains(event.pos()):
                self.__scene.removeItem(self.__ghostShip)
                self.__dragShip = False

            self.__validatePlacer()

    
    def __accept(x, y):
        log.debug(f"accepted hit on point ({x}, {y})")


    def __decline(x, y):
        log.debug(f"declined hit on point ({x}, {y})")



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(os.path.join(Environment.Resources.path(), "fonts", "Roboto", "Roboto-Bold.ttf"))
    
    widget = GameArea()
    widget.show()

    sys.exit(app.exec_())