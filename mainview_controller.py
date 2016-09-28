import sys
from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui, QtSql
from assets.anviz_reader import AnvizReader
import assets.work_day_tools as tool
import assets.dates_tricks as md
import assets.sql as sql
import assets.helpers as helpers
import configview_controller
from assets.printReport import PrintReport


qtCreatorFile = "ui\\MainView.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


(ID, DAY, WORKER,
 INTIME_1, OUTTIME_1, INTIME_2, OUTTIME_2, INTIME_3, OUTTIME_3,
 SHIFT, WORKED_TIME, EXTRA_TIME, ABSENT_TIME) = list(range(13))


class MainView(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showMaximized()
        self.stackedWidget.setCurrentIndex(0)

        self.initProcedure()

        self.anvReader = self.conectToDatabase()

        # setting the models and filters

        self.model = QtSql.QSqlRelationalTableModel(self)
        self.model.setTable('WorkDays')
        self.model.setRelation(WORKER, QtSql.QSqlRelation("Userinfo", "Userid",
                                                          "Name"))
        self.model.setRelation(SHIFT, QtSql.QSqlRelation("Schedule", "Schid",
                                                         "Schname"))
        self.model.sort(DAY, Qt.AscendingOrder)
        self.model.select()
        while self.model.canFetchMore():
            self.model.fetchMore()

        self.calculusModel = tool.CalculusModel(self)
        self.calculusModel.setSourceModel(self.model)
        self.calculusModel.calculateWorkedHours()

        self.nameFilter = QtGui.QSortFilterProxyModel(self)
        self.nameFilter.setSourceModel(self.calculusModel)
        self.nameFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.nameFilter.setFilterKeyColumn(WORKER)

        self.scheduleFilter = QtGui.QSortFilterProxyModel(self)
        self.scheduleFilter.setSourceModel(self.nameFilter)
        self.scheduleFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.scheduleFilter.setFilterKeyColumn(SHIFT)

        self.dateFilter = tool.DateFilterProxyModel(self)
        self.dateFilter.setSourceModel(self.scheduleFilter)

        # configuring the table
        self.tableView.setModel(self.dateFilter)
        self.tableView.setItemDelegate(tool.WorkDayDelegate(self))
        for column in (0, 7, 8): self.tableView.setColumnHidden(column, True)
        self.tableView.resizeColumnsToContents()
        self.tableView.setSortingEnabled(False)

        # setting the initial values of the comboboxes
        self.qworkers.addItems(
            ["Todos"] + self.anvReader.workers_names)
        self.qschedules.addItems(
            ["Todos"] + self.anvReader.schedules)
        self.qdatesfilter.setCurrentIndex(0)

        # setting the initial values of the filters
        self.qdate.setDate(QtCore.QDate().currentDate())
        self.qtodate.setDate(QtCore.QDate().currentDate())
        self.qfromdate.setDate(QtCore.QDate().currentDate())

        # mostrar todos los registros al inicio
        self.nameFilter.setFilterRegExp('.*')
        self.dateFilter.removeFilter()

    def ask_user_to_reopen_program(self):
        helpers.PopUps.inform_user("Usted cambio la direccion de la base de datos.\n"
                                   "El programa cerrara automaticamente,"
                                   "por favor, abralo nuevamente")
        QtGui.QApplication.instance().closeAllWindows()
        sys.exit()

    @QtCore.pyqtSlot("QAction*")
    def on_menubar_triggered(self, action):
        if action is self.action_database:
            configview = configview_controller.ScheduleConfiguration_Controller(self)
            self.connect(configview, QtCore.SIGNAL('dbChanged()'), self.ask_user_to_reopen_program)
            configview.exec()
        elif action is self.action_registers:
            from checkinoutview_controller import Checkinoutview_Controller
            checkioview = Checkinoutview_Controller(self)
            checkioview.exec()
        elif action is self.action_schedules:
            from schedulesview_controller import  Schedulesview_Controller
            schview = Schedulesview_Controller(self)
            schview.exec()
        else:
            helpers.PopUps.inform_user("not implemented!")

    @QtCore.pyqtSlot("QString")
    def on_qworkers_currentIndexChanged(self, text):
        if text == "Todos":
            self.nameFilter.setFilterRegExp('.*')
        else:
            self.nameFilter.setFilterRegExp(text)

    @QtCore.pyqtSlot("QString")
    def on_qschedules_currentIndexChanged(self, text):
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
        print_report = PrintReport()
        if print_report.setOutputFileName() == print_report.CANCELED:
            return
        print_report.setup()
        print_report.setSourceModel(self.dateFilter)
        print_thread = helpers.Thread(lambda: print_report.load_and_create_file)
        self.connect(print_thread, QtCore.SIGNAL("finished()"), self.documentCreated)
        print_thread.start()
        QtGui.QApplication.processEvents()  # flushes the signal queue and prevents multiple clicks

    @QtCore.pyqtSlot()
    def on_configview_dbChanged(self):
        print('aja!')

    @QtCore.pyqtSlot()
    def on_qdatesrangebutton_clicked(self):
        self.dateFilter.setRangeDateFilter(self.qfromdate.date(),
                                           self.qtodate.date())

    @staticmethod
    def closeProgram():
        app = QtGui.QApplication.instance()
        app.closeAllWindows()
        sys.exit()

    def initProcedure(self):
        pass

    def documentCreated(self):
        from assets.helpers import PopUps
        PopUps.inform_user("El documento fue creado exitosamente")

    # TODO reformular este mecanismo para q el update table sea creado en otro thread
    def conectToDatabase(self):

        initial_path = sql.ConfigFile.get("database_path")
        try:
            anvizReader = AnvizReader()
        except ConnectionError:
            if helpers.PopUps.ask_user_to('Error en la base de datos, desea ubicar '
                                          'una base de datos valida?') == QtGui.QMessageBox.Yes:
                sql.ConfigFile.set('database_path',
                                   helpers.PopUps.search_file("Seleccione una base de datos valida",
                                                              initial_path,
                                                              "database"))
                self.conectToDatabase()
            else:
                self.closeProgram()
        try:
            # TODO if by any reason the database is not correctly configured, load an empy model
            anvizReader.updateTable()
        except TypeError:
            if (helpers.PopUps.ask_user_to("El archivo de la base de datos esta incompleto",
                                           "Desea buscar un archivo distinto?")
                    == QtGui.QMessageBox.Yes):
                self.conectToDatabase()
        except Exception as e:
            helpers.PopUps.error_message(str(e))
        return anvizReader


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec())



