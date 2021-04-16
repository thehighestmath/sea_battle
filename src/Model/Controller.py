import logging
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

log = logging.getLogger("GameArea")

class Controller(QObject):
    hit = pyqtSignal(int, int)
    
    def __init__(self):
        super(Controller, self).__init__()
        self.__lastHit = None

    def emitHit(self, x, y):
        log.debug(f"emit hit on ({x}, {y})")
        self.__lastHit = (x, y)
        self.hit.emit(x, y)

    def _accept(self):
        raise NotImplementedError()

    def _decline(self):
        raise NotImplementedError()

    def accept(self):
        if self.__lastHit is None:
            raise LookupError("Event already handled")

        x, y = self.__lastHit
        self.__lastHit = None
        self._accept(x, y)

    def decline(self):
        if self.__lastHit is None:
            raise LookupError("Event already handled")

        x, y = self.__lastHit
        self.__lastHit = None
        self._decline(x, y)


if __name__ == "__main__":
    pass
