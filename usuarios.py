# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'usuarios.ui'
#
# Created: Wed Mar 16 11:02:43 2016
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(489, 474)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.botonAgregar = QtGui.QPushButton(Dialog)
        self.botonAgregar.setMaximumSize(QtCore.QSize(60, 16777215))
        self.botonAgregar.setObjectName(_fromUtf8("botonAgregar"))
        self.verticalLayout.addWidget(self.botonAgregar)
        self.botonModificar = QtGui.QPushButton(Dialog)
        self.botonModificar.setMaximumSize(QtCore.QSize(60, 16777215))
        self.botonModificar.setObjectName(_fromUtf8("botonModificar"))
        self.verticalLayout.addWidget(self.botonModificar)
        self.botonEliminar = QtGui.QPushButton(Dialog)
        self.botonEliminar.setMaximumSize(QtCore.QSize(60, 16777215))
        self.botonEliminar.setObjectName(_fromUtf8("botonEliminar"))
        self.verticalLayout.addWidget(self.botonEliminar)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Trabajadores", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Nombre", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Horario", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Activo?", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Numero", None))
        self.botonAgregar.setText(_translate("Dialog", "Agregar", None))
        self.botonModificar.setText(_translate("Dialog", "Modificar", None))
        self.botonEliminar.setText(_translate("Dialog", "Eliminar", None))

