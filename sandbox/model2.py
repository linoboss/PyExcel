from PyQt4 import QtSql
from PyQt4 import QtCore
from PyQt4 import QtGui
import assets.work_day_tools as tool


(ID, DAY, WORKER,
 INTIME_1, OUTTIME_1, INTIME_2, OUTTIME_2, INTIME_3, OUTTIME_3,
 SHIFT, WORKED_TIME, EXTRA_TIME, ABSENT_TIME) = list(range(13))


class MainForm(QtGui.QDialog):
    def __init__(self):

        QtGui.QDialog.__init__(self)

        db = QtSql.QSqlDatabase.addDatabase("QODBC")

        MDB = r"C:\workspace\PyExcel\sandbox\Att2003.mdb"
        DRV = '{Microsoft Access Driver (*.mdb)}'
        PWD = 'pw'
        db.setDatabaseName("DRIVER={};DBQ={};PWD={}".format(DRV, MDB, PWD))

        if not db.open():
            QtGui.QMessageBox.warning(None, "Error", "Database Error: {}".format(db.lastError().text()))
            sys.exit(1)

        self.model = QtSql.QSqlTableModel(self, db)
        self.model.setTable("WorkDays")
        self.model.select()

        self.proxymodel = tool.CalculusModel(self)
        self.proxymodel.setSourceModel(self.model)
        self.proxymodel.calculateWorkedHours()

        self.finalModel = tool.DateFilterProxyModel(self)
        self.finalModel.setSourceModel(self.proxymodel)
        self.finalModel.setSingleDateFilter(QtCore.QDate(2014, 9, 2))
        print(self.finalModel.index(0, DAY).data())

        self.scheduleFilter = QtGui.QSortFilterProxyModel(self)
        self.scheduleFilter.setSourceModel(self.finalModel)
        self.scheduleFilter.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.scheduleFilter.setFilterKeyColumn(SHIFT)

        delegate = tool.WorkDayDelegate(self)

        self.tableView = QtGui.QTableView(self)
        self.tableView.setModel(self.scheduleFilter)
        self.tableView.setItemDelegate(delegate)

        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.addWidget(self.tableView)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ventana = MainForm()
    ventana.setGeometry(100, 100, 1100, 500)
    ventana.show()
    sys.exit(app.exec_())
