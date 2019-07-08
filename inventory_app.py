from PySide2 import QtCore, QtWidgets, QtGui
from ui import mainwindow
from database import *
from datetime import datetime


class Interface(mainwindow.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Database.initialize(database="singaporeschoolcebu", user="postgres", host="localhost", port="5434")
    dateToday = datetime.now().strftime("%Y-%m-%d")
    MainWindow = Interface()
    MainWindow.show()
    sys.exit(app.exec_())

