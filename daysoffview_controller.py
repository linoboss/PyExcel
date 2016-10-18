import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
from assets.work_day_tools import DateFilterProxyModel


# Uic Loader
qtCreatorFile = "ui\\daysoffview.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Daysoffview_controller(Ui_MainWindow, QtBaseClass):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent

        # widgets de complemento
        self.qhdays = QtGui.QSpinBox()
        self.qhdays.setValue(1)
        self.qdayofftype = QtGui.QSpinBox()
        self.qdayofftype.setValue(3)
        self.qname = QtGui.QLineEdit()

        # valores iniciales
        for dateEdit in (self.qh2date, self.qwpbdate, self.qwptdate,
                         self.qvacbdate, self.qvactdate):
            dateEdit.setDate(QtCore.QDate().currentDate())

        INITIAL_INDEX = 0

        # setup of comoboxes
        userinfo_model = QtSql.QSqlTableModel(self)
        userinfo_model.setTable("Userinfo")
        userinfo_model.select()
        for combobox in (self.qwpworker, self.qvacworker):
            combobox.setModel(userinfo_model)
            combobox.setModelColumn(1)
        # setup mapper
        self.mapper = QtGui.QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
        self.setupMapper_(INITIAL_INDEX)
        self.setupTable_(INITIAL_INDEX)

        # Set Fecha Nacional as the default option to view
        self.qoption.setCurrentIndex(INITIAL_INDEX)
        self.stackedWidget.setCurrentIndex(INITIAL_INDEX)

    @QtCore.pyqtSlot("QModelIndex")
    def on_tableView_clicked(self, index):
        self.mapper.setCurrentModelIndex(index)

    @QtCore.pyqtSlot("QString")
    def on_qoption_currentIndexChanged(self):
        index = self.qoption.currentIndex()
        self.setupMapper_(index)
        self.setupTable_(index)

    @QtCore.pyqtSlot()
    def on_qadd_to_database_clicked(self):
        row = self.mapper.currentIndex()
        model = self.mapper.model().sourceModel().sourceModel()

        option = self.stackedWidget.currentIndex()
        if option == 2:
            self.qdayofftype.setValue(2)
        elif option == 3:
            self.qdayofftype.setValue(1)
        if self.mapper.currentIndex() == model.rowCount() - 1:
            # Creation
            self.qname.setText(
                self.selectedWorkerid()
            )
            self.mapper.submit()
            model.submitAll()
            model.select()
            row = model.rowCount()
            model.insertRow(row)
        else:
            # Edition
            model.select()
            for i in range(1, 6):
                widget = self.mapper.mappedWidgetAt(i)
                item = None
                if isinstance(widget, QtGui.QDateEdit):
                    item = widget.date()
                elif isinstance(widget, QtGui.QLineEdit):
                    item = widget.text()
                elif isinstance(widget, QtGui.QSpinBox):
                    item = widget.value()
                elif isinstance(widget, QtGui.QComboBox):
                    item = widget.currentText()
                elif isinstance(widget, QtGui.QTextEdit):
                    item = widget.toPlainText()
                index = model.index(row, i)
                model.setData(index, item)

            model.submitAll()
            row = model.rowCount()
            model.insertRow(row)

        self.mapper.setCurrentIndex(row)

    @QtCore.pyqtSlot()
    def on_qdelete_clicked(self):
        row = self.mapper.currentIndex()
        basemodel = self.mapper.model().sourceModel().sourceModel()
        model = self.mapper.model()
        basemodel.select()
        model.removeRow(row)
        basemodel.submitAll()
        basemodel.select()
        basemodel.insertRow(basemodel.rowCount())
        self.mapper.toLast()

    def setupMapper_(self, option):
        model = QtSql.QSqlRelationalTableModel()
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        proxy1 = DateFilterProxyModel()
        proxy1.setSourceModel(model)
        proxy2 = QtGui.QSortFilterProxyModel()
        proxy2.setSourceModel(proxy1)

        if option == 0:
            model.setTable('Holiday')
            self.mapper.setModel(proxy2)
            # National date
            mapperList = ((self.qhname, 1),
                          (self.qhdate, 2),
                          (self.qhdays, 3))

        elif option == 1:
            # Special date
            model.setTable('Holiday')
            self.mapper.setModel(proxy2)
            mapperList = ((self.qh2name, 1),
                          (self.qh2date, 2),
                          (self.qh2days, 3))

        elif option == 2:
            # Days off
            model.setTable('WorkerPass')
            model.setRelation(model.fieldIndex("Userid"),
                              QtSql.QSqlRelation(
                                  "Userinfo",
                                  "Userid", "Name"))
            self.mapper.setModel(proxy2)
            mapperList = ((self.qname, 1),
                          (self.qwpbdate, 2),
                          (self.qwptdate, 3),
                          (self.qtext, 4),
                          (self.qdayofftype, 5))

        elif option == 3:
            # Vacations
            model.setTable('WorkerPass')
            model.setRelation(model.fieldIndex("Userid"),
                              QtSql.QSqlRelation(
                                  "Userinfo",
                                  "Userid", "Name"))
            self.mapper.setModel(proxy2)
            mapperList = ((self.qname, 1),
                          (self.qvacbdate, 2),
                          (self.qvactdate, 3),
                          (self.qdayofftype, 5))

        else:
            raise IndexError("(setupMapper_ has not "
                             "implemented index {}".format(option))

        for k, v in mapperList:
            self.mapper.addMapping(k, v)

        model.select()
        row = model.rowCount()
        model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        self.tableView.setModel(proxy2)

    def setupTable_(self, option):
        # self.tableView = QtGui.QTableView()
        typeproxy = self.tableView.model()
        dateproxy = typeproxy.sourceModel()
        model = dateproxy.sourceModel()

        if option == 0:  # Fecha nacional
            hidden_columns = (model.fieldIndex("Holidayid"),
                              model.fieldIndex("Days"))
            visible_columns = (model.fieldIndex("Name"),
                               model.fieldIndex("BDate"))
            model_header_data = ((model.fieldIndex("Name"),
                                  QtCore.Qt.Horizontal,
                                  "Nombre y Descripcion"),
                                 (model.fieldIndex("BDate"),
                                  QtCore.Qt.Horizontal,
                                  "Fecha"))
            dateproxy.setFilterKeyColumn(model.fieldIndex("BDate"))
            dateproxy.setRangeDateFilter(QtCore.QDate(2000, 1, 1),
                                         QtCore.QDate(2000, 12, 31))
        elif option == 1:  # Fecha especial
            hidden_columns = (model.fieldIndex("Holidayid"),)
            visible_columns = (model.fieldIndex("Name"),
                               model.fieldIndex("BDate"),
                               model.fieldIndex("Days"))
            model_header_data = ((model.fieldIndex("Name"),
                                  QtCore.Qt.Horizontal,
                                  "Nombre y Descripcion"),
                                 (model.fieldIndex("BDate"),
                                  QtCore.Qt.Horizontal,
                                  "Fecha"),
                                 (model.fieldIndex("Days"),
                                  QtCore.Qt.Horizontal,
                                  "Dias"))

            dateproxy.setFilterKeyColumn(model.fieldIndex("BDate"))
            dateproxy.setRangeDateFilter(QtCore.QDate(2001, 1, 1),
                                         QtCore.QDate(2040, 1, 1))

        elif option == 2:  # Dias libres
            hidden_columns = (model.fieldIndex("WPid"),
                              model.fieldIndex("Type"))
            visible_columns = (model.fieldIndex("Name"),
                               model.fieldIndex("BDate"),
                               model.fieldIndex("TDate"),
                               model.fieldIndex("Description"))
            model_header_data = ((model.fieldIndex("Name"),
                                  QtCore.Qt.Horizontal,
                                  "Nombre"),
                                 (model.fieldIndex("BDate"),
                                  QtCore.Qt.Horizontal,
                                  "Desde"),
                                 (model.fieldIndex("TDate"),
                                  QtCore.Qt.Horizontal,
                                  "Hasta"),
                                 (model.fieldIndex("Description"),
                                  QtCore.Qt.Horizontal,
                                  "Caracteristica"))

            typeproxy.setFilterKeyColumn(model.fieldIndex('type'))
            typeproxy.setFilterRegExp('2')

        elif option == 3:  # Vacaciones
            hidden_columns = (model.fieldIndex("Vacid"),
                              model.fieldIndex("Caract"),
                              model.fieldIndex("Type"))
            visible_columns = (model.fieldIndex("Name"),
                               model.fieldIndex("BDate"),
                               model.fieldIndex("TDate"))
            model_header_data = ((model.fieldIndex("Name"),
                                  QtCore.Qt.Horizontal,
                                  "Nombre"),
                                 (model.fieldIndex("BDate"),
                                  QtCore.Qt.Horizontal,
                                  "Desde"),
                                 (model.fieldIndex("TDate"),
                                  QtCore.Qt.Horizontal,
                                  "Hasta"),
                                 (model.fieldIndex("Carat"),
                                  QtCore.Qt.Horizontal,
                                  "Caracteristica"))
            typeproxy.setFilterKeyColumn(model.fieldIndex('type'))
            typeproxy.setFilterRegExp('1')

        else:
            hidden_columns = []
            visible_columns = []
            model_header_data = []

        for column in hidden_columns:
            self.tableView.hideColumn(column)
        for column in visible_columns:
            self.tableView.showColumn(column)
        for header_data in model_header_data:
            model.setHeaderData(*header_data)

    def selectedWorkerid(self):
        option = self.stackedWidget.currentIndex()
        if option == 2: # DaysOff
            index = self.qwpworker.currentIndex()
            model = self.qwpworker.model()
        elif option == 3: # Vacations
            index = self.qvacworker.currentIndex()
            model = self.qvacworker.model()
        else:
            raise IndexError
        return model.index(index, 0).data()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = sql.AnvizRegisters()

    print(QtSql.QSqlDatabase().database().tables())
    print('Vacations' in QtSql.QSqlDatabase().database().tables())
    w = Daysoffview_controller()
    w.show()
    sys.exit(app.exec())
