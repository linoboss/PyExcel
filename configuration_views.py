import sys
import usuarios
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot
from manejo_detablas import QTableWidgetHelper
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
        database = sql.Setup()

        workerstable = database.getWorkersTable()
        self.tableWidget.setRowCount(len(workerstable))
        for i, w, h, s in workerstable:
            self.append([w, h, str(s)])

    @pyqtSlot()
    def on_botonGuardar_clicked(self):
        self.getTableContent()

    def on_botonCancelar_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    users = Usuarios()
    users.show()
    app.exec()

