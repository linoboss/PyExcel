# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created: Tue Sep 29 20:56:01 2015
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(538, 283)
        MainWindow.setMaximumSize(QtCore.QSize(700, 500))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 29, 251, 31))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.loadButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.loadButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.horizontalLayout.addWidget(self.loadButton)
        self.loadLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.loadLabel.setObjectName(_fromUtf8("loadLabel"))
        self.horizontalLayout.addWidget(self.loadLabel)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(280, 30, 231, 31))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.saveLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.saveLabel.setObjectName(_fromUtf8("saveLabel"))
        self.horizontalLayout_2.addWidget(self.saveLabel)
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 70, 251, 171))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.workersLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.workersLabel.setObjectName(_fromUtf8("workersLabel"))
        self.verticalLayout.addWidget(self.workersLabel)
        self.workersList = QtGui.QListView(self.verticalLayoutWidget)
        self.workersList.setObjectName(_fromUtf8("workersList"))
        self.verticalLayout.addWidget(self.workersList)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(280, 90, 230, 98))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.initDate = QtGui.QDateEdit(self.verticalLayoutWidget_2)
        self.initDate.setObjectName(_fromUtf8("initDate"))
        self.gridLayout_2.addWidget(self.initDate, 0, 1, 1, 1)
        self.initDateLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.initDateLabel.setObjectName(_fromUtf8("initDateLabel"))
        self.gridLayout_2.addWidget(self.initDateLabel, 0, 0, 1, 1)
        self.endDateLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.endDateLabel.setObjectName(_fromUtf8("endDateLabel"))
        self.gridLayout_2.addWidget(self.endDateLabel, 1, 0, 1, 1)
        self.endDate = QtGui.QDateEdit(self.verticalLayoutWidget_2)
        self.endDate.setObjectName(_fromUtf8("endDate"))
        self.gridLayout_2.addWidget(self.endDate, 1, 1, 1, 1)
        self.createButon = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.createButon.setObjectName(_fromUtf8("createButon"))
        self.gridLayout_2.addWidget(self.createButon, 2, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.checkBox = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout_3.addWidget(self.checkBox)
        self.checkBox1 = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox1.setObjectName(_fromUtf8("checkBox1"))
        self.verticalLayout_3.addWidget(self.checkBox1)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 2, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 538, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Reporte del personal", None))
        self.loadButton.setText(_translate("MainWindow", "Cargar Archivo", None))
        self.loadLabel.setText(_translate("MainWindow", "Presione el boton", None))
        self.pushButton.setText(_translate("MainWindow", "Guardar en:", None))
        self.saveLabel.setText(_translate("MainWindow", "TextLabel", None))
        self.workersLabel.setText(_translate("MainWindow", "Trabajadores", None))
        self.initDateLabel.setText(_translate("MainWindow", "Desde", None))
        self.endDateLabel.setText(_translate("MainWindow", "Hasta", None))
        self.createButon.setText(_translate("MainWindow", "Crear\n"
"archivo", None))
        self.checkBox.setText(_translate("MainWindow", "entrada/salida", None))
        self.checkBox1.setText(_translate("MainWindow", "resumen", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))

