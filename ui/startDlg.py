# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startDlg.ui'
#
# Created: Wed Sep 28 15:07:42 2016
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
        Dialog.resize(371, 399)
        Dialog.setSizeGripEnabled(False)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.image = QtGui.QLabel(Dialog)
        self.image.setText(_fromUtf8(""))
        self.image.setPixmap(QtGui.QPixmap(_fromUtf8("../../../Users/Lino Bossio/Pictures/1965243.jpg")))
        self.image.setObjectName(_fromUtf8("image"))
        self.verticalLayout.addWidget(self.image)
        self.info = QtGui.QLabel(Dialog)
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setObjectName(_fromUtf8("info"))
        self.verticalLayout.addWidget(self.info)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.info.setText(_translate("Dialog", "Cargando...", None))

