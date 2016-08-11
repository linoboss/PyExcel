import sys
from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui

ID, DAY, WORKER, INTIME_1, OUTTIME_1, INTIME_2, OUTTIME_2, INTIME_3, OUTTIME_3, SHIFT = list(range(10))


class WorkDayDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        document = QtGui.QTextDocument()

        color = QtGui.QColor(255, 255, 255)

        if index.column() == DAY:
            datetime = index.model().data(index)
            if datetime.date().day() % 2 == 0:

                color = QtGui.QColor(200, 200, 255)
            else:
                color = QtGui.QColor(200, 255, 200)
            text = str(datetime.date().toString())

        elif index.column() == WORKER:
            worker = index.model().data(index)
            text = worker

        elif index.column() == SHIFT:
            shift = index.model().data(index)
            text = str(shift)
        else:
            date = index.model().data(index)
            text = str(date.time().toString())

        painter.save()
        painter.fillRect(option.rect, color)
        painter.translate(option.rect.x(), option.rect.y())
        document.setHtml(text)
        document.drawContents(painter)
        painter.restore()

    def setEditorData(self, editor, index):
        pass

    def createEditor(self, parent, option, index):
        pass

"""
    def sizeHint(self, option, index):
        pass

    def createEditor(self, parent, option, index):
        pass

    def commitAndCloseEditor(self):
        pass

    def setModelData(self, editor, model, index):
        pass
"""


class DateFilterProxyModel(QtGui.QSortFilterProxyModel):
    """
    Filters the dates by range or individually by reimplementing
    the lessThan and filterAcceptsRow methods
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.single_date = None
        self.from_date = None
        self.to_date = None
        self.mode = "no filter"

    def removeFilter(self):
        self.mode = "no filter"
        self.invalidateFilter()

    def setSingleDateFilter(self, date):
        self.mode = "single"
        self.single_date = date
        self.invalidateFilter()

    def setRangeDateFilter(self, from_date, to_date):
        self.mode = "range"
        self.from_date = from_date
        self.to_date = to_date
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):
        """
        Reimplemented from base class
        Executes a set of tests from the filterFunctions, if any fails, the row is rejected
        """
        dateindex = self.sourceModel().index(row, DAY, parent)
        date = self.sourceModel().data(dateindex).date()

        if self.mode == "single":
            return date == self.single_date

        elif self.mode == "range":
            return self.from_date <= date <= self.to_date

        elif self.mode == "no filter":
            return True
        else:
            raise ValueError(str(self.mode) + " is not a valid mode")

    def lessThan(self, left, right):
        """
        Return the comparation of 2 rows
        :param left: QModelIndex
        :param right: QModelIndex_1
        :return:
        """
        leftdate = self.sourceModel().data(left)
        rightdate = self.sourceModel().data(right)
        if isinstance(left, QtCore.QDateTime):
            return leftdate < rightdate
        else: return True


