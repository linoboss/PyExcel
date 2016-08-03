import sys
from PyQt4 import uic
from PyQt4 import QtSql, QtCore, QtGui
from PyQt4.QtSql import QSqlDatabase
from PyQt4.QtCore import SIGNAL, Qt, pyqtSlot
import datetime as dt


# Uic Loader
qtCreatorFile = "tableView.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class LearningSqlModel(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        db = QSqlDatabase.addDatabase("QODBC")
        MDB = r"C:\workspace\PyExcel\sandbox\Att2003.mdb"
        DRV = '{Microsoft Access Driver (*.mdb)}'
        PWD = 'pw'

        db.setDatabaseName("DRIVER={};DBQ={};PWD={}".format(DRV, MDB, PWD))
        if not db.open():
            QtGui.QMessageBox.warning(None, "Error", "Database Error: {}".format(db.lastError().text()))
            sys.exit(1)

        self.progressBar.setValue(1)

        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable('Checkinout')

        # Headings indexes
        ID, A, B, C = 0, 1, 2, 3

        self.model.sort(B, Qt.AscendingOrder)
        self.model.select()

        self.proxymodel = MyProxyModel(self)
        self.proxymodel.setSourceModel(self.model)
        self.proxymodel.sort(1, Qt.AscendingOrder)
        self.proxymodel.setDynamicSortFilter(True)
        self.proxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        #self.tableView = QTableView()
        self.tableView.setModel(self.proxymodel)
        self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
        for column in [4, 5, 6, 7]: self.tableView.setColumnHidden(column, True)
        self.tableView.resizeColumnsToContents()
        self.tableView.setSortingEnabled(True)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.mapper = QtGui.QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QtGui.QDataWidgetMapper.AutoSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.a, A)
        self.mapper.addMapping(self.b, B)
        self.mapper.addMapping(self.c, C)
        self.mapper.addMapping(self.id, ID)

        query = QtSql.QSqlQuery("SELECT Userid FROM Userinfo WHERE int(Userid) < 100")
        print(query.lastError().text())
        while query.next():
            # self.workersList = QtGui.QComboBox()
            self.workersList.addItem(query.value(0))



        #QtCore.QModelIndex().internalPointer()

    @pyqtSlot("QModelIndex")
    def on_tableView_clicked(self, index):
        self.mapper.setCurrentIndex(index.row())
        """ FILTROS
            Aceptan o rechazan filas retornando True or False."""

        self.proxymodel.addFilterFunction(
            "id",
            lambda r: 2 < int(self.model.record(r).value(1)) < 15
        )
        self.d_from = QtCore.QDateTime(dt.datetime(2015, 1, 1))
        self.d_to = QtCore.QDateTime(dt.datetime(2015, 4, 1))

        self.proxymodel.addFilterFunction(
            "CheckTime",
            lambda r:
            self.d_from <
            self.model.record(r).value(2) <
            self.d_to
        )


class MyProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.filterFunctions = {}
        self.i = 0
        # self.progressBar = QtGui.QProgressBar()
        self.progressBar = parent.progressBar
        self.progressBar.setMinimum(0)

    def addFilterFunction(self, name, new_func):
        self.filterFunctions[name] = new_func
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):
        """
        Reimplemented from base class
        Executes a set of tests from the filterFunctions, if any fails, the row is rejected
        """
        # tests = [func(QModelIndex.row()) for func in self.filterFunctions.values()]

        tests = []
        self.progressBar.setValue(row)
        for k, func in self.filterFunctions.items():
            tests.append(func(row))

        return False not in tests


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = LearningSqlModel()
    window.show()
    sys.exit(app.exec())

