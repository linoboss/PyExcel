__author__ = 'Lino Bossio'

import sys
import datetime as dt
from assets.performance import Workday, WorkersPerformance
from assets.sql import SQL, Setup, AnvizRegisters
from assets.horarios import HorarioDiurno, HorarioNocturno
from assets.diasnolaborables import DiasNoLaborables
from assets.dates_tricks import MyDates as md
from PyQt4 import QtSql
from PyQt4 import QtGui
from PyQt4 import QtCore


schedules = ['Vespertino', 'Matutino', 'nocturno']
work_time_reference = dt.timedelta(hours=8)


schedules_regular_workdays = {'diurno': ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes'),
                              'nocturno': ('Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado')}


class AnvizReader:
    def __init__(self):
        """
        Reorganiza la información en las distintas tablas de la base de datos y
        la almacena en la tabla WorDays que funciona como una tabla temporal para acelerar el accesso a los datos y
        mantener cierta referencia de configuración vigente al momento de la captura del captahuellas

        As WorkDays table contains all the relevant information to the personel logs,
        it will be the main table of the AnvizReader class, so, unless explicitly, all Table actions will be
        referred to the WorkDays table

        """
        self.anvRgs = AnvizRegisters()  # sets the connection to the database

        self.schedules_details = self.anvRgs.getShcedulesDetails()
        self.schedules_map = self.anvRgs.schedules_map()
        self.workers_by_id = self.anvRgs.getWorkers("byId")
        self.workers_shift = self.anvRgs.getWorkers("shifts by Id")

        self.exeptions = []  # list of indexes of Checkinout logs that failed the validation

    @property
    def first_date(self):
        return self.anvRgs.min_date_of("WorkDays")

    @property
    def last_date(self):
        return self.anvRgs.max_date_of("WorkDays")

    @property
    def workers_names(self):
        return self.anvRgs.getWorkers("names")

    @property
    def workers_shifts(self):
        return self.anvRgs.getWorkers('shifts')

    def updateTable(self):
        from_date = self.anvRgs.max_date_of("WorkDays")
        search_operator = '>'

        if from_date is None:
            from_date = self.anvRgs.min_date_of("Checkinout")
            search_operator = '>='

        to_date = self.anvRgs.max_date_of("Checkinout")
        """
        Iterate over dates
        """
        dates_range = md.dates_range(from_date.date(), to_date.date())

        self.anvRgs.query.exec("SELECT Logid, Userid, CheckTime "
                               "FROM Checkinout "
                               "WHERE CheckTime {operator} #{from_date}# AND CheckTime <= #{to_date}# "
                               "ORDER BY CheckTime ASC".format(from_date=from_date,
                                                               to_date=to_date,
                                                               operator=search_operator))

        LOGID, USERID, CHECKTIME = 0, 1, 2

        if not self.anvRgs.next():
            print("Up to date")
            print(self.anvRgs.query.lastError().text())
            return

        CheckDate = self.anvRgs.value(CHECKTIME).toPyDateTime().date()
        d1 = md.ahora()

        workdays = []

        for d in dates_range:
            # WorkDay day template
            workday = self.workdayTemplate(d)
            while CheckDate == d:
                logid = self.anvRgs.value(LOGID)
                userid = self.anvRgs.value(USERID)
                checktime = self.anvRgs.value(CHECKTIME)
                if userid in self.workers_by_id.keys():
                    time_pos = self.__map_to_schedules(userid, checktime)
                    workday[userid][0] = QtCore.QDate(CheckDate)
                    workday[userid][1] = str(userid)

                    if time_pos is not None:
                        workday[userid][2 + time_pos] = checktime
                    else:
                        self.exeptions.append(logid)

                # user defines the schedule, while the checktime defines the shift
                # go to the next register
                if not self.anvRgs.next():
                    break
                CheckDate = self.anvRgs.value(CHECKTIME).toPyDateTime().date()

            workdays.append(workday)
        """
        Una vez analizados todos los registros, estos seran almacenados en la tabla
        """
        for workday in workdays:
            for w, register in workday.items():
                self.anvRgs.insertInto("WorkDays", *register)

        d2 = md.ahora()
        print(d2 - d1)

    def __map_to_schedules(self, userid, checktime):
        """
        This is a helper function to complement the workday template dictionary.
        It maps the checktime to the correct schedule by comparing it to the
        shift margins.

        :param userid:
        :param checktime:
        :return:
        """
        coords = 0
        # determine CheckTime Shift
        schedule = self.workers_shift[userid]
        log = checktime.toPyDateTime().time()
        i = 0
        for id_, details in self.schedules_details[schedule].items():

            [in_1, in_2, out_1, out_2] = map(lambda h: dt.datetime.strptime(h, "%H:%M").time(),
                                             [details[2], details[3], details[4], details[5]])
            if in_1 <= log <= in_2:
                i += 1
                break
            coords += 1
            if out_1 <= log <= out_2:
                break
            coords += 1
            i += 1
        if coords != 0 and coords == i * 2:
            coords = None
        return coords

    def workdayTemplate(self, day):
        """
        Creates a template of a day in the WorkDays table
        which includes all the workers and their logs that day
        :return: a dict with the structure of a work day
        """
        INTIME_1, OUTTIME_1, INTIME_2, OUTTIME_2, INTIME_3, OUTTIME_3, SHIFT = [None for n in range(7)]

        day = QtCore.QDate(day)
        wd_temp = {}
        for w in self.workers_by_id:
            wd_temp[w] = [day, str(w), INTIME_1, OUTTIME_1, INTIME_2, OUTTIME_2, INTIME_3, OUTTIME_3, SHIFT]

        return wd_temp


# *** Tests ***


def update():
    reader = AnvizReader()
    reader.updateTable()
    sys.exit()


def tests():
    reader = AnvizReader()
    pprint(reader.workers_shift)
    pprint(reader.schedules_map)
    sys.exit()


def run():
    reader = AnvizReader()
    pprint(reader.workers_names)
    print(reader.first_date, reader.last_date)
    sys.exit()


def maptest():
    reader = AnvizReader()
    print(reader.__map_to_schedules('8', QtCore.QDateTime(2014,9,5,14,0,0)))
    sys.exit()

if __name__ == "__main__":    # run()
    from pprint import pprint
    app = QtGui.QApplication(sys.argv)

    update()
    sys.exit(app.exec())

