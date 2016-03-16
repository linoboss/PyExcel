import sys
import usuarios
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot, SIGNAL
from manejo_detablas import QTableWidgetHelper
import sql
from pprint import pprint
import nuevo_trabajador_control as nt


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
        self.workersinfo = {}

        self.loadTable()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def loadTable(self):
        self.resetTable()
        database = sql.Setup()
        workerstable = database.getWorkersTable()
        self.tableWidget.setRowCount(len(workerstable))

        for i, w, s, h, n in workerstable:
            self.workersinfo[n] = (i, w, s, h, n)
            self.append([w, h, str(s), str(n)])



    @pyqtSlot()
    def on_botonGuardar_clicked(self):
        pprint(self.getTableContent())
        table = self.workerstable

        for t in table:
            database = sql.Setup()
            database.modifyWorker(*t)

    @pyqtSlot()
    def on_botonAgregar_clicked(self):
        interface = nt.Control(self)
        interface.show()
        self.connect(interface, SIGNAL("Guardar(PyQt_PyObject)"), self.agregarTrabajador)

    def agregarTrabajador(self, params):
        nombre = params['nombre']
        horario = params['horario']
        activo = params['status']
        numero = params['numero']
        for v in self.workersinfo.values():
            if numero in v:
                print("El numero {} ya existe, por favor agregue otro".format(numero))
                QMessageBox().setText("El numero {} ya existe, por favor agregue otro".format(numero))
                return
        values = (nombre,
                  horario,
                  activo,
                  numero)
        self.workersinfo[numero] = values
        self.loadTable()


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

