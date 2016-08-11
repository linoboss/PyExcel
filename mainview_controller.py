import sys
import time
from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui, QtSql
from assets.anviz_reader import AnvizReader
import assets.work_day_tools as tool
import assets.dates_tricks as md


qtCreatorFile = "ui\\MainView.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


ID, DAY, WORKER, INTIME_1, OUTTIME_1, INTIME_2, OUTTIME_2, INTIME_3, OUTTIME_3,  SHIFT = list(range(10))


class MainView(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.anvReader = AnvizReader()

        self.anvReader.updateTable()

        self.model = QtSql.QSqlRelationalTableModel(self)
        self.model.setTable('WorkDays')
        self.model.setRelation(WORKER, QtSql.QSqlRelation("Userinfo", "Userid",
                                                          "Name"))
        self.model.select()

        self.nameFilter = QtGui.QSortFilterProxyModel(self)
        self.nameFilter.setSourceModel(self.model)
        self.nameFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.nameFilter.setFilterKeyColumn(WORKER)

        self.scheduleFilter = QtGui.QSortFilterProxyModel(self)
        self.scheduleFilter.setSourceModel(self.nameFilter)
        self.scheduleFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.scheduleFilter.setFilterKeyColumn(SHIFT)

        self.dateFilter = tool.DateFilterProxyModel(self)
        self.dateFilter.setSourceModel(self.scheduleFilter)

        # self.qtable = QtGui.QTableView()
        self.qtable.setModel(self.dateFilter)
        self.qtable.setItemDelegate(tool.WorkDayDelegate(self))
        for column in (0, 7, 8): self.qtable.setColumnHidden(column, True)
        self.qtable.resizeColumnsToContents()
        self.qtable.setSortingEnabled(False)

        # self.qworkers = QtGui.QComboBox()
        self.qworkers.addItems(
            ["Todos"] + self.anvReader.workers_names)
        self.qdatesfilter.setCurrentIndex(0)
        self.qdate.setDate(QtCore.QDate().currentDate())

        # self.qschedules = QtGui.QComboBox()
        self.qschedules.addItems(
            ["Todos"] + list(map(lambda x: str(x.id), self.anvReader.schedules_map.keys())))
        self.qdatesfilter.setCurrentIndex(0)
        self.qdate.setDate(QtCore.QDate().currentDate())

        # mostrar todos los registros al inicio
        self.nameFilter.setFilterRegExp('.*')
        self.dateFilter.removeFilter()

    @QtCore.pyqtSlot("QString")
    def on_qworkers_currentIndexChanged(self, text):
        print(text)
        if text == "Todos":
            self.nameFilter.setFilterRegExp('.*')
        else:
            self.nameFilter.setFilterRegExp(text)

    @QtCore.pyqtSlot("QString")
    def on_qschedules_currentIndexChanged(self, text):
        print(text)
        if text == "Todos":
            self.scheduleFilter.setFilterRegExp('.*')
        else:
            self.scheduleFilter.setFilterRegExp(text)

    @QtCore.pyqtSlot("QDate")
    def on_qdate_dateChanged(self, d):
        self.dateFilter.setSingleDateFilter(d)

    @QtCore.pyqtSlot("int")
    def on_qdatesfilter_activated(self, option):
        self.dateFilter.removeFilter()
        if option == 1:
            self.dateFilter.setSingleDateFilter(option)

    @QtCore.pyqtSlot()
    def on_qprint_clicked(self):
        self.qprint.setDisabled(True)
        printFilter = tool.DateFilterProxyModel()
        printFilter.setSourceModel(self.dateFilter)
        FIRST_REGISTER = 0
        LAST_REGISTER = printFilter.rowCount() - 1

        # Si no hay registros retorna None
        if LAST_REGISTER == 0:
            return

        from_date = printFilter.index(FIRST_REGISTER, DAY).data().toPyDateTime().date()
        to_date = printFilter.dateFilter.index(LAST_REGISTER, DAY).data().toPyDateTime().date()

        for date in md.MyDates.dates_range(from_date, to_date):
            printFilter.setSingleDateFilter(date)
            # from_date1 =
            print()


        QtGui.QApplication.processEvents()  # flushes the signal queue and prevents multiple clicks

        self.qprint.setDisabled(False)

    @QtCore.pyqtSlot()
    def on_qdatesrangebutton_clicked(self):
        self.dateFilter.setRangeDateFilter(self.qfromdate.date(),
                                           self.qtodate.date())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec())



