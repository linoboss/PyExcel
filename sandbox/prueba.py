from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys


app = QApplication(sys.argv)
printer = QPrinter()
dpi = 96

#painter = QPainter(printer)
printer.setResolution(dpi)
printer.setOutputFileName("foo.pdf")
printer.setOutputFormat(QPrinter.PdfFormat)
printer.setPageSize(QPrinter.Letter)
printer.setPageMargins(30, 16, 12, 20, QPrinter.Millimeter)
#painter.scale(50, 50)
font = QFont()
font.setPointSize(12)
doc = QTextDocument()
doc.setDefaultFont(font)


html = ""
html += "<html><body><p>Que ricos estan muchachones</p></body></html>"

doc.setHtml(html)

doc.print_(printer)
doc.documentLayout().setPaintDevice(printer)
# Done.



