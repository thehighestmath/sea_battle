# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Git\sea_battle\src\OffGame\InitWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InitWidget(object):
    def setupUi(self, InitWidget):
        InitWidget.setObjectName("InitWidget")
        InitWidget.resize(696, 537)
        self.gridLayout = QtWidgets.QGridLayout(InitWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.layoutWidget = QtWidgets.QWidget(InitWidget)
        self.layoutWidget.setMaximumSize(QtCore.QSize(500, 500))
        self.layoutWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.layoutWidget.setStyleSheet("")
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.startGameLayout = QtWidgets.QHBoxLayout()
        self.startGameLayout.setObjectName("startGameLayout")
        self.PVP = QtWidgets.QPushButton(self.layoutWidget)
        self.PVP.setStyleSheet("QPushButton{\n"
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
        self.PVP.setObjectName("PVP")
        self.startGameLayout.addWidget(self.PVP)
        self.PVE = QtWidgets.QPushButton(self.layoutWidget)
        self.PVE.setStyleSheet("QPushButton{\n"
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
        self.PVE.setObjectName("PVE")
        self.startGameLayout.addWidget(self.PVE)
        self.verticalLayout.addLayout(self.startGameLayout)
        self.highscoreTableLayout = QtWidgets.QHBoxLayout()
        self.highscoreTableLayout.setObjectName("highscoreTableLayout")
        self.highscoreTable = QtWidgets.QPushButton(self.layoutWidget)
        self.highscoreTable.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.highscoreTable.setStyleSheet("QPushButton{\n"
"background: white;\n"
"border: none;\n"
"border: 1px solid #bbb;\n"
"max-width: 378px;\n"
"font-size: 20px;\n"
"padding: 10px 20px;\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: #bbb\n"
"}")
        self.highscoreTable.setObjectName("highscoreTable")
        self.highscoreTableLayout.addWidget(self.highscoreTable)
        self.verticalLayout.addLayout(self.highscoreTableLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.exit = QtWidgets.QPushButton(self.layoutWidget)
        self.exit.setStyleSheet("QPushButton{\n"
"background: white;\n"
"border: none;\n"
"border: 1px solid #bbb;\n"
"max-width: 378px;\n"
"font-size: 20px;\n"
"padding: 10px 20px;\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: #bbb\n"
"}")
        self.exit.setObjectName("exit")
        self.horizontalLayout.addWidget(self.exit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.layoutWidget, 0, 0, 1, 1)

        self.retranslateUi(InitWidget)
        QtCore.QMetaObject.connectSlotsByName(InitWidget)

    def retranslateUi(self, InitWidget):
        _translate = QtCore.QCoreApplication.translate
        InitWidget.setWindowTitle(_translate("InitWidget", "Form"))
        self.PVP.setText(_translate("InitWidget", "PVP"))
        self.PVE.setText(_translate("InitWidget", "PVE"))
        self.highscoreTable.setText(_translate("InitWidget", "Таблица рекордов"))
        self.exit.setText(_translate("InitWidget", "Выход из игры"))
