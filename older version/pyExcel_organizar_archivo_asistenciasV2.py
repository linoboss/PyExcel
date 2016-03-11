__author__ = 'Lino Bossio'

import os
import calendar
import datetime
from tkinter.filedialog import askopenfilename
from xlwings import Workbook, Sheet, Range, Chart
import itertools
from copy import deepcopy

schedules = ['Vespertino', 'Matutino', 'nocturno']
work_time_reference = datetime.timedelta(hours=8)
DIAS_SEMANA = ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo')
MESES = ('', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
         'Diciembre')

class ToExcel():
    def __init__(self):
        self._wb = Workbook()
        self._i = 1

    def append(self, item, column='A'):
        if type(item) == list:
            if item[0] == list:
                index_increment = len(item)
            else:
                index_increment = 1
        else:
            index_increment = 1
        Range(column + str(self._i)).value = item
        self._i += index_increment

    def add_sheet(self, name):
        Sheet.add(name)

    def skip_line(self):
        self._i += 1

    def goto_line(self, line):
        self._i = line

    def goto_sheet(self, name):
        Sheet(name).activate()


class InstanceMeta(type):
    """ Metaclass to make instance counter not share count with descendants
    """
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._ids = itertools.count(1)


class Horary:
    def __init__(self):
        self.content = {'matutino': {'entrada': datetime.timedelta(hours=0), 'salida': datetime.timedelta(hours=0)},
                        'vespertino': {'entrada': datetime.timedelta(hours=0), 'salida': datetime.timedelta(hours=0)},
                        'nocturno': {'entrada': datetime.timedelta(hours=0), 'salida': datetime.timedelta(hours=0)}}

    def load(self, time_segment, entry_time, exit_time):
        self.content[time_segment]['entrada'] = entry_time
        self.content[time_segment]['salida'] = exit_time

    def get_formated_content(self):
        c = deepcopy(self.content)
        for k, v in self.content.items():
            for g, j in v.items():
                c[k][g] = str(j)
        return c


