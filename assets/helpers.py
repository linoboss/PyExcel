import sys, os
from PyQt4 import QtGui, QtCore, QtSql
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
        messageBox.exec()

    @staticmethod
    def error_message(text):
        messageBox = QtGui.QMessageBox()
        messageBox.setText(text)
        messageBox.setStandardButtons(QtGui.QMessageBox.Ok)
        messageBox.setIcon(QtGui.QMessageBox.Warning)
        messageBox.exec()

    @staticmethod
    def search_file(text, initial_path, target, action='get', parent=None):
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
                    parent, text, initial_path, filter_)
            elif action == 'save':
                filename = QtGui.QFileDialog.getSaveFileName(
                    parent, text, initial_path, filter_)
            filename = filename.replace('/', '\\')
            if filename:
                break
            if PopUps.ask_user_to('Intentar nuevamente?') == NO:
                return ''

        if filename.split('.')[-1] != 'pdf':
            filename += '.pdf'

        return filename


class Db:
    @staticmethod
    def tableHeader(table):
        model = QtSql.QSqlTableModel()
        model.setTable(table)
        model.select()

        from collections import OrderedDict
        headerMap = OrderedDict()
        i = 0
        for i in range(model.columnCount()):
            headerMap[model.headerData(i, QtCore.Qt.Horizontal,
                                       QtCore.Qt.DisplayRole)] = i
        if table == "WorkDays":
            headerMap["workedtime"] = i + 1
            headerMap["extratime"] = i + 2
            headerMap["absenttime"] = i + 3
        return headerMap


class Thread(QtCore.QThread):
    def __init__(self, func):
        super().__init__()
        self.func = func

    # the execution oh the thread will be by calling
    # the start method, which calls the run method
    def run(self):
        self.func()


if __name__ == "__main__":
    import assets.anviz_reader as av

    app = QtGui.QApplication(sys.argv)
    av.AnvizReader()
    print(Db.tableHeader('WorkDays'))
