import calendar
import datetime
from dateutil.relativedelta import relativedelta


def emptyFunc(*args, **kwargs): pass


class YearMonthDay:
    def __init__(self, start_date, stop_date, initialize=emptyFunc,
                 yearCycle=emptyFunc, monthCycle=emptyFunc,
                 dayCycle=emptyFunc, postMonthCycle=emptyFunc,
                 postYearCycle=emptyFunc, closure=emptyFunc):
        self.start_date = start_date
        self.stop_date = stop_date
        initialize()
        date = start_date
        # inicio del ciclo
        for year in self.iterable:
            yearCycle(date)
            for month in year:
                monthCycle(date)
                for day in month:
                    dayCycle(date)
                    date += relativedelta(days=1)
                postMonthCycle(date)
            postYearCycle(date)
        closure(date)

    @property
    def iterable(self):
        """
        Crea una lista de listas que contiene todas las fechas contenidas en el lapso tiempo
        :return: [years[trimestres[months[weeks]]]]
        """
        cal = calendar.Calendar()
        years = [cal.yeardays2calendar(y) for y in range(self.start_date.year, self.stop_date.year + 1)]
        dates_in_range = []
        __year = self.start_date.year
        for year in years:
            dates_in_range.append([])
            __month = 1
            for trimestre in year:
                for month in trimestre:
                    dates_in_range[-1].append([])
                    for week in month:
                        for day in week:
                            if day[0] == 0: continue
                            date = datetime.date(__year, __month, day[0])
                            if date < self.start_date: continue
                            if date > self.stop_date: break
                            dates_in_range[-1][-1].append(date)
                    __month += 1
            __year += 1
        dates_in_range = [[j for j in i if j] for i in dates_in_range]
        return dates_in_range


class DaybyDay:
    def __init__(self, start_date, last_date, initialize=emptyFunc, daysCycle=emptyFunc, postDayCicle=emptyFunc):
        assert type(start_date) == datetime.date and type(last_date) == datetime.date, \
            "start_date and last_date most be date objects"
        initialize()
        d = start_date
        while d <= last_date:
            daysCycle(d)
            d += relativedelta(days=1)
        postDayCicle()


class WeekbyWeek:
    def __init__(self, start_date, stop_date, initialize=emptyFunc,
                 dayCycle=emptyFunc, weekCycle=emptyFunc,
                 yearCycle=emptyFunc, postWeekCycle=emptyFunc,
                 postYearCycle=emptyFunc,ending=emptyFunc):
        assert type(start_date) == datetime.date and type(stop_date) == datetime.date, \
            "start_date and stop_date most be date objects"
        self.start_date = start_date
        self.stop_date = stop_date
        initialize()
        date = start_date
        # inicio de ciclo
        for year in self.iterable:
            yearCycle(date)
            for week in year:
                weekCycle(date)
                for day in week:
                    # day es un objeto datetime.date
                    dayCycle(date)
                    date += relativedelta(days=1)
                postWeekCycle(date)
            postYearCycle(date)
        ending(date)

    @property
    def iterable(self):
        """
        Crea una lista de listas que contiene todas las fechas contenidas en el lapso tiempo
        :return: [years[trimestres[months[weeks]]]]
        """
        cal = calendar.Calendar()
        years = [cal.yeardatescalendar(y) for y in range(self.start_date.year, self.stop_date.year + 1)]
        dates_in_range = []
        lastWeek = []
        for year in years:
            dates_in_range.append([])
            for trimestre in year:
                for month in trimestre:
                    for week in month:
                        dates_in_range[-1].append([])
                        if week == lastWeek: continue
                        lastWeek = week
                        for day in week:
                            if day < self.start_date: continue
                            if day > self.stop_date: break
                            dates_in_range[-1][-1].append(week)
        dates_in_range = [[j for j in i if j] for i in dates_in_range]
        return dates_in_range

d1 = datetime.date(2014,1,22)
d2 = datetime.date(2015,12,1)
WeekbyWeek(d1,d2)
