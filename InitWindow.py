from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InitWindow(object):
    def setupUi(self, InitWindow):
        InitWindow.setObjectName("InitWindow")
        # InitWindow.resize(400, 500)
        InitWindow.setFixedSize(400, 500)
        InitWindow.setStyleSheet("#InitWindow {\n"
                                 "border-image: url(./waves.jpg) 0 0 0 0 stretch stretch;\n"
                                 "}")

        self.centralwidget = QtWidgets.QWidget(InitWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.label = QtWidgets.QLabel(InitWindow)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setStyleSheet("#label {\n"
                                 "    background: white;\n"
                                 "}")
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
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

        self.PVP = QtWidgets.QPushButton(InitWindow)
        self.PVP.setObjectName("PVP")
        self.horizontalLayout.addWidget(self.PVP)

        self.PVAI = QtWidgets.QPushButton(InitWindow)
        self.PVAI.setObjectName("PVAI")
        self.horizontalLayout.addWidget(self.PVAI)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.hst = QtWidgets.QPushButton(InitWindow)
        self.hst.setObjectName("hst")
        self.verticalLayout.addWidget(self.hst)

        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)

        InitWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(InitWindow)
        QtCore.QMetaObject.connectSlotsByName(InitWindow)

    def retranslateUi(self, InitWindow):
        _translate = QtCore.QCoreApplication.translate
        InitWindow.setWindowTitle(_translate("InitWindow", "Sea Battle"))
        self.label.setText(_translate("InitWindow", " Sea Battle "))
        self.PVP.setText(_translate("InitWindow", "Player VS Player"))
        self.PVAI.setText(_translate("InitWindow", "Player VS AI"))
        self.hst.setText(_translate("InitWindow", "High Score Table"))