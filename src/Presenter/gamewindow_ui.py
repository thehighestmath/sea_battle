# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gamewindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GameWindow(object):
    def setupUi(self, GameWindow):
        GameWindow.setObjectName("GameWindow")
        GameWindow.resize(1000, 600)
        GameWindow.setMinimumSize(QtCore.QSize(100, 100))
        GameWindow.setMaximumSize(QtCore.QSize(16000, 9000))
        GameWindow.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(GameWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.centralWidget = QtWidgets.QWidget(GameWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.wigdetPlayer_1 = QtWidgets.QWidget(self.centralWidget)
        self.wigdetPlayer_1.setObjectName("wigdetPlayer_1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.wigdetPlayer_1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelPlayer_1 = QtWidgets.QLabel(self.wigdetPlayer_1)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelPlayer_1.setFont(font)
        self.labelPlayer_1.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPlayer_1.setObjectName("labelPlayer_1")
        self.verticalLayout.addWidget(self.labelPlayer_1)
        self.gameArea_1 = GameArea(self.wigdetPlayer_1)
        self.gameArea_1.setObjectName("gameArea_1")
        self.verticalLayout.addWidget(self.gameArea_1)
        self.verticalLayout.setStretch(1, 9)
        self.gridLayout_2.addWidget(self.wigdetPlayer_1, 1, 0, 1, 1)
        self.wigdetPlayer_2 = QtWidgets.QWidget(self.centralWidget)
        self.wigdetPlayer_2.setObjectName("wigdetPlayer_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.wigdetPlayer_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelPlayer_2 = QtWidgets.QLabel(self.wigdetPlayer_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelPlayer_2.setFont(font)
        self.labelPlayer_2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPlayer_2.setObjectName("labelPlayer_2")
        self.verticalLayout_2.addWidget(self.labelPlayer_2)
        self.gameArea_2 = GameArea(self.wigdetPlayer_2)
        self.gameArea_2.setObjectName("gameArea_2")
        self.verticalLayout_2.addWidget(self.gameArea_2)
        self.verticalLayout_2.setStretch(1, 9)
        self.gridLayout_2.addWidget(self.wigdetPlayer_2, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.centralWidget, 0, 0, 1, 1)
        self.statusbar = QtWidgets.QStatusBar(GameWindow)
        self.statusbar.setObjectName("statusbar")
        self.gridLayout.addWidget(self.statusbar, 4, 0, 1, 1)
        self.buttonWidget = QtWidgets.QWidget(GameWindow)
        self.buttonWidget.setObjectName("buttonWidget")
        self.buttonLayout = QtWidgets.QHBoxLayout(self.buttonWidget)
        self.buttonLayout.setObjectName("buttonLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacerItem)
        self.finishSettingShips = QtWidgets.QPushButton(self.buttonWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.finishSettingShips.sizePolicy().hasHeightForWidth())
        self.finishSettingShips.setSizePolicy(sizePolicy)
        self.finishSettingShips.setMinimumSize(QtCore.QSize(200, 40))
        self.finishSettingShips.setObjectName("finishSettingShips")
        self.buttonLayout.addWidget(self.finishSettingShips)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.buttonWidget, 3, 0, 1, 1)
        self.actionPreparePlayer_1 = QtWidgets.QAction(GameWindow)
        self.actionPreparePlayer_1.setObjectName("actionPreparePlayer_1")
        self.actionPreparePlayer_2 = QtWidgets.QAction(GameWindow)
        self.actionPreparePlayer_2.setObjectName("actionPreparePlayer_2")
        self.actionPlayer_1 = QtWidgets.QAction(GameWindow)
        self.actionPlayer_1.setObjectName("actionPlayer_1")
        self.actionPlayer_2 = QtWidgets.QAction(GameWindow)
        self.actionPlayer_2.setObjectName("actionPlayer_2")

        self.retranslateUi(GameWindow)
        QtCore.QMetaObject.connectSlotsByName(GameWindow)

    def retranslateUi(self, GameWindow):
        _translate = QtCore.QCoreApplication.translate
        GameWindow.setWindowTitle(_translate("GameWindow", "Sea battle"))
        self.labelPlayer_1.setText(_translate("GameWindow", "Player 1"))
        self.labelPlayer_2.setText(_translate("GameWindow", "Player 2"))
        self.finishSettingShips.setText(_translate("GameWindow", "Я закончил расставлять"))
        self.actionPreparePlayer_1.setText(_translate("GameWindow", "Prepare player 1"))
        self.actionPreparePlayer_2.setText(_translate("GameWindow", "Prepare player 2"))
        self.actionPlayer_1.setText(_translate("GameWindow", "Player 1"))
        self.actionPlayer_2.setText(_translate("GameWindow", "Player 2"))
from Presenter.GameArea import GameArea