class Workday(object, metaclass=InstanceMeta):
    """
    Empaqueta el trabajo realizado por los trabajadores en un dia de trabajo
    Metodos asocioados:
        -> Calcular el tiempo de trabajo del personal
        -> Organizar las jornadas de trabajo
        -> Asociar el dia a una fecha en una variable de tipo ºdatetimeº

    La info será organizada por trabajador, dentro deldiccionario 'workwers' donde las keys son el nombre
    de cada trabajador.
    """
    def __init__(self, workday_date, workers):
        """
        La  clase se inicializa recibiendo la fecha del dia de trabajo y los trabajjadores asociados a ese día
        """
        assert type(workday_date) is str, "Agregar la fecha como str"
        self.day_schedule = {}
        self.workers = self.workers_preconfig(workers)
        self.date = self.str_date_to_datetime(workday_date)

    @staticmethod
    def workers_preconfig(workers):
        return {w: {'nombre': w, 'horario': Horary(),
                    'tiempo trabajado': None, 'tiempo extra': None,
                    'tiempo ausente': None} for w in workers}

    def load_horary(self, worker, time_segment, entry_time, exit_time):
        """
        Asigna al trabajador "worker" las horas de entrada y salida del segmento laborado, sea "Vespertino, Maturino, etx"
        Automáticamente transforma las horas laboradas a timedelta
        """
        assert self.workers[worker] is not None, 'el trabajador "' + worker + '" no existe o está mal escrito'\
            'los trabajadores válidos son:\n' + str(self.workers.keys())
        time_segment = time_segment.lower()
        entry_time_dt = self.str_hour_to_timedelta(entry_time)
        exit_time_dt = self.str_hour_to_timedelta(exit_time)

        self.workers[worker]['horario'].load(time_segment, entry_time_dt, exit_time_dt)

    def get_info_of(self):
        pass

    def calculate_worked_time(self):
        for w, w_info in self.workers.items():
            h = w_info['horario'].content
            """

            """
            cero_time = datetime.timedelta(hours=0)
            worked_time = cero_time
            for k, v in h.items():
                v_out = v['salida']
                v_in = v['entrada']
                if v_out != cero_time and v_in != cero_time:
                    if k == 'nocturno':
                        worked_time += datetime.timedelta(hours=24) + (v_out - v_in)
                    else:
                        worked_time += v_out - v_in

            #si no hay tiempo extra, el resultado será cero. Es decir, no habrán resultados negativos
            if worked_time > work_time_reference: extra_time = worked_time - work_time_reference
            else: extra_time = datetime.timedelta(hours=0)
            #si no hay tiempo ausente, el resultado será cero. Igual que para el tiempo extra
            if worked_time < work_time_reference: absent_time = work_time_reference - worked_time
            else: absent_time = datetime.timedelta(hours=0)
            self.workers[w]['tiempo trabajado'] = worked_time
            self.workers[w]['tiempo extra'] = extra_time
            self.workers[w]['tiempo ausente'] = absent_time

    def get_worker_info(self, w):
        w_i = deepcopy(self.workers)
        w_i[w]['horario'] = w_i[w]['horario'].get_formated_content()
        w_i[w]['tiempo extra'] = str(w_i[w]['tiempo extra'])
        w_i[w]['tiempo ausente'] = str(w_i[w]['tiempo ausente'])
        w_i[w]['tiempo trabajado'] = str(w_i[w]['tiempo trabajado'])
        return w_i[w]

    def get_workday_date(self):
        return str(self.date)

    def get_workers_info(self):
        w_i = deepcopy(self.workers)
        for w, inf in w_i.items():
            w_i[w]['horario'] = inf['horario'].get_formated_content()
            w_i[w]['tiempo extra'] = str(inf['tiempo extra'])
            w_i[w]['tiempo ausente'] = str(inf['tiempo ausente'])
            w_i[w]['tiempo trabajado'] = str(inf['tiempo trabajado'])
        return w_i

    def get_workers_raw(self):
        return self.workers

    def get_workers_names(self):
        return self.workers.keys()

    @staticmethod
    def str_hour_to_timedelta(hour):
        try:
            tup = tuple(map(int, hour.split(':')))
            return datetime.timedelta(hours=tup[0], minutes=tup[1], seconds=tup[2])
        except Exception as e:
            #print('ERROR: in str_hour_to_timedelta ', e)
            return datetime.timedelta(hours=0)

    @staticmethod
    def str_date_to_datetime(date):
        tup = tuple(map(int, date.split('-')))
        return datetime.datetime(year=tup[0], month=tup[1], day=tup[2])

    def __str__(self):
        text = ''
        for k, v in self.workers.items():
            text += str(k) + str(v)

        return text


class WorkerPerformance:
    """
    Permitirá llevar el desempeño de cada trabajador con mayor facilidad
    """
    def __init__(self, workers):
        self.work_resume = {}

        for w in workers:
            self.work_resume[w] = {'tiempo trabajado': datetime.timedelta(hours=0),
                                    'tiempo extra': datetime.timedelta(hours=0),
                                    'tiempo ausente': datetime.timedelta(hours=0)}

    def add(self, worker, tiempo_trabajado, tiempo_extra, tiempo_ausente):
        self.work_resume[worker]['tiempo trabajado'] += tiempo_trabajado
        self.work_resume[worker]['tiempo extra'] += tiempo_extra
        self.work_resume[worker]['tiempo ausente'] += tiempo_ausente

    def __str__(self):
        r = {}
        for w, t in self.work_resume.items():
            r[w] = {}
            for i, j in t.items():
                r[w][i] = str(j)
        return str(r)

    def get_info(self):
        r = {}
        for w, t in self.work_resume.items():
            r[w] = {}
            for i, j in t.items():
                r[w][i] = str(j)
        return r


