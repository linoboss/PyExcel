from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot


class QTableWidgetHelper:
    def __init__(self):
        self.row = 0
        self.activeTable = None


    def append(self, item, column=0, color=None):
        if type(item) == list:
            for i in item:
                newItem = QTableWidgetItem(i)
                if color is not None: newItem.setBackground(QColor(color))
                self.activeTable.setItem(self.row, column, newItem)
                column += 1
            index_increment = 1
        else:
            newItem = QTableWidgetItem(item)
            if color is not None:
                newItem.setBackground(color)
            index_increment = 1
            self.activeTable.setItem(self.row, column, newItem)
            column += 1
        self.row += index_increment

    def getTableContent(self):
        content = []
        headercount = self.activeTable.columnCount()
        rowcount = self.activeTable.rowCount()
        for y in range(0, rowcount):
            row = []
            for x in range(0,headercount):
                row.append(self.activeTable.item(y, x).text())
            content.append(row)
        from pprint import pprint
        pprint(content)




