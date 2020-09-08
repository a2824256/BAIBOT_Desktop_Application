# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from Ui_Main import Ui_Main
import threading as th
import rospy
from teleoperation.msg import Gui
from multiprocessing import Process
from std_msgs.msg import Int8

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)


    def updateStatusBar(self, str):
        self.ui.statusBar.showMessage(str)


if __name__ == "__main__":
    app = QApplication([])
    try:
        widget = Main()
        widget.showFullScreen()
        widget.updateStatusBar("BAIBOT病原标本采集机器人已就绪。  Version: 1.0")
        widget.show()
        try:
            widget.ui.force_process()
        except:
            print("力感知连接失败")
        try:
            widget.ui.run_ros_subscriber()
        except:
            print("ros消息订阅失败")
        try:
            widget.ui.start_parameter_monitor()
        except:
            print("参数监控开启失败")
        sys.exit(app.exec_())
    except:
        kill_id = widget.ui.kill_pid
        if kill_id != 0:
            cmd = "kill -9 " + str(kill_id)
            print(cmd)
            print("已杀ros监听进程")
            widget.ui.cmd_run(cmd)
        if widget.ui.force_pid != 0:
            cmd = "kill -9 " + str(widget.ui.force_pid)
            print(cmd)
            print("已杀气压监听进程")
            widget.ui.cmd_run(cmd)
        pid = os.getpid()
        cmd = "kill -9 " + str(pid)
        print(cmd)
        print("已杀主进程")
        widget.ui.cmd_run(cmd)
