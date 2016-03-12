import sys
import nuevo_trabajador
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot
import sql
from pprint import pprint


class Control(QDialog,
              nuevo_trabajador.Ui_Dialog):
    def __init__(self, parent=None):
        super(Control, self).__init__(parent)
        self.setupUi(self)
        horarios = ("diurno", "nocturno")
        for h in horarios:
            self.comboBoxHorario.addItem(h)
        self.lineEditNumero.setValidator(QIntValidator(0,10000))

    @pyqtSlot()
    def on_botonListo_clicked(self):
        nombre = self.lineEditNombre.text()
        horario = self.comboBoxHorario.currentText()
        status = bool(self.checkBoxActivo.checkState())
        numero = self.lineEditNumero.text()
        sql.Setup().addWorker(nombre, status, horario, numero)

    @pyqtSlot()
    def on_botonCancelar_clicked(self):
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    users = Control()
    users.show()
    app.exec()