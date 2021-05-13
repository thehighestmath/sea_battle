import logging
import os
import sys

from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

# inner project imports
import Environment
from OffGame.ui_ScoreBoard import Ui_Scoreboard


class ScoreBoardWidget(QWidget):
    onExit = pyqtSignal()

    def __init__(self, parent=None):
        super(ScoreBoardWidget, self).__init__(parent)
        self.ui = Ui_Scoreboard()
        self.ui.setupUi(self)

        resourcePath = Environment.Resources.path()
        iconExit = QIcon(QPixmap(os.path.join(resourcePath, "img", "miscellaneous", "logout.png")))
        iconTrash = QIcon(QPixmap(os.path.join(resourcePath, "img", "miscellaneous", "trash.png")))

        self.ui.exit.setIcon(iconExit)
        self.ui.clean.setIcon(iconTrash)

        self.__font = QFont("Roboto")
        self.__font.setPixelSize(28)
        self.ui.pve_label.setFont(self.__font)
        self.ui.pvp_label.setFont(self.__font)

        self.ui.clean.clicked.connect(self.__clean)
        self.ui.exit.clicked.connect(lambda: self.onExit.emit())

        self.__draw()
        
    def __clean(self):
        Environment.ScoreBoard.write({"PVP": [], "PVE": []})
        self.onExit.emit()

    def __createLine(self, name, score, widget):
        lineLayout = QHBoxLayout()
        self.__font.setPixelSize(16)

        labelName = QLabel(self)
        labelName.setText(name)
        labelName.setFont(self.__font)

        labelScore = QLabel(self)
        labelScore.setText(str(score))
        labelScore.setFont(self.__font)

        horizontalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lineLayout.addWidget(labelName)
        lineLayout.addItem(horizontalSpacer)
        lineLayout.addWidget(labelScore)

        widget.layout().insertLayout(widget.layout().count() - 1, lineLayout)

    def __draw(self):
        sb = Environment.ScoreBoard.read()

        PVPsb = sb.get("PVP", [])
        PVEsb = sb.get("PVE", [])

        if PVPsb:
            top10 = sorted(PVPsb, key=lambda line: line["scores"], reverse=True)[:10]
            for line in top10:
                self.__createLine(line["name"], line["scores"], self.ui.pvp_lines)

        if PVEsb:
            top10 = sorted(PVEsb, key=lambda line: line["scores"], reverse=True)[:10]
            for line in top10:
                self.__createLine(line["name"], line["scores"], self.ui.pve_lines)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    widget = ScoreBoardWidget()
    widget.show()
    sys.exit(app.exec_())
