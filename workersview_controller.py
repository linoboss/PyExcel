import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
import assets.helpers as helpers
import assets.work_day_tools as tool

# Uic Loader
qtCreatorFile = "ui\\workersview.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


(USERID, NAME, SEX, ISACTIVE) = range(4)
ISACTIVE = 28


class Workerswiev_controller(Ui_MainWindow, QtBaseClass):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent

        model = QtSql.QSqlRelationalTableModel(self)
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        model.setTable('Userinfo')
        model.select()

        model.setHeaderData(USERID, QtCore.Qt.Horizontal, "ID en\nCaptahuellase")
        model.setHeaderData(NAME, QtCore.Qt.Horizontal, "Nombre")
        model.setHeaderData(SEX, QtCore.Qt.Horizontal, "Sexo")
        model.setHeaderData(ISACTIVE, QtCore.Qt.Horizontal, "Esta\nActivo?")

        # self.tableView = QtGui.QTableView()
        self.tableView.setModel(model)
        self.tableView.setItemDelegate(CustomDelegate(self))
        from itertools import chain
        for hc in chain(range(3, 28), range(29, 40)):
            self.tableView.hideColumn(hc)
        self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QTableView.SelectItems)

    @QtCore.pyqtSlot()
    def on_qadd_clicked(self):
        from addworkerview_controller import AddWorkerView_controller
        awv_c = AddWorkerView_controller(self)
        awv_c.exec()

    @QtCore.pyqtSlot()
    def on_qdelete_clicked(self):
        from deleteworkerview_controller import DeleteWorkerView_controller
        dwv_c = DeleteWorkerView_controller(self)
        dwv_c.exec()


class CustomDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent = None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        column = index.column()
        item = index.data()
        if column == ISACTIVE:
            painter.save()
            if option.state & QtGui.QStyle.State_Selected:
                painter.setPen(QtCore.Qt.white)
                painter.setBrush(option.palette.highlightedText())
                painter.fillRect(option.rect, option.palette.highlight())
            isActive = 'Si' if item else 'No'
            painter.drawText(option.rect, QtCore.Qt.AlignCenter, isActive)
            painter.restore()
        else:
            QtSql.QSqlRelationalDelegate().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        column = index.column()
        if column == ISACTIVE:
            editor = QtGui.QComboBox(parent)
            return editor
        else:
            return QtGui.QTextEdit(parent)

    def setEditorData(self, editor, index):
        column = index.column()
        item = index.data()
        if column == ISACTIVE:
            # editor = QtGui.QComboBox()
            editor.addItems('No Si'.split())
            editor.setCurrentIndex(item)
        else:
            editor.setText(item)

    def commitAndCloseEditor(self):
        pass

    def setModelData(self, editor, model, index):
        # model = QtSql.QSqlRelationalTableModel()
        if isinstance(editor, QtGui.QTextEdit):
            item = editor.toPlainText()
        else:
            # editor = QtGui.QComboBox()
            item = editor.currentIndex()
        model.setData(index, item)

    def sizeHint(self, option, item):
        return QtCore.QSize(100, 20)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    sql.AnvizRegisters()

    checkioview = Workerswiev_controller()
    checkioview.show()

    sys.exit(app.exec())
