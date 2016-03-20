import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Test1(QDialog,):
    def __init__(self, parent=None):
        super(Test1, self).__init__(parent)
        self.dateTimeEdit = QDateTimeEdit(self)
        self.dateTimeEdit.setGeometry(QRect(290, 20, 81, 241))


class Test2(QDialog,):
    def __init__(self, parent=None):
        super(Test2, self).__init__(parent)
        self.dateTimeEdit = QDateTimeEdit(self)
        self.dateTimeEdit.setGeometry(QRect(290, 20, 81, 241))
        t1 = Test1()
        t1.show()

app = QApplication(sys.argv)
t2 = Test2()
t2.show()
app.exec()