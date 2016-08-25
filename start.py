import sys, os
from PyQt4 import QtGui, QtCore
from mainview_controller import MainView
import assets.sql as sql

YES = QtGui.QMessageBox.Yes
NO = QtGui.QMessageBox.No

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
                                   " la direccion C:\\standard")
    elif option == "reselect":
        messageBox.setText("Desea intentar de nuevo?")

    return messageBox.exec()

def search_db_file():
    def retryLoop():
        while True:
            file_name = QtGui.QFileDialog.getOpenFileName(
                None, "Seleccionar archivo Access", "C:\\", "Access db (*.mdb)")
            if file_name:
                break
            if ask_user_to("reselect") == NO:
                sys.exit()

    file_name = QtGui.QFileDialog.getOpenFileName(
        None, "Seleccionar archivo Access", "C:\\", "Access db (*.mdb)")
    if file_name:
        sql.ConfigFile.setDatabasePath(file_name)
    else:
        retryLoop()


app = QtGui.QApplication(sys.argv)

start_dialog = QtGui.QDialog()
start_dialog.resize(500, 400)
start_dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
verticalLayout = QtGui.QVBoxLayout(start_dialog)
init_label = QtGui.QLabel("Iniciando el programa")
verticalLayout.addWidget(init_label)

# Revision de elementos críticos para el funcionamiento
# del programa

if sql.ConfigFile.exist():
    text = "Archivo de configuracion encontrado"
else:
    text = "Archivo de configuracion creado"
    sql.ConfigFile.create()

verticalLayout.addWidget(QtGui.QLabel(
        text))

if os.path.exists(
        sql.ConfigFile.getDatabasePath()):
    text = "Base de datos encontrada"
else:
    if ask_user_to("serach db") == YES:
        search_db_file()
    else:
        sys.exit()

    text = "Base de datos seleccionada"

verticalLayout.addWidget(QtGui.QLabel(
        text))

try:
    sql.AnvizRegisters()
except ConnectionError:
    if ask_user_to('search db', 'invalid') == YES:
        search_db_file()
    else:
        sys.exit()

if sql.AnvizRegisters().tableExists("WorkDays"):
    text = "Tabla WorkDays existente"
else:
    sql.AnvizRegisters().createTable("WorkDays")
    text = "Tabla WorkDays creada"


mainview = MainView()

start_dialog.close()

mainview.show()
sys.exit(app.exec())