from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class UI_AiChoose(object):
    def setupUi(self, UI_AiChoose):
        if not UI_AiChoose.objectName():
            UI_AiChoose.setObjectName(u"UI_AI_Choose")
        self.pushButton = QPushButton(UI_AiChoose)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 20, 131, 41))
        font = QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet('color: black')
        self.label = QLabel(UI_AiChoose)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(220, 90, 371, 61))
        self.label.setStyleSheet('color: black')
        font1 = QFont()
        font1.setPointSize(26)
        self.label.setFont(font1)
        self.pushButton_2 = QPushButton(UI_AiChoose)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(311, 221, 179, 32))
        self.pushButton_2.setStyleSheet('color: black')
        self.pushButton_2.setFont(font)
        self.pushButton_3 = QPushButton(UI_AiChoose)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(311, 257, 179, 33))
        self.pushButton_3.setStyleSheet('color: black')

        self.pushButton_3.setFont(font)
        self.pushButton_4 = QPushButton(UI_AiChoose)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(311, 294, 179, 32))
        self.pushButton_4.setStyleSheet('color: black')

        self.pushButton_4.setFont(font)

        self.retranslateUi(UI_AiChoose)

        QMetaObject.connectSlotsByName(UI_AiChoose)

    # setupUi

    def retranslateUi(self, UI_AiChoose):
        UI_AiChoose.setWindowTitle(QCoreApplication.translate("UI_AI_Choose", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("UI_AI_Choose", u"Назад", None))
        self.label.setText(QCoreApplication.translate("UI_AI_Choose",
                                                      u"Выберите сложность",
                                                      None))
        self.pushButton_2.setText(QCoreApplication.translate("UI_AI_Choose",
                                                             u"Простой уровень",
                                                             None))
        self.pushButton_3.setText(QCoreApplication.translate("UI_AI_Choose",
                                                             u"Средний уровень",
                                                             None))
        self.pushButton_4.setText(QCoreApplication.translate("UI_AI_Choose",
                                                             u"Сложный уровень",
                                                             None))
    # retranslateUi
