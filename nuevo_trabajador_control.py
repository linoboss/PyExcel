import sys
import nuevo_trabajador
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, SIGNAL
import sql
from pprint import pprint


class Control(QDialog,
              nuevo_trabajador.Ui_Dialog):
    trigger = pyqtSignal()
    def __init__(self, parent=None):
        super(Control, self).__init__(parent)
        self.setupUi(self)
        horarios = ("diurno", "nocturno")
        for h in horarios:
            self.comboBoxHorario.addItem(h)
        self.lineEditNumero.setValidator(QIntValidator(0, 10000))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.params = {}

    @pyqtSlot()
    def on_botonListo_clicked(self):
        self.params['nombre'] = self.lineEditNombre.text()
        self.params['horario'] = self.comboBoxHorario.currentText()
        self.params['status'] = bool(self.checkBoxActivo.checkState())
        self.params['numero'] = self.lineEditNumero.text()
        self.emit(SIGNAL('Guardar()'))
        #sql.Setup().addWorker(nombre, status, horario, numero)

    @pyqtSlot()
    def on_botonCancelar_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    users = Control()
    users.show()
    QObject.connect(users, SIGNAL("Guardar()"), lambda: print('hola'))
    app.exec()