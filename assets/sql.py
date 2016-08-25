# https://code.google.com/p/pyodbc/wiki/Cursor
import sys, os
import pyodbc
import datetime as dt
import shelve
from PyQt4 import QtSql
from PyQt4 import QtCore
from assets.dates_tricks import MyDates as md

global_var = globals()
global_var['CONFIG_FILE'] = '..\\persistence\\config'


class ConfigFile:
    @staticmethod
    def create():
        shelve_ = shelve.open(global_var['CONFIG_FILE'],
                              flag='c')
        shelve_.close()

    @staticmethod
    def exist():
        return (os.path.exists(global_var['CONFIG_FILE']) +
                '.bak')

    @staticmethod
    def setDatabasePath(database_path):
        """
        :param database_path: path to the database
        """
        shelve_ = shelve.open(global_var['CONFIG_FILE'],
                              flag='w', protocol=None,
                              writeback=True)
        shelve_['dbadd'] = database_path
        shelve_.close()
        return database_path

    @staticmethod
    def getDatabasePath():
        shelve_ = shelve.open(global_var['CONFIG_FILE'],
                              flag='r', protocol=None,
                              writeback=True)
        path = shelve_['dbadd']
        shelve_.close()
        return path


class SchMapping:
    def __init__(self, name, id_):
        self.name = name
        self.id = id_

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __repr__(self):
        return "<{id}: {name}>".format(name=self.name, id=self.id)

    def __eq__(self, other):
        if isinstance(other, int):
            comp = self.id == other
        else:
            comp = self.id == other.id

        return comp

    def __hash__(self):
        return hash(int(self))


