from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InitWidget(object):
    def setupUi(self, InitWidget):
        InitWidget.setObjectName("InitWidget")
        InitWidget.resize(400, 500)

        self.verticalLayout = QtWidgets.QVBoxLayout(InitWidget) #(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.label = QtWidgets.QLabel(InitWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setMidLineWidth(1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        
        self.PVP = QtWidgets.QPushButton(InitWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PVP.sizePolicy().hasHeightForWidth())
        self.PVP.setSizePolicy(sizePolicy)
        self.PVP.setMinimumSize(QtCore.QSize(187, 0))
        self.PVP.setObjectName("PVP")
        self.horizontalLayout.addWidget(self.PVP)

        self.PVAI = QtWidgets.QPushButton(InitWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PVAI.sizePolicy().hasHeightForWidth())
        self.PVAI.setSizePolicy(sizePolicy)
        self.PVAI.setMinimumSize(QtCore.QSize(187, 0))
        self.PVAI.setBaseSize(QtCore.QSize(187, 0))
        self.PVAI.setObjectName("PVAI")
        self.horizontalLayout.addWidget(self.PVAI)

        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)

        self.hst = QtWidgets.QPushButton(InitWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hst.sizePolicy().hasHeightForWidth())
        self.hst.setSizePolicy(sizePolicy)
        self.hst.setMinimumSize(QtCore.QSize(400, 0))
        self.hst.setObjectName("hst")
        self.horizontalLayout_3.addWidget(self.hst)

        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)

        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)


        self.retranslateUi(InitWidget)
        QtCore.QMetaObject.connectSlotsByName(InitWidget)

    def retranslateUi(self, InitWidget):
        _translate = QtCore.QCoreApplication.translate
        InitWidget.setWindowTitle(_translate("InitWidget", "Sea Battle"))
        self.label.setText(_translate("InitWidget", " Sea Battle "))
        self.PVP.setText(_translate("InitWidget", "Player VS Player"))
        self.PVAI.setText(_translate("InitWidget", "Player VS AI"))
        self.hst.setText(_translate("InitWidget", "High Score Table"))