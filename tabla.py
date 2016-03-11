import sys
import datetime
from PyQt4.QtGui import *
from table import Ui_Form
import AnvizReader
from diasnolaborables import DiasNoLaborables
from dates_tricks import MyDates
from to_excel import ToExcel
from sql import Setup
from pprint import pprint

header = [['', 'Matutino', '', 'Vespertino'],
          ['Nombre', 'entrada', 'salida', 'entrada', 'salida','Horas\nlaboradas',
           'Tiempo\nextra', 'Tiempo\nausente', '   Firma   ']]
header2 = ["Nombre", "Tiempo\ntrabajado", "Tiempo\nextra", "Tiempo\nausente"]
header3 = [['', 'Nocturno'],
          ['Nombre', 'entrada', 'salida', 'Horas\nlaboradas',
           'Tiempo\nextra', 'Tiempo\nausente', '   Firma   ']]

personalShift = Setup().personalShift()
horarios = ('diurno', 'nocturno')

heads = {'diurno': header, 'nocturno': header3}


class Table(QWidget, Ui_Form):
    def __init__(self):
        super(Table, self).__init__()
        self.setupUi(self)

        self.table_logs.setColumnCount(10)
        self.table_rango.setColumnCount(10)
        self.__row = 0
        self.diasnolaborables = DiasNoLaborables()
        self.tablesContent = {'logs': [], 'rango': []}

    def append(self, item, column=0, color=None):

        if type(item) == list:
            for i in item:
                newItem = QTableWidgetItem(i)
                if color is not None: newItem.setBackground(QColor(color))
                self.activeTable.setItem(self.__row, column, newItem)
                column += 1
            index_increment = 1
        else:
            newItem = QTableWidgetItem(item)
            if color is not None:
                newItem.setBackground(color)
            index_increment = 1
            self.activeTable.setItem(self.__row, column, newItem)
            item = [item]
            column += 1
        self.__row += index_increment

        if self.activeTable is self.table_logs: tableName = 'logs'
        elif self.activeTable is self.table_rango: tableName = 'rango'
        else: tableName = 'otra'
        save = item + ['' for i in range(10 - column)]
        self.tablesContent[tableName] += [save, ]

    def paintHorary(self, row, horary):
        column = 1
        for h in (horary['matutino']['entrada'], horary['matutino']['salida'],
                         horary['vespertino']['entrada'], horary['vespertino']['salida'],
                         horary['nocturno']['entrada'], horary['nocturno']['salida'],):
            if not h == '--':
                self.activeTable.item(row, column).setBackground(QColor(150, 255, 150))
            else:
                self.activeTable.item(row, column).setBackground(QColor(255, 100, 100))
            column += 1

    def paintNotWorkable(self):
        pass

    def loadTables(self, reporte):
        self.reporte = reporte
        self.totals = AnvizReader.TotalizeByRange(reporte)
        self.reset()

        #Cargar tabla de dias
        self.activeTable = self.table_logs
        self.__workdays = list(self.reporte.content)
        day_table_length = len(self.__workdays) * (2 + len(header) + len(self.reporte.personal))
        self.table_logs.setRowCount(day_table_length)
        while self.__workdays: self.workDays()
        self.table_logs.setRowCount(self.__row + 1)

        #Cargar tabla de rango
        self.activeTable = self.table_rango
        self.__row = 0
        self.__workrange = list(self.totals.byRange)
        month_table_length = len(self.__workrange) * (5 + len(self.reporte.personal))
        self.table_rango.setRowCount(month_table_length)
        while self.__workrange: self.workRange()
        self.table_rango.setRowCount(self.__row + 1)

    def workDays(self):

        date = self.__workdays[0].date
        year, month, day = date.year, date.month, date.day
        fecha_invertida = "Fecha: {dia} {d} de {m} del {year}".format(dia=MyDates.dayName(year, month, day),
                                                                      d=day,
                                                                      m=MyDates.monthName(month),
                                                                      year=year)
        #TODO mostrar los dias no laborables como una fecha coloreada en azul claro
        if not self.diasnolaborables.isWorkable(date):
            self.activeTable.setSpan(self.__row, 0, 1, 10)
            self.append(fecha_invertida, color=QColor(200,200,255))

            if self.diasnolaborables.significado(date) is not None:
                self.activeTable.setSpan(self.__row, 0, 1, 10)
                self.append(self.diasnolaborables.significado(date), color=QColor(200,200,255))
            self.append('')
            del self.__workdays[0]
            return
        #implementando una lista FIFO
        try:
            workday = self.__workdays[0]
        except IndexError:
            print('--- END ---')
            return
        else:
            # self..append(header)
            # Cargar en excel el desempeño de los trabajadores en el día
            workday_info = workday.get_workers_info()
            self.activeTable.setSpan(self.__row, 0, 1, 10)
            self.append(fecha_invertida)
            for horario in horarios:
                for i in heads[horario]:
                    self.append(i)
                for worker in self.reporte.personal:
                    if personalShift[worker] != horario: continue
                    schedule = workday_info[worker]
                    # print(worker, schedule)
                    h = schedule['horario']
                    if horario == 'diurno':
                        line_to_QTable = [schedule['nombre'],
                                          h['matutino']['entrada'], h['matutino']['salida'],
                                          h['vespertino']['entrada'], h['vespertino']['salida'],
                                          schedule['tiempo trabajado'],
                                          schedule['tiempo extra'],
                                          schedule['tiempo ausente']]
                    else:
                        line_to_QTable = [schedule['nombre'],
                                          h['nocturno']['entrada'], h['nocturno']['salida'],
                                          schedule['tiempo trabajado'],
                                          schedule['tiempo extra'],
                                          schedule['tiempo ausente']]

                    self.append(line_to_QTable)
                    #self.paintHorary(self.__row - 1, h)
                self.append('')
                # salto de linea
            self.append('')
            del self.__workdays[0]

    def workRange(self):
        if not self.__workrange: return

        self.activeTable = self.table_rango
        _wm = self.__workrange
        year, month, day = _wm.from_date.year, _wm.from_date.month, _wm.from_date.day
        fecha_invertida1 = "Desde el {dia} {d} de {m} del {year}".format(dia=MyDates.dayName(year, month, day),
                                                                         d=day,
                                                                         m=MyDates.monthName(month),
                                                                         year=year)
        year, month, day = _wm.to_date.year, _wm.to_date.month, _wm.to_date.day
        fecha_invertida2 = "Hasta el {dia} {d} de {m} del {year}".format(dia=MyDates.dayName(year, month, day),
                                                                         d=day,
                                                                         m=MyDates.monthName(month),
                                                                         year=year)

        self.activeTable.setSpan(self.__row, 0, 1, 4)
        self.append(fecha_invertida1)
        self.activeTable.setSpan(self.__row, 0, 1, 4)
        self.append(fecha_invertida2)
        self.activeTable.setSpan(self.__row, 0, 1, 4)
        self.append("Horas diurnas laborables: {}".format(_wm.workableHours['diurno']))
        self.activeTable.setSpan(self.__row, 0, 1, 4)
        self.append("Horas nocturnas laborables: {}".format(_wm.workableHours['nocturno']))
        self.append(header2)
        for worker in self.reporte.personal:
            schedule = _wm.getWorkerInfo(worker)
            # print(worker, schedule)
            line_to_QTable = [worker,
                              str(schedule['tiempo trabajado']),
                              str(schedule['tiempo extra']),
                              str(schedule['tiempo ausente'])]
            self.append(line_to_QTable)
        # salto de linea
        self.append('')

    def loadRange(self, reporte):
        self.reporte = reporte
        self.totals = AnvizReader.TotalizeByRange(reporte)
        self.reset()

        # Cargar tabla de dias
        self.activeTable = self.table_logs
        self.__workdays = list(self.reporte.content)
        day_table_length = len(self.__workdays) * (2 + len(header) + len(self.reporte.personal))
        self.table_logs.setRowCount(day_table_length)
        while self.__workdays: self.workDays()

        # Cargar tabla de meses
        self.__row = 0
        self.__workrange = self.totals.byRange
        month_table_length = 5 + len(self.reporte.personal)
        self.table_rango.setRowCount(month_table_length)
        self.workRange()

    def reset(self):
        self.__row = 0
        self.table_rango.clearContents()
        self.table_logs.clearContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Table()
    reporte = AnvizReader.Reorganizar()
    reporte.organizar_por_fecha()
    reporte.calculateWorkedTime()
    reporte.filter(datetime.date(2015, 2, 5), datetime.date(2015, 5, 18))
    w.loadRange(reporte)
    to_excel = ToExcel()
    to_excel.add_sheet("Logs")
    to_excel.goto_sheet("Logs")
    from pprint import pprint
    pprint(w.tablesContent["logs"])
    to_excel.append(w.tablesContent['logs'])
    w.show()
    app.exec()
