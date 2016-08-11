__author__ = 'Lino Bossio'

from assets import ciclos
from assets.performance import Workday, WorkersPerformance
from assets.sql import SQL, Setup
from assets.horarios import HorarioDiurno, HorarioNocturno
from assets.dates_tricks import MyDates
from assets.diasnolaborables import DiasNoLaborables
import datetime as dt

schedules = ['Vespertino', 'Matutino', 'nocturno']
work_time_reference = dt.timedelta(hours=8)


schedules_regular_workdays = {'diurno': ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes'),
                              'nocturno': ('Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado')}


def isworkable(date, jornada):
    dia = MyDates.dayName(date)

    if dia in schedules_regular_workdays[jornada]:
        return True
    else:
        return False


class Reorganizar:
    def __init__(self):
        database = SQL()
        database.loadChekInOutTable()

        self.jornada_personal = Setup().personalShift()
        print(self.jornada_personal)
        self.matriz = database.data_matrix
        self.personal = sorted(self.jornada_personal.keys())
        dates = database.dates
        self.dates = [d for d in dates if d > dt.date(2014, 1, 1)]
        self.start_date = self.dates[0]
        self.stop_date = self.dates[-1]
        self.exceptions = None
        self.workers_not_found = None
        self.days_of_work = {}  # contendrá los días de trabajo del archivo empaquetados en la clase Workday
        self.validateCheck()
        self.content = ()
        self.thisday = DiasNoLaborables()
        self.organizar_por_fecha()

    def validateCheck(self):
        matrix = []
        exceptions = []
        workers_not_found = []
        for row in self.matriz:
            # determiar si el check in es valido
            worker = row[0]
            check = row[1]
            in_or_out = row[2]

            # Los checks mal hechos o fuera de los parametros aceptados
            # pasan a una lista para ser verificados
            try:
                jornada = self.jornada_personal[worker]
            except KeyError:
                if worker not in workers_not_found:
                    workers_not_found.append(worker)
                continue
            if jornada == "diurno":
                if not HorarioDiurno.validateCheck(check, in_or_out):
                    exceptions.append(row)
                    continue
            if jornada == "nocturno":
                if not HorarioNocturno.validateCheck(check, in_or_out):
                    exceptions.append(row)
                    continue
            matrix.append(row)

        self.exceptions = exceptions
        self.workers_not_found = workers_not_found
        self.matriz = matrix

    def __str__(self):
        texto = ''
        for line in self.matriz:
            line = line[:8]
            line = '\t'.join(line)
            texto += line + '\n'
        return texto

    def organizar_por_fecha(self):
        """
        return: dict
        """
        # ordena las self.fechas por lista para luego generar el documento por fecha

        self.__matriz = self.matriz.copy()
        self.content = ()
        # Rango de fechas
        start_date = min(self.dates)
        stop_date = max(self.dates)
        ciclos.DaybyDay(start_date, stop_date, daysCycle=self.loadContent)

    def loadContent(self, date):
        """
        Función sobre la cual se iterará para llenar los work_days.
                Por cada día en el intervalo se generará un Workday que será almacenado en work_days
        :param date: recibe la fecha de iteración
        :return: work_days (lista)
        """
        # organiza la matriz que generara el documento de salida por fecha
        workday = Workday(date, self.personal)
        temp = []  # matriz temporal
        for line in self.__matriz:
            if date == line[1].date():
                # line [worker, checktime, in/out]
                temp.append(line)  # agrega la matriz correspondiente a la fecha

        for worker in self.personal:
            # transformar a [worker, time_segment, entry_time, exit_time]
            worker_schedule = self.jornada_personal[worker]

            if worker_schedule == "diurno":
                w = {"worker": worker, "matutino": {"entrada": None, "salida": None},
                     "vespertino": {"entrada": None, "salida": None}}
                for line in temp:
                    if worker in line:
                        # checktime, in/out -> time_segment, entry_time, exit_time
                        checktime = line[1]
                        in_out = line[2]
                        if HorarioDiurno.is_matutino(checktime, in_out):
                            if in_out == "I":
                                w["matutino"]["entrada"] = checktime
                            elif in_out == "O":
                                w["matutino"]["salida"] = checktime
                        elif HorarioDiurno.is_vespertino(checktime, in_out):
                            if in_out == "I":
                                w["vespertino"]["entrada"] = checktime
                            elif in_out == "O":
                                w["vespertino"]["salida"] = checktime

                workday.load_horary(
                        w["worker"], "matutino", w["matutino"]["entrada"], w["matutino"]["salida"])
                workday.load_horary(
                        w["worker"], "vespertino", w["vespertino"]["entrada"], w["vespertino"]["salida"])

            elif worker_schedule == "nocturno":
                w = {"worker": worker, "nocturno": {"entrada": None, "salida": None}}
                for line in temp:
                    if worker in line:
                        # checktime, in/out -> time_segment, entry_time, exit_time
                        checktime = line[1]
                        in_out = line[2]
                        if in_out == "I":
                            w["nocturno"]["entrada"] = checktime
                        elif in_out == "O":
                            w["nocturno"]["salida"] = checktime
                workday.load_horary(w["worker"], "nocturno", w["nocturno"]["entrada"], w["nocturno"]["salida"])

            else:
                print("Este tipo de horario no existe aun")
                raise TypeError
            # end for worker in self.personal
        # end for date in self.dates
        # TODO mecanismo para detectar las fechas especiales y modificar las horas laborables
        if not self.thisday.isWorkable(date):
            workday.isworkable = False
            workday.changeWorkableHours(diurno=0, nocturno=0)

        self.content += (workday,)

    def calculateWorkedTime(self):
        """
        Agrega los workday del contenido los calculos del tiempo trabajado, tiempo ausente y tiempo extra
        """

        content = list(self.content)
        content_length = len(self.content)
        assert content_length > 0, "No hay contenido que analizar."
        for i in range(content_length):
            workday = self.content[i]
            date = workday.date

            try:
                next_workday = self.content[i + 1]
            except IndexError:
                next_workday = None

            # cargar el resumen del mes
            for w in self.personal:
                w_info = workday.workers[w]
                h = w_info['horario'].content
                zero_time = dt.timedelta(hours=0)
                worked_time = zero_time

                for k, v in h.items():
                    if k == 'matutino' or k == 'vespertino':
                        v_in = v['entrada']
                        v_out = v['salida']
                    elif k == 'nocturno':
                        # worked_time += datetime.timedelta(hours=24) + (v_out - v_in)
                        v_in = v['entrada']
                        if next_workday is None:
                            v_out = None
                        else:
                            v_out = next_workday.workers[w]['horario'].content['nocturno']['salida']
                    if v_out != None and v_in != None:
                        worked_time += v_out - v_in
                    else: continue

                #Dependiendo de la jornada del trabajador, las horas laborables del dia pueden variar
                work_time_reference = workday.workableHours[self.jornada_personal[w]]

                # si no hay tiempo extra, el resultado será zero. Es decir, no habrán resultados negativos
                if worked_time > work_time_reference:
                    extra_time = worked_time - work_time_reference
                else:
                    extra_time = dt.timedelta(hours=0)
                # si no hay tiempo ausente, el resultado será zero. Igual que para el tiempo extra
                if worked_time < work_time_reference:
                    absent_time = work_time_reference - worked_time
                else:
                    absent_time = dt.timedelta(hours=0)

                workday.addPerformance(w, worked_time, extra_time, absent_time)
                print(w, worked_time, extra_time, absent_time)
            content[i] = workday

    def row(self, n):
        row = self.matriz[n]
        # print(row)
        return row

    def column(self, n):
        column = []
        for line in self.matriz:
            try:
                column.append(line[n])
            except IndexError:
                raise Exception(IndexError, str(line[n]))
        return column

    def filter(self, from_date, to_date, personal=None):
        # TODO filtrar personal
        if personal is None: personal = self.personal
        self.start_date = from_date
        self.stop_date = to_date
        filtered_content = ()
        for wd in self.content:
            d = wd.date
            if from_date > d: continue
            if to_date < d: continue
            filtered_content += (wd.filterWorkers(personal),)
        self.content = filtered_content


