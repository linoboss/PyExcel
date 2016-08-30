import sys
from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui, QtSql
from assets.anviz_reader import AnvizReader
import assets.work_day_tools as tool
import assets.dates_tricks as md


qtCreatorFile = "ui\\MainView.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


(ID, DAY, WORKER,
 INTIME_1, OUTTIME_1, INTIME_2, OUTTIME_2, INTIME_3, OUTTIME_3,
 SHIFT, WORKED_TIME, EXTRA_TIME, ABSENT_TIME) = list(range(13))


class MainView(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(100, 100, 1200, 600)
        self.stackedWidget.setCurrentIndex(0)

        self.anvReader = AnvizReader()

        self.anvReader.updateTable()

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

        scheduleFilter = QtGui.QSortFilterProxyModel(self)
        scheduleFilter.setSourceModel(self.dateFilter)
        scheduleFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        scheduleFilter.setFilterKeyColumn(SHIFT)

        printFilter = tool.DateFilterProxyModel()
        printFilter.setSourceModel(scheduleFilter)

        # self.qtable = QtGui.QTableView()
        self.qtable.setModel(printFilter)
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
            ["Todos"] + self.anvReader.schedules)
        self.qdatesfilter.setCurrentIndex(0)
        self.qdate.setDate(QtCore.QDate().currentDate())

        # mostrar todos los registros al inicio
        self.nameFilter.setFilterRegExp('.*')
        self.dateFilter.removeFilter()

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
        self.qprint.setDisabled(True)
        scheduleFilter = QtGui.QSortFilterProxyModel(self)
        scheduleFilter.setSourceModel(self.dateFilter)
        scheduleFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        scheduleFilter.setFilterKeyColumn(SHIFT)

        printFilter = tool.DateFilterProxyModel()
        printFilter.setSourceModel(scheduleFilter)

        FIRST_REGISTER = 0
        LAST_REGISTER = printFilter.rowCount() - 1

        # Si no hay registros retorna None
        if LAST_REGISTER == 0:
            return

        from_date = printFilter.index(FIRST_REGISTER, DAY).data().toPyDateTime().date()
        to_date = printFilter.index(LAST_REGISTER, DAY).data().toPyDateTime().date()

        not_css = {"td": "padding:5px;",
                   "table": "border-width: 1px;border-style: solid;border-color: black;color: black;"}
        html = ""

        for date in md.MyDates.dates_range(from_date, to_date):
            printFilter.setSingleDateFilter(date)
            if printFilter.rowCount() == 0: continue
            html += ("<html>"
                     "<body>"
                     "<table><tr>"
                     "<td><img src='C:\\workspace\\PyExcel\\images\\SGlogo.png'></td>"
                     "<td align=right valign=bottom style='padding-left:450px'>"
                     "<div style='font-size:25px'><b>ASISTENCIAS<br>DIARIAS</b></div></td>"
                     "</tr></table><br><hr>")
            html += ("<p>"
                     "{} {} de {} del {}</p><br>".format(md.MyDates.dayName(date),
                                                         date.day,
                                                         md.MyDates.monthName(date.month),
                                                         date.year))
            for sch in self.anvReader.schedules:
                if sch.lower() == 'nocturno': continue
                scheduleFilter.setFilterRegExp(sch)
                if printFilter.rowCount() == 0: continue
                html += "Horario {}".format(sch)
                html += "<table cellspacing='0' style='{}'>".format(not_css["table"])
                html += ("<tr>"
                         "<th width=170>Nombre</th>"
                         "<th width=70>Entrada</th>"
                         "<th width=70>Salida</th>"
                         "<th width=70>Entrada</th>"
                         "<th width=70>Salida</th>"
                         "<th width=70 style='font-size:10px'>Tiempo<br>Trabajado</th>"
                         "<th width=70 style='font-size:10px'>Tiempo<br>Extra</th>"
                         "<th width=70 style='font-size:10px'>Tiempo<br>Ausente</th>"
                         "<th width=200>Firma</th>"
                         "</tr>")
                for row in range(printFilter.rowCount()):
                    html += "<tr>"

                    for column in range(13):

                        if column == ID: continue
                        elif column == DAY: continue
                        elif column == INTIME_3: continue
                        elif column == OUTTIME_3: continue
                        elif column == SHIFT: continue
                        elif INTIME_1 <= column <= OUTTIME_3:
                            qdate = printFilter.index(row, column).data()
                            if qdate == QtCore.QTime():
                                item = '--:--'
                            else:
                                item = qdate.toString("hh:mm")
                        elif column >= WORKED_TIME:
                            item = printFilter.index(row, column).data().toString('hh:mm')
                        else:
                            item = printFilter.index(row, column).data()
                        html += "<td align=center style='{}'>".format(not_css["td"])
                        html += item
                        html += "</td>"

                    html += "<td style='{}'></td>".format(not_css["td"])
                    html += "</tr>"
                html += "</table>"

            #  html += "<br>"*6
            #  html += "<hr width=300>"
            #  html += "<p style='margin-left:380px;'>Revisado por</p>"
            html += "<div style='page-break-before:always'></div>"

        # send the html document to the printer
        printer = QtGui.QPrinter()
        dpi = 96
        printer.setResolution(dpi)
        printer.setOutputFileName("foo.pdf")
        printer.setPageSize(QtGui.QPrinter.Letter)
        printer.setOrientation(QtGui.QPrinter.Landscape)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        # printer.setPageMargins(30, 16, 12, 20, QtGui.QPrinter.Millimeter)
        font = QtGui.QFont()
        font.setPointSize(12)
        doc = QtGui.QTextDocument()
        doc.setDefaultFont(font)
        doc.setHtml(html)
        doc.print_(printer)
        doc.documentLayout().setPaintDevice(printer)

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



