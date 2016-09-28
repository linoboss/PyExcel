import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
import assets.helpers as helpers
import assets.work_day_tools as tool

# Uic Loader
qtCreatorFile = "ui\\addworkerview.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class AddWorkerView_controller(Ui_MainWindow, QtBaseClass):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.anvRgs = sql.AnvizRegisters()
        self.qindate.setDate(QtCore.QDate(1, 1, 1).currentDate())
        self.shifts = self.anvRgs.schedules_map()
        self.workers = self.anvRgs.getWorkers("byId")
        self.qschedule.addItems(list(map(lambda k: k.name, self.shifts.keys()))[::-1])
        self.toolBox.setCurrentIndex(0)

    @QtCore.pyqtSlot()
    def on_qadd_clicked(self):
        # Escenciales
        id_worker = self.qid.value()
        name = self.qname.text()
        isactive = self.qisactive.isChecked()
        schedule = self.qschedule.currentText()

        # Personal data
        sex = self.qsex.currentText()
        ci = self.qci.text()
        birthdate = self.qbirthdate.text()
        phone = self.qphone.text()
        address = self.qaddress.text()
        description = self.qdescription.toPlainText()
        # Work data
        position = self.qposition.text()
        indate = self.qindate.date()

        # set schedule id
        id_sch = None
        for k in self.shifts.keys():
            if str(k) == schedule:
                id_sch = int(k)

        # Checking for no duplicated ids
        if id_worker == 0:
            helpers.PopUps.inform_user("ID en captahuellas no puede ser cero")
            return
        elif id_worker in self.workers:
            helpers.PopUps.inform_user("ID en captahuellas duplicada")
            return

        # inserting new worker's schedule
        sql.AnvizRegisters().insertInto("UserShift",
                                        Userid=id_worker,
                                        Schid=id_sch,
                                        BeginDate=indate,
                                        EndDate=" ")

        # inserting new worker's data
        sql.AnvizRegisters().insertInto("Userinfo",
                                        Userid=id_worker,
                                        Name=name,
                                        Sex=sex,
                                        Brithday=birthdate,
                                        EmployDate=indate,
                                        Telephone=phone,
                                        Duty=position,
                                        Address=address,
                                        Remark=description,
                                        IDCard=ci,
                                        isActive=isactive)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    AddWorkerView_controller().exec()
    sys.exit(app.exec())

