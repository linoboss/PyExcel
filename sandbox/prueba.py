import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
from assets.work_day_tools import DateFilterProxyModel


app = QtGui.QApplication(sys.argv)
a = sql.AnvizRegisters()
model = QtSql.QSqlTableModel()
model.setTable("Dept")
model.select()
row = model.rowCount()

print(row)
model.insertRow(row)
proxymodel = QtGui.QSortFilterProxyModel()
proxymodel.setSourceModel(model)
proxymodel.setFilterKeyColumn(2)
proxymodel.setFilterRegExp(".*")
prow = proxymodel.rowCount()
proxymodel.insertRow(row)

print(prow)
mapper = QtGui.QDataWidgetMapper()
mapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
mapper.setModel(proxymodel)

w1 = QtGui.QLineEdit()
w2 = QtGui.QSpinBox()

tableView = QtGui.QTableView()
tableView.setModel(proxymodel)
tableView.show()
mapper.addMapping(w1, 1)
mapper.addMapping(w2, 2)
mapper.toLast()

w1.setText("eee")
w2.setValue(5)

mapper.submit()
proxymodel.submit()
model.submitAll()

model.select()
row = model.rowCount()
print(row)

app.exec()