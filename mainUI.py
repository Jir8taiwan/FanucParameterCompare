# -*- coding: utf-8 -*-
#####################
# Author: https://github.com/Jir8taiwan/
# Version. 2022.10.28
#
# Using PYTHON3 language to open the two converted CSV files at
# FANUC controller system of parameter backup for difference.
# Please prepare two any ".CSV" documents in somewhere.
# It will output CSV and EXCEL files for studying in a formatted
# data about difference line for reference.
#
# ****************************************************************
# If this small code is helping any needed case, it can donate
# to me for encourage as following address:
# 1. BTC - 3M4wWghm4MxmrSfXmHMEeCFNwP8Lxxqjzk
# 2. BCH - bitcoincash:qq6ghvdmyusnse9735rd5q09ensacl8z8qzrlwf49q
# 3. LTC - MR6HaFkfkmsfifX3jWu7xz33dULGotVUWB
# 4. DOGE- DGEFd3AAfJrBuaUwc4P6R2ZT754Jon9fQ7
#
#####################
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(473, 189)
        self.Msg4textBrowser = QtWidgets.QTextBrowser(MainWindow)
        self.Msg4textBrowser.setGeometry(QtCore.QRect(10, 90, 321, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Msg4textBrowser.setFont(font)
        self.Msg4textBrowser.setObjectName("Msg4textBrowser")
        self.layoutWidget = QtWidgets.QWidget(MainWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(13, 13, 441, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.File1lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.File1lineEdit.setObjectName("File1lineEdit")
        self.horizontalLayout.addWidget(self.File1lineEdit)
        self.File1pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.File1pushButton.setObjectName("File1pushButton")
        self.horizontalLayout.addWidget(self.File1pushButton)
        self.layoutWidget1 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget1.setGeometry(QtCore.QRect(13, 44, 441, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.File2lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.File2lineEdit.setObjectName("File2lineEdit")
        self.horizontalLayout_2.addWidget(self.File2lineEdit)
        self.File2pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.File2pushButton.setObjectName("File2pushButton")
        self.horizontalLayout_2.addWidget(self.File2pushButton)
        self.layoutWidget2 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget2.setGeometry(QtCore.QRect(336, 80, 131, 91))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.GoCpmarepushButton = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.GoCpmarepushButton.setFont(font)
        self.GoCpmarepushButton.setObjectName("GoCpmarepushButton")
        self.verticalLayout.addWidget(self.GoCpmarepushButton)
        self.OpenResultpushButton = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.OpenResultpushButton.setFont(font)
        self.OpenResultpushButton.setObjectName("OpenResultpushButton")
        self.verticalLayout.addWidget(self.OpenResultpushButton)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FanucParameterCompareQTgui_byJIR_221028"))
        self.File1pushButton.setText(_translate("MainWindow", "open FILE 1"))
        self.File2pushButton.setText(_translate("MainWindow", "open FILE 2"))
        self.GoCpmarepushButton.setText(_translate("MainWindow", "Go Compare"))
        self.OpenResultpushButton.setText(_translate("MainWindow", "Open Result"))
