import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
import assets.helpers as helpers
import assets.work_day_tools as tool

# Uic Loader
qtCreatorFile = "ui\\checkinoutview.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


(LOGID, USERID, CHECKTIME, CHECKTYPE,
 SENSORID, CHECHED, WORKTYPE, ATTFLAG) = range(8)


class Checkinoutview_Controller(Ui_MainWindow, QtBaseClass):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent

        model = QtSql.QSqlRelationalTableModel(self)
        model.setTable('Checkinout')
        model.setRelation(USERID,
                          QtSql.QSqlRelation(
                              "Userinfo",
                              "Userid", "Name"))
        model.select()

        self.dateFilter = tool.DateFilterProxyModel(self)
        self.dateFilter.setSourceModel(model)
        self.dateFilter.setFilterKeyColumn(model.fieldIndex("CheckTime"))

        self.tableView.setModel(self.dateFilter)
        self.tableView.setItemDelegate(CustomDelegate())
        for hc in (0, 3, 4, 5, 6, 7):
            self.tableView.hideColumn(hc)
        self.tableView.sortByColumn(CHECKTIME, QtCore.Qt.AscendingOrder)
        self.tableView.setSortingEnabled(True)
        self.tableView.adjustSize()

    @QtCore.pyqtSlot("QDate")
    def on_dateEdit_dateChanged(self, date):
        self.dateFilter.setSingleDateFilter(date)

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        self.dateFilter.removeFilter()


class CustomDelegate(QtGui.QStyledItemDelegate):
    def paint(self, painter, option, index):
        document = QtGui.QTextDocument()
        column = index.column()
        item = index.model().data(index)

        if column == CHECKTIME:
            text = item.toString('yyyy/MM/dd | hh:mm')
        else:
            text = str(item)

        painter.save()
        painter.translate(option.rect.x(), option.rect.y())
        document.setHtml(text)
        document.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(200, 20)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    sql.AnvizRegisters()

    checkioview = Checkinoutview_Controller()
    checkioview.show()

    sys.exit(app.exec())
