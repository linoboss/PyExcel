__author__ = 'Sonidos Guayana'
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSlot, SIGNAL
import AnvizReader
import GUI, tabla, controles_tabla
from to_excel import ToExcel
from configuration_views import PersonalSetup


class Controles(QWidget,
                controles_tabla.Ui_Form):
    def __init__(self, parent):
        super(Controles, self).__init__()
        self.setupUi(self)
        self.parent = parent

        self.reporte = self.getDatosLector()

        first_date, last_date = self.reporte.content[0].date, self.reporte.content[-1].date
        self.qdateFrom.setDate(first_date)
        self.qdateTo.setDate(last_date)

    @pyqtSlot()
    def on_qbuttonGenerar_clicked(self, **kwargs):
        self.reporte = self.getDatosLector()
        dateFrom = self.qdateFrom.date().toPyDate()
        dateTo = self.qdateTo.date().toPyDate()
        self.reporte.filter(dateFrom, dateTo)
        self.parent.tables.loadRange(self.reporte)

    @pyqtSlot()
    def on_excelButton_clicked(self, **kwargs):
        content = self.parent.tables
        to_excel = ToExcel()
        to_excel.add_sheet("Logs")
        to_excel.goto_sheet("Logs")
        to_excel.append(content.tablesContent['logs'])
        to_excel.autofit()
        to_excel.add_sheet("Total")
        to_excel.goto_sheet("Total")
        to_excel.append(content.tablesContent['rango'])
        from xlwings import Sheet
        Sheet('Total').autofit()
        Sheet('Logs').autofit()

    def getDatosLector(self):
        datoslector = AnvizReader.Reorganizar()
        datoslector.organizar_por_fecha()
        datoslector.calculateWorkedTime()
        return datoslector


class MainViewController(QMainWindow,
                         GUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainViewController, self).__init__(parent)
        self.setupUi(self)

        self.tables = tabla.Table()
        self.controls = Controles(self)
        self.gridLayout.addWidget(self.tables, 0, 0)
        self.gridLayout.addWidget(self.controls, 0, 1)
        self.actionPersonal.triggered.connect(self.personalSetup)

    def personalSetup(self):
        ps = PersonalSetup()
        ps.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainview_controller = MainViewController()
    mainview_controller.show()
    app.exec()



