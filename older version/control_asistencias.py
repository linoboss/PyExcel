__author__ = 'Lino Bossio'

import os
import calendar
import datetime
from tkinter.filedialog import askopenfilename
from xlwings import Workbook


class Reorganizar:
    def __init__(self):
        file_direccion = askopenfilename(initialdir=os.getcwd(),
                                         filetypes=[('txt', '.txt')])
        file_name = file_direccion.split('/')[-1].split('.')[0]
        self.datos_archivo = {}
        self.datos_archivo['nombre'] = file_name
        self.datos_archivo['direccion'] = file_direccion
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

        print('nueva_matriz:', nueva_matriz)
        self.matriz = nueva_matriz


    def __str__(self):
        texto = ''
        for line in self.matriz:
            line = line[:8]
            line = '\t'.join(line)
            texto += line + '\n'
        return texto

    def organizar_por_persona(self):

        personal = {}
        for persona in personal:
            personal[persona] = []
            for line in self.matriz:
                if persona in line:
                    personal[persona].append(line[1:])
        print(personal)

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

        personal = list(set(self.column(0)[1:]))
        tiempo_personal = {}
        #Inicializa las horas trabajadas de los trabajadores
        for trabajador in personal:
            tiempo_personal[trabajador] = 0

        for fecha in self.fechas:
            #arreglo en elcabezado para q quede: <<Fecha: Sabado, 2015-01-17>>
            y, m, d = fecha.split('-')
            dia = calendar.weekday(int(y), int(m), int(d))
            fecha_invertida = fecha.split('-')[::-1]
            fecha_invertida[1] = self.MESES[int(fecha_invertida[1])] + ' de ' #inserta el nombre del mes en la cadena
            fecha_invertida = ' '.join(fecha_invertida)
            texto += 'Fecha: ' + self.DIAS_SEMANA[dia] + ', ' + fecha_invertida + '\n'
            #Encabezado
            texto += '\t' + 'Matutino' + '\t' + '\t' + 'Vespertino' + '\t' + '\t' + 'nocturno' + '\t' + '\t' + 'Ausente' + '\t' + 'Extra' + '\t' + 'Horas laboradas' + '\n'
            texto += 'Nombre' + '\t' + 'Entrada' + '\t' + 'Salida' + '\t' + 'Entrada' + '\t' + 'Salida' + '\t' + 'Entrada' + '\t' + 'Salida' + '\t' + '(Horas)' + '\t' + '(Horas)' + '\n'
            #agrego el cuerpo del dia

            for trabajador in self.personal:
                nueva_linea = [trabajador, '', '', '', '', '', '']
                tipo_jornada = 'Diurno'
                jornadas = {'Vespertino': [trabajador, 'Vespertino', '', ''],
                            'Matutino': [trabajador, 'Matutino', '', ''],
                            'nocturno': [trabajador, 'nocturno', '', '']}
                for linea in matriz_por_fecha[fecha]:
                    if trabajador in linea:
                        if 'Vespertino' in linea:
                            tipo_jornada = 'Diurno'
                            jornadas['Vespertino'] = linea[:5]
                        elif 'Matutino' in linea:
                            tipo_jornada = 'Diurno'
                            jornadas['Matutino'] = linea[:5]
                        elif 'nocturno':
                            tipo_jornada = 'nocturno'
                            jornadas['nocturno'] = linea[:5]
                        del linea
                if tipo_jornada == 'Diurno':
                    entrada_matutina = self.arreglar_hora(jornadas['Matutino'][2])
                    salida_matutina = self.arreglar_hora(jornadas['Matutino'][3])
                    entrada_vespertina = self.arreglar_hora(jornadas['Vespertino'][2])
                    salida_vespertina = self.arreglar_hora(jornadas['Vespertino'][3])
                    horas_trabajadas = self.sumar_horas(self.horas_trabajadas(entrada_matutina, salida_matutina, 'Matutino'),
                                                        self.horas_trabajadas(entrada_vespertina, salida_vespertina, 'Vespertino'))
                    tiempo_ausente = self.calculo_ausente(horas_trabajadas)
                    tiempo_extra = self.calculo_extra(horas_trabajadas)

                    nueva_linea = [trabajador,
                                   self.hora_no_militar(entrada_matutina), self.hora_no_militar(salida_matutina),
                                   self.hora_no_militar(entrada_vespertina), self.hora_no_militar(salida_vespertina),
                                   '', '',
                                   tiempo_ausente, tiempo_extra, self.correccioncita(horas_trabajadas)]
                elif tipo_jornada == 'nocturno':
                    entrada_nocturna = self.arreglar_hora(jornadas['nocturno'][2])
                    salida_nocturna = self.arreglar_hora(jornadas['nocturno'][3])
                    horas_trabajadas = self.horas_trabajadas(entrada_nocturna, salida_nocturna, 'nocturno')
                    tiempo_ausente = self.calculo_ausente(horas_trabajadas)
                    tiempo_extra = self.calculo_extra(horas_trabajadas)
                    nueva_linea = [trabajador,
                                   '', '',
                                   '', '',
                                   self.hora_no_militar(entrada_nocturna), self.hora_no_militar(salida_nocturna),
                                   tiempo_ausente, tiempo_extra, self.correccioncita(horas_trabajadas)]
                else:
                    #planteo el caso solo para evitar el duck typing
                    horas_trabajadas = '00:00:00'

                tiempo_personal[trabajador] += self.transformar_a_segundos(horas_trabajadas)

                line = '\t'.join(nueva_linea)
                texto += line + '\n'
            texto += '\n'
        texto += '\n'

        texto += '\n'
        texto += 'Horas trabajadas por trabajador:\n'
        for trabajador, tiempo in tiempo_personal.items():
            texto += '\t' + trabajador + ': ' + '\t' + str(int(round(tiempo/3600, 0))) + ' horas\n'
        print()
        print('matriz por fecha:', texto)
        archivo = self.datos_archivo['direccion']
        archivo = archivo.split('.')[0] + '.xls'
        print('direccion a guardar el archivo:', archivo)
        f = open(archivo, 'w')
        f.write(texto)

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


if __name__ == '__main__':
    reporte = Reorganizar()

    reporte.organizar_por_fecha()
    #print(matriz)


