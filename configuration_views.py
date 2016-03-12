import sys
import usuarios
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot
from manejo_detablas import QTableWidgetHelper
import sql
from pprint import pprint


class Usuarios(QTableWidgetHelper,
               QDialog,
               usuarios.Ui_Dialog
               ):
    def __init__(self):
        super(Usuarios, self).__init__()
        super(QTableWidgetHelper, self).__init__()
        self.setupUi(self)
        self.activeTable = self.tableWidget

        self.tableWidget.setColumnCount(4)
        database = sql.Setup()

        self.workerstable = database.getWorkersTable()
        self.tableWidget.setRowCount(len(self.workerstable))

        for i, w, s, h, n in self.workerstable:
            self.append([w, h, str(s), str(n)])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    @pyqtSlot()
    def on_botonGuardar_clicked(self):
        pprint(self.getTableContent())
        table = self.workerstable

        for t in table:
            print(t)
            database = sql.Setup()
            database.modifyWorker(*t)

    @pyqtSlot()
    def on_botonAgregar_clicked(self):
        print('agregar')

    @pyqtSlot()
    def on_botonModificar_clicked(self):
        print("Modificar")

    @pyqtSlot()
    def on_botonEliminar_clicked(self):
        print("eliminar")




    def on_botonCancelar_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    users = Usuarios()
    users.show()
    app.exec()

