import sys, os
from PyQt4 import QtGui, QtCore
from mainview_controller import MainView
import assets.sql as sql

YES = QtGui.QMessageBox.Yes
NO = QtGui.QMessageBox.No


class Help():
    @staticmethod
    def ask_user_to(option, sub=None):
        messageBox = QtGui.QMessageBox()
        messageBox.setStandardButtons(QtGui.QMessageBox.Yes |
                                      QtGui.QMessageBox.No)
        messageBox.setIcon(QtGui.QMessageBox.Question)

        if option == "search db":
            if sub is None:
                messageBox.setText("La base de datos no fue encontrada...")
            elif sub == "invalid":
                messageBox.setText("La base de datos encontrada es invalida...")

            messageBox.setInformativeText("Desea buscarla?")
            messageBox.setDetailedText("Probablemente se encuentre en"
                                       " la direccion:\n C:\\standard")
        elif option == "reselect":
            messageBox.setText("Desea intentar de nuevo?")

        return messageBox.exec()

    @staticmethod
    def closeApp(app):
        app.closeAllWindows()
        sys.exit()