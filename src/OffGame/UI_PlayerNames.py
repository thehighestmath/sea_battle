from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class UI_PlayerNames(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Form")
        Widget.resize(800, 600)
        self.lineEdit = QLineEdit(Widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(360, 240, 151, 31))
        font = QFont()
        font.setPointSize(14)
        self.lineEdit.setStyleSheet('color: black')
        self.lineEdit.setFont(font)
        self.lineEdit.setMaxLength(20)
        self.lineEdit_2 = QLineEdit(Widget)
        self.lineEdit_2.setStyleSheet('color: black')
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(360, 280, 151, 31))
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(20)
        self.label = QLabel(Widget)
        self.label.setStyleSheet('color: black')
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(190, 130, 410, 51))
        font1 = QFont()
        font1.setPointSize(26)
        self.label.setFont(font1)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label_2 = QLabel(Widget)
        self.label_2.setStyleSheet('color: black')
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(260, 240, 81, 31))
        self.label_2.setFont(font)
        self.label_3 = QLabel(Widget)
        self.label_3.setStyleSheet('color: black')
        self.label_3.setStyleSheet('color: black')
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(260, 280, 81, 31))
        self.label_3.setFont(font)
        self.pushButton = QPushButton(Widget)
        self.pushButton.setStyleSheet('color: black')
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(320, 350, 131, 41))
        self.pushButton.setFont(font)
        self.pushButton_2 = QPushButton(Widget)
        self.pushButton_2.setStyleSheet('color: black')
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(10, 20, 131, 41))
        self.pushButton_2.setFont(font)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Enter name", u"Enter name", None))
        self.label.setText(QCoreApplication.translate("Enter name", u"Введите имена игроков", None))
        self.label_2.setText(QCoreApplication.translate("Enter name", u"Игрок 1:", None))
        self.label_3.setText(QCoreApplication.translate("Enter name", u"Игрок 2:", None))
        self.pushButton.setText(QCoreApplication.translate("Enter name", u"Начать игру", None))
        self.pushButton_2.setText(QCoreApplication.translate("Enter name", u"Меню", None))
    # retranslateUi

