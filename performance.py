import itertools
import datetime
from copy import deepcopy
from dates_tricks import MyDates
from sql import Setup

schedules = ['Vespertino', 'Matutino', 'nocturno']
work_time_reference = datetime.timedelta(hours=8)
jornada_personal = Setup().personalShift()

schedules_regular_workdays = {'diurno': ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes'),
                              'nocturno': ('Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado')}


def isworkable(date, jornada):
    print(date)
    dia = MyDates.dayName(date)

    if dia in schedules_regular_workdays[jornada]:
        return True
    else:
        return False


class InstanceMeta(type):
    """ Metaclass to make instance counter not share count with descendants
    """
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._ids = itertools.count(1)


class Horary:
    def __init__(self):
        self.content = {'matutino': {'entrada': None, 'salida': None},
                        'vespertino': {'entrada': None, 'salida': None},
                        'nocturno': {'entrada': None, 'salida': None}}

    def load(self, time_segment, entry_time, exit_time):
        self.content[time_segment]['entrada'] = entry_time
        self.content[time_segment]['salida'] = exit_time

    def get_formated_content(self):
        c = deepcopy(self.content)
        for k, v in self.content.items():
            for g, j in v.items():
                try:
                    c[k][g] = str(j.time())
                except AttributeError:
                    c[k][g] = '--'
        return c

    def __str__(self):
        text = '{'
        for k, v in self.content.items():
            text += str(k) + ': {'
            for i, j in v.items():
                text += str(i) + ': ' + str(j) + ', '
            text += '} '
        text += '} '
        return text


class Workday(object, metaclass=InstanceMeta):
    """
    Empaqueta el trabajo realizado por los trabajadores en un dia de trabajo
    Metodos asocioados:
        -> Organizar las jornadas de trabajo
        -> Asociar el dia a una fecha en una variable de tipo ºdatetimeº

    La info será organizada por trabajador, dentro deldiccionario 'workers' donde las keys son el nombre
    de cada trabajador.
    """
    def __init__(self, workday_date, workers, workableHours={'diurno': 8, 'nocturno': 8}):
        """
        Crea la base para almacenar las horas de entrada y salida de un día normal de trabajo
        :param workday_date: (str) fecha del dia de trabajo
        :param workers: (list) listaa de trabjadores del dia
        :return:
        """
        assert isinstance(workableHours, dict), "workableHours DEBE SER UN DICCIONARIO!!!!"
        #assert type(workday_date) is str, "Agregar la fecha como str"
        self.day_schedule = {}
        self.workers = {w: {'nombre': w, 'horario': Horary(),
                        'tiempo trabajado': None, 'tiempo extra': None, 'tiempo ausente': None} for w in workers}
        self.date = workday_date
        self.workableHours = {'diurno': datetime.timedelta(hours=1) * workableHours['diurno'],
                              'nocturno': datetime.timedelta(hours=1) * workableHours['nocturno']}
        self.isworkable = True

    def changeWorkableHours(self, diurno= 8, nocturno=8):
        self.workableHours = {'diurno': datetime.timedelta(hours=1) * diurno,
                              'nocturno': datetime.timedelta(hours=1) * nocturno}

    def load_horary(self, worker, time_segment, entry_time, exit_time):
        """
        Asigna al trabajador "worker" las horas de entrada y salida del segmento laborado, sea "Vespertino, Maturino, etx"
        Automáticamente transforma las horas laboradas a timedelta
        """
        assert self.workers[worker] is not None, 'el trabajador "' + worker + '" no existe o está mal escrito'\
            'los trabajadores válidos son:\n' + str(self.workers.keys())
        time_segment = time_segment.lower()
        entry_time_dt = entry_time
        exit_time_dt = exit_time

        self.workers[worker]['horario'].load(time_segment, entry_time_dt, exit_time_dt)

    def get_info_of(self):
        pass

    def get_worker_info(self, w):
        w_i = deepcopy(self.workers)
        w_i[w]['horario'] = w_i[w]['horario'].get_formated_content()
        return w_i[w]

    def get_workday_date(self):
        return str(self.date)

    def get_workers_info(self):
        w_i = deepcopy(self.workers)

        for w, inf in w_i.items():
            w_i[w]['horario'] = inf['horario'].get_formated_content()
            w_i[w]['tiempo trabajado'] = self.hours_repr(self.workers[w]['tiempo trabajado'])
            w_i[w]['tiempo extra'] = self.hours_repr(self.workers[w]['tiempo extra'])
            w_i[w]['tiempo ausente'] = self.hours_repr(self.workers[w]['tiempo ausente'])
        return w_i

    def get_workers_raw(self):
        return self.workers

    def get_workers_names(self):
        return self.workers.keys()

    def __str__(self):
        text = ''
        for k, v in self.workers.items():
            text += str(k) + str(v) + '\n'
        return text

    def addPerformance(self, worker, tiempo_trabajado, tiempo_extra, tiempo_ausente):
        """
        worker: str
        tiempo_trabajado, tiempo_extra, tiempo_ausente: timedelta         
        """
        self.workers[worker]['tiempo trabajado'] = tiempo_trabajado
        self.workers[worker]['tiempo extra'] = tiempo_extra
        self.workers[worker]['tiempo ausente'] = tiempo_ausente

    def filterWorkers(self, workers):
        self.workers = {w: self.workers[w] for w in workers}
        return self



    @staticmethod
    def hours_repr(td):
        def correct(x):
            """
            tengo 0:0
            quiero 00:00
            """
            if x=='None' or x==None:
                return '00'
            elif len(str(x)) < 2:
                return "0{}".format(x)
            else:
                return x
        if td is None:
            return None

        if type(td) == datetime.datetime:
            d = td.day
            h = td.hour
            m = td.minute
            h = 24*d + h
             
        elif type(td) == datetime.timedelta:
            d = td.days
            h, r = divmod(td.seconds, 3600)
            m, s = divmod(r, 60)
            h = d*24 + h
        else:
            h, m = None, None
        h = correct(h)
        m = correct(m)
        
        return "{} : {}".format(h, m)

    def __add__(self, other):
        if isinstance(other, Workday):
            #suma 2 workdays
            wp = WorkersPerformance(self.workers.keys())
            wp.add(self)
            wp.add(other)
            return wp
        elif isinstance(other, WorkersPerformance):
            return other.add(self)


