# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'controles_tabla.ui'
#
# Created: Sat Feb 13 07:44:43 2016
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(302, 396)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_2.addWidget(self.label_9)
        self.formLayout_5 = QtGui.QFormLayout()
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.qdateFrom = QtGui.QDateEdit(Form)
        self.qdateFrom.setDate(QtCore.QDate(2015, 1, 1))
        self.qdateFrom.setObjectName(_fromUtf8("qdateFrom"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.qdateFrom)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_8)
        self.qdateTo = QtGui.QDateEdit(Form)
        self.qdateTo.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(7999, 12, 30), QtCore.QTime(23, 59, 59)))
        self.qdateTo.setDate(QtCore.QDate(2015, 1, 1))
        self.qdateTo.setObjectName(_fromUtf8("qdateTo"))
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.FieldRole, self.qdateTo)
        self.verticalLayout_2.addLayout(self.formLayout_5)
        self.qbuttonGenerar = QtGui.QPushButton(Form)
        self.qbuttonGenerar.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qbuttonGenerar.sizePolicy().hasHeightForWidth())
        self.qbuttonGenerar.setSizePolicy(sizePolicy)
        self.qbuttonGenerar.setMinimumSize(QtCore.QSize(75, 23))
        self.qbuttonGenerar.setMaximumSize(QtCore.QSize(1500, 16777215))
        self.qbuttonGenerar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.qbuttonGenerar.setObjectName(_fromUtf8("qbuttonGenerar"))
        self.verticalLayout_2.addWidget(self.qbuttonGenerar)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.excelButton = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.excelButton.sizePolicy().hasHeightForWidth())
        self.excelButton.setSizePolicy(sizePolicy)
        self.excelButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.excelButton.setObjectName(_fromUtf8("excelButton"))
        self.verticalLayout_2.addWidget(self.excelButton)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_9.setText(_translate("Form", "Cargar por rango", None))
        self.label_7.setText(_translate("Form", "Desde:", None))
        self.label_8.setText(_translate("Form", "Hasta:", None))
        self.qbuttonGenerar.setText(_translate("Form", "Generar", None))
        self.excelButton.setText(_translate("Form", "Enviar a\n"
"Excel", None))

