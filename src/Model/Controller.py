import logging
from collections import deque

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

log = logging.getLogger("GameArea")


class Controller(QObject):
    hit = pyqtSignal(QObject, int, int)

    def __init__(self):
        super(Controller, self).__init__()
        self.__lastHit = deque()
        self.isBot = False

    def onBot(self):
        self.isBot = True

    def emitHit(self, x, y):
        log.debug(f"emit hit on ({x}, {y})")
        self.__lastHit.append((x, y))
        self.hit.emit(self, x, y)

    def _accept(self, x, y, hit_type):
        raise NotImplementedError()

    def _decline(self, x, y):
        raise NotImplementedError()

    def accept(self, hit_type):
        if not self.__lastHit:
            raise LookupError("Event already handled")

        x, y = self.__lastHit.popleft()
        self._accept(x, y, hit_type)

    def decline(self):
        if not self.__lastHit:
            raise LookupError("Event already handled")

        x, y = self.__lastHit.popleft()
        self._decline(x, y)


if __name__ == "__main__":
    pass
