import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from MainWindow import MainWindow
import Environment

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(os.path.join(Environment.Resources.path(), "fonts", "Roboto", "Roboto-Bold.ttf"))
    ex = MainWindow()
    sys.exit(app.exec_())
