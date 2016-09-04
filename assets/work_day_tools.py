import sys
from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui

(ID, DAY, WORKER,
 INTIME_1, OUTTIME_1, INTIME_2, OUTTIME_2, INTIME_3, OUTTIME_3,
 SHIFT, WORKED_TIME, EXTRA_TIME, ABSENT_TIME) = list(range(13))


class WorkDayDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        document = QtGui.QTextDocument()
        column = index.column()
        item = index.model().data(index)

        color = QtGui.QColor(255, 255, 255)
        if column == DAY:
            if item.date().day() % 2 == 0:

                color = QtGui.QColor(200, 200, 255)
            else:
                color = QtGui.QColor(200, 255, 200)
            text = item.toString("yyyy-MM-dd")

        elif column == WORKER:
            text = str(item)

        elif column == SHIFT:
            text = str(item)
        elif isinstance(item, QtCore.QDateTime):
            text = item.toString("hh:mm")
        elif isinstance(item, QtCore.QTime):
            text = item.toString('hh:mm')
        else:
            text = str(item)

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

    def sizeHint(self, option, index):
        return QtCore.QSize(100, 20)

    """
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
        date = self.sourceModel().index(row, DAY, parent).data()
        if date is None:
            return False
        date = date.date()

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


class CalculusModel(QtGui.QIdentityProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculations = []

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.sourceModel().columnCount()

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.sourceModel().rowCount()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignVCenter |\
                       Qt.AlignHCenter
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == DAY:
                return "Dia"
            elif section == WORKER:
                return "Trabajador"
            elif (section == INTIME_1 or
                  section == INTIME_2 or
                  section == INTIME_3):
                return "Entrada"
            elif (section == OUTTIME_1 or
                  section == OUTTIME_2 or
                  section == OUTTIME_3):
                return "Salida"
            elif section == SHIFT:
                return "Turno"
            elif section == WORKED_TIME:
                return "Tiempo\nTrabajado"
            elif section == EXTRA_TIME:
                return "Tiempo\nExtra"
            elif section == ABSENT_TIME:
                return "Tiempo\nAusente"
        return str(section)

    def data(self, index, role=None):
        row = index.row()
        column = index.column()
        if not index.isValid():
            return None
        item = self.sourceModel().data(self.sourceModel().index(row, column))

        if role == Qt.EditRole:
            return None
        elif role == Qt.DisplayRole:
            if column == DAY:
                return item
            elif column >= WORKED_TIME:
                if self.calculations:
                    if column == 10:
                        return self.calculations[row][0]
                    elif column == 11:
                        return self.calculations[row][1]
                    elif column == 12:
                        return self.calculations[row][2]
        elif column == 10:
            return self.calculations[row][0]
        elif column == 11:
            return self.calculations[row][1]
        elif column == 12:
            return self.calculations[row][2]
        return item

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def calculateWorkedHours(self):
        self.beginInsertColumns(QtCore.QModelIndex(), 10, 13)
        self.insertColumns(10, 3)
        self.endInsertColumns()

        for row in range(self.rowCount()):
            # index = self.proxymodel.createIndex(r, 10)
            total_seconds = 0
            for column in (INTIME_1, INTIME_2, INTIME_3):
                in_ = self.data(self.sourceModel().index(row, column))
                out = self.data(self.sourceModel().index(row, column + 1))
                if in_ is None or out is None:
                    return [QtCore.QTime(0, 0, 0)] * 3
                total_seconds += in_.secsTo(out)
            worked_time = QtCore.QTime(0, 0, 0).addSecs(
                total_seconds)

            relative_time = QtCore.QTime(8, 0, 0).secsTo(worked_time)
            if relative_time > 0:
                extra_time = QtCore.QTime(0, 0, 0).addSecs(relative_time)
                absent_time = QtCore.QTime(0, 0, 0)
            else:
                extra_time = QtCore.QTime(0, 0, 0)
                absent_time = QtCore.QTime(0, 0, 0).addSecs(- relative_time)

            self.calculations.append(
                [worked_time, extra_time, absent_time]
            )
        self.emit(QtCore.SIGNAL("dataChanged()"), self)


