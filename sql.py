# https://code.google.com/p/pyodbc/wiki/Cursor

import pyodbc
from pprint import pprint
from datetime import datetime, date
from pprint import pprint


class SQL:
    def __init__(self):
        # set up some constants
        MDB = 'Att2003.mdb'; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = 'pw'

        # connect to db
        self.con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
        self.cur = self.con.cursor()

    def loadChekInOutTable(self):
        SQLcommand = 'SELECT * FROM Userinfo'  # your query goes here
        userinfo_table = self.cur.execute(SQLcommand)
        rows = userinfo_table.fetchall()

        personal_ids = {}
        for row in rows:
            personal_ids[str(row[0])] = row[1]

        # run a query and get the results
        SQLcommand = 'SELECT * FROM Checkinout'  # your query goes here
        checkinout_table = self.cur.execute(SQLcommand)
        rows = checkinout_table.fetchall()

        """
        Reorganizar la matriz en las siguientes columnas:
        Nombre	Hora y fecha	 ¿entrada o salida?
        de checkeo
        """
        result = []
        ids = personal_ids.keys()
        for row in rows:
            userid = row[1]
            if userid in ids:
                result.append([
                    personal_ids[userid],
                    row[2],
                    row[3]
                    ])

        columns = [column[0] for column in self.cur.description]

        SQLcommand = 'SELECT CheckTime FROM Checkinout'  # your query goes here
        checkinout_table = self.cur.execute(SQLcommand)
        dates = checkinout_table.fetchall()
        dates = [d[0] for d in dates]
        self.cur.close()
        self.con.close()
        self.personal = personal_ids.values()
        self.data_matrix = result
        self.headers = columns
        self.dates = [date(*d.timetuple()[:3]) for d in dates]
        self.dates = sorted(list(set(self.dates)))

    @property
    def personalShift(self):
        personalShift = {}
        shift = {}
        schedule = {}


        SQLcommand = 'SELECT * FROM Userinfo'  # your query goes here
        userinfo_table = self.cur.execute(SQLcommand)
        personalID = dict([(tab[0], tab[1]) for tab in userinfo_table.fetchall()])

        SQLcommand = 'SELECT * FROM UserShift'  # your query goes here
        usershift_table = self.cur.execute(SQLcommand)
        shift = dict([(tab[0], tab[1]) for tab in usershift_table.fetchall()])

        SQLcommand = 'SELECT * FROM Schedule'  # your query goes here
        schedule_table = self.cur.execute(SQLcommand)
        schedule = dict([(tab[0], tab[1]) for tab in schedule_table.fetchall()])

        self.cur.close()
        self.con.close()

        for k, v in personalID.items():
            try:
                personalShift[v] = schedule[shift[k]].lower()
            except:
                pass
        return personalShift


class Setup:
    def __init__(self):
        # set up some constants
        pass

    def addWorker(self, worker, horario, status):
        MDB = r'C:\Users\Keko\Documents\PyExcel\Setup.accdb'; DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'; PWD = 'pw'

        con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
        cur = con.cursor()

        SQLcommand = "INSERT INTO Trabajadores (Nombre, Horario, Status) VALUES ('{}', '{}', {});"\
            .format(worker, horario, status)  # your query goes here
        cur.execute(SQLcommand)
        con.commit()

    def getWorkerID(self):
        MDB = r'C:\Users\Keko\Documents\PyExcel\Setup.accdb'; DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'; PWD = 'pw'

        con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
        cur = con.cursor()

        SQLcommand = "SELECT ID, Nombre FROM Trabajadores" # your query goes here
        workerstatus_table = cur.execute(SQLcommand)
        rows = workerstatus_table.fetchall()

        workerId = {}
        for row in rows:
            workerId[str(row[1])] = row[0]
        return workerId

    #def modifyWorker(self, nombre, horario, status):




    def getWorkerStatus(self):
        MDB = r'C:\Users\Keko\Documents\PyExcel\Setup.accdb'; DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'; PWD = 'pw'

        con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
        cur = con.cursor()

        SQLcommand = "SELECT * FROM Trabajadores" # your query goes here
        workerstatus_table = cur.execute(SQLcommand)
        rows = workerstatus_table.fetchall()

        workerstatus = {}
        for row in rows:
            workerstatus[str(row[1])] = row[3]
        return workerstatus

    def getWorkersTable(self):
        MDB = r'C:\Users\Keko\Documents\PyExcel\Setup.accdb'; DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'; PWD = 'pw'

        con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
        cur = con.cursor()

        SQLcommand = "SELECT Id, Nombre,Horario,Status FROM Trabajadores" # your query goes here
        workerstatus_table = cur.execute(SQLcommand)
        return workerstatus_table.fetchall()

    def personalShift(self):
        MDB = r'C:\Users\Keko\Documents\PyExcel\Setup.accdb'; DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'; PWD = 'pw'

        con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
        cur = con.cursor()

        SQLcommand = "SELECT Nombre, Horario, Status FROM Trabajadores" # your query goes here
        workerstatus_table = cur.execute(SQLcommand)
        rows = workerstatus_table.fetchall()

        personalShift = {}
        for row in rows:
            if row[2]:
                personalShift[str(row[0])] = row[1]
        return personalShift


if __name__ == "__main__":
    """
    import AnvizReader
    reporte = AnvizReader.Reorganizar()
    setup = Setup()
    workerStatus = setup.getWorkerStatus()
    jornada_personal = SQL().personalShift

    for w in reporte.personal:
        try: status = workerStatus[w]
        except KeyError:
            setup.addWorker(w, jornada_personal[w], True)
    """

    pprint(Setup().personalShift())
