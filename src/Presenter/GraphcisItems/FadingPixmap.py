from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QLinearGradient
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal


class FadingPixmapItem(QGraphicsItem):
    def __init__(self, pixmap = None, parent=None):
        super(FadingPixmapItem, self).__init__(parent)

        self.__pixmap = pixmap
        if self.__pixmap is None:
            self.__pixmap = QPixmap()

        self.__boundingRect = QRectF(self.__pixmap.rect())

        self.__opacity = 100
        self.__opacitySpeed = 3

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__changeOpacity)
        self.__timer.start(17)

    def setPixmap(pixmap):
        if pixmap is None:
            raise ValueError("pixmap is None")
        self.__pixmap = pixmap
        self.__boundingRect = QRectF(__pixmap.rect())

    def setSize(width, height):
        self.__boundingRect = QRectF(0, 0, width, height)

    def __changeOpacity(self):
        self.__opacity -= self.__opacitySpeed
        if self.__opacity <= 0:
            self.__opacity = 100
        self.update(self.__boundingRect)

    def boundingRect(self):
        return self.__boundingRect

    def paint(self, painter, style_option, widget):
        painter.setOpacity(self.__opacity / 100)
        width = self.__boundingRect.width()
        height = self.__boundingRect.height()
        painter.drawPixmap(
            0, 0, width, height,
            self.__pixmap,
            0, 0, self.__pixmap.width(), self.__pixmap.height()
        )


if __name__ == "__main__":
    pass