class Totalize:
    def __init__(self, reporte):
        self.reporte = reporte
        self.workers = reporte.personal
        self.start_date = reporte.content[0].date
        self.stop_date = reporte.content[-1].date

        #return variables initialization
        self.byDay = ()
        self.byWeek = ()
        self.byMonth = ()

        #analisys execution
        ciclos.YearMonthDay(self.start_date, self.stop_date,
                            initialize=self.initTotal,
                            postMonthCycle=self.monthsTotal,
                            dayCycle=self.daysTotal)
        ciclos.WeekbyWeek(self.start_date, self.stop_date,
                          initialize=self.initTotal,
                          dayCycle=self.daysTotal,
                          postWeekCycle=self.weekTotal)

    def preload(self):
            return WorkersPerformance(self.workers)

    def initTotal(self):
        #weekFunction variables initialization
        self.__workdays = list(self.reporte.content)
        self.__month_resume = self.preload()
        self.__week_resume = self.preload()
        self.__day_resume = self.preload()

    def monthsTotal(self, date):
        self.byMonth += (self.__month_resume,)
        self.__month_resume = self.preload()

    def daysTotal(self, date):
        """
        Creates a list which contains the weekly performance of the personnel
        """
        workday = self.__currentWorkday
        self.__month_resume += workday
        self.__week_resume += workday

    def weekTotal(self, date):
        """
        Creates a list which contains the weekly performance of the personnel
        """
        self.byWeek += (self.__week_resume,)
        self.__week_resume = self.preload()

    @property
    def __currentWorkday(self):
        w = self.__workdays[0]
        del self.__workdays[0]
        return w


class TotalizeByRange:
    def __init__(self, reporte):
        self.reporte = reporte
        self.workers = reporte.personal
        self.start_date = reporte.content[0].date
        self.stop_date = reporte.content[-1].date

        #return variables initialization
        self.byRange = ()

        #analisys execution
        ciclos.DaybyDay(self.start_date, self.stop_date,
                        initialize=self.initTotal,
                        daysCycle=self.daysTotal)

    def preload(self):
            return WorkersPerformance(self.workers)

    def initTotal(self):
        #weekFunction variables initialization
        self.__workdays = list(self.reporte.content)
        self.byRange = self.preload()

    def daysTotal(self, date):
        """
        Creates a list which contains the weekly performance of the personnel
        """
        workday = self.__currentWorkday
        workday.get_workers_info()
        self.byRange += workday

    @property
    def __currentWorkday(self):
        w = self.__workdays[0]
        del self.__workdays[0]
        return w


if __name__ == "__main__":
    reporte = Reorganizar()
    reporte.organizar_por_fecha()
    reporte.calculateWorkedTime()
    reporte.filter(dt.date(2015,1,1), dt.date(2015,5,5))
    totalize = TotalizeByRange(reporte)
    print(totalize.byRange)
