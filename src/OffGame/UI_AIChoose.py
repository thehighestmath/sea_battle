# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AI_Choose.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AiChoose(object):
    def setupUi(self, AiChoose):
        AiChoose.setObjectName("AiChoose")
        AiChoose.resize(646, 453)
        self.verticalLayout = QtWidgets.QVBoxLayout(AiChoose)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(AiChoose)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
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
"}")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(AiChoose)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(AiChoose)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"background: white;\n"
"border: none;\n"
"border: 1px solid #bbb;\n"
"max-width: 200px;\n"
"font-size: 20px;\n"
"padding: 10px 20px;\n"
"border-radius: 10px;\n"
"color: black;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: #bbb\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"background: #ccc;\n"
"border-color: #bbb;\n"
"color: #999;\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(AiChoose)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"background: white;\n"
"border: none;\n"
"border: 1px solid #bbb;\n"
"max-width: 200px;\n"
"font-size: 20px;\n"
"padding: 10px 20px;\n"
"border-radius: 10px;\n"
"color: black;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: #bbb\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"background: #ccc;\n"
"border-color: #bbb;\n"
"color: #999;\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_4 = QtWidgets.QPushButton(AiChoose)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"background: white;\n"
"border: none;\n"
"border: 1px solid #bbb;\n"
"max-width: 200px;\n"
"font-size: 20px;\n"
"padding: 10px 20px;\n"
"border-radius: 10px;\n"
"color: black;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: #bbb\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"background: #ccc;\n"
"border-color: #bbb;\n"
"color: #999;\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_4.addWidget(self.pushButton_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(AiChoose)
        QtCore.QMetaObject.connectSlotsByName(AiChoose)

    def retranslateUi(self, AiChoose):
        _translate = QtCore.QCoreApplication.translate
        AiChoose.setWindowTitle(_translate("AiChoose", "Form"))
        self.label.setText(_translate("AiChoose", "Выберите сложность"))
        self.pushButton_2.setText(_translate("AiChoose", "Простой уровень"))
        self.pushButton_3.setText(_translate("AiChoose", "Срединй уровень"))
        self.pushButton_4.setText(_translate("AiChoose", "Сложный уровень"))
