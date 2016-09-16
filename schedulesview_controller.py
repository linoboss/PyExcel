import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
import assets.helpers as helpers
import assets.work_day_tools as tool

# Uic Loader
qtCreatorFile = "ui\\schedulesview.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


(TIMEID, TIMENAME, INTIME, OUTTIME,
 BINTIME, EINTIME, BOUTTIME, EOUTTIME) = range(8)


class Schedulesview_Controller(Ui_MainWindow, QtBaseClass):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent

        model = QtSql.QSqlRelationalTableModel(self)
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        model.setTable('TimeTable')
        model.select()
        model.setHeaderData(TIMENAME, QtCore.Qt.Horizontal, "Nombre")
        model.setHeaderData(INTIME, QtCore.Qt.Horizontal, "Entrada")
        model.setHeaderData(OUTTIME, QtCore.Qt.Horizontal, "Salida")
        model.setHeaderData(BINTIME, QtCore.Qt.Horizontal, "Inicio de\nEntrada")
        model.setHeaderData(EINTIME, QtCore.Qt.Horizontal, "Fin de la\nEntrada")
        model.setHeaderData(BOUTTIME, QtCore.Qt.Horizontal, "Inicio de\nSalida")
        model.setHeaderData(EOUTTIME, QtCore.Qt.Horizontal, "Fin de la\nSalida")

        # self.tableView = QtGui.QTableView()
        self.tableView.setModel(model)
        self.tableView.setItemDelegate(CustomDelegate(self))
        for hc in (0, 8, 9, 10, 11, 12, 13, 14, 15):
            self.tableView.hideColumn(hc)
        self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QTableView.SelectItems)


class CustomDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent = None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        column = index.column()
        item = index.data()
        if column == TIMENAME:
            painter.save()
            if option.state & QtGui.QStyle.State_Selected:
                painter.setPen(QtCore.Qt.white)
                painter.setBrush(option.palette.highlightedText())
                painter.fillRect(option.rect, option.palette.highlight())
            painter.drawText(option.rect, QtCore.Qt.AlignCenter, item.capitalize())
            painter.restore()
        else:
            QtSql.QSqlRelationalDelegate().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        column = index.column()
        item = index.model().data(index)
        if column == TIMENAME:
            return QtGui.QTextEdit(parent)
        else:
            return QtGui.QTimeEdit(parent)

    def setEditorData(self, editor, index):
        column = index.column()
        item = index.data()
        if column == TIMENAME:
            editor.setText(item)
        else:
            # editor = QtGui.QTimeEdit()
            time = QtCore.QTime().fromString(item, "h:m")
            editor.setTime(time)

    def commitAndCloseEditor(self):
        pass

    def setModelData(self, editor, model, index):
        # model = QtSql.QSqlRelationalTableModel()
        if isinstance(editor, QtGui.QTextEdit):
            text = editor.toPlainText()
        else:
            text = editor.time().toString("hh:mm")
        model.setData(index, text)

    def sizeHint(self, option, index):
        return QtCore.QSize(100, 20)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    sql.AnvizRegisters()

    checkioview = Schedulesview_Controller()
    checkioview.show()

    sys.exit(app.exec())
