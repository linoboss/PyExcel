import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
import assets.helpers as helpers
import assets.work_day_tools as tool

# Uic Loader
qtCreatorFile = "ui\\addworkerview.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


(USERID, NAME, SEX, ISACTIVE) = range(4)
ISACTIVE = 28


class AddWorkerView_controller(Ui_MainWindow, QtBaseClass):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    @QtCore.pyqtSlot()
    def on_qadd_clicked(self):
        # QtGui.QSpinBox().value()
        # QtGui.QCheckBox().isChecked()
        id_ = self.qid.value()
        name = self.qname.text()
        sex = self.qsex.currentText()
        isactive = self.qisactive.isChecked()
        sql.AnvizRegisters().insertInto("Userinfo", id_, name, sex, isactive)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    AddWorkerView_controller().exec()
    sys.exit(app.exec())