class AnvizRegisters:
    def __init__(self):
        # *** Variable declaration ***
        self.db = None
        self.query = None

        # *** init actions ***
        self.__connect()

    def __connect(self):

        self.db = QtSql.QSqlDatabase.addDatabase("QODBC")

        MDB = ConfigFile.getDatabasePath()
        DRV = '{Microsoft Access Driver (*.mdb)}'
        PWD = 'pw'

        self.db.setDatabaseName("DRIVER={};DBQ={};PWD={}".format(DRV, MDB, PWD))

        if not self.db.open():
            raise ConnectionError("UNABLE TO CONECT TO THE DATABASE ")

        self.query = QtSql.QSqlQuery()

    def tableExists(self, name):
        if name == "WorkDays":
            self.query.exec("SELECT workdayid FROM WorkDays")
            return self.howthequerydid() == "Query completed"

    def createTable(self, name):
        """
        Creates the tables required by the program
        :param name:  select one of the available tables to create
                __Available Tables__
                -> Workdays

        :return: a message of success or failure depending of the outcome.
        """
        if name == "WorkDays":
            self.query.exec("CREATE TABLE WorkDays "
                            "("
                            "workdayid AUTOINCREMENT, "
                            "day DATE NOT NULL, "
                            "worker VARCHAR(50) REFERENCES Userinfo(Userid), "
                            "InTime_1 DATETIME, "
                            "OutTime_1 DATETIME, "
                            "InTime_2 DATETIME, "
                            "OutTime_2 DATETIME, "
                            "InTime_3 DATETIME, "
                            "OutTime_3 DATETIME, "
                            "shift INTEGER REFERENCES Schedule(Schid)"
                            ")")
        else:
            raise KeyError(name + ' is not a valid option')
        return self.howthequerydid()

    def readTable(self, name,
                  from_date=dt.datetime(1999, 1, 1),  # minimum valid date
                  till_date=dt.datetime(2100, 1, 1)   # large valid date
                  ):
        """

        Makes a READ query on the "name" table

        :param name: indicates the table in which the query wants to be made
        :param from_date: \ _  date filters, as most of the queries will be
        :param till_date: /    bounded by a date range restrain
        :return: a message with the result status of the query
        """
        if name == "Checkinout":
            self.query.prepare("SELECT Logid, Userid, CheckTime, CheckType "
                               "FROM Checkinout "
                               "WHERE CheckTime >= :from_date AND CheckTime <= :till_date")
            self.query.bindValue(":from_date", QtCore.QDateTime(from_date))
            self.query.bindValue(":till_date", QtCore.QDateTime(till_date))
            self.query.exec_()

        return self.howthequerydid(name)

    def insertInto(self, table, *args):
        print(table)
        print(args)
        if table == "WorkDays":
            self.query.prepare("INSERT INTO WorkDays ("
                               "    day, worker, InTime_1, OutTime_1, InTime_2, "
                               "    OutTime_2, InTime_3 , OutTime_3, shift) "
                               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
            for i, value in enumerate(args):
                print(i, value)
                self.query.bindValue(i, value)
            self.query.exec_()

    def randomLoad(self, name):
        if name == "WorkDays":
            self.query.prepare("INSERT INTO WorkDays (workdayid, worker, checkin, checkout, shift) "
                               "VALUES (:id, :worker, :checkin, :checkout, :shift)")

            self.query.bindValue(":id", 2)
            self.query.bindValue(":worker", 20)
            self.query.bindValue(":checkin", QtCore.QDateTime(dt.datetime(2016, 1, 1)))
            self.query.bindValue(":checkout", QtCore.QDateTime(dt.datetime(2016, 1, 1)))
            self.query.bindValue(":shift", 3)

            self.query.exec_()

        return self.howthequerydid(name)

    def getShcedulesDetails(self, option="byId"):
        """
        :return: a dictionary with the parameters of the work shifts defined in the databse
        """
        shift_details = dict()
        if option == "byName":
            self.query.exec("SELECT DISTINCT c.Schname, Timename, Intime, Outtime, "
                            "   BIntime, EIntime, BOuttime, EOuttime "
                            "FROM ("
                            "   TimeTable a "
                            "   INNER JOIN "
                            "   SchTime b "
                            "       ON (a.Timeid = b.Timeid)) "
                            "   INNER JOIN "
                            "   Schedule c "
                            "       ON (b.Schid = c.Schid)")
        elif option == "byId":
            self.query.exec(
                "SELECT DISTINCT c.Schid, a.Timeid, Intime, Outtime, BIntime, EIntime, BOuttime, EOuttime "
                "FROM ("
                "   TimeTable a "
                "   INNER JOIN "
                "   SchTime b "
                "       ON (a.Timeid = b.Timeid)) "
                "   INNER JOIN "
                "   Schedule c "
                "       ON (b.Schid = c.Schid)")
        else:
            raise KeyError("INVALID OPTION \"{}\", only available: byName and byId".format(option))

        while self.query.next():
            shift = self.query.value(0)
            schedule = self.query.value(1)

            if shift not in shift_details:
                shift_details[shift] = {}
            else: pass

            shift_details[shift][schedule] = [self.query.value(i) for i in range(2, 8)]

        return shift_details

    def schedules_map(self):
        """
        Returns a relation for all the schedules and the shifts
        :return: dict
        """
        schmap = dict([])

        self.query.exec("SELECT DISTINCT a.Schid, b.Schname, a.Timeid, c.Timename "
                        "FROM ("
                        "   SchTime a "
                        "   INNER JOIN Schedule b "
                        "       ON (a.Schid = b.Schid)) "
                        "   INNER JOIN "
                        "   TimeTable c "
                        "       ON (a.Timeid = c.Timeid)")

        while self.query.next():
            schid = self.query.value(0)
            schname = self.query.value(1)
            timeid = self.query.value(2)
            timename = self.query.value(3)

            sch = SchMapping(schname, schid)
            time = SchMapping(timename, timeid)

            if sch not in schmap:
                schmap[sch] = [time]
            else:
                schmap[sch] += [time]

        return schmap

    def getWorkers(self, option="byName", isActive=True):
        """
        Grants access to the information related to the workers
        :param option: defines the information to be returned
        :param isActive: sets the workers to search
            if True -> return only active workers
            if False -> returns only inactive workers
            else -> returns all the workers in registers
        :return: a dict with the info specified by the option parameter
        """
        workers = {}

        if isActive is True:
            ifActive = "WHERE isActive=true"
        elif isActive is False:
            ifActive = "WHERE isActive=false"
        else:
            ifActive = ''

        if option == "byName":
            self.query.exec("SELECT Userid, Name "
                            "FROM Userinfo " +
                            ifActive)

            while self.query.next():
                id_ = self.query.value(0)
                name = self.query.value(1)
                workers[name] = id_

        elif option == "byId":
            self.query.exec("SELECT Userid, Name "
                            "FROM Userinfo " +
                            ifActive)

            while self.query.next():
                id_ = self.query.value(0)
                name = self.query.value(1)
                workers[id_] = name

        elif option == "shifts by name":
            self.query.exec("SELECT Name, Schname "
                            "FROM ("
                            "   Userinfo a "
                            "   INNER JOIN "
                            "   UserShift b "
                            "       ON (a.Userid = b.Userid)) "
                            "   INNER JOIN "
                            "   Schedule c "
                            "       ON (b.Schid = c.Schid) " +
                            ifActive)
            while self.query.next():
                name = self.query.value(0)
                sch = self.query.value(1).lower()
                workers[name] = sch

        elif option == "shifts by id":
            self.query.exec("SELECT a.Userid, b.Schid "
                            "FROM ("
                            "   Userinfo a "
                            "   INNER JOIN "
                            "   UserShift b "
                            "       ON (a.Userid = b.Userid)) "
                            "   INNER JOIN "
                            "   Schedule c "
                            "       ON (b.Schid = c.Schid) " +
                            ifActive)
            while self.query.next():
                name = self.query.value(0)
                sch = self.query.value(1)
                workers[name] = sch

        elif option == "names":

            workers = []

            self.query.exec("SELECT Name "
                            "FROM Userinfo " +
                            ifActive)
            while self.query.next():
                name = self.query.value(0)
                workers.append(name)

        else:
            raise KeyError("invalid option \"{}\"".format(option))

        return workers

    def min_date_of(self, table):

        if table == 'Checkinout':
            self.query.exec("SELECT MIN(CheckTime) "
                            "FROM Checkinout".format(table))

        elif table == 'WorkDays':
            self.query.exec("SELECT MIN(CheckTime) "
                            "FROM WorkDays")
        else:
            raise KeyError(table + " is not a valid option")

        if self.query.next():
            date_ = self.query.value(0).toPyDateTime()
        else:
            date_ = None

        return date_

    def max_date_of(self, table):
        if table == 'Checkinout':
            self.query.exec("SELECT MAX(CheckTime) "
                            "FROM Checkinout".format(table))
        elif table == 'WorkDays':
            self.query.exec("SELECT MAX(InTime_1), "
                            "   MAX(OutTime_1), "
                            "   MAX(InTime_2), "
                            "   MAX(OutTime_2), "
                            "   MAX(InTime_3), "
                            "   MAX(OutTime_3) "
                            "FROM WorkDays")

            self.query.next()
            max_date = max([self.query.value(i) for i in range(6)])
            if max_date == QtCore.QDateTime():
                return None
            else:
                return max_date.toPyDateTime()
        else:
            raise KeyError(table + " is not a valid option")

        if self.query.next():
            date_ = self.query.value(0).toPyDateTime()
        else:
            date_ = None

        return date_

    def max_index_of(self, table):
        if table == 'WorkDays':
            self.query.exec("SELECT MAX(workdayid) "
                            "FROM WorkDays")
        else:
            raise KeyError(table + " is not a valid option")

        if self.query.next():
            id_ = self.query.value(0)
        else:
            id_ = None

        return id_

    def min_index_of(self, table):
        if table == 'WorkDays':
            self.query.exec("SELECT MIN(workdayid) "
                            "FROM WorkDays")
        else:
            raise KeyError(table + " is not a valid option")

        if self.query.next():
            id_ = self.query.value(0)
        else:
            id_ = None

        return id_

    def di_it_failed(self):
        if self.query.lastError().number() == -1:
            return False
        else:
            return True

    def howthequerydid(self, optional_info=''):
        error = self.query.lastError().text()
        if error is None:
            message = optional_info + ' NOT a valid option'
        elif error == ' ':
            message = "Query completed"
        else:
            message = error

        return message

    def value(self, i):
        return self.query.value(i)

    def next(self):
        return self.query.next()

    def firstlog(self):
        return

# *** TESTS ***


def setDatabasePath():
    config_editor = ConfigFile()

    file_name = QtGui.QFileDialog.getOpenFileName(None, "Open")
    app.closeAllWindows()
    print(config_editor.setDatabasePath(file_name))


def setSetupPath():
    config_editor = ConfigFile()
    file_name = QtGui.QFileDialog.getOpenFileName(None, "Open")
    print(config_editor.setSetupFilePath(file_name))


def createTable(name):
    anvizRegs = AnvizRegisters()
    print(anvizRegs.createTable(name))
    anvizRegs.db.close()
    sys.exit()


def readTable(name):
    anvizRegs = AnvizRegisters()
    print(anvizRegs.readTable(name,
                              dt.datetime(2015, 1, 1),
                              dt.datetime(2015, 3, 1)))
    q = anvizRegs.query

    print("Logid\tUserid\tCheckTime\tCheckType")
    while q.next():
        print(q.value(0), q.value(1), q.value(2), q.value(3))

    anvizRegs.db.close()
    sys.exit()


def updateTable(name):
    anvizRegs = AnvizRegisters()
    print(anvizRegs.updateTable(name))
    print('a', anvizRegs.query.value(0))
    anvizRegs.db.close()
    sys.exit()


def genericTest():
    anvizRegs = AnvizRegisters()
    pprint(anvizRegs.getShcedulesDetails())
    pprint(list(map(lambda x: str(x.id), anvizRegs.schedules_map().keys())))
    # pprint(anvizRegs.getWorkers("shifts by name"))
    anvizRegs.db.close()
    sys.exit()


def getShcedules():
    anvizRegs = AnvizRegisters()
    anvizRegs.getShcedulesDetails()
    anvizRegs.db.close()
    sys.exit()


def getWorkers():
    anvizRegs = AnvizRegisters()
    print("byName")
    pprint(anvizRegs.getWorkers("byName"))
    print("byId")
    pprint(anvizRegs.getWorkers("byId"))
    print("shift")
    pprint(anvizRegs.getWorkers("andShift"))
    print(anvizRegs.howthequerydid())
    anvizRegs.db.close()
    sys.exit()


def update():
    anvizRegs = AnvizRegisters()
    pprint(anvizRegs.updateTable("WorkDays"))
    anvizRegs.db.close()
    sys.exit()


def insertInto():
    anvizRegs = AnvizRegisters()
    pprint(anvizRegs.insertInto("WorkDays", *(
        QtCore.QDate(dt.date(2014, 9, 2)),
        '10',
        None,
        None,
        None,
        None,
        None,
        None,
        4
    )))
    anvizRegs.db.close()
    sys.exit()


def dates():
    anvizRegs = AnvizRegisters()
    print(anvizRegs.max_date_of("WorkDays"))
    sys.exit()


if __name__ == "__main__":
    from PyQt4 import QtGui
    from pprint import pprint
    app = QtGui.QApplication(sys.argv)
    # setDatabasePath()
    # setSetupPath()
    # getShcedulesDetails()
    # getWorkers()
    update()
    # createTable("WorkDays")
    # genericTest()
    # insertInto()
    # dates()
    app.exec()