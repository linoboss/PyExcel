import sys
from assets.dates_tricks import MyDates as md
from assets.sql import AnvizRegisters
from assets.anviz_reader import AnvizReader
from PyQt4 import QtGui, QtCore


app = QtGui.QApplication(sys.argv)
anvizReader = AnvizReader()
anvRgs = anvizReader.anvRgs

# TODO delete next line when development is over
anvRgs.deleteRegistersFrom("WorkDays")

from_date = anvRgs.max_date_of("WorkDays")

if from_date is None:
    from_date = anvRgs.min_date_of("Checkinout")
else:
    anvRgs.deleteDay(from_date)

to_date = anvRgs.max_date_of("Checkinout")
"""
Iterate over dates
"""
dates_range = md.dates_range(from_date.date(), to_date.date())

anvRgs.query.exec("SELECT Logid, Userid, CheckTime "
                  "FROM Checkinout "
                  "WHERE CheckTime >= #{from_date}# AND CheckTime <= #{to_date}# "
                  "ORDER BY CheckTime ASC".format(from_date=from_date,
                                                  to_date=to_date))

LOGID, USERID, CHECKTIME = 0, 1, 2

if not anvRgs.next():
    sys.exit()

CheckDate = anvRgs.value(CHECKTIME).toPyDateTime().date()

workdays = []

for d in dates_range:
    # WorkDay day template
    workday = anvizReader.workdayTemplate(d)
    while CheckDate == d:
        logid = anvRgs.value(LOGID)
        userid = anvRgs.value(USERID)
        checktime = anvRgs.value(CHECKTIME)
        if userid in anvizReader.workers_by_id.keys():
            time_pos = anvizReader.map_to_schedules(userid, checktime)
            workday[userid][0] = QtCore.QDate(CheckDate)
            workday[userid][1] = str(userid)

            if time_pos is not None:
                workday[userid][2 + time_pos] = checktime
            else:
                anvizReader.exeptions.append(logid)


        # user defines the schedule, while the checktime defines the shift
        # go to the next register
        if not anvRgs.next():
            break
        CheckDate = anvRgs.value(CHECKTIME).toPyDateTime().date()

    workdays.append(workday)

from pprint import pprint
# con workdays ya organizado, se prrocede a reorganizar a los trabajadores cuyos horarios
# contengan la condicion de Overnight

overnight_workers = anvizReader.overnightWorkers()
overnight_work = dict((k, []) for k in overnight_workers)

out_aux = [None, None]
for workday in workdays[::-1]:
    for w in overnight_workers:
        out = [workday[w][3], workday[w][5]]
        workday[w][3], workday[w][5] = out_aux
        out_aux = out

for workday in workdays:
    for worker in workday:
        if worker in overnight_workers:
            print(workday[worker])

"""
Una vez analizados todos los registros, estos seran almacenados en la tabla
"""
"""
for workday in workdays:
    for w, register in sorted(workday.items()):
        anvRgs.insertInto("WorkDays", *register)
"""