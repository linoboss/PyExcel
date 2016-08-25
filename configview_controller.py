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
        self.file_name = ''

    @pyqtSlot()
    def on_changeDB_clicked(self):
        self.file_name = \
            QtGui.QFileDialog.getOpenFileName(
                self, "Seleccionar archivo Access")

        if self.file_name is not None:
            sql.ConfigFile().setDatabasePath(
                self.file_name
            )

    @pyqtSlot()
    def on_init_clicked(self):
        pass

    @pyqtSlot()
    def on_erase_clicked(self):
        print("erase")

    @pyqtSlot()
    def on_eraseDay_clicked(self):
        print("eraseDay")

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        print("button_box")



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    schConfig_controller = ScheduleConfiguration_Controller()
    schConfig_controller.show()
    sys.exit(app.exec())