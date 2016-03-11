import itertools
from xlwings import Workbook, Sheet, Range

class InstanceCounterMeta(type):
    """ Metaclass to make instance counter not share count with descendants
    """
    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)
        self._ids = itertools.count(1)
        self.c = 1

class b(object, metaclass=InstanceCounterMeta):
    """ Mixin to add automatic ID generation
    """
    def __init__(self):
        self.id = next(self.__class__._ids)
        self.c = self.__class__.c

def instance_inheritance_test():
    a = InstanceCounterMeta('', (), {})
    x = b()
    z = b()
    v = b()
    print(z.id)
    print(a.c)
    a.c = 2
    s = InstanceCounterMeta('', (), {})
    print(s.c)

def prueba_xlwings():
    wb = Workbook()
    print(wb.name)
    wb.name = 'hola'
    print(wb.name)
    Sheet.add('hola')
    Sheet('hola').activate()
    Range('A1').value = 1
    wb.save(r'C:\Temp')

if __name__ == "__main__":
    wb = Workbook('Libro3')
    wb.active_sheet.autofit()