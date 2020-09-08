from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, Signal, Slot)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
                           QPixmap, QRadialGradient, QImage, QMouseEvent)
from PySide2.QtWidgets import *
import pyrealsense2 as rs
import threading
import time
import socket
import PIL.Image as Image
import numpy as np
import subprocess
from playsound import playsound
import rospy
from teleoperation.msg import Gui
from multiprocessing import Process
from std_msgs.msg import Int8
import math
import redis
import json
import cv2
import os
import serial

FPS = 30
DELAY = 0
cmd_ros_core = "roscore"
cmd_force = "rosrun serialPort forceSerial"
WIDTH = 1280
HEIGHT = 720
COMMAND = dict(common={
    # "com1": "roslaunch ur_gazebo ur5.launch ; rosrun teleoperation jointAngleController",  # 5~6s
    "com1": "roslaunch ur_robot_driver ur5_bringup.launch robot_ip:=192.168.103.115",  # 5~6s
    "com2": "roslaunch ur5_moveit_config ur5_moveit_planning_execution.launch",  # 5~6s
    "com3": 'echo "123qwe" | sudo -S chmod 777 /dev/ttyACM0',
    "com4": "roslaunch teleoperation run_touch.launch",
    "com5": "roslaunch teleoperation run_serial_control.launch"
}, tele={
    "com1": "rosrun teleoperation touch_ctl"
}, auto={
    "com1": "roslaunch teleoperation camera_calibration_pub.launch",
    "com2": "python ~/lee/ThroatSwap/src/teleoperation/src/tcp_camera_uvual.py",
    "com3": "rosrun teleoperation automation_new"                                  #
}, other={
    "com1": "python ~/lee/ThroatSwap/src/teleoperation/src/detection_request.py",
    "com2": "python /home/desmond/lee/ThroatSwap/src/teleoperation/src/emergency_stop.py",
    "lj": ". ~/lee/ThroatSwap/src/teleoperation/hybrid_real_uvula.sh",
    "force": "python3 /home/desmond/文档/Avatar_Desktop_Application-master/force.py"
})


