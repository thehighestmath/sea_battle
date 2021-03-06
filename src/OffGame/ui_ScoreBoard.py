# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScoreBoard.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Scoreboard(object):
    def setupUi(self, Scoreboard):
        Scoreboard.setObjectName("Scoreboard")
        Scoreboard.resize(772, 554)
        Scoreboard.setStyleSheet("QPushButton{\n"
"width: 30px;\n"
"max-width: 30px;\n"
"height: 30px;\n"
"background: white;\n"
"border: none;\n"
"border: 1px solid #bbb;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: #bbb\n"
"}\n"
"\n"
"#pve_lines, #pvp_lines{\n"
"background: white;\n"
"border: 1px solid #bbb;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"#pvp_label, #pve_label{\n"
"border: None;\n"
"border-bottom: 1px solid gray;\n"
"}\n"
"\n"
"QLabel{\n"
"background: transparent;\n"
"}\n"
"\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(Scoreboard)
        self.gridLayout.setObjectName("gridLayout")
        self.toolbar = QtWidgets.QHBoxLayout()
        self.toolbar.setObjectName("toolbar")
        self.exit = QtWidgets.QPushButton(Scoreboard)
        self.exit.setText("")
        self.exit.setObjectName("exit")
        self.toolbar.addWidget(self.exit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.toolbar.addItem(spacerItem)
        self.clean = QtWidgets.QPushButton(Scoreboard)
        self.clean.setText("")
        self.clean.setObjectName("clean")
        self.toolbar.addWidget(self.clean)
        self.gridLayout.addLayout(self.toolbar, 0, 1, 1, 1)
        self.types = QtWidgets.QHBoxLayout()
        self.types.setObjectName("types")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.types.addItem(spacerItem1)
        self.pvp_lines = QtWidgets.QFrame(Scoreboard)
        self.pvp_lines.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pvp_lines.setObjectName("pvp_lines")
        self.pvp_layout = QtWidgets.QVBoxLayout(self.pvp_lines)
        self.pvp_layout.setObjectName("pvp_layout")
        self.pvp_label = QtWidgets.QLabel(self.pvp_lines)
        self.pvp_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pvp_label.setObjectName("pvp_label")
        self.pvp_layout.addWidget(self.pvp_label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.pvp_layout.addItem(spacerItem2)
        self.types.addWidget(self.pvp_lines)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.types.addItem(spacerItem3)
        self.pve_lines = QtWidgets.QFrame(Scoreboard)
        self.pve_lines.setStyleSheet("")
        self.pve_lines.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.pve_lines.setFrameShadow(QtWidgets.QFrame.Plain)
        self.pve_lines.setObjectName("pve_lines")
        self.pve_layout = QtWidgets.QVBoxLayout(self.pve_lines)
        self.pve_layout.setObjectName("pve_layout")
        self.pve_label = QtWidgets.QLabel(self.pve_lines)
        self.pve_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pve_label.setObjectName("pve_label")
        self.pve_layout.addWidget(self.pve_label)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.pve_layout.addItem(spacerItem4)
        self.types.addWidget(self.pve_lines)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.types.addItem(spacerItem5)
        self.types.setStretch(1, 1)
        self.types.setStretch(3, 1)
        self.gridLayout.addLayout(self.types, 1, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 2, 1, 1, 1)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(Scoreboard)
        QtCore.QMetaObject.connectSlotsByName(Scoreboard)

    def retranslateUi(self, Scoreboard):
        _translate = QtCore.QCoreApplication.translate
        Scoreboard.setWindowTitle(_translate("Scoreboard", "Form"))
        self.pvp_label.setText(_translate("Scoreboard", "PVP"))
        self.pve_label.setText(_translate("Scoreboard", "PVE"))
