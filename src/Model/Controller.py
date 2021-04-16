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

    def emitHit(self, x, y):
        log.debug(f"emit hit on ({x}, {y})")
        self.__lastHit.append((x, y))
        self.hit.emit(self, x, y)
        print(self.__lastHit)

    def _accept(self):
        raise NotImplementedError()

    def _decline(self):
        raise NotImplementedError()

    def accept(self):
        if not self.__lastHit:
            raise LookupError("Event already handled")

        x, y = self.__lastHit.popleft()
        self._accept(x, y)

    def decline(self):
        if not self.__lastHit:
            raise LookupError("Event already handled")

        x, y = self.__lastHit.popleft()
        self._decline(x, y)


if __name__ == "__main__":
    pass
