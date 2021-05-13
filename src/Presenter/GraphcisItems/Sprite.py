from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QTimer


class SpriteItem(QGraphicsItem):
    def __init__(self, parent=None):
        super(SpriteItem, self).__init__(parent)
        self.__spritePixmap = None
        self.__currentFrame = 0
        self.__boundingRect = QRectF(0, 0, 0, 0)
        
        self.__frameCount = 0
        self.__loopAnimation = False

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__nextFrame)

        self.__animationFinishedCallback = None

    def __nextFrame(self):
        self.__currentFrame += 1
        isAnimationFinished = False
        if self.__currentFrame >= self.__frameCount:
            self.__currentFrame = 0
            isAnimationFinished = True
            
        self.update(self.__boundingRect)

        if isAnimationFinished and not self.__loopAnimation:
            if(self.__animationFinishedCallback):
                self.__animationFinishedCallback()

    def startAnimation(self, frame_length, loop, animationFinishedCallback = None):
        self.__timer.start(frame_length)
        self.__loopAnimation = loop
        self.__animationFinishedCallback = animationFinishedCallback

    def stopAnimation(self):
        self.__timer.stop()

    def setSpriteMap(self, pixmap, height, width, count):
        self.__frameCount = count
        self.__spritePixmap = pixmap
        self.__boundingRect = QRectF(0, 0, width, height)

    def boundingRect(self):
        return self.__boundingRect

    def paint(self, painter, style_option, widget):
        width = self.__boundingRect.width()
        height = self.__boundingRect.height()
        
        sourceRect = QRectF(width * self.__currentFrame, 0, width, height)
        painter.drawPixmap(
            self.__boundingRect,
            self.__spritePixmap,
            sourceRect
        )


if __name__ == "__main__":
    pass