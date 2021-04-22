# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Git\sea_battle\src\OffGame\GameOverWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GameOverWidget(object):
    def setupUi(self, GameOverWidget):
        GameOverWidget.setObjectName("GameOverWidget")
        GameOverWidget.resize(771, 589)
        self.gridLayout = QtWidgets.QGridLayout(GameOverWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.layoutWidget = QtWidgets.QWidget(GameOverWidget)
        self.layoutWidget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image = QtWidgets.QLabel(self.layoutWidget)
        self.image.setText("")
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setObjectName("image")
        self.verticalLayout.addWidget(self.image)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setStyleSheet("QLabel{\n"
"margin: 20px;\n"
"font-size: 20px;\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newGameButton = QtWidgets.QPushButton(self.layoutWidget)
        self.newGameButton.setStyleSheet("QPushButton{\n"
"background: white;\n"
"border: none;\n"
"border: 1px solid #bbb;\n"
"max-width: 150px;\n"
"font-size: 20px;\n"
"padding: 10px 20px;\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: #bbb\n"
"}")
        self.newGameButton.setObjectName("newGameButton")
        self.horizontalLayout.addWidget(self.newGameButton)
        self.menuButton = QtWidgets.QPushButton(self.layoutWidget)
        self.menuButton.setStyleSheet("QPushButton{\n"
"background: white;\n"
"border: none;\n"
"border: 1px solid #bbb;\n"
"max-width: 150px;\n"
"font-size: 20px;\n"
"padding: 10px 20px;\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: #bbb\n"
"}")
        self.menuButton.setObjectName("menuButton")
        self.horizontalLayout.addWidget(self.menuButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 512, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.layoutWidget, 0, 0, 1, 1)

        self.retranslateUi(GameOverWidget)
        QtCore.QMetaObject.connectSlotsByName(GameOverWidget)

    def retranslateUi(self, GameOverWidget):
        _translate = QtCore.QCoreApplication.translate
        GameOverWidget.setWindowTitle(_translate("GameOverWidget", "Form"))
        self.label.setText(_translate("GameOverWidget", "DUMMY"))
        self.newGameButton.setText(_translate("GameOverWidget", "Новая игра"))
        self.menuButton.setText(_translate("GameOverWidget", "Главное меню"))