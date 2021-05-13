from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QLinearGradient
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal


class FloatingGradientItem(QGraphicsItem):
    def __init__(self, rect, finishCallback=None, parent=None):
        super(FloatingGradientItem, self).__init__(parent)
        self.__boundingRect = QRectF(0, 0, rect.width(), rect.height())
        self.setPos(rect.x(), rect.y())

        self.__front = 0.0
        self.__rear = 0.0

        self.__frontSpeed = 1.0
        self.__rearSpeed = 0

        self.__backwards = True

        self.__frontColor = QColor.fromRgb(0, 255, 0, 255)  # defualt green
        self.__rearColor = QColor.fromRgb(0, 0, 0, 0)  # default transparent

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__moveGradient)
        self.__timer.start(17)

        self.__finishCallback = finishCallback

    def setFrontSpeed(self, value):
        if value < 0 or value > 100:
            raise ValueError(f"value is {value}. Accepted [0, 100]")

        self.__frontSpeed = value

    def setRearSpeed(self, value):
        if value < 0 or value > 100:
            raise ValueError(f"value is {value}. Accepted [0, 100]")

        self.__rearSpeed = value

    def setBackwards(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"value is not a bool")
        self.__backwards = value

    def setWidth(self, width):
        self.__boundingRect.setWidth(width)

    def setHeight(self, height):
        self.__boundingRect.setHeight(height)

    def setSize(self, width, height):
        self.setWidth(width)
        self.setHeight(height)

    def __moveGradient(self):
        self.__front += self.__frontSpeed
        if self.__front > 100:
            self.__front = 100

        self.__rear += self.__rearSpeed
        if self.__rear > 100:
            self.__front = 0
            self.__rear = 0
            self.__rearSpeed = 0

        self.__rearSpeed += 2 * self.__frontSpeed**2 /  100
        self.update(self.__boundingRect)

        if self.__front < 0.00001 and self.__finishCallback:
            self.__finishCallback()

    def boundingRect(self):
        return self.__boundingRect

    def paint(self, painter, style_option, widget):
        frontPos = self.__boundingRect.height() * self.__front / 100
        rearPos = self.__boundingRect.height() * self.__rear / 100

        width = self.__boundingRect.width()
        height = self.__boundingRect.height()

        if self.__backwards:
            frontPos = height - frontPos
            rearPos = height - rearPos

        gradient = QLinearGradient(width / 2, frontPos, width / 2, rearPos) 
        gradient.setColorAt(0, self.__frontColor)
        gradient.setColorAt(1, self.__rearColor)

        painter.fillRect(QRectF(0, rearPos, width, frontPos - rearPos), gradient)


if __name__ == "__main__":
    pass