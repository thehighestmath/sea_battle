import logging
import os
import sys

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication

import Environment
from MainWindow import MainWindow

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(os.path.join(Environment.Resources.path(), "fonts", "Roboto", "Roboto-Bold.ttf"))
    ex = MainWindow()
    sys.exit(app.exec_())
