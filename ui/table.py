# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table.ui'
#
# Created: Mon Feb 29 20:29:18 2016
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
        Form.resize(580, 429)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_logs = QtGui.QWidget()
        self.tab_logs.setObjectName(_fromUtf8("tab_logs"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_logs)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.table_logs = QtGui.QTableWidget(self.tab_logs)
        self.table_logs.setObjectName(_fromUtf8("table_logs"))
        self.table_logs.setColumnCount(0)
        self.table_logs.setRowCount(0)
        self.gridLayout_2.addWidget(self.table_logs, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_logs, _fromUtf8(""))
        self.tab_rango = QtGui.QWidget()
        self.tab_rango.setObjectName(_fromUtf8("tab_rango"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_rango)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.table_rango = QtGui.QTableWidget(self.tab_rango)
        self.table_rango.setObjectName(_fromUtf8("table_rango"))
        self.table_rango.setColumnCount(0)
        self.table_rango.setRowCount(0)
        self.gridLayout_4.addWidget(self.table_rango, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_rango, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_logs), _translate("Form", "Logs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_rango), _translate("Form", "Rango", None))

