import sys
from pprint import pprint

import nuevo_trabajador_control as nt
import sql
from PyQt4.QtCore import pyqtSlot, SIGNAL
from PyQt4.QtGui import *
from manejo_detablas import QTableWidgetHelper

from ui import usuarios


class PersonalSetup(QTableWidgetHelper,
                    QDialog,
                    usuarios.Ui_Dialog
                    ):
    def __init__(self, parent=None):
        super(PersonalSetup, self).__init__()
        super(QTableWidgetHelper, self).__init__()
        super(QDialog, self).__init__(parent)

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
        col_num = 4
        selectedItems = [i.text() for i in self.tableWidget.selectedItems()]
        converted = []
        index = 0
        for i in range(len(selectedItems)):
            index += 1
            if index % col_num == 0:
                converted.append(selectedItems[i])
                index = 0
        sql.Setup().removeWorkers(converted)
        self.loadTable()

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
    users = PersonalSetup()
    users.show()
    app.exec()

