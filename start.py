import sys, os
from PyQt4 import QtGui
from mainview_controller import MainView
import assets.sql as sql

YES = QtGui.QMessageBox.Yes
NO = QtGui.QMessageBox.No


class Start:
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)

    def program(self):
        # Revision de elementos críticos para el funcionamiento
        # del programa

        # Buscar archivo shelve de configuracion
        if sql.ConfigFile.exist():
            text = "Archivo de configuracion encontrado"
        else:
            text = "Archivo de configuracion creado"
            sql.ConfigFile.create()

        # buscar archivo de la base de datos
        if os.path.exists(
                sql.ConfigFile.getDatabasePath()):
            text = "Base de datos encontrada"
        else:
            if self.ask_user_to("search db") == YES:
                self.search_db_file()
            else:
                self.close()

            text = "Base de datos seleccionada"
        # conectar con la base de datos
        try:
            anvRgs = sql.AnvizRegisters()
        except ConnectionError:
            if self.ask_user_to('search db', 'invalid') == YES:
                self.search_db_file()
            else:
                self.close()

        # revisar la existencia de la tabla WorkDays
        if anvRgs.tableExists("WorkDays"):
            text = "Tabla WorkDays existente"
        else:
            anvRgs.createTable("WorkDays")
            text = "Tabla WorkDays creada"
        anvRgs.disconnect()

        mainview = MainView()

        mainview.show()
        sys.exit(self.app.exec())

    @staticmethod
    def ask_user_to(option, sub=None):
        messageBox = QtGui.QMessageBox()
        messageBox.setStandardButtons(QtGui.QMessageBox.Yes |
                                      QtGui.QMessageBox.No)
        messageBox.setIcon(QtGui.QMessageBox.Question)

        if option == "search db":
            if sub is None:
                messageBox.setText("La base de datos no fue encontrada...")
            elif sub == "invalid":
                messageBox.setText("La base de datos encontrada es invalida...")

            messageBox.setInformativeText("Desea buscarla?")
            messageBox.setDetailedText("Probablemente se encuentre en"
                                       " la direccion:\n C:\\standard")
        elif option == "reselect":
            messageBox.setText("Desea intentar de nuevo?")

        return messageBox.exec()

    def close(self):
        self.app.closeAllWindows()
        sys.exit()

    def search_db_file(self):
        file_name = ''
        while True:
            file_name = QtGui.QFileDialog.getOpenFileName(
                None, "Seleccionar archivo Access", "C:\\", "Access db (*.mdb)")
            file_name = file_name.replace('/', '\\')
            if file_name:
                sql.ConfigFile.setDatabasePath(file_name)
                break
            if self.ask_user_to("reselect") == NO:
                self.close()
        return file_name

if __name__ == "__main__":
    start = Start()
    start.program()
