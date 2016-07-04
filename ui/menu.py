import sys
from PyQt4.QtGui import QTableWidgetItem, QDialog, QApplication
from ui import trabajadores, qhorario

from persistence.sql import SQL


class Trabajadores(trabajadores.Ui_Dialog,
                 QDialog):
    def __init__(self):
        super(Trabajadores, self).__init__()
        self.setupUi(self)
        self.trabajadores = SQL().personalShift
        self.__row = 0
        self.tableWidget.setRowCount(len(self.trabajadores.keys()))
        for t, sch in self.trabajadores.items():
            self.append([t, sch.capitalize()])

    def append(self, item, column=0, table=None):
        if type(item) == list:
            for i in item:
                newItem = QTableWidgetItem(i)
                self.tableWidget.setItem(self.__row, column, newItem)
                column += 1
            index_increment = 1
        else:
            newItem = QTableWidgetItem(item)
            index_increment = 1
            self.tableWidget.setItem(self.__row, column, newItem)
        self.__row += index_increment


class Horario(qhorario.Ui_Dialog,
              QDialog):
    def __init__(self):
        super(Horario, self).__init__()
        self.setupUi(self)


app = QApplication(sys.argv)
trab = Trabajadores()
trab.show()
app.exec_()
