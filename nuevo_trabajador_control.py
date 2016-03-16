import sys
import nuevo_trabajador
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, SIGNAL
import sql
from pprint import pprint


class Control(QDialog,
              nuevo_trabajador.Ui_Dialog):
    """
    hola :)
    """

    def __init__(self, parent=None):
        """
        aha!
        :param parent:
        :return:
        """
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

        sql.Setup().addWorker(self.params['nombre'],
                              self.params['status'],
                              self.params['horario'],
                              self.params['numero'])
        self.emit(SIGNAL('Guardar(PyQt_PyObject)'), self.params)

    @pyqtSlot()
    def on_botonCancelar_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    users = Control()
    users.show()
    QObject.connect(users, SIGNAL("Guardar(PyQt_PyObject)"), lambda x: print(x))
    app.exec()