class Reorganizar:
    def __init__(self):
        file_direccion = askopenfilename(initialdir=os.getcwd(),
                                         filetypes=[('txt', '.txt')])
        file_name = file_direccion.split('/')[-1].split('.')[0]
        self.datos_archivo = {'nombre': file_name, 'direccion': file_direccion}
        file = open(file_direccion)
        self.matriz = []
        for line in file:
            line = line.replace('\n', '')
            new_line = line.split('\t')
            if '\n' in new_line:
                new_line.remove('\n')
            self.matriz.append(new_line)
        self.matriz[0][0] = 'Nombre'
        self.matriz[0][1] = 'Fecha'
        del(self.matriz[1])
        self.fechas = list(set(self.column(1)[1:]))
        self.fechas.sort()
        self.personal = list(set(self.column(0)[1:]))
        self.corregir_jornadas()
        self.DIAS_SEMANA = ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo')
        self.MESES =('', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')

        self.days_of_work = {} # contendrá los días de trabajo del archivo empaquetados en la clase Workday

    def corregir_jornadas(self):
        """
        Para la jornada diaria de cada trabajador hay un horario matutino y uno vespertino que debe cumplirse,
        pero por negligencia los trbajadores no respetan eso. La correccion se hará así:
        Se iterará por fechas dentro de la matriz y por cada una, se le aplicará la correccion de horario a cada trabajador.
        Se irá eliminando las fechas corregidas para descatarlas y acelerar el proceso.
        """
        #inicializa las variables a utilizar
        matriz = self.matriz.copy() # si no se utiliza una copia se modifica la Lista original
        matriz_por_fecha = {}
        for fecha in self.fechas:
            matriz_por_fecha[fecha] = []  # inicializa la matriz por fecha
            for line in matriz:
                if fecha in line:
                    matriz_por_fecha[fecha].append(line)  #agrega la matriz correspondiente a la fecha
                    del (line)  # elimina la linea ya revisada
        nueva_matriz = []
        for fecha, sub_matriz in matriz_por_fecha.items():
            for trabajador in self.personal:
                tipo_jornada = 'Diurna'
                jornadas = {'Vespertino': [trabajador, fecha, 'Vespertino', '', ''], 'Matutino': [trabajador, fecha, 'Matutino', '', ''], 'nocturno': [trabajador, fecha, 'nocturno', '', '']}
                for linea in sub_matriz:
                    tipo_jornada = 'Diurna'
                    if trabajador in linea:
                        if 'Vespertino' in linea:
                            jornadas['Vespertino'] = linea[:5]
                        elif 'Matutino' in linea:
                            jornadas['Matutino'] = linea[:5]
                        elif 'nocturno':
                            tipo_jornada = 'nocturno'
                            jornadas['nocturno'] = linea[:5]
                        del linea
                if tipo_jornada == 'Diurna':
                    nueva_matriz.append(jornadas['Matutino'])
                    nueva_matriz.append(jornadas['Vespertino'])
                elif tipo_jornada == 'nocturno':
                    nueva_matriz.append(jornadas['nocturno'])
        self.matriz = nueva_matriz

    def __str__(self):
        texto = ''
        for line in self.matriz:
            line = line[:8]
            line = '\t'.join(line)
            texto += line + '\n'
        return texto

    def organizar_por_fecha(self):
        #ordena la las self.fechas por lista para luego generar el documento por fecha
        texto = ''

        matriz = self.matriz.copy()
        del(matriz[0]) #elimina el factor fecha
        matriz_por_fecha = {}
        #organiza la matriz que generara el documento de salida por fecha
        for fecha in self.fechas:
            matriz_por_fecha[fecha] = [] #inicializa la matriz por fecha
            for line in matriz:
                if fecha in line:
                    del(line[1]) #elimina la fecha de la lista
                    matriz_por_fecha[fecha].append(line) #agrega la matriz correspondiente a la fecha
        #self.fechas = ['2015-03-17', '2015-03-16', '2015-03-14']
        for fecha in self.fechas:
            #arreglo en elcabezado para q quede: <<Fecha: Sabado, 2015-01-17>>
            self.days_of_work[fecha] = Workday(fecha, self.personal)
            for trabajador in self.personal:
                for linea in matriz_por_fecha[fecha]:
                    self.days_of_work[fecha].load_horary(linea[0], linea[1], linea[2][11:], linea[3][11:])
                    del linea
            self.days_of_work[fecha].calculate_worked_time()

        return self.days_of_work

    def row(self, n):
        row = self.matriz[n]
        #print(row)
        return row

    def column(self, n):
        column = []
        for line in self.matriz:
            column.append(line[n])
        return column

    def correccioncita(self, hora):
        try:
            tup = tuple(map(int, hora.split(':')))
        except:
            hora = '0:00:00'
        return hora

    @staticmethod
    def arreglar_hora(hora):
        try:
            hora = hora.split(' ')[1]
        except IndexError:
            hora = '--:--:--'
        return hora

    @staticmethod
    def hora_no_militar(hora):
        referencia = datetime.timedelta(hours=13)
        try:
            tup = tuple(map(int, hora.split(':')))
            t = datetime.timedelta(hours=tup[0], minutes=tup[1], seconds=tup[2])
        except:
            return ''
        if t >= referencia:
            return str(t-datetime.timedelta(hours=12)) + ' pm'
        else:
            return str(t) + ' am'

    @staticmethod
    def transformar_a_segundos(hora):
        try:
            tup = tuple(map(int, hora.split(':')))
            t = datetime.timedelta(hours=tup[0], minutes=tup[1], seconds=tup[2])
        except:
            return 0
        return t.total_seconds()


    @staticmethod
    def sumar_horas(hora1, hora2):

        try:
            tup = tuple(map(int, hora1.split(':')))
            t1 = datetime.timedelta(hours=tup[0], minutes=tup[1], seconds=tup[2])
            tup = tuple(map(int, hora2.split(':')))
            t2 = datetime.timedelta(hours=tup[0], minutes=tup[1], seconds=tup[2])
        except:
            return ''
        return str(t1 + t2)

    @staticmethod
    def horas_trabajadas(entrada, salida, horario):
        try:
            tup = tuple(map(int, entrada.split(':')))
            t1 = datetime.timedelta(hours=tup[0], minutes=tup[1], seconds=tup[2])
            tup = tuple(map(int, salida.split(':')))
            t2 = datetime.timedelta(hours=tup[0], minutes=tup[1], seconds=tup[2])
        except:
            return ''
        else:
            if horario == 'Matutino' or horario == 'Vespertino':
                return str(t2 - t1)
            elif horario == 'nocturno':
                return str((t2 - t1) + datetime.timedelta(hours=24))

    @staticmethod
    def calculo_extra(horas_trabajadas):
        try:
            tup = tuple(map(int, horas_trabajadas.split(':')))
            t_trabajado = datetime.timedelta(hours=tup[0], minutes=tup[1], seconds=tup[2])

        except:

            return ''
        else:
            referencia_cero = datetime.timedelta()
            resultado = t_trabajado - datetime.timedelta(hours=8)
            if resultado >= referencia_cero:
                return str(resultado)
            else:
                return ''

    @staticmethod
    def calculo_ausente(horas_trabajadas):
        try:
            tup = tuple(map(int, horas_trabajadas.split(':')))
            t_trabajado = datetime.timedelta(hours=tup[0], minutes=tup[1], seconds=tup[2])
        except:
            return ''
        else:
            referencia_cero = datetime.timedelta()
            resultado = datetime.timedelta(hours=8) - t_trabajado
            if resultado >= referencia_cero:
                return str(resultado)
            else:
                return ''




def prueba_workday():
    reporte = Reorganizar()

    wd1 = Workday(reporte.matriz[-1][1], reporte.personal)
    wd1.load_horary(reporte.personal[0], 'Vespertino', '02:19:18', '05:19:18')
    wd1.load_horary(reporte.personal[0], 'Matutino', '08:19:18', '012:19:18')
    wd1.calculate_worked_time()

def generar_archivo():
    reporte = Reorganizar()
    i = 1
    header = [['Nombre', '', '', 'Horario', '', '', '', 'Horas laboradas', 'Tiempo extra', 'Tiempo ausente'],
              ['', 'Matutino', '', 'Vespertino', '', 'Nocturno', '', '', '', ''],
              ['', 'entrada', 'salida', 'entrada', 'salida', 'entrada', 'salida', '', '', '']]
    # reporte.organizar_por_fecha()
    #raise SystemExit(0)
    wb = Workbook()
    for date, workday in reporte.organizar_por_fecha().items():
        Range("A" + str(i)).value = date
        i += 1
        Range("A" + str(i)).value = header
        i += 3
        #print(date)
        for worker, schedule in workday.get_workers_info().items():
            #print(worker, schedule)
            h = schedule['horario']
            line_to_excel = [schedule['nombre'],
                             h['matutino']['entrada'], h['matutino']['salida'],
                             h['vespertino']['entrada'], h['vespertino']['salida'],
                             h['nocturno']['entrada'], h['nocturno']['salida'],
                             schedule['tiempo trabajado'],
                             schedule['tiempo extra'],
                             schedule['tiempo ausente']]

            horary = [h['matutino']['entrada'], h['matutino']['salida'],
                      h['vespertino']['entrada'], h['vespertino']['salida'],
                      h['nocturno']['entrada'], h['nocturno']['salida']]

            colors_out = []

            for j in range(len(horary)):
                if horary[j] == '0:00:00':
                    Range(['B', 'C', 'D', 'E', 'F', 'G'][j] + str(i)).color = (255, 150, 150)

                else:
                    Range(['B', 'C', 'D', 'E', 'F', 'G'][j] + str(i)).color = (150, 255, 150)

            Range("A" + str(i)).value = line_to_excel
            i += 1
        i += 1
    Sheet('Hoja1').autofit()


def generate_file_by_workday():
    i = 1


    header = [['', '', '', 'Horario', '', '', '', '', '', ''],
              ['', 'Matutino', '', 'Vespertino', '', 'Nocturno', '', '', '', ''],
              ['Nombre', 'entrada', 'salida', 'entrada', 'salida', 'entrada', 'salida', 'Horas laboradas', 'Tiempo extra', 'Tiempo ausente']]

    reporte = Reorganizar()
    report_by_dates = reporte.organizar_por_fecha()
    work_dates = report_by_dates.keys()
    workers = reporte.personal

    start_date = min(work_dates)
    start_year = int(start_date.split('-')[0])
    start_month = int(start_date.split('-')[1])
    end_date = max(work_dates)
    end_year = int(end_date.split('-')[0])
    end_month = int(end_date.split('-')[1])
    years = range(start_year, end_year+1)
    months = range(start_month, end_month+1)

    #print('Rango de fechas:')
    #print(list(years))
    #print(list(months))
    #print()
    to_excel = ToExcel()
    to_excel.add_sheet('Resumen')
    for year in years:
        for month in months:
            weeks = calendar.monthcalendar(year, month)
            month_resume = WorkerPerformance(workers)

            for week in weeks:
                week_resume = WorkerPerformance(workers)
                for day in week:
                    if day != 0:
                        """
                        Los condicionales siguientes corrigen las fechas para que
                        coincidan con las keys del diccionario report_by_dates
                        """
                        if month < 10: m = '0' + str(month)
                        else: m = str(month)
                        if day < 10: d = '0' + str(day)
                        else: d = str(day)

                        date = str(year) + '-' + m + '-' + d
                        #print(date)

                        try:
                            workday = report_by_dates[date]

                        except KeyError:
                            pass

                        else:
                            # carga el resumen del mes
                            y, m, d = date.split('-')
                            dia = calendar.weekday(int(y), int(m), int(d))
                            fecha_invertida = date.split('-')[::-1]
                            fecha_invertida[1] = MESES[int(
                                fecha_invertida[1])] + ' de '  # inserta el nombre del mes en la cadena
                            fecha_invertida = ' '.join(fecha_invertida)
                            texto = 'Fecha: ' + DIAS_SEMANA[dia] + ', ' + fecha_invertida

                            Range("A" + str(i)).value = texto
                            i += 1
                            Range("A" + str(i)).value = header
                            i += 3

                            for w in workers:
                                week_resume.add(w, workday.get_workers_raw()[w]['tiempo trabajado'],
                                                 workday.get_workers_raw()[w]['tiempo extra'],
                                                 workday.get_workers_raw()[w]['tiempo ausente'])
                                month_resume.add(w, workday.get_workers_raw()[w]['tiempo trabajado'],
                                                 workday.get_workers_raw()[w]['tiempo extra'],
                                                 workday.get_workers_raw()[w]['tiempo ausente'])

                            # Cargar en excel el desempeño de los trabajadores en el día
                            for worker, schedule in workday.get_workers_info().items():
                                #print(worker, schedule)
                                h = schedule['horario']
                                line_to_excel = [schedule['nombre'],
                                                 h['matutino']['entrada'], h['matutino']['salida'],
                                                 h['vespertino']['entrada'], h['vespertino']['salida'],
                                                 h['nocturno']['entrada'], h['nocturno']['salida'],
                                                 schedule['tiempo trabajado'],
                                                 schedule['tiempo extra'],
                                                 schedule['tiempo ausente']]

                                horary = [h['matutino']['entrada'], h['matutino']['salida'],
                                          h['vespertino']['entrada'], h['vespertino']['salida'],
                                          h['nocturno']['entrada'], h['nocturno']['salida']]

                                for j in range(len(horary)):
                                    if horary[j] == '0:00:00':
                                        Range(['B', 'C', 'D', 'E', 'F', 'G'][j] + str(i)).color = (255, 150, 150)

                                    else:
                                        Range(['B', 'C', 'D', 'E', 'F', 'G'][j] + str(i)).color = (150, 255, 150)

                                Range("A" + str(i)).value = line_to_excel
                                i += 1
                            i += 1
                #Muestreo del resumen semanal
                Range("K" + str(i)).value = 'Resumen Semanal'
                i += 1
                Range("K" + str(i)).value = ['Nombre', 'Tiempo trabajado', 'Tiempo extra', 'Tiempo ausente']
                i += 1

                for w, info in week_resume.get_info().items():
                    Range("K" + str(i)).value = [w, info['tiempo trabajado'], info['tiempo extra'],
                                                 info['tiempo ausente']]
                    i += 1
                i += 1
            #Muestreo del resumen mensual
            Range("K" + str(i)).value = 'Resumen Mensual'
            i += 1
            Range("K" + str(i)).value = ['Nombre', 'Tiempo trabajado', 'Tiempo extra', 'Tiempo ausente']
            i += 1
            for w, info in month_resume.get_info().items():
                Range("K" + str(i)).value = [w, info['tiempo trabajado'], info['tiempo extra'], info['tiempo ausente']]
                i += 1
            i += 1
    Sheet('Hoja1').autofit()

if __name__ == '__main__':
    generate_file_by_workday()

    #print()

    """
    y, m, d = fecha.split('-')
    dia = calendar.weekday(int(y), int(m), int(d))
    fecha_invertida = fecha.split('-')[::-1]
    fecha_invertida[1] = self.MESES[int(fecha_invertida[1])] + ' de '  # inserta el nombre del mes en la cadena
    fecha_invertida = ' '.join(fecha_invertida)
    texto += 'Fecha: ' + self.DIAS_SEMANA[dia] + ', ' + fecha_invertida + '\n'
    # Encabezado
    texto += '\t' + 'Matutino' + '\t' + '\t' + 'Vespertino' + '\t' + '\t' + 'nocturno' + '\t' + '\t' + 'Ausente' + '\t' + 'Extra' + '\t' + 'Horas laboradas' + '\n'
    texto += 'Nombre' + '\t' + 'Entrada' + '\t' + 'Salida' + '\t' + 'Entrada' + '\t' + 'Salida' + '\t' + 'Entrada' + '\t' + 'Salida' + '\t' + '(Horas)' + '\t' + '(Horas)' + '\n'
    #agrego el cuerpo del dia
    #print(matriz)
    """



