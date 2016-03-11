# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Thu Jan 21 11:08:34 2016
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
        Dialog.resize(332, 210)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listView = QtGui.QListView(Dialog)
        self.listView.setMaximumSize(QtCore.QSize(100, 16777215))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.gridLayout.addWidget(self.listView, 2, 1, 4, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.qbuttonMesAnterior = QtGui.QPushButton(Dialog)
        self.qbuttonMesAnterior.setObjectName(_fromUtf8("qbuttonMesAnterior"))
        self.horizontalLayout_2.addWidget(self.qbuttonMesAnterior)
        self.qbuttonMesActual = QtGui.QPushButton(Dialog)
        self.qbuttonMesActual.setObjectName(_fromUtf8("qbuttonMesActual"))
        self.horizontalLayout_2.addWidget(self.qbuttonMesActual)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_5.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 5, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.qlabelToday = QtGui.QLabel(Dialog)
        self.qlabelToday.setObjectName(_fromUtf8("qlabelToday"))
        self.horizontalLayout.addWidget(self.qlabelToday)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 2, 0, 1, 1)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.qdateFrom = QtGui.QDateEdit(Dialog)
        self.qdateFrom.setDate(QtCore.QDate(2015, 1, 1))
        self.qdateFrom.setObjectName(_fromUtf8("qdateFrom"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.qdateFrom)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.qdateTo = QtGui.QDateEdit(Dialog)
        self.qdateTo.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(7999, 12, 30), QtCore.QTime(23, 59, 59)))
        self.qdateTo.setDate(QtCore.QDate(2015, 1, 1))
        self.qdateTo.setObjectName(_fromUtf8("qdateTo"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.qdateTo)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.LabelRole, self.formLayout)
        self.qbuttonGenerar = QtGui.QPushButton(Dialog)
        self.qbuttonGenerar.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qbuttonGenerar.sizePolicy().hasHeightForWidth())
        self.qbuttonGenerar.setSizePolicy(sizePolicy)
        self.qbuttonGenerar.setMinimumSize(QtCore.QSize(75, 23))
        self.qbuttonGenerar.setMaximumSize(QtCore.QSize(75, 16777215))
        self.qbuttonGenerar.setObjectName(_fromUtf8("qbuttonGenerar"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.qbuttonGenerar)
        self.gridLayout.addLayout(self.formLayout_2, 4, 0, 1, 1)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Reporte", None))
        self.qbuttonMesAnterior.setText(_translate("Dialog", "Mes anterior", None))
        self.qbuttonMesActual.setText(_translate("Dialog", "Mes actual", None))
        self.label_6.setText(_translate("Dialog", "Fecha de hoy:", None))
        self.qlabelToday.setText(_translate("Dialog", "--/--/----", None))
        self.label_2.setText(_translate("Dialog", "Desde:", None))
        self.label.setText(_translate("Dialog", "Hasta:", None))
        self.qbuttonGenerar.setText(_translate("Dialog", "Generar", None))
        self.label_7.setText(_translate("Dialog", "Personal:", None))

