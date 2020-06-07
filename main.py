# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from Ui_Main import Ui_Main


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)

    def updateStatusBar(self, str):
        self.ui.statusbar.showMessage(str)

if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    widget.updateStatusBar("Ready")
    widget.show()
    sys.exit(app.exec_())
