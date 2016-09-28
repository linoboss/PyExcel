import sys
from assets.dates_tricks import MyDates as md
import assets.sql as sql
import assets.helpers as helpers
from assets.anviz_reader import AnvizReader
from PyQt4 import QtGui, QtCore
from pprint import pprint

app = QtGui.QApplication(sys.argv)
anvRgs = sql.AnvizRegisters()
if 'isActive' not in helpers.Db.tableHeader('Userinfo'):
    anvRgs.addColumn('Userinfo', 'isActive', bool)

if 'isOvernight' not in helpers.Db.tableHeader('Schedule'):
    anvRgs.addColumn('Schedule', 'isOvernight', bool)

sys.exit()