import sys
import usuarios
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot, SIGNAL
from manejo_detablas import QTableWidgetHelper
import sql
from pprint import pprint
import nuevo_trabajador_control as nt
import sql


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
        pprint(self.workersinfo)

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
        interface = nt.AgregarTrabajador(self)
        interface.show()
        self.connect(interface, SIGNAL("Guardar(PyQt_PyObject)"), self.agregarTrabajador)

    def agregarTrabajador(self, params):
        self.errorCheck(params)
        sql.Setup().addWorker(params['nombre'],
                              params['status'],
                              params['horario'],
                              params['numero'])
        self.loadTable()

    def remove(self):
        selectedItems = self.tableWidget.selectedItems()
        self.activeTable.removeRow(selectedItems)

    @pyqtSlot()
    def on_botonModificar_clicked(self):
        selectedItems = self.tableWidget.selectedItems()
        if not selectedItems:
            print("Seleccione un trabajador")
            return
        selectedRow = [i.text() for i in selectedItems]
        nombre = selectedRow[0]
        horario = selectedRow[1]
        status = selectedRow[2]
        numero = selectedRow[3]
        params = {'id': self.workersinfo[int(numero)][0],
                  'nombre': nombre,
                  'status': status,
                  'numero': numero,
                  'horario': horario}

        interface = nt.ModificarTrabajador(self, params)
        interface.show()
        self.connect(interface, SIGNAL("Guardar(PyQt_PyObject)"), self.modificarTrabajador)

    def modificarTrabajador(self, params):
        self.errorCheck(params)
        sql.Setup().modifyWorker(params['id'],
                                 params['nombre'],
                                 params['status'],
                                 params['horario'],
                                 params['numero'])
        self.loadTable()

    @pyqtSlot()
    def on_botonEliminar_clicked(self):
        print("eliminar")


    def on_botonCancelar_clicked(self):
        self.close()

    def errorCheck(self, params):
        numero = params['numero']
        for v in self.workersinfo.values():
            if int(numero) == int(v[4]):
                if int(params['id']) != v[0]:
                    print("El numero {} ya existe, por favor agregue otro".format(numero))
                    QMessageBox().setText("El numero {} ya existe, por favor agregue otro".format(numero))
                    raise ValueError

if __name__ == "__main__":
    app = QApplication(sys.argv)
    users = Usuarios()
    users.show()
    app.exec()

