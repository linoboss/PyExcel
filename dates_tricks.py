import datetime
import calendar
from dateutil.relativedelta import relativedelta

DIAS_SEMANA = ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo')
MESES = ('', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
         'Diciembre')

class MyDates:
    @staticmethod
    def monthFirstDate(year, month):
        return datetime.date(year, month, 1)

    @staticmethod
    def monthLastDate(year, month):
        cal = calendar.Calendar()
        to_date_last = max(list(cal.itermonthdays(year, month)))
        return datetime.date(year, month, to_date_last)

    @staticmethod
    def monthName(m):
        return MESES[m]

    @staticmethod
    def dayName(y=1, m=1, d=1):
        if isinstance(y, datetime.date):
            date = y
            return DIAS_SEMANA[calendar.weekday(date.year, date.month, date.day)]
        return DIAS_SEMANA[calendar.weekday(y, m, d)]

    @staticmethod
    def fechaActual():
        return datetime.datetime.now().date()

    @staticmethod
    def mesSiguiente(date):
        return date + relativedelta(months=1)

    @staticmethod
    def mesAnterior(date):
        return date - relativedelta(months=1)

    @staticmethod
    def getWeek(date):
        print(date)
        week = None
        weeks = calendar.monthcalendar(date.year, date.month)
        for week in weeks:
            if date.day in week:
                break
        return week

    @staticmethod
    def oneDay():
        return datetime.timedelta(days=1)

    @staticmethod
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = int(sourcedate.year + month / 12)
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

