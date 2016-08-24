from PyQt4 import QtSql
from PyQt4 import QtCore
from PyQt4 import QtGui


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[[]]):
        super().__init__(self)
        self.__data = data

    def rowCount(self, index):
        return len(self.__data)

    def columnCount(self, index):
        return len(self.__data[0])

    def data(self, index=QtCore.QModelIndex, role=None):
        if not index.isValid():
            return None
        elif role == QtCore.Qt.EditRole:
            return None
        elif role == QtCore.Qt.DisplayRole:
            return self.__data[index.row()][index.column()]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled


class MyProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__i = QtCore.QDate(2000, 1, 1)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.sourceModel().columnCount() + 1

    def data(self, index, role=None):
        row = index.row()
        column = index.column()
        if not index.isValid():
            return None
        elif role == QtCore.Qt.EditRole:
            print(index.data())
            return None
        elif role == QtCore.Qt.DisplayRole:
            if column == 7:
                i = self.__i.toString()
                self.__i = self.__i.addDays(1)
                return i
            else:
                return str(self.sourceModel().data(index))
        print(role)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled


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
        self.model.setTable("Checkinout")

        self.model.select()

        query = QtSql.QSqlQuery()
        query.exec_("""CREATE TABLE setup(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    a VARCHAR(40) NOT NULL,
                    b DATETIME NOT NULL,
                    c INTEGER NOT NULL,
                    FOREIGN KEY (c FROM """)

        self.gridLayout = QtGui.QGridLayout()

        self.tableView = QtGui.QTableView(self)

        self.proxymodel = MyProxyModel(self)
        self.proxymodel.setSourceModel(self.model)

        self.tableView.setModel(self.proxymodel)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ventana = MainForm()
    ventana.setGeometry(100, 100, 500, 300)
    ventana.show()
    sys.exit(app.exec_())
