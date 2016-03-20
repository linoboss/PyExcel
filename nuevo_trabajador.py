# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nuevo_trabajador.ui'
#
# Created: Thu Mar 17 18:49:29 2016
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
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(450, 75)
        Dialog.setMinimumSize(QtCore.QSize(450, 75))
        Dialog.setMaximumSize(QtCore.QSize(450, 75))
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBoxHorario = QtGui.QComboBox(Dialog)
        self.comboBoxHorario.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBoxHorario.setMaximumSize(QtCore.QSize(150, 16777215))
        self.comboBoxHorario.setObjectName(_fromUtf8("comboBoxHorario"))
        self.gridLayout.addWidget(self.comboBoxHorario, 1, 1, 1, 1)
        self.lineEditNombre = QtGui.QLineEdit(Dialog)
        self.lineEditNombre.setObjectName(_fromUtf8("lineEditNombre"))
        self.gridLayout.addWidget(self.lineEditNombre, 1, 0, 1, 1)
        self.lineEditNumero = QtGui.QLineEdit(Dialog)
        self.lineEditNumero.setMaximumSize(QtCore.QSize(75, 16777215))
        self.lineEditNumero.setObjectName(_fromUtf8("lineEditNumero"))
        self.gridLayout.addWidget(self.lineEditNumero, 1, 3, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.checkBoxActivo = QtGui.QCheckBox(Dialog)
        self.checkBoxActivo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBoxActivo.setText(_fromUtf8(""))
        self.checkBoxActivo.setObjectName(_fromUtf8("checkBoxActivo"))
        self.gridLayout.addWidget(self.checkBoxActivo, 1, 2, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.botonListo = QtGui.QPushButton(Dialog)
        self.botonListo.setObjectName(_fromUtf8("botonListo"))
        self.gridLayout.addWidget(self.botonListo, 0, 4, 1, 1)
        self.botonCancelar = QtGui.QPushButton(Dialog)
        self.botonCancelar.setObjectName(_fromUtf8("botonCancelar"))
        self.gridLayout.addWidget(self.botonCancelar, 1, 4, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Nuevo Trabajador", None))
        self.label.setText(_translate("Dialog", "Nombre", None))
        self.label_2.setText(_translate("Dialog", "Horario", None))
        self.label_3.setText(_translate("Dialog", "Activo?", None))
        self.label_4.setText(_translate("Dialog", "Numero", None))
        self.botonListo.setText(_translate("Dialog", "Listo", None))
        self.botonCancelar.setText(_translate("Dialog", "Cancelar", None))

