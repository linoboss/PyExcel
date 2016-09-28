from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui
import assets.helpers as helpers
import assets.sql as sql
import assets.work_day_tools as tool
from assets.dates_tricks import MyDates as md
from assets.anviz_reader import AnvizReader
import assets.sql as sql


WDH = helpers.Db.tableHeader('Workday')


class PrintReport:
    ACCEPTED = "accepted"
    CANCELED = "canceled"

    def __init__(self, parent=None):
        self.sourceModel = None
        self.doc = QtGui.QTextDocument()
        self.printer = QtGui.QPrinter()
        self.filename = ''

        self.anvReader = AnvizReader()

    def setSourceModel(self, sourceModel):
        self.sourceModel = sourceModel

    def setOutputFileName(self, filename=None):
        filename = helpers.PopUps.search_file(
            'Donde desea ubicar el archivo?',
            sql.ConfigFile.get('print_path'),
            'pdf',
            'save') if not filename else filename
        if filename == '':
            return self.ACCEPTED
        self.printer.setOutputFileName(filename)
        sql.ConfigFile.set('print_path',
                           str.join('\\', filename.split('\\')[:-1]))
        self.filename = filename
        return self.CANCELED

    def setup(self):
        dpi = 96
        self.printer.setResolution(dpi)
        self.printer.setPageSize(QtGui.QPrinter.Letter)
        self.printer.setOrientation(QtGui.QPrinter.Landscape)
        self.printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doc.setDefaultFont(font)

    def createFile(self):
        # printer.setPageMargins(30, 16, 12, 20, QtGui.QPrinter.Millimeter)
        self.doc.print_(self.printer)
        self.doc.documentLayout().setPaintDevice(self.printer)

    def loadDocument(self):
        if self.filename == '':
            raise ValueError('Enter the filename before printing')
        if self.sourceModel is None:
            raise ValueError('Enter the sourceModel before printing')

        scheduleFilter = QtGui.QSortFilterProxyModel(self)
        scheduleFilter.setSourceModel(self.sourceModel)
        scheduleFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        scheduleFilter.setFilterKeyColumn(WDH['shift'])

        printFilter = tool.DateFilterProxyModel()
        printFilter.setSourceModel(scheduleFilter)

        FIRST_REGISTER = 0
        LAST_REGISTER = printFilter.rowCount() - 1

        # Si no hay registros retorna None
        if LAST_REGISTER == 0:
            return

        from_date = printFilter.index(FIRST_REGISTER, WDH['day']).data().toPyDateTime().date()
        to_date = printFilter.index(LAST_REGISTER, WDH['day']).data().toPyDateTime().date()

        not_css = {"td": "padding:5px;",
                   "table": "border-width: 1px;border-style: solid;border-color: black;color: black;"}
        html = ""

        for date in md.dates_range(from_date, to_date):
            printFilter.setSingleDateFilter(date)
            if printFilter.rowCount() == 0: continue
            html += ("<html>"
                     "<body>"
                     "<table><tr>"
                     # "<td><img src='C:\\ControlHorario\\PyExcel\\images\\SGlogo.png'></td>"
                     "<td align=right valign=bottom style='padding-left:450px'>"
                     "<div style='font-size:25px'><b>ASISTENCIAS<br>DIARIAS</b></div></td>"
                     "</tr></table><br><hr>")
            html += ("<p>"
                     "{} {} de {} del {}</p><br>".format(md.dayName(date),
                                                         date.day,
                                                         md.monthName(date.month),
                                                         date.year))
            for sch in self.anvReader.schedules:
                # if sch.lower() == 'nocturno': continue
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

                        if column == WDH['workdayid']:
                            continue
                        elif column == WDH['day']:
                            continue
                        elif column == WDH['intime_3']:
                            continue
                        elif column == WDH['outtime_3']:
                            continue
                        elif column == WDH['shift']:
                            continue
                        elif WDH['intime_1'] <= column <= WDH['outtime_3']:
                            qdate = printFilter.index(row, column).data()
                            if qdate == QtCore.QTime():
                                item = '--:--'
                            else:
                                item = qdate.toString("hh:mm")
                        elif column >= WDH["workedtime"]:
                            item = printFilter.index(row, column).data().toString('hh:mm')
                        else:
                            item = printFilter.index(row, column).data()
                        html += "<td align=center style='{}'>".format(not_css["td"])
                        html += item
                        html += "</td>"

                    html += "<td style='{}'></td>".format(not_css["td"])
                    html += "</tr>"
                html += "</table>"

            # html += "<br>"*6
            # html += "<hr width=300>"
            # html += "<p style='margin-left:380px;'>Revisado por</p>"
            if date != to_date:
                html += "<div style='page-break-before:always'></div>"

        self.doc.setHtml(html)

    def load_and_create_file(self):
        self.loadDocument()
        self.createFile()
