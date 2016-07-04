# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created: Sun Mar 20 23:32:19 2016
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
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMenu = QtGui.QMenu(self.menubar)
        self.menuMenu.setObjectName(_fromUtf8("menuMenu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionPersonal = QtGui.QAction(MainWindow)
        self.actionPersonal.setObjectName(_fromUtf8("actionPersonal"))
        self.actionHorarios = QtGui.QAction(MainWindow)
        self.actionHorarios.setObjectName(_fromUtf8("actionHorarios"))
        self.actionBase_de_datos = QtGui.QAction(MainWindow)
        self.actionBase_de_datos.setObjectName(_fromUtf8("actionBase_de_datos"))
        self.menuMenu.addAction(self.actionPersonal)
        self.menuMenu.addAction(self.actionHorarios)
        self.menuMenu.addAction(self.actionBase_de_datos)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu", None))
        self.actionPersonal.setText(_translate("MainWindow", "Personal", None))
        self.actionHorarios.setText(_translate("MainWindow", "Horarios", None))
        self.actionBase_de_datos.setText(_translate("MainWindow", "Base de datos", None))

