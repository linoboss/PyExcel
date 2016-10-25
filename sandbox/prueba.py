import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
from assets.work_day_tools import DateFilterProxyModel


app = QtGui.QApplication(sys.argv)
a = sql.AnvizRegisters()

a.createTable("WorkerPass")
print(a.howthequerydid())
