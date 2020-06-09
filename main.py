# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from Ui_Main import Ui_Main
import threading as th


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)

    def updateStatusBar(self, str):
        self.ui.statusBar.showMessage(str)

    # def logic(self):
    #     self.ui.pushButton.connect(self.output)

    # def output(self):
    #     self.ui.textEdit.setText("test")


if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    widget.showFullScreen()
    widget.updateStatusBar("系统已准备,  Avatar version: 1.0")
    widget.show()
    widget.ui.open_camera()
    try:
        widget.ui.force_out()
    except:
        print("force dead")
    sys.exit(app.exec_())

# QTabWidget::tab-bar{
#         alignment:left;
# }
