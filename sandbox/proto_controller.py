import sys
from PyQt4 import uic
from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtCore import Qt, SIGNAL, pyqtSlot

""" **** Load Ui**** """
qtCreatorFile = "prototype.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class ProtoController(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        db = QtSql.QSqlDatabase.addDatabase("QODBC")
        MDB = r"C:\workspace\PyExcel\sandbox\Att2003.mdb"
        DRV = '{Microsoft Access Driver (*.mdb)}'
        PWD = 'pw'

        db.setDatabaseName("DRIVER={};DBQ={};PWD={}".format(DRV, MDB, PWD))
        if not db.open():
            QtGui.QMessageBox.warning(None, "Error", "Database Error: {}".format(db.lastError().text()))
            sys.exit(1)

        self.model = QtSql.QSqlRelationalTableModel(self)
        self.model.setTable('Checkinout')
        self.model.setRelation(1, QtSql.QSqlRelation("Userinfo", "Userid", "Name"))
        self.model.select()

        self.proxymodel = QtGui.QSortFilterProxyModel(self)
        self.proxymodel.setSourceModel(self.model)
        self.proxymodel.sort(1, Qt.AscendingOrder)
        self.proxymodel.setDynamicSortFilter(True)
        self.proxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # self.tableView = QTableView()
        self.logs_table.setModel(self.proxymodel)
        self.logs_table.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.logs_table.setSelectionBehavior(QtGui.QTableView.SelectRows)
        for column in [4, 5, 6, 7]: self.logs_table.setColumnHidden(column, True)
        self.logs_table.resizeColumnsToContents()
        self.logs_table.setSortingEnabled(True)
        self.logs_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        query = QtSql.QSqlQuery()
        query.exec("SELECT Userid, Name FROM Userinfo WHERE isActive")

        print(query.isActive(), query.lastError().text())
        while query.next():
            #self.worker_filter = QtGui.QComboBox()
            print(query.value(1))
            self.worker_filter.addItem(query.value(1))


        """
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.a, A)
        self.mapper.addMapping(self.b, B)
        self.mapper.addMapping(self.c, C)
        self.mapper.addMapping(self.id, ID)
        self.mapper.toFirst()
        """

        """
        from PyQt4.QtGui import QComboBox
        self.date_filter = QComboBox()
        """
        self.date_filter.addItems(["(Noris)", ".*", "[1]+"])

    @pyqtSlot("QString")
    def on_date_filter_activated(self, a):
        self.proxymodel.setFilterKeyColumn(1)
        self.proxymodel.setFilterRegExp(a)

    @pyqtSlot("QString")
    def on_schedulefilter_activated(self, a):
        self.proxymodel.setFilterKeyColumn(1)
        self.proxymodel.setFilterRegExp(a)

    @pyqtSlot("QString")
    def on_worker_filter_activated(self, a):
        self.proxymodel.setFilterKeyColumn(1)
        self.proxymodel.setFilterRegExp(a)

    @pyqtSlot("QDate")
    def on_calendarWidget_clicked(self, d):
        print(d)

    @pyqtSlot()
    def on_nextday_clicked(self):
        print("next day")

    @pyqtSlot()
    def on_prevday_clicked(self):
        print("prev day")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = ProtoController()
    window.show()
    sys.exit(app.exec())
