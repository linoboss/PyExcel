import sys, os
from PyQt4 import QtGui, QtCore
import assets.sql as sql

YES = QtGui.QMessageBox.Yes
NO = QtGui.QMessageBox.No


class PopUps:
    @staticmethod
    def ask_user_to(text, infotext='', detailedtext=''):
        messageBox = QtGui.QMessageBox()
        messageBox.setStandardButtons(QtGui.QMessageBox.Yes |
                                      QtGui.QMessageBox.No)
        messageBox.setIcon(QtGui.QMessageBox.Question)
        messageBox.setText(text)
        messageBox.setInformativeText(infotext)
        messageBox.setDetailedText(detailedtext)
        return messageBox.exec()

    @staticmethod
    def inform_user(text):
        messageBox = QtGui.QMessageBox()
        messageBox.setText(text)
        messageBox.setStandardButtons(QtGui.QMessageBox.Ok)
        messageBox.setIcon(QtGui.QMessageBox.Information)

    @staticmethod
    def search_file(text, initial_path, target, action='get'):
        if target == 'database':
            filter_ = "Access db (*.mdb)"
        elif target == 'pdf':
            filter_ = "pdf (*.pdf)"
        else:
            filter_ = '*'
        filename = initial_path
        while True:
            if action == 'get':
                filename = QtGui.QFileDialog.getOpenFileName(
                    None, text, initial_path, filter_)
            elif action == 'save':
                filename = QtGui.QFileDialog.getSaveFileName(
                    None, text, initial_path, filter_)
            filename = filename.replace('/', '\\')
            if filename:
                break
            if PopUps.ask_user_to('Intentar nuevamente?') == NO:
                return ''

        return filename


if __name__ == "__main__":
    pass
