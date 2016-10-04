import sys
from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui, QtSql
from assets.anviz_reader import AnvizReader
import assets.work_day_tools as tool
import assets.helpers as helpers
from assets.printReport import PrintReport


qtCreatorFile = "tableView.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class View(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
def intentoDeQuery():
    anvReader = AnvizReader()
    print(anvReader.)


app = QtGui.QApplication(sys.argv)
view = View()
anvReader = AnvizReader()
model = QtSql.QSqlRelationalTableModel()
model.setTable('WorkDays')
model.select()
view.tableView.setModel(model)

view.show()

thread = helpers.Thread()


sys.exit(app.exec())


