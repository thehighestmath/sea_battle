# This Python file uses the following encoding: utf-8
import sys
import os

# use PyQt5
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QWidget, QGraphicsScene
from PyQt5.QtCore import Qt, QSize, QVariant
from PyQt5.QtGui import QImage, QIcon, QPixmap

from ui_ShipListWidget import Ui_ShipListWidget

DEBUG_RESOURCE = ""

def ShipMimeType():
    return "image/x-ship"

class ShipListWidget(QWidget):
    def __init__(self, parent = None):
        super(ShipListWidget, self).__init__(parent)
        self.ui = Ui_ShipListWidget()
        self.ui.setupUi(self)

        self.remained1 = 4
        self.remained2 = 3
        self.remained3 = 2
        self.remained4 = 1

        self.LoadResources()
        self.CreateGraphicsView()

        self.setMouseTracking(True)


    def mousePressEvent(self, event):
        print("press")


    def LoadResources(self):
        pass


    def CreateGraphicsView(self):
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.ui.graphicsView.setScene(self.scene)


    def addShip(self, pixmap):
        pass


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(ShipMimeType()):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat(ShipMimeType()):
            event.setDropAction(Qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasFormat(ShipMimeType()):
            event.accept()
        else:
            event.ignore()


    def startDrag(self, supported_actions):
        print("start drag")
        pass




if __name__ == "__main__":
    DEBUG_RESOURCE = os.path.join(os.path.dirname(__file__), "res")

    app = QApplication([])
    widget = ShipListWidget()

    ship1 = QPixmap(DEBUG_RESOURCE, "PNG")
    ship2 = QPixmap(DEBUG_RESOURCE, "PNG")
    ship3 = QPixmap(DEBUG_RESOURCE, "PNG")
    ship4 = QPixmap(DEBUG_RESOURCE, "PNG")
    ship5 = QPixmap(DEBUG_RESOURCE, "PNG")

    widget.show()
    sys.exit(app.exec_())
