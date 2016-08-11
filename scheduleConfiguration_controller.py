import sys
from PyQt4 import uic
from PyQt4 import QtSql, QtCore, QtGui
from PyQt4.QtSql import QSqlDatabase
from PyQt4.QtCore import SIGNAL, Qt, pyqtSlot
import datetime as dt

# Uic Loader
qtCreatorFile = "ui\\scheduleConfiguration.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


# TODO add to the program my own Schedule Configuration interface, for now, i'll work with the default
class ScheduleConfiguration_Controller(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    @pyqtSlot()
    def on_btn_agregarUsuario_clicked(self):
        print("btn_a")



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    schConfig_controller = ScheduleConfiguration_Controller()
    schConfig_controller.show()
    sys.exit(app.exec())