class Ui_Main(QObject):
    # force = 0.0
    first_val = 0.0
    tips_signal = Signal(str)
    dis_update = Signal(QPixmap)
    dis_update2 = Signal(QPixmap)
    display_tid = None
    mask_type = "origin"
    force = Signal(str)
    sound_lock = False
    mode_disp_text = Signal(str)
    set_detection_mode_pub = None
    detection_mode = 2
    kill_pid = 0
    force_pid = 0
    # ----- GUI辅助信息 -----
    touch_mode_signal = Signal(str)
    running_state_signal = Signal()
    touch_pose_x_signal = Signal()
    touch_pose_y_signal = Signal()
    touch_pose_z_signal = Signal()
    manipulator_state_signal = Signal(str)
    touch_mode = 0
    touch_pose_x = 0
    touch_pose_y = 0
    touch_pose_z = 0
    manipulator_state = 1
    running_state = 2
    time_counter = 0
    time_signal = Signal()
    time_stop_flag = False
    main_screen = 1

    redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)


    def setupUi(self, Main):
        if not Main.objectName():
            Main.setObjectName(u"Main")
        Main.resize(1920, 1100)
        Main.setStyleSheet(u"QTabBar::tab{\n"
                           "	background-color: rgb(92, 53, 102);\n"
                           "	color:white;\n"
                           "}\n"
                           "\n"
                           "QTabBar::tab:selected{\n"
                           "	border-color: white;\n"
                           "	background: white;\n"
                           "	color:black\n"
                           "}\n"
                           "font:  \"Ubuntu\";")
        self.centralwidget = QWidget(Main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background:rgb(92, 53, 102);")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1920, 1178))
        self.tabWidget.setStyleSheet(u"QTabWidget::pane{border-width:0px;\n"
"border-style: outset;background-color: rgb(255, 255, 255);\n"
"}\n"
"QTabBar::tab{border-bottom-color: #C2C7CB;\n"
"             border-top-left-radius: 0px;\n"
"             border-top-right-radius: 0px;\n"
"             max-width: 200px; min-width:200px; \n"
"			   min-height:60px;\n"
"             font:20px \"Ubuntu\";;\n"
"             padding: 0px 0px 0px 0px;\n"
" }")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideRight)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab1 = QWidget()
        self.tab1.setObjectName(u"tab1")
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tab1.setFont(font)
        self.tab1.setAutoFillBackground(False)
        self.tab1.setStyleSheet(u"background-color: rgb(244, 244, 244);")
        self.groupBox_2 = QGroupBox(self.tab1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(30, 20, 471, 211))
        font1 = QFont()
        font1.setPointSize(20)
        self.groupBox_2.setFont(font1)
        self.NWarning = QLabel(self.groupBox_2)
        self.NWarning.setObjectName(u"NWarning")
        self.NWarning.setGeometry(QRect(10, 54, 451, 141))
        font2 = QFont()
        font2.setPointSize(40)
        self.NWarning.setFont(font2)
        self.NWarning.setStyleSheet(u"background-color: rgb(211, 215, 207);\n"
"border-radius: 17px;\n"
"color: white")
        self.NWarning.setAlignment(Qt.AlignCenter)
        self.groupBox_4 = QGroupBox(self.tab1)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(510, 90, 1391, 901))
        self.groupBox_4.setFont(font1)
        self.camera_label = QLabel(self.groupBox_4)
        self.camera_label.setObjectName(u"camera_label")
        self.camera_label.setGeometry(QRect(10, 50, 1371, 841))
        self.camera_label.setStyleSheet(u"background-color: black;")
        self.camera_label_2 = QLabel(self.groupBox_4)
        self.camera_label_2.setObjectName(u"camera_label_2")
        self.camera_label_2.setGeometry(QRect(10, 50, 360, 270))
        self.camera_label_2.setStyleSheet(u"background-color: black;")
        self.emergency_stop = QPushButton(self.tab1)
        self.emergency_stop.setObjectName(u"emergency_stop")
        self.emergency_stop.setGeometry(QRect(20, 910, 471, 71))
        font3 = QFont()
        font3.setPointSize(30)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setWeight(50)
        self.emergency_stop.setFont(font3)
        self.emergency_stop.setStyleSheet(u"background-color: rgb(204, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.groupBox_10 = QGroupBox(self.tab1)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setGeometry(QRect(30, 240, 471, 121))
        self.groupBox_10.setFont(font1)
        self.mode_label = QLabel(self.groupBox_10)
        self.mode_label.setObjectName(u"mode_label")
        self.mode_label.setGeometry(QRect(10, 50, 451, 61))
        font4 = QFont()
        font4.setPointSize(25)
        self.mode_label.setFont(font4)
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.tabWidget_2 = QTabWidget(self.tab1)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setGeometry(QRect(19, 380, 481, 521))
        font5 = QFont()
        font5.setPointSize(15)
        self.tabWidget_2.setFont(font5)
        self.tabWidget_2.setStyleSheet(u"QTabWidget::tab-bar{\n"
                                       "left:0px;\n"
                                       "}\n"
                                       "QTabBar::tab{\n"
                                       "    max-width: 235px; min-width:235px;\n"
                                       "	background-color: rgb(92, 53, 102);\n"
                                       "	color:white;\n"
                                       "   margin-left:0px;\n"
                                       "}\n"
                                       "QTabBar::tab{\n"
                                       "	background-color: white;\n"
                                       "	color:black;\n"
                                       "}\n"
                                       "\n"
                                       "QTabBar::tab:selected{\n"
                                       "	border-color: white;\n"
                                       "	background: rgb(92, 53, 102);\n"
                                       "	color:white\n"
                                       "}")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.start_btn = QPushButton(self.tab_2)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setGeometry(QRect(0, 20, 471, 71))
        self.start_btn.setFont(font3)
        self.start_btn.setStyleSheet(u"background-color: rgb(115, 210, 22);\n"
"color: rgb(255, 255, 255);")
        self.mode_2_btn = QPushButton(self.tab_2)
        self.mode_2_btn.setObjectName(u"mode_2_btn")
        self.mode_2_btn.setGeometry(QRect(0, 110, 471, 71))
        self.mode_2_btn.setFont(font3)
        self.mode_2_btn.setStyleSheet(u"background-color: rgb(114, 159, 207);\n"
"color: rgb(255, 255, 255);")
        self.mode_1_btn = QPushButton(self.tab_2)
        self.mode_1_btn.setObjectName(u"mode_1_btn")
        self.mode_1_btn.setGeometry(QRect(0, 200, 471, 71))
        self.mode_1_btn.setFont(font3)
        self.mode_1_btn.setStyleSheet(u"background-color: rgb(114, 159, 207);\n"
"color: white;")
        self.sound_tips_btn_1 = QPushButton(self.tab_2)
        self.sound_tips_btn_1.setObjectName(u"sound_tips_btn_1")
        self.sound_tips_btn_1.setGeometry(QRect(0, 290, 231, 71))
        font6 = QFont()
        font6.setPointSize(16)
        font6.setBold(False)
        font6.setItalic(False)
        font6.setWeight(50)
        self.sound_tips_btn_1.setFont(font6)
        self.sound_tips_btn_1.setStyleSheet(u"background-color: rgb(114, 159, 207);\n"
"color: white;")
        self.sound_tips_btn_3 = QPushButton(self.tab_2)
        self.sound_tips_btn_3.setObjectName(u"sound_tips_btn_3")
        self.sound_tips_btn_3.setGeometry(QRect(0, 380, 471, 71))
        self.sound_tips_btn_3.setFont(font6)
        self.sound_tips_btn_3.setStyleSheet(u"background-color: rgb(114, 159, 207);\n"
"color: white;")
        self.sound_tips_btn_2 = QPushButton(self.tab_2)
        self.sound_tips_btn_2.setObjectName(u"sound_tips_btn_2")
        self.sound_tips_btn_2.setGeometry(QRect(240, 290, 231, 71))
        self.sound_tips_btn_2.setFont(font6)
        self.sound_tips_btn_2.setStyleSheet(u"background-color: rgb(114, 159, 207);\n"
"color: white;")
        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_5 = QLabel(Main)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(700, -2, 700, 64))
        self.label_5.setText("BAIBOT病原标本采集机器人")
        self.label_5.setStyleSheet(u"color:white;font-size:50px;")

        self.cuhk = QLabel(Main)
        self.cuhk.setObjectName(u"cuhk")
        self.cuhk.setGeometry(QRect(1840, 5, 64, 52))
        pixmap2 = QPixmap("./img/cuhk.png")
        pixmap2 = pixmap2.scaled(68, 56, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.cuhk.setPixmap(pixmap2)

        self.airs = QLabel(Main)
        self.airs.setObjectName(u"airs")
        self.airs.setGeometry(QRect(1700, 0, 107, 56))
        pixmap3 = QPixmap("./img/airs.png")
        pixmap3 = pixmap3.scaled(107, 56, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.airs.setPixmap(pixmap3)

        self.label_4 = QLabel(self.tab_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 30, 211, 31))
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.touch_position_label = QLabel(self.tab_3)
        self.touch_position_label.setObjectName(u"touch_position_label")
        self.touch_position_label.setGeometry(QRect(230, 30, 141, 31))
        self.touch_position_label.setFont(font1)
        self.label_9 = QLabel(self.tab_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 80, 211, 31))
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.touch_mode_label = QLabel(self.tab_3)
        self.touch_mode_label.setObjectName(u"touch_mode_label")
        self.touch_mode_label.setGeometry(QRect(230, 80, 200, 31))
        self.touch_mode_label.setFont(font1)
        self.position_btn = QPushButton(self.tab_3)
        self.position_btn.setObjectName(u"position_btn")
        self.position_btn.setGeometry(QRect(0, 380, 471, 71))
        self.position_btn.setFont(font3)
        self.position_btn.setStyleSheet(u"background-color: rgb(115, 210, 22);\n"
"color: rgb(255, 255, 255);")
        self.change_screen_btn = QPushButton(self.tab_3)
        self.change_screen_btn.setObjectName(u"change_screen_btn")
        self.change_screen_btn.setGeometry(QRect(0, 280, 471, 71))
        self.change_screen_btn.setFont(font3)
        self.change_screen_btn.setStyleSheet(u"background-color: blue;\n"
                                        "color: rgb(255, 255, 255);")
        self.init_local_btn = QPushButton(self.tab_3)
        self.init_local_btn.setObjectName(u"init_local_btn")
        self.init_local_btn.setGeometry(QRect(0, 190, 471, 71))
        self.init_local_btn.setFont(font3)
        self.init_local_btn.setStyleSheet(u"background-color: blue;\n"
                                             "color: rgb(255, 255, 255);")
        self.label_25 = QLabel(self.tab_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(-10, 130, 231, 31))
        self.label_25.setFont(font1)
        self.label_25.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_26 = QLabel(self.tab_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(230, 130, 220, 31))
        self.label_26.setFont(font1)
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tips_label = QLabel(self.tab1)
        self.tips_label.setObjectName(u"tips_label")
        self.tips_label.setGeometry(QRect(510, 0, 231, 81))
        font7 = QFont()
        font7.setPointSize(30)
        self.tips_label.setFont(font7)
        self.tips_label.setStyleSheet(u"padding: 20px;color:red;")
        self.tips_content_label = QLabel(self.tab1)
        self.tips_content_label.setObjectName(u"tips_content_label")
        self.tips_content_label.setGeometry(QRect(750, 0, 1151, 81))
        self.tips_content_label.setFont(font7)
        self.tips_content_label.setStyleSheet(u"padding: 20px;color:red;")
        self.tabWidget.addTab(self.tab1, "")
        font10 = QFont()
        font10.setPointSize(20)
        font10.setBold(False)
        font10.setItalic(False)
        font10.setWeight(50)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"background-color: rgb(244, 244, 244);\n"
