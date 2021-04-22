import logging
import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QStyle
from PyQt5.QtCore import Qt

import Environment
from MainWindow import MainWindow

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(os.path.join(Environment.Resources.path(), "fonts", "Roboto", "Roboto-Bold.ttf"))
    window = MainWindow()
    window.setGeometry(QStyle.alignedRect(
        Qt.LeftToRight,
        Qt.AlignCenter,
        window.size(),
        app.desktop().availableGeometry()
    ))
    window.show()
    sys.exit(app.exec_())
