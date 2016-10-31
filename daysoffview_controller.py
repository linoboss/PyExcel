import sys
from PyQt4 import uic
from PyQt4 import QtGui, QtSql, QtCore
import assets.sql as sql
from assets.work_day_tools import DateFilterProxyModel
from assets.dates_tricks import MyDates as md


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

        # tableView Setup
        self.tableView.resizeColumnsToContents()

    @QtCore.pyqtSlot("QModelIndex")
    def on_tableView_clicked(self, index):
        pass

    @QtCore.pyqtSlot("QString")
    def on_qoption_currentIndexChanged(self):
        index = self.qoption.currentIndex()
        self.setupMapper_(index)
        self.setupTable_(index)

    @QtCore.pyqtSlot()
    def on_qadd_to_database_clicked(self):
        model = self.mapper.model()

        option = self.stackedWidget.currentIndex()
        if option == 0:
            self.qhdays.setValue(1)
        elif option == 2:
            self.qdayofftype.setValue(2)
        elif option == 3:
            self.qdayofftype.setValue(1)

        self.qname.setText(
            self.selectedWorkerid()
        )

        workdays_model = QtSql.QSqlTableModel()
        workdays_model.setTable("WorkDays")
        workdays_model.select()
        while workdays_model.canFetchMore(): workdays_model.fetchMore()
        workdays_model.setEditStrategy(workdays_model.OnManualSubmit)

        if option < 2:
            # National date and SpecialDate
            nameFilter = '.*'
            fdate = self.mapper.mappedWidgetAt(2).date()
            days = self.mapper.mappedWidgetAt(3).value()
            tdate = fdate.addDays(days - 1)
            keyColumn = workdays_model.fieldIndex("Holidayid")

        else:
            # WorkerPass and Vacations
            nameFilter = self.mapper.mappedWidgetAt(1).text()
            fdate = self.mapper.mappedWidgetAt(2).date()
            tdate = self.mapper.mappedWidgetAt(3).date()
            keyColumn = workdays_model.fieldIndex("WPid")

        nameproxymodel = QtGui.QSortFilterProxyModel()
        nameproxymodel.setSourceModel(workdays_model)
        nameproxymodel.setFilterKeyColumn(workdays_model.fieldIndex("worker"))
        nameproxymodel.setFilterRegExp(nameFilter)

        dateproxymodel = DateFilterProxyModel()
        dateproxymodel.setSourceModel(nameproxymodel)
        dateproxymodel.setFilterKeyColumn(workdays_model.fieldIndex("day"))
        dateproxymodel.setRangeDateFilter(fdate, tdate)
        if option == 0: dateproxymodel.ignoreYear = True

        self.mapper.submit()
        model.submitAll()

        # Its necesary to wait for the database to autoincrement the id and assign a value
        item = model.index(model.rowCount()-1, 0).data()

        for row in range(dateproxymodel.rowCount()):
            index = dateproxymodel.index(row, keyColumn)
            dateproxymodel.setData(index, item)

        workdays_model.submitAll()

        model.addRow()
        self.mapper.toLast()

        self.tableView.resizeColumnsToContents()

    @QtCore.pyqtSlot()
    def on_qdelete_clicked(self):

        model = self.mapper.model()

        # As the Selection behavior of the tableView is set to singleRowSelection,
        # there can only be the first row.
        # But warning, the index error on not selectedIndex must be avoided
        if len(self.tableView.selectedIndexes()) == 0:
            return
        tindex = self.tableView.selectedIndexes()[0]
        index = model.sourceIndex(tindex)
        item = model.index(index.row(), 0).data()

        # To delete a register from the holidays and workerPass table,
        # the reference from the workdays table must also be removed
        workdays_model = QtSql.QSqlTableModel()
        workdays_model.setTable("WorkDays")
        workdays_model.select()
        while workdays_model.canFetchMore(): workdays_model.fetchMore()
        workdays_model.setEditStrategy(workdays_model.OnManualSubmit)

        # Set column on the workdays model related to the current table being edited
        keyColumn = (workdays_model.fieldIndex("Holidayid") if self.stackedWidget.currentIndex() < 2
                     else workdays_model.fieldIndex("WPid"))

        proxymodel = QtGui.QSortFilterProxyModel()
        proxymodel.setSourceModel(workdays_model)
        proxymodel.setFilterKeyColumn(keyColumn)
        proxymodel.setFilterRegExp(str(item))

        # Scan the proxymodel and remove the references to the holidayid or workerpasid
        # A List of indexes must be created else the proxymodel updates after each record
        # modification will bypass some of the values
        windexes = []
        for prow in range(proxymodel.rowCount()):
            pindex = proxymodel.index(prow, keyColumn)
            windex = proxymodel.mapToSource(pindex)
            windexes.append(windex)

        for windex in windexes:
            record = workdays_model.record(windex.row())
            record.setValue(keyColumn, None)
            workdays_model.setRecord(windex.row(), record)

        workdays_model.submitAll()

        # Resets the model, allowing deletion
        model.select()
        print(index.row())
        model.removeRow(index.row())
        model.submitAll()
        model.addRow()
        self.mapper.toLast()

        self.tableView.resizeColumnsToContents()

    def setupMapper_(self, option):
        model = DaysoffModel(self)

        if option == 0:
            model.setTable('Holiday')
            self.mapper.setModel(model)
            # National date
            mapperList = ((self.qhname, 1),
                          (self.qhdate, 2),
                          (self.qhdays, 3))

        elif option == 1:
            # Special date
            model.setTable('Holiday')
            self.mapper.setModel(model)
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
            self.mapper.setModel(model)
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
            self.mapper.setModel(model)
            mapperList = ((self.qname, 1),
                          (self.qvacbdate, 2),
                          (self.qvactdate, 3),
                          (self.qdayofftype, 5))

        else:
            raise IndexError("(setupMapper_ has not "
                             "implemented index {}".format(option))

        for k, v in mapperList:
            self.mapper.addMapping(k, v)

        model.addRow()
        self.mapper.toLast()
        self.tableView.setModel(model.filtered)

    def setupTable_(self, option):
        model = self.mapper.model()
        for i in range(model.columnCount()):
            self.tableView.setItemDelegateForColumn(i, QtGui.QStyledItemDelegate(self))

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
            model.setFilterDateColumn(model.fieldIndex("BDate"))
            model.setRangeDateFilter(QtCore.QDate(2000, 1, 1),
                                     QtCore.QDate(2000, 12, 31))
            self.tableView.setItemDelegateForColumn(model.fieldIndex("BDate"),
                                                    DateColumnDelegate(self, "day and month"))

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

            model.setFilterDateColumn(model.fieldIndex("BDate"))
            model.setRangeDateFilter(QtCore.QDate(2001, 1, 1),
                                     QtCore.QDate(2100, 1, 1))
            self.tableView.setItemDelegateForColumn(model.fieldIndex("BDate"),
                                                    DateColumnDelegate(self))

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

            model.setFilterStringColumn(model.fieldIndex('type'))
            model.setFilterString('2')
            self.tableView.setItemDelegateForColumn(model.fieldIndex("BDate"),
                                                    DateColumnDelegate(self))
            self.tableView.setItemDelegateForColumn(model.fieldIndex("TDate"),
                                                    DateColumnDelegate(self))

        elif option == 3:  # Vacaciones
            hidden_columns = (model.fieldIndex("Vacid"),
                              model.fieldIndex("Description"),
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
            model.setFilterStringColumn(model.fieldIndex('type'))
            model.setFilterString('1')
            self.tableView.setItemDelegateForColumn(model.fieldIndex("BDate"),
                                                    DateColumnDelegate(self))
            self.tableView.setItemDelegateForColumn(model.fieldIndex("TDate"),
                                                    DateColumnDelegate(self))

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

        self.tableView.resizeColumnsToContents()

    def selectedWorkerid(self):
        option = self.stackedWidget.currentIndex()
        if option == 2: # DaysOff
            index = self.qwpworker.currentIndex()
            model = self.qwpworker.model()
        elif option == 3: # Vacations
            index = self.qvacworker.currentIndex()
            model = self.qvacworker.model()
        else:
            return ""
        return model.index(index, 0).data()


class DaysoffModel(QtSql.QSqlRelationalTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.dateFilter = DateFilterProxyModel(parent)
        self.dateFilter.setSourceModel(self)
        self.stringFilter = QtGui.QSortFilterProxyModel(parent)
        self.stringFilter.setSourceModel(self.dateFilter)

    @property
    def filtered(self):
        return self.stringFilter

    def setFilterDateColumn(self, column):
        self.dateFilter.setFilterKeyColumn(column)

    def setFilterStringColumn(self, column):
        self.stringFilter.setFilterKeyColumn(column)

    def setRangeDateFilter(self, bdate, tdate):
        self.dateFilter.setRangeDateFilter(bdate, tdate)

    def setFilterString(self, string):
        self.stringFilter.setFilterRegExp(string)

    def addRow(self):
        self.select()
        row = self.rowCount()
        self.insertRow(row)
        return row

    def sourceIndex(self, index):
        source_index = \
            self.dateFilter.mapToSource(
                self.stringFilter.mapToSource(index))
        return source_index


class DateColumnDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent=None, format="yyyy-MM-dd"):
        super().__init__(parent)
        self.format = format

    def createEditor(self, parent, option, index):
        dateedit = QtGui.QDateEdit(parent)
        dateedit.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if self.format == "day and month":
            dateedit.setDisplayFormat("dd-MM")
        else:
            dateedit.setDisplayFormat("dd-MM-yyyy")
        dateedit.setCalendarPopup(True)
        return dateedit

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        if isinstance(value, QtCore.QDateTime):
            value = value.date()
        editor.setDate(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.date())

    def paint(self, painter, option, index):
        document = QtGui.QTextDocument()
        item = index.data()
        color = QtGui.QColor(255, 255, 255)

        if isinstance(item, QtCore.QDateTime):
            item = item.date()

        if isinstance(item, QtCore.QDate):
            if self.format == "day and month":
                date = item.toPyDate()
                text = '{} de {}'.format(date.day,
                                         md.monthName(date.month))
            else:
                text = item.toString(self.format)
        else:
            text = str(item)

        painter.save()
        painter.fillRect(option.rect, color)
        painter.translate(option.rect.x(), option.rect.y())
        document.setHtml(text)
        document.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(100, 20)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = sql.AnvizRegisters()

    print(QtSql.QSqlDatabase().database().tables())
    print('Vacations' in QtSql.QSqlDatabase().database().tables())
    w = Daysoffview_controller()
    w.show()
    sys.exit(app.exec())