"font: \"Ubuntu\";")
        self.groupBox_6 = QGroupBox(self.tab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(20, 710, 521, 261))
        self.groupBox_6.setFont(font10)
        self.shutdown_btn = QPushButton(self.groupBox_6)
        self.shutdown_btn.setObjectName(u"shutdown_btn")
        self.shutdown_btn.setGeometry(QRect(30, 80, 461, 61))
        self.shutdown_btn.setFont(font10)
        self.shutdown_btn.setStyleSheet(u"background-color: rgb(204, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.groupBox_7 = QGroupBox(self.tab)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(560, 10, 611, 681))
        self.groupBox_7.setFont(font10)
        self.cv_local_btn = QPushButton(self.groupBox_7)
        self.cv_local_btn.setObjectName(u"cv_local_btn")
        self.cv_local_btn.setGeometry(QRect(40, 70, 431, 61))
        self.cv_local_btn.setFont(font10)
        self.cv_local_btn.setStyleSheet(u"background-color: rgb(114, 159, 207);\n"
"color: white;")
        self.cv_remote_btn = QPushButton(self.groupBox_7)
        self.cv_remote_btn.setObjectName(u"cv_remote_btn")
        self.cv_remote_btn.setGeometry(QRect(40, 150, 431, 61))
        self.cv_remote_btn.setFont(font10)
        self.cv_remote_btn.setStyleSheet(u"background-color: rgb(114, 159, 207);\n"
"color: rgb(255, 255, 255);")
        self.cv_local_cbtn = QPushButton(self.groupBox_7)
        self.cv_local_cbtn.setObjectName(u"cv_local_cbtn")
        self.cv_local_cbtn.setGeometry(QRect(490, 70, 91, 61))
        self.cv_local_cbtn.setFont(font6)
        self.cv_local_cbtn.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.cv_remote_cbtn = QPushButton(self.groupBox_7)
        self.cv_remote_cbtn.setObjectName(u"cv_remote_cbtn")
        self.cv_remote_cbtn.setGeometry(QRect(490, 150, 91, 61))
        self.cv_remote_cbtn.setFont(font6)
        self.cv_remote_cbtn.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.host_content = QLineEdit(self.groupBox_7)
        self.host_content.setObjectName(u"host_content")
        self.host_content.setGeometry(QRect(170, 240, 361, 41))
        self.port_content = QLineEdit(self.groupBox_7)
        self.port_content.setObjectName(u"port_content")
        self.port_content.setGeometry(QRect(170, 310, 361, 41))
        self.label_27 = QLabel(self.groupBox_7)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(60, 240, 91, 31))
        self.label_27.setFont(font6)
        self.label_27.setAlignment(Qt.AlignCenter)
        self.label_28 = QLabel(self.groupBox_7)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(60, 310, 91, 31))
        self.label_28.setFont(font6)
        self.label_28.setAlignment(Qt.AlignCenter)
        self.display_ctrl_btn = QPushButton(self.groupBox_7)
        self.display_ctrl_btn.setObjectName(u"display_ctrl_btn")
        self.display_ctrl_btn.setGeometry(QRect(40, 380, 541, 61))
        self.display_ctrl_btn.setFont(font10)
        self.display_ctrl_btn.setStyleSheet(u"background-color: rgb(114, 159, 207);\n"
"color: rgb(255, 255, 255);")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 531, 681))
        self.groupBox.setFont(font10)
        self.btn1 = QPushButton(self.groupBox)
        self.btn1.setObjectName(u"btn1")
        self.btn1.setGeometry(QRect(10, 50, 391, 60))
        self.btn1.setFont(font10)
        self.btn2 = QPushButton(self.groupBox)
        self.btn2.setObjectName(u"btn2")
        self.btn2.setGeometry(QRect(10, 120, 391, 60))
        self.btn2.setFont(font10)
        self.btn3 = QPushButton(self.groupBox)
        self.btn3.setObjectName(u"btn3")
        self.btn3.setGeometry(QRect(10, 190, 391, 60))
        self.btn3.setFont(font10)
        self.btn4 = QPushButton(self.groupBox)
        self.btn4.setObjectName(u"btn4")
        self.btn4.setGeometry(QRect(10, 260, 391, 60))
        self.btn4.setFont(font10)
        self.btn5 = QPushButton(self.groupBox)
        self.btn5.setObjectName(u"btn5")
        self.btn5.setGeometry(QRect(10, 330, 391, 60))
        self.btn5.setFont(font10)
        self.btn6 = QPushButton(self.groupBox)
        self.btn6.setObjectName(u"btn6")
        self.btn6.setGeometry(QRect(10, 400, 391, 60))
        self.btn6.setFont(font10)
        self.btn7 = QPushButton(self.groupBox)
        self.btn7.setObjectName(u"btn7")
        self.btn7.setGeometry(QRect(10, 470, 391, 60))
        self.btn7.setFont(font10)
        self.cbtn_1 = QPushButton(self.groupBox)
        self.cbtn_1.setObjectName(u"cbtn_1")
        self.cbtn_1.setGeometry(QRect(420, 50, 91, 61))
        self.cbtn_1.setFont(font6)
        self.cbtn_1.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.cbtn_2 = QPushButton(self.groupBox)
        self.cbtn_2.setObjectName(u"cbtn_2")
        self.cbtn_2.setGeometry(QRect(420, 120, 91, 61))
        self.cbtn_2.setFont(font6)
        self.cbtn_2.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.cbtn_3 = QPushButton(self.groupBox)
        self.cbtn_3.setObjectName(u"cbtn_3")
        self.cbtn_3.setGeometry(QRect(420, 190, 91, 61))
        self.cbtn_3.setFont(font6)
        self.cbtn_3.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.cbtn_4 = QPushButton(self.groupBox)
        self.cbtn_4.setObjectName(u"cbtn_4")
        self.cbtn_4.setGeometry(QRect(420, 260, 91, 61))
        self.cbtn_4.setFont(font6)
        self.cbtn_4.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.cbtn_5 = QPushButton(self.groupBox)
        self.cbtn_5.setObjectName(u"cbtn_5")
        self.cbtn_5.setGeometry(QRect(420, 330, 91, 61))
        self.cbtn_5.setFont(font6)
        self.cbtn_5.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.cbtn_6 = QPushButton(self.groupBox)
        self.cbtn_6.setObjectName(u"cbtn_6")
        self.cbtn_6.setGeometry(QRect(420, 400, 91, 61))
        self.cbtn_6.setFont(font6)
        self.cbtn_6.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.cbtn_7 = QPushButton(self.groupBox)
        self.cbtn_7.setObjectName(u"cbtn_7")
        self.cbtn_7.setGeometry(QRect(420, 470, 91, 61))
        self.cbtn_7.setFont(font6)
        self.cbtn_7.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.btn8 = QPushButton(self.groupBox)
        self.btn8.setObjectName(u"btn8")
        self.btn8.setGeometry(QRect(10, 540, 391, 60))
        self.btn8.setFont(font10)
        self.btn9 = QPushButton(self.groupBox)
        self.btn9.setObjectName(u"btn9")
        self.btn9.setGeometry(QRect(10, 610, 391, 60))
        self.btn9.setFont(font10)
        self.cbtn_8 = QPushButton(self.groupBox)
        self.cbtn_8.setObjectName(u"cbtn_8")
        self.cbtn_8.setGeometry(QRect(420, 540, 91, 61))
        self.cbtn_8.setFont(font6)
        self.cbtn_8.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        self.cbtn_9 = QPushButton(self.groupBox)
        self.cbtn_9.setObjectName(u"cbtn_9")
        self.cbtn_9.setGeometry(QRect(420, 610, 91, 61))
        self.cbtn_9.setFont(font6)
        self.cbtn_9.setStyleSheet(u"background-color: rgb(204, 0, 0);color:white;")
        font12 = QFont()
        font12.setPointSize(15)
        font12.setBold(False)
        font12.setItalic(False)
        font12.setWeight(50)
        self.groupBox_8 = QGroupBox(self.tab)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(560, 710, 611, 261))
        self.groupBox_8.setFont(font10)
        self.collection_mode_change_btn = QPushButton(self.groupBox_8)
        self.collection_mode_change_btn.setObjectName(u"collection_mode_change_btn")
        self.collection_mode_change_btn.setGeometry(QRect(30, 170, 551, 61))
        self.collection_mode_change_btn.setFont(font10)
        self.collection_mode_change_btn.setStyleSheet(u"background-color: rgb(114, 159, 207);\n"
"color: rgb(255, 255, 255);")
        self.label_29 = QLabel(self.groupBox_8)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QRect(40, 70, 231, 61))
        self.label_29.setFont(font3)
        self.label_29.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.collection_mode_change_label = QLabel(self.groupBox_8)
        self.collection_mode_change_label.setObjectName(u"collection_mode_change_label")
        self.collection_mode_change_label.setGeometry(QRect(320, 70, 231, 61))
        self.collection_mode_change_label.setFont(font3)
        self.tabWidget.addTab(self.tab, "")
        Main.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(Main)
        self.statusBar.setObjectName(u"statusBar")
        Main.setStatusBar(self.statusBar)
        self.cv_remote_btn.clicked.connect(self.start_display_thread)
        self.dis_update.connect(self.camera_view)
        self.dis_update2.connect(self.camera_view2)
        self.display_ctrl_btn.clicked.connect(self.change_mask_type)
        self.force.connect(self.update_force)
        self.mode_1_btn.clicked.connect(self.start_tele)
        self.mode_2_btn.clicked.connect(self.start_auto)
        self.start_btn.clicked.connect(self.start_common)
        self.cv_local_btn.clicked.connect(self.open_local_camera_thread)
        self.mode_disp_text.connect(self.update_mode)
        self.touch_mode_signal.connect(self.update_touch_mode)
        self.touch_pose_x_signal.connect(self.update_touch_position)
        self.touch_pose_y_signal.connect(self.update_touch_position)
        self.touch_pose_z_signal.connect(self.update_touch_position)
        self.collection_mode_change_btn.clicked.connect(self.update_detection_mode)
        self.position_btn.clicked.connect(self.detection_start)
        self.change_screen_btn.clicked.connect(self.change_main_screen)
        self.emergency_stop.clicked.connect(self.stop_start)
        self.running_state_signal.connect(self.start_time_counter)
        self.time_signal.connect(self.update_timer_display)
        self.sound_tips_btn_1.clicked.connect(self.open_mouth_sound_thread)
        self.sound_tips_btn_2.clicked.connect(self.a_sound_thread)
        self.sound_tips_btn_3.clicked.connect(self.finished_sound_thread)
        self.tips_signal.connect(self.update_tips_label)
        self.init_local_btn.clicked.connect(self.init_local)
        # ----------绑定-----------
        self.retranslateUi(Main)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Main)
    # setupUi

    def change_main_screen(self):
        self.main_screen = 0 if self.main_screen is 1 else 1

    def update_timer_display(self):
        self.label_26.setText(str(self.time_counter) + " s")

    def start_time_counter(self):
        if self.time_stop_flag != True:
            t = threading.Thread(target=self.start_time_counter_thread)
            t.start()

    # 计时器计时
    def start_time_counter_thread(self):
        if self.time_counter == 0 and self.time_stop_flag == False and self.manipulator_state == '2':
            self.time_stop_flag = True
            while self.time_stop_flag == True:
                self.time_counter += 1
                self.time_signal.emit()
                time.sleep(1)
            self.time_counter = 0

    def start_display_thread(self):
        display_thread = threading.Thread(target=self.get_display)
        display_thread.setName("display")
        display_thread.start()


    def change_mask_type(self):
        if self.mask_type == "origin":
            self.mask_type = "pred"
            self.display_ctrl_btn.setText("关闭mask")
        else:
            self.mask_type = "origin"
            self.display_ctrl_btn.setText("开启mask")

    def open_local_camera_thread(self):
        self.camera_label_2.show()
        t1 = threading.Thread(target=self.open_local_camera)
        t1.start()

    def open_local_camera(self):
        capture = None
        for i in range(10):
            try:
                capture = cv2.VideoCapture(i)
                if capture.isOpened() is True:
                    print(capture.isOpened())
                    break
            except:
                continue
        while True:
            ret, frame = capture.read()
            try:
                qimage = QImage(frame, 960, 720, QImage.Format_BGR888)
                pixmap = QPixmap.fromImage(qimage)
                if self.main_screen is 1:
                    self.dis_update2.emit(pixmap)
                else:
                    self.dis_update.emit(pixmap)
            except:
                continue


    def get_display(self):
        s = socket.socket()
        s.connect((self.host_content.text(), int(self.port_content.text())))
        while True:
            try:
                s.send(bytes(self.mask_type, encoding='utf-8'))
                str = s.recv(4)
                data = bytearray(str)
                headIndex = 0
                if headIndex == 0:
                    allLen = int.from_bytes(data[headIndex:headIndex + 4], byteorder='little')
                    curSize = 0
                    allData = b''
                    while curSize < allLen:
                        data = s.recv(1024)
                        allData += data
                        curSize += len(data)
                    imgData = allData[0:921600]
                    img = Image.frombuffer('RGB', (640, 480), imgData)
                    img = img.transpose(Image.FLIP_TOP_BOTTOM)
                    img_conv = np.asarray(img)
                    qimage = QImage(img_conv, 640, 480, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(qimage)
                    if self.main_screen is 1:
                        self.dis_update.emit(pixmap)
                    else:
                        self.dis_update2.emit(pixmap)
            except:
                s.close()
                continue

    def open_realsense(self):
        try:
                pipeline = rs.pipeline()
                config = rs.config()
                config.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, FPS)
                config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, FPS)

                pipeline.start(config)

                align_to = rs.stream.color
                align = rs.align(align_to)
                while True:
                    frames = pipeline.wait_for_frames()
                    aligned_frames = align.process(frames)
                    aligned_depth_frame = aligned_frames.get_depth_frame()
                    color_frame = aligned_frames.get_color_frame()
                    if not aligned_depth_frame or not color_frame:
                        continue
                    c = np.asanyarray(color_frame.get_data())
                    qimage = QImage(c, 1280, 720, QImage.Format_BGR888)
                    pixmap = QPixmap.fromImage(qimage)
                    self.dis_update.emit(pixmap)
                pipeline.stop()
        except:
                print("本地打开realsense失败")


    @Slot(str)
    def update_force(self, force):
        self.NWarning.setText(str(float(force)))
        if float(force) > 15.0:
            self.NWarning.setStyleSheet("background-color:red;border-radius:17px;color:white;")
            if self.sound_lock is False:
                self.warning_sound_thread()
        else:
            self.NWarning.setStyleSheet("background-color:rgb(0, 255, 0);border-radius:17px;color:white;")


    @Slot(str)
    def update_mode(self, txt):
            self.mode_label.setText(txt)


    @Slot(QImage)
    def camera_view(self, c):
        self.camera_label.setPixmap(c)
        self.camera_label.setScaledContents(True)

    @Slot(QImage)
    def camera_view2(self, c):
        self.camera_label_2.setPixmap(c)
        self.camera_label_2.setScaledContents(True)

    def init_local_thread(self):
        print("恢复初始位姿")
        os.system("rosrun teleoperation backtoinitialpose")

    def init_local(self):
        t1 = threading.Thread(target=self.init_local_thread)
        t1.start()

    def start_tele(self):
        self.mode_disp_text.emit("遥操作模式")
        self.tips_signal.emit("运行中")
        t1 = threading.Thread(target=self.start_tele_thread)
        t1.start()

    def start_auto(self):
        self.mode_disp_text.emit("自动/分段控制模式")
        self.tips_signal.emit("运行中")
        t1 = threading.Thread(target=self.start_auto_thread)
        t1.start()

    def start_common(self):
        t1 = threading.Thread(target=self.start_common_thread)
        t1.start()

    def start_lj(self):
        self.cmd_run(COMMAND['other']['lj'])

    def start_common_thread(self):
        self.mode_disp_text.emit("启动中")
        # return
        self.run_ros_subscriber()
        t1 = threading.Thread(target=self.start_lj)
        t1.start()
        # print("common")
        # t1 = threading.Thread(target=self.output1)
        # t1.start()
        # print('common—1')
        # time.sleep(6)
        # t2 = threading.Thread(target=self.output2)
        # t2.start()
        # print('common—2')
        # time.sleep(6)
        # t3 = threading.Thread(target=self.output3)
        # t3.start()
        # print('common—3')
        # time.sleep(2)
        # t4 = threading.Thread(target=self.output4)
        # t4.start()
        # print('common—4')
        # time.sleep(2)
        # t5 = threading.Thread(target=self.output5)
        # t5.start()
        # time.sleep(2)
        # print('common—5')
        # t7 = Process(target=self.auto_output1())
        # t7.start()
        # print('common—6')
        # t6 = Process(target=self.auto_output2())
        # t6.start()
        print("finished")
        self.mode_disp_text.emit("启动完成，等待选择模式")

    def start_auto_thread(self):
        t3 = Process(target=self.auto_output3())
        t3.start()
        print("auto-3")

    def start_force(self):
        self.cmd_run(COMMAND['other']['force'])

    def start_force_process(self):
        t = Process(target=self.start_force)
        t.start()
        self.force_pid = t.pid

    def start_tele_thread(self):
        t1 = threading.Thread(target=self.tele_output1)
        t1.start()

    def output1(self):
        command = COMMAND['common']['com1']
        self.cmd_run(command)

    def output2(self):
        command = COMMAND['common']['com2']
        self.cmd_run(command)

    def output3(self):
        command = COMMAND['common']['com3']
        self.cmd_run(command)

    def output4(self):
        command = COMMAND['common']['com4']
        self.cmd_run(command)

    def output5(self):
        command = COMMAND['common']['com5']
        self.cmd_run(command)

    def tele_output1(self):
        command = COMMAND['tele']['com1']
        self.cmd_run(command)

    def auto_output1(self):
        command = COMMAND['auto']['com1']
        self.cmd_run(command)

    def auto_output2(self):
        command = COMMAND['auto']['com2']
        self.cmd_run(command)

    def auto_output3(self):
        command = COMMAND['auto']['com3']
        self.cmd_run(command)

    def run(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        while True:
                line = process.stdout.readline().rstrip()
                if not line:
                        break
                yield line

    def warning_sound_thread(self):
        t = threading.Thread(target=self.warning_sound)
        t.start()

    def warning_sound(self):
        self.sound_lock = True
        playsound("./sound/warning.mp3")
        self.sound_lock = False

    def open_mouth_sound_thread(self):
        t = threading.Thread(target=self.open_mouth_sound)
        t.start()

    def open_mouth_sound(self):
        if self.sound_lock is False:
            self.sound_lock = True
            playsound("./sound/open_mouth.mp3")
            self.sound_lock = False

    def a_sound_thread(self):
        t = threading.Thread(target=self.a_sound)
        t.start()

    def a_sound(self):
        if self.sound_lock is False:
            self.sound_lock = True
            playsound("./sound/a_sound.mp3")
            self.sound_lock = False

    def entered_mouth_thread(self):
        t = threading.Thread(target=self.entered_mouth)
        t.start()

    def entered_mouth(self):
        if self.sound_lock is False:
            self.sound_lock = True
            playsound("./sound/entered_mouth.mp3")
            self.sound_lock = False

    def finished_sound_thread(self):
        t = threading.Thread(target=self.finished_sound)
        t.start()

    def finished_sound(self):
        if self.sound_lock is False:
            self.sound_lock = True
            playsound("./sound/finished.mp3")
            self.sound_lock = False


    def force_process(self):
        t1 = threading.Thread(target=self.run_roscore)
        t1.start()
        time.sleep(1)
        self.start_force_process()
        # t2 = threading.Thread(target=self.force_out)
        # t2.start()
        t3 = threading.Thread(target=self.get_force_serial)
        t3.start()

    def force_out(self):
        for path in self.run_force():
            try:
                s = str(path, encoding="utf8")
                js = json.loads(s)
                self.force.emit(js['force'])
            except:
                continue

    def run_roscore(self):
        subprocess.Popen(cmd_ros_core, stdout=subprocess.PIPE, shell=True)

    def cmd_run(self, command):
        print(os.system(command))
        # subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    def run_force(self):
        process = subprocess.Popen(cmd_force, stdout=subprocess.PIPE, shell=True)
        while True:
            line = process.stdout.readline().rstrip()
            if not line:
                break
            yield line

    def run_force_v2(self):
        process = subprocess.Popen(cmd_force, stdout=subprocess.PIPE, shell=True)
        while True:
            line = process.stdout.readline().rstrip()
            if not line:
                break
            yield line


    @Slot(str)
    def update_tips_label(self, txt):
        self.tips_content_label.setText(txt)


    @Slot(str)
    def update_running_state(self, txt):
        self.touch_mode_label.setText(txt)

    def update_touch_position(self):
        self.touch_position_label.setText(str(self.touch_pose_x) + "," + str(self.touch_pose_y) + "," + str(self.touch_pose_z))

    @Slot(str)
    def update_touch_mode(self, txt):
        if txt == "1":
            self.touch_mode_label.setText("manipulator")
        else:
            self.touch_mode_label.setText("finger")

    def subscriber_event(self, msg):
        r = redis.Redis(connection_pool=self.redis_pool)
        r.set("touch_mode", str(msg.touch_mode))
        r.set("touch_pose_x", str(msg.touch_pose.position.x))
        r.set("touch_pose_y", str(msg.touch_pose.position.y))
        r.set("touch_pose_z", str(msg.touch_pose.position.z))
        r.set("manipulator_state", str(msg.manipulator_state))

    def start_parameter_monitor(self):
        r = redis.Redis(connection_pool=self.redis_pool)
        r.delete("manipulator_state")
        t1 = threading.Thread(target=self.start_parameter_monitor_thread)
        t1.start()

    def start_parameter_monitor_thread(self):
        r = redis.Redis(connection_pool=self.redis_pool)
        while True:
           try:
               touch_mode = r.get("touch_mode")
               if touch_mode != self.touch_mode:
                    self.touch_mode_signal.emit(str(touch_mode))
                    self.touch_mode = touch_mode
               touch_pose_x = r.get("touch_pose_x")
               if touch_pose_x != self.touch_pose_x:
                    self.touch_pose_x_signal.emit()
                    self.touch_pose_x = round(touch_pose_x, 2)
               touch_pose_y = r.get("touch_pose_y")
               if touch_pose_y != self.touch_pose_y:
                    self.touch_pose_y_signal.emit()
                    self.touch_pose_y = round(touch_pose_y, 2)
               touch_pose_z = r.get("touch_pose_z")
               if touch_pose_z != self.touch_pose_z:
                    self.touch_pose_z_signal.emit()
                    self.touch_pose_z = round(touch_pose_z, 2)
               manipulator_state = r.get("manipulator_state")

               if manipulator_state != self.manipulator_state:
                   # 中心点
                   if manipulator_state is '3':
                       self.tips_signal.emit("到达口腔中心及采集")

                   elif manipulator_state is '2':
                       self.tips_signal.emit("定位和移动中")
                       self.running_state_signal.emit()

                   elif manipulator_state is '1':
                       self.tips_signal.emit("闲置状态")
                       self.time_stop_flag = False
                   else:
                       manipulator_state = 1
                       r.set("manipulator_state", manipulator_state)
                   self.manipulator_state = manipulator_state
               time.sleep(0.2)
           except:
               break

    def detection_start_process(self):
        command = COMMAND['other']['com1']
        self.cmd_run(command)

    def detection_start(self):
        t1 = Process(target=self.detection_start_process)
        t1.start()
        self.first_val = 0.0

    def stop_start(self):
        t1 = threading.Thread(target=self.stop_start_thread)
        t1.start()

    def stop_start_thread(self):
        command = COMMAND['other']['com2']
        self.cmd_run(command)

    def get_force_serial(self):
            r = redis.Redis(connection_pool=self.redis_pool)
            ser = serial.Serial('/dev/Force', 115200)
            # first_val 为初始值
            while True:
                    while ser.inWaiting() > 0:
                            status = 0
                            temp = float(ser.read(8).decode())
                            if self.first_val <= 0.0:
                                    self.first_val = temp
                            try:
                                status = 1
                                pressure = float(r.get("pressure"))
                            except:
                                status = 2
                                pressure = 0
                            print(temp, status, pressure)
                            res = 0.0
                            if pressure > 0 and pressure <= 10:
                                    res = math.fabs(temp - (0.002 * pressure))
                            elif pressure > 10 and pressure <= 60:
                                    res = math.fabs(temp - (0.003 * (pressure - 10) - 0.002))
                            elif pressure > 60 and pressure <= 150:
                                    res = math.fabs(temp - 0.14 - (0.004 * (pressure - 60)))
                            else:
                                    res = math.fabs(temp)
                            res = math.fabs(self.first_val - res) * 60
                            # 阈值，小于这个值不显示
                            self.force.emit(str(round(res, 2)))
                            # if res > 2:
                            #         self.force.emit(str(round(res, 2)))
                            # else:
                            #         self.force.emit(str(0.0))



    # 更新检测模式
    def update_detection_mode(self):
        r = redis.Redis(connection_pool=self.redis_pool)
        if r.get("push_lock") != "1":
            if r.get("is_push") == "0" or r.get("is_push") == None:
                r.set("push_lock", "1")
                if self.detection_mode == 1:
                    self.detection_mode = 2
                    self.collection_mode_change_label.setText("二阶采集")
                    self.collection_mode_change_btn.setText("切换模式-一阶采集")
                else:
                    self.detection_mode = 1
                    self.collection_mode_change_label.setText("一阶采集")
                    self.collection_mode_change_btn.setText("切换模式-二阶采集")
                r.set("push_value", str(self.detection_mode))
                r.set("is_push", "1")

    # 运行消息订阅推送
    def run_ros_subscriber_process(self):
        rospy.init_node('test_gui_ros')
        rospy.Subscriber('/test_gui_ros', Gui, self.subscriber_event)
        set_detection_mode_pub = rospy.Publisher('/set_detection_mode', Int8, queue_size=10)
        t1 = threading.Thread(target=rospy.spin)
        t1.start()
        r = redis.Redis(connection_pool=self.redis_pool)
        detection_mode = Int8()
        while True:
            try:
                # 推送切换检测模式
                is_push = r.get("is_push")
                if is_push == "1":
                    if r.get("push_value") == "1":
                        detection_mode.data = 1
                    else:
                        detection_mode.data = 2
                    set_detection_mode_pub.publish(detection_mode)
                    r.set("is_push", "0")
                    r.set("push_lock", "0")
                    print("push mode finished")
            except:
                break



    def run_ros_subscriber(self):
        p = Process(target=self.run_ros_subscriber_process)
        p.start()
        self.kill_pid = p.pid

    def retranslateUi(self, Main):
        Main.setWindowTitle(QCoreApplication.translate("Main", u"Avatar", None))
        self.camera_label_2.hide()
        self.groupBox_2.setTitle(QCoreApplication.translate("Main", u"末端接触力", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Main", u"实时图像", None))
        self.camera_label.setText("")
        self.emergency_stop.setText(QCoreApplication.translate("Main", u"急停", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Main", u"\u5f53\u524d\u6a21\u5f0f", None))
        self.mode_label.setText(QCoreApplication.translate("Main", u"\u7b49\u5f85\u542f\u52a8", None))
        self.start_btn.setText(QCoreApplication.translate("Main", u"\u542f\u52a8", None))
        self.mode_2_btn.setText(QCoreApplication.translate("Main", u"\u81ea\u52a8/\u5206\u6bb5\u63a7\u5236\u6a21\u5f0f", None))
        self.mode_1_btn.setText(QCoreApplication.translate("Main", u"\u9065\u64cd\u4f5c\u6a21\u5f0f", None))
        self.sound_tips_btn_1.setText(QCoreApplication.translate("Main", u"\u8bed\u97f3\u63d0\u9192\n"
"-\u8bf7\u5f20\u5634-", None))
        self.sound_tips_btn_3.setText(QCoreApplication.translate("Main", u"\u8bed\u97f3\u63d0\u9192\n"
"-\u91c7\u96c6\u7ed3\u675f\u53ef\u4ee5\u79bb\u5f00\u4e86-", None))
        self.sound_tips_btn_2.setText(QCoreApplication.translate("Main", u"\u8bed\u97f3\u63d0\u9192\n"
"-\u8bf7\u53d1\u51fa\u554a\u7684\u58f0\u97f3-", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QCoreApplication.translate("Main", u"\u542f\u52a8\u4e0e\u6a21\u5f0f\u9009\u62e9", None))
        self.label_4.setText(QCoreApplication.translate("Main", u"Touch\u4f4d\u59ff\uff1a", None))
        self.touch_position_label.setText(QCoreApplication.translate("Main", u"\u7b49\u5f85\u542f\u52a8", None))
        self.label_9.setText(QCoreApplication.translate("Main", u"Touch\u6a21\u5f0f\uff1a", None))
        self.touch_mode_label.setText(QCoreApplication.translate("Main", u"\u7b49\u5f85\u542f\u52a8", None))
        self.position_btn.setText(QCoreApplication.translate("Main", u"\u83b7\u53d6\u5b9a\u4f4d", None))
        self.change_screen_btn.setText(QCoreApplication.translate("Main", "切换显示", None))
        self.init_local_btn.setText(QCoreApplication.translate("Main", "恢复位姿", None))
        self.label_25.setText(QCoreApplication.translate("Main", u"\u91c7\u96c6\u65f6\u95f4\uff1a", None))
        self.label_26.setText(QCoreApplication.translate("Main", u"0 s", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("Main", u"\u8f85\u52a9\u4fe1\u606f", None))
        self.tips_label.setText(QCoreApplication.translate("Main", "系统提示:", None))
        self.tips_content_label.setText("闲置状态")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QCoreApplication.translate("Main", u"\u63a7\u5236", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Main", u"\u7cfb\u7edf\u64cd\u4f5c", None))
        self.shutdown_btn.setText(QCoreApplication.translate("Main", u"\u9000\u51fa", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Main", u"\u89c6\u89c9\u4e3b\u673a\u8bbe\u7f6e", None))
        self.cv_local_btn.setText(QCoreApplication.translate("Main", u"\u672c\u673a", None))
        self.cv_remote_btn.setText(QCoreApplication.translate("Main", u"\u8fdc\u7a0b", None))
        self.cv_local_cbtn.setText(QCoreApplication.translate("Main", u"X", None))
        self.cv_remote_cbtn.setText(QCoreApplication.translate("Main", u"X", None))
        self.host_content.setText(QCoreApplication.translate("Main", u"192.168.1.236", None))
        self.port_content.setText(QCoreApplication.translate("Main", u"60000", None))
        self.label_27.setText(QCoreApplication.translate("Main", u"Host\uff1a", None))
        self.label_28.setText(QCoreApplication.translate("Main", u"Port\uff1a", None))
        self.display_ctrl_btn.setText(QCoreApplication.translate("Main", u"\u663e\u793a/\u5173\u95edMask", None))
        self.groupBox.setTitle(QCoreApplication.translate("Main", u"\u673a\u68b0\u81c2\u63a7\u5236", None))
        self.btn1.setText(QCoreApplication.translate("Main", u"\u901a\u7528\u64cd\u4f5c1", None))
        self.btn2.setText(QCoreApplication.translate("Main", u"\u901a\u7528\u64cd\u4f5c2", None))
        self.btn3.setText(QCoreApplication.translate("Main", u"\u901a\u7528\u64cd\u4f5c3", None))
        self.btn4.setText(QCoreApplication.translate("Main", u"\u901a\u7528\u64cd\u4f5c4", None))
        self.btn5.setText(QCoreApplication.translate("Main", u"\u901a\u7528\u64cd\u4f5c5", None))
        self.btn6.setText(QCoreApplication.translate("Main", u"\u9065\u64cd\u4f5c1", None))
        self.btn7.setText(QCoreApplication.translate("Main", u"\u81ea\u52a8\u5316/\u6df7\u54081", None))
        self.cbtn_1.setText(QCoreApplication.translate("Main", u"X", None))
        self.cbtn_2.setText(QCoreApplication.translate("Main", u"X", None))
        self.cbtn_3.setText(QCoreApplication.translate("Main", u"X", None))
        self.cbtn_4.setText(QCoreApplication.translate("Main", u"X", None))
        self.cbtn_5.setText(QCoreApplication.translate("Main", u"X", None))
        self.cbtn_6.setText(QCoreApplication.translate("Main", u"X", None))
        self.cbtn_7.setText(QCoreApplication.translate("Main", u"X", None))
        self.btn8.setText(QCoreApplication.translate("Main", u"\u81ea\u52a8\u5316/\u6df7\u54082", None))
        self.btn9.setText(QCoreApplication.translate("Main", u"\u81ea\u52a8\u5316/\u6df7\u54083", None))
        self.cbtn_8.setText(QCoreApplication.translate("Main", u"X", None))
        self.cbtn_9.setText(QCoreApplication.translate("Main", u"X", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Main", u"\u91c7\u96c6\u6a21\u5f0f\u5207\u6362", None))
        self.collection_mode_change_btn.setText(QCoreApplication.translate("Main", u"\u5207\u6362\u6a21\u5f0f - \u4e00\u9636\u91c7\u96c6", None))
        self.label_29.setText(QCoreApplication.translate("Main", u"\u5f53\u524d\u6a21\u5f0f\uff1a", None))
        self.collection_mode_change_label.setText(QCoreApplication.translate("Main", u"\u4e8c\u9636\u91c7\u96c6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Main", u"\u8bbe\u7f6e", None))