class WorkersPerformance:
    def __init__(self, workers):
        self.work_resume = {}
        self.workdays = []
        self.workers = workers
        #initialization
        self.workable_time = {'diurno': datetime.timedelta(hours=0),
                      'nocturno': datetime.timedelta(hours=0)}

        for w in self.workers:
            self.work_resume[w] = {'tiempo trabajado': datetime.timedelta(hours=0),
                                   'tiempo extra': datetime.timedelta(hours=0),
                                   'tiempo ausente': datetime.timedelta(hours=0)}

    def add(self, workday):
        """
        worker: str
        tiempo_trabajado, tiempo_extra, tiempo_ausente: timedelta
        """
        date_before = self.dateBefore
        if date_before is not None: assert workday.date > date_before
        self.workdays.append(workday)
        for worker in self.work_resume.keys():
            for times in self.work_resume[worker]:
                self.work_resume[worker][times] += workday.workers[worker][times]
        for k, v in self.workable_time.items():
            self.workable_time[k] += workday.workableHours[k]
        return self

    def __add__(self, other):
        if isinstance(other, WorkersPerformance):
            for workday in other.workdays:
                self.add(workday)
        elif isinstance(other, Workday):
            self.add(other)
        return self

    def addWorkableDays(self, workable_days):
        """
        workable_days: dict.keys = ('diurno', 'nocturno')
        """
        self.workable_time['diurno'] = workable_days['diurno'] * datetime.timedelta(hours=8)
        self.workable_time['nocturno'] = workable_days['nocturno'] * datetime.timedelta(hours=11)

    def __str__(self):
        r = {}
        for w, t in self.work_resume.items():
            r[w] = {}
            for i, j in t.items():
                r[w][i] = self.hours_repr(j)
        return str(r)

    def get_info(self):
        r = {}
        for w, t in self.work_resume.items():
            r[w] = {}
            for i, j in t.items():
                r[w][i] = self.hours_repr(j)
        return r

    def getWorkerInfo(self, w):
        r = {}
        for i, j in self.work_resume[w].items():
            r[i] = self.hours_repr(j)
        return r

    @property
    def from_date(self):
        try:
            return self.workdays[0].date
        except IndexError:
            return None

    @property
    def to_date(self):
        try:
            return self.workdays[-1].date
        except IndexError:
            return None

    @property
    def dateBefore(self):
        try:
            return self.workdays[-1].date
        except:
            return None

    @property
    def workableHours(self):
        #transformando el formato datetime de #days, #minutes, #seconds
        # a #hours, seconds
        diurno = self.workable_time['diurno']
        nocturno = self.workable_time['nocturno']

        return {'diurno': self.hours_repr(diurno),
                'nocturno': self.hours_repr(nocturno)}

    @staticmethod
    def hours_repr(td):
        def correct(x):
            """
            tengo 0:0
            quiero 00:00
            """
            if x=='None' or x==None:
                return '00'
            elif len(str(x)) < 2:
                return "0{}".format(x)
            else:
                return x
        if td is None:
            return None

        if type(td) == datetime.datetime:
            d = td.day
            h = td.hour
            m = td.minute
            h = 24*d + h
             
        elif type(td) == datetime.timedelta:
            d = td.days
            h, r = divmod(td.seconds, 3600)
            m, s = divmod(r, 60)
            h = d*24 + h
        else:
            h, m = None, None
        h = correct(h)
        m = correct(m)
        
        return "{} : {}".format(h, m)





