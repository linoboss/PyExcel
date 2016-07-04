from datetime import date
from dates_tricks import MyDates



class Dia:
    def __init__(self, dia=None, mes=None, status="dia regular", laborable=True):
        self.dia, self.mes = dia, mes
        self.status = status
        self.laborable = laborable
        self.id = (dia,mes)

    def toDate(self, año):
        return date(año, self.mes, self.dia)

    def __repr__(self):
        return "Objeto: {dia} de {mes}".format(dia=self.dia,
                                               mes=MyDates.monthName(self.mes))

    def __eq__(self, other):
        if isinstance(other, date):
            id1 = (other.day, other.month)
            id2 = self.id
            if id1 == id2:
                return True
        return False



class DiasNoLaborables:
    def __init__(self):
        self.diasNoLaborables = (Dia(1, 1, "Año nuevo", False),
                                 Dia(19, 4, "Declaración de Independencia", False),
                                 Dia(1, 5, "Dia del Trabajador", False),
                                 Dia(24, 6, "Batalla de Carabobo", False),
                                 Dia(5, 7, "Firma del Acta de Independencia", False),
                                 Dia(24, 7, "Natalicio de Simón Bolívar", False),
                                 Dia(12, 10, "Día de la Resistencia Indígena", False),
                                 Dia(24, 12, "Víspera de Navidad", False),
                                 Dia(25, 12, "Víspera de Navidad", False),
                                 Dia(31, 12, "Fín de Año", False))
        self.diasDescanso = {'diurno': ("sabado", "domingo"), 'nocturno': {'domingo', 'lunes'}}

    def between(self, fromDate, toDate):
        assert fromDate < toDate
        listaDias = []
        for year in range(fromDate.year, toDate.year + 1):
            for dnl in self.diasNoLaborables:
                d = dnl.toDate(year)
                if fromDate <= d <= toDate:
                    listaDias.append(d)
        return listaDias

    def significado(self, fecha):
        if fecha in self.diasNoLaborables:
            for d in self.diasNoLaborables:
                id = (fecha.day, fecha.month)
                if d.id == id:
                    return d.status
        else:
            return None

    def isWorkable(self, fecha):
        #TODO agregar isworkable por turno
        dayname = MyDates.dayName(fecha).lower()
        if dayname == 'domingo':
            return False
        for d in self.diasNoLaborables:
            if d.toDate(fecha.year) == fecha:
                return False
        return True
    #TODO agregar mecanismo para agregar nuevos dias no laborables



if __name__ == "__main__":
    from pprint import pprint
    ds = (Dia(1,2), Dia(2,3))
    print(date(2015,2,1) in ds)
