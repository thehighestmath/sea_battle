import logging
import os
import sys

from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

# inner project imports
import Environment
from OffGame.ui_GameOverWidget import Ui_GameOverWidget


class GameOverWidget(QWidget):
    def __init__(self, player, parent=None):
        super(GameOverWidget, self).__init__(parent)
        self.ui = Ui_GameOverWidget()
        self.ui.setupUi(self)

        resourcePath = Environment.Resources.path()
        imagePath = os.path.join(resourcePath, "img", "miscellaneous", "game_over.png")
        pixmap = QPixmap(imagePath)

        font = QFont("Roboto")
        font.setPixelSize(25)
        self.ui.label.setFont(font)
        self.ui.label.setText(f"Выиграл {player}!")

        self.ui.image.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    widget = GameOverWidget("DEBIL")
    widget.show()
    sys.exit(app.exec_())
