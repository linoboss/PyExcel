import sys
from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui, QtSql
from assets.anviz_reader import AnvizReader
import assets.work_day_tools as tool
import assets.helpers as helpers

qtCreatorFile = "C:\\workspace\\PyExcel\\sandbox\\tableView.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class TableWindow(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setModel(self, model):
        self.tableView.setModel(model)

app = QtGui.QApplication(sys.argv)
window = TableWindow()
window.show()

anvReader = AnvizReader()

WDH = helpers.Db.tableHeader("WorkDays")

model = QtSql.QSqlRelationalTableModel(window)
model.setTable('WorkDays')
model.setRelation(WDH["worker"], QtSql.QSqlRelation("Userinfo", "Userid",
                                                    "Name"))
model.setRelation(WDH["shift"], QtSql.QSqlRelation("Schedule", "Schid",
                                                   "Schname"))
model.sort(WDH["day"], Qt.AscendingOrder)
model.select()
while model.canFetchMore():
    model.fetchMore()

calculusModel = tool.CalculusModel(window)
calculusModel.setSourceModel(model)
calculusModel.calculateWorkedHours()

totalWorkedTime = tool.TotalizeWorkedTime(calculusModel)
window.setModel(totalWorkedTime)

sys.exit(app.exec())
