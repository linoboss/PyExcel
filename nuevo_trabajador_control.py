import sys
import nuevo_trabajador
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, SIGNAL

from pprint import pprint

horarios = ("diurno", "nocturno")


class AgregarTrabajador(QDialog,
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
        super(AgregarTrabajador, self).__init__(parent)
        self.setupUi(self)
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

        self.emit(SIGNAL('Guardar(PyQt_PyObject)'), self.params)

    @pyqtSlot()
    def on_botonCancelar_clicked(self):
        self.close()


class ModificarTrabajador(QDialog,
                          nuevo_trabajador.Ui_Dialog):
    """
    hola :)
    """

    def __init__(self, parent=None, params=None):
        """
        aha!
        :param parent:
        :return:
        """
        assert isinstance(params, dict), "params debe ser un diccionario con las keys:" +\
            "id, nombre, status, horario, numero"
        super(ModificarTrabajador, self).__init__(parent)
        self.setupUi(self)
        self.params = params

        for h in horarios:
            self.comboBoxHorario.addItem(h)

        self.lineEditNumero.setText(params['numero'])
        self.lineEditNombre.setText(params["nombre"])
        self.checkBoxActivo.setCheckable(bool(params['status']))
        self.comboBoxHorario.setCurrentText(params['horario'])

        self.lineEditNumero.setValidator(QIntValidator(0, 10000))
        self.setAttribute(Qt.WA_DeleteOnClose)

    @pyqtSlot()
    def on_botonListo_clicked(self):
        self.params['nombre'] = self.lineEditNombre.text()
        self.params['horario'] = self.comboBoxHorario.currentText()
        self.params['status'] = bool(self.checkBoxActivo.checkState())
        self.params['numero'] = self.lineEditNumero.text()

        self.emit(SIGNAL('Guardar(PyQt_PyObject)'), self.params)

    @pyqtSlot()
    def on_botonCancelar_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    users = ModificarTrabajador()
    users.show()
    QObject.connect(users, SIGNAL("Guardar(PyQt_PyObject)"), lambda x: print(x))
    app.exec()