import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
import assets.helpers as helpers

# Uic Loader
qtCreatorFile = "ui\\workersview.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


(USERID, NAME, SEX) = range(3)
ISACTIVE = 28


class Workersview_controller(Ui_MainWindow, QtBaseClass):
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
        self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)

    @QtCore.pyqtSlot()
    def on_qadd_clicked(self):
        from addworkerview_controller import AddWorkerView_controller
        awv_c = AddWorkerView_controller(self)
        awv_c.exec()

    @QtCore.pyqtSlot()
    def on_qdelete_clicked(self):
        table_model = self.tableView.model()
        selection = self.tableView.selectionModel()
        row = selection.currentIndex().row()
        worker_id = table_model.index(row, 0).data()
        worker_name = table_model.index(row, 1).data()
        worker_gender = table_model.index(row, 2).data()
        letter = 'a' if worker_gender == "Femenino" else 'o'

        user_ans = helpers.PopUps.ask_user_to("{} sera eliminad{} de la base de "
                                              "datos permanentemente, proceder?".format(worker_name, letter))
        if user_ans == helpers.YES:
            self.removeWorker(worker_id)
            table_model.select()

    @staticmethod
    def removeWorker(worker_id):
        workdays_model = QtSql.QSqlTableModel()
        workdays_model.setTable("WorkDays")
        workdays_model.setFilter("worker='{}'".format(worker_id))
        workdays_model.select()
        for row in range(workdays_model.rowCount()):
            workdays_model.removeRow(row)
        workdays_model.submitAll()

        usershift_model = QtSql.QSqlTableModel()
        usershift_model.setTable("UserShift")
        usershift_model.setFilter("Userid='{}'".format(worker_id))
        usershift_model.select()
        usershift_model.removeRow(0)
        usershift_model.submitAll()

        userinfo_model = QtSql.QSqlTableModel()
        userinfo_model.setTable("Userinfo")
        userinfo_model.setFilter("Userid='{}'".format(worker_id))
        userinfo_model.select()
        userinfo_model.removeRow(0)
        userinfo_model.submitAll()
        userinfo_model.select()


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

    checkioview = Workersview_controller()
    checkioview.show()

    sys.exit(app.exec())
