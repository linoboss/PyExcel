import sys
from PyQt4 import uic
from PyQt4 import QtSql, QtCore, QtGui
from PyQt4.QtCore import SIGNAL, Qt, pyqtSlot
import assets.sql as sql

# Uic Loader
qtCreatorFile = "ui\\config_dialog.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


# TODO add to the program my own Schedule Configuration interface, for now, i'll work with the default
class ScheduleConfiguration_Controller(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.database_path = QtGui.QLabel()
        self.database_path.setText(
            sql.ConfigFile.get("database_path")
        )

    @pyqtSlot()
    def on_changeDB_clicked(self):
        filename = \
            QtGui.QFileDialog.getOpenFileName(
                self, "Seleccionar archivo Access")

        if filename is not None:
            sql.ConfigFile().set(
                "database_path", filename
            )
            self.database_path.setText(filename)

    @pyqtSlot()
    def on_init_clicked(self):
        if self.confirmar():
            pass
        else:
            return

    @pyqtSlot()
    def on_erase_clicked(self):
        if self.confirmar():
            print('si')
        else:
            return

    @pyqtSlot()
    def on_eraseDay_clicked(self):
        if self.confirmar():
            print('si')
        else:
            return

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        pass

    def confirmar(self):
        messageBox = QtGui.QMessageBox()
        messageBox.setStandardButtons(QtGui.QMessageBox.Yes |
                                      QtGui.QMessageBox.No)
        messageBox.setIcon(QtGui.QMessageBox.Question)
        messageBox.setText("Esta seguro?")
        return messageBox.exec() == QtGui.QMessageBox.Yes


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    schConfig_controller = ScheduleConfiguration_Controller()
    schConfig_controller.show()
    sys.exit(app.exec())