from PyQt4.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt4.QtGui import QDialog, QTableView, QApplication, QMessageBox


class TableModel(QAbstractTableModel):
    def __init__(self, data=[[]]):
        QAbstractTableModel.__init__(self)
        self.__data = data

    def rowCount(self, index):
        return len(self.__data)

    def columnCount(self, index):
        return len(self.__data[0])

    def data(self, index=QModelIndex, role=None):
        if not index.isValid():
            return None
        elif role == Qt.EditRole:
            return None
        elif role == Qt.DisplayRole:
            return self.__data[index.row()][index.column()]

    def flags(self, index):
        return Qt.ItemIsEnabled


class MainForm(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        db = QSqlDatabase.addDatabase("QODBC")

        MDB = r"C:\workspace\PyExcel\sandbox\Att2003.mdb"
        DRV = '{Microsoft Access Driver (*.mdb)}'
        PWD = 'pw'
        db.setDatabaseName("DRIVER={};DBQ={};PWD={}".format(DRV, MDB, PWD))

        if not db.open():
            QMessageBox.warning(None, "Error", "Database Error: {}".format(db.lastError().text()))
            sys.exit(1)

        self.model = QSqlTableModel(self, db)
        self.model.setTable("Checkinout")

        self.model.select()

        query = QSqlQuery()
        query.exec_("""CREATE TABLE setup(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    a VARCHAR(40) NOT NULL,
                    b DATETIME NOT NULL,
                    c INTEGER NOT NULL,
                    FOREIGN KEY (c FROM """)



        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = MainForm()
    ventana.setGeometry(100, 100, 500, 300)
    ventana.show()
    sys.exit(app.exec_())
