# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import time
import subprocess
import threading as th
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, Signal, Slot)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient, QImage, QMouseEvent)
from PySide2.QtWidgets import *
import pyrealsense2 as rs
import numpy as np
import json
from math import *

FPS = 30
DELAY = 0
cmd_ros_core = "roscore"
cmd_force = "rosrun serialPort forceSerial"
WIDTH = 1280
HEIGHT = 720

class AIRSDisplay(QLabel):
    last_x = 0
    last_y = 0
    last_z = 0
    pos = QPoint
    frame = None
    paren = None
    depth_intr = None
    def __init__(self, parent=None):
        self.paren = parent
        super().__init__(parent)
        self.setMouseTracking(True)

    def mousePressEvent(self, ev:QMouseEvent):
        self.pos = ev.pos()
        real_x = round(self.pos.x()/self.width()*WIDTH)
        real_y = round(self.pos.y()/self.height()*HEIGHT)
        d = self.frame.get_distance(real_x,real_y)
        point = rs.rs2_deproject_pixel_to_point(intrin=self.depth_intr,pixel=[real_x,real_y],depth=d)
        distance = sqrt(pow(point[0] - self.last_x, 2) + pow(point[1] - self.last_y, 2) + pow(d - self.last_z, 2))
        QMessageBox().about(self.paren, "相机坐标系",
                              "--------本次坐标--------\n"
                              + str(point[0]) + "," + str(point[1]) + "," + str(point[2])
                              + "\n--------上次坐标--------\n" + str(self.last_x) + "," + str(self.last_y) + "," + str(self.last_z)
                            + "\n-------distance----------\ndistance=" + str(distance)

                              )
        self.last_x = point[0]
        self.last_y = point[1]
        self.last_z = point[2]

    def setting(self, f, depth_intr):
        self.frame = f
        self.depth_intr = depth_intr

class Ui_Main(QObject):
    output_str1 = Signal(str)
    output_str2 = Signal(str)
    output_str3 = Signal(str)
    output_str4 = Signal(str)
    output_str5 = Signal(str)
    output_str6 = Signal(str)
    output_str7 = Signal(str)
    output_str8 = Signal(str)
    force = Signal(str)
    dis_update = Signal(QPixmap)
    def setupUi(self, Main):
        if not Main.objectName():
            Main.setObjectName(u"Main")
        Main.resize(1920, 1100)
        Main.setStyleSheet(u"QTabBar::tab{\n"
"	background-color: rgb(0, 175, 255);\n"
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
        self.centralwidget.setStyleSheet(u"background:rgb(0, 175, 255);")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1920, 1178))
        self.tabWidget.setStyleSheet(u"QTabWidget::pane{border-width:0px;\n"
"border-style: outset;background-color: rgb(255, 255, 255);\n"
"}\n"
"QTabBar::tab{border-bottom-color: #C2C7CB;\n"
"             border-top-left-radius: 0px;\n"
"             border-top-right-radius: 0px;\n"
"             max-width: 100px; min-width:100px; \n"
"			   min-height:60px;\n"
"             font:20px \"Ubuntu\";;\n"
"             padding: 0px 20px 0px 20px;\n"
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
        self.groupBox = QGroupBox(self.tab1)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 20, 381, 611))
        font1 = QFont()
        font1.setPointSize(20)
        self.groupBox.setFont(font1)
        self.btn1 = QPushButton(self.groupBox)
        self.btn1.setObjectName(u"btn1")
        self.btn1.setGeometry(QRect(10, 50, 361, 60))
        font2 = QFont()
        font2.setPointSize(16)
        self.btn1.setFont(font2)
        self.btn2 = QPushButton(self.groupBox)
        self.btn2.setObjectName(u"btn2")
        self.btn2.setGeometry(QRect(10, 120, 361, 60))
        self.btn2.setFont(font2)
        self.btn3 = QPushButton(self.groupBox)
        self.btn3.setObjectName(u"btn3")
        self.btn3.setGeometry(QRect(10, 190, 361, 60))
        self.btn3.setFont(font2)
        self.btn4 = QPushButton(self.groupBox)
        self.btn4.setObjectName(u"btn4")
        self.btn4.setGeometry(QRect(10, 260, 361, 60))
        self.btn4.setFont(font2)
        self.btn5 = QPushButton(self.groupBox)
        self.btn5.setObjectName(u"btn5")
        self.btn5.setGeometry(QRect(10, 330, 361, 60))
        self.btn5.setFont(font2)
        self.btn6 = QPushButton(self.groupBox)
        self.btn6.setObjectName(u"btn6")
        self.btn6.setGeometry(QRect(10, 400, 361, 60))
        self.btn6.setFont(font2)
        self.btn7 = QPushButton(self.groupBox)
        self.btn7.setObjectName(u"btn7")
        self.btn7.setGeometry(QRect(10, 470, 361, 60))
        self.btn7.setFont(font2)
        self.btn8 = QPushButton(self.groupBox)
        self.btn8.setObjectName(u"btn8")
        self.btn8.setGeometry(QRect(10, 540, 361, 60))
        self.btn8.setFont(font2)
        self.groupBox_2 = QGroupBox(self.tab1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(30, 640, 381, 141))
        self.groupBox_2.setFont(font1)
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(60, 50, 131, 31))
        self.label_3.setFont(font2)
        self.NDisplay = QLabel(self.groupBox_2)
        self.NDisplay.setObjectName(u"NDisplay")
        self.NDisplay.setGeometry(QRect(190, 50, 131, 31))
        self.NDisplay.setFont(font2)
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(80, 90, 101, 31))
        self.label_5.setFont(font2)
        self.NWarning = QLabel(self.groupBox_2)
        self.NWarning.setObjectName(u"NWarning")
        self.NWarning.setGeometry(QRect(190, 90, 35, 35))
        self.NWarning.setStyleSheet(u"background-color: rgb(0, 255, 0);\n"
"border-radius: 17px;\n"
"")
        self.groupBox_3 = QGroupBox(self.tab1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(30, 790, 381, 201))
        self.groupBox_3.setFont(font1)
        self.cvSwitch = QPushButton(self.groupBox_3)
        self.cvSwitch.setObjectName(u"cvSwitch")
        self.cvSwitch.setGeometry(QRect(140, 50, 231, 51))
        self.cvSwitch.setFont(font2)
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(20, 60, 101, 31))
        self.label_11.setFont(font2)
        self.groupBox_4 = QGroupBox(self.tab1)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(440, 20, 1461, 971))
        self.groupBox_4.setFont(font1)
        self.label_12 = AIRSDisplay(self.groupBox_4)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 50, 1441, 911))
        self.label_12.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QWidget()
        self.tab2.setObjectName(u"tab2")
        font3 = QFont()
        font3.setFamily(u"Ubuntu")
        font3.setPointSize(20)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setWeight(50)
        self.tab2.setFont(font3)
        self.tab2.setStyleSheet(u"background-color: rgb(244, 244, 244);\n"
"font: \"Ubuntu\";")
        self.content1 = QTextEdit(self.tab2)
        self.content1.setObjectName(u"content1")
        self.content1.setGeometry(QRect(10, 50, 451, 451))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setWeight(50)
        self.content1.setFont(font4)
        self.content1.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:rgb(0, 255, 0);")
        self.label = QLabel(self.tab2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 321, 31))
        self.label.setFont(font3)
        self.label.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_2 = QLabel(self.tab2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(490, 10, 311, 31))
        font5 = QFont()
        font5.setPointSize(20)
        font5.setBold(False)
        font5.setItalic(False)
        font5.setWeight(50)
        self.label_2.setFont(font5)
        self.label_2.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.content2 = QTextEdit(self.tab2)
        self.content2.setObjectName(u"content2")
        self.content2.setGeometry(QRect(490, 50, 451, 451))
        self.content2.setFont(font4)
        self.content2.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:rgb(0, 255, 0);")
        self.content3 = QTextEdit(self.tab2)
        self.content3.setObjectName(u"content3")
        self.content3.setGeometry(QRect(970, 50, 451, 451))
        self.content3.setFont(font4)
        self.content3.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:rgb(0, 255, 0);")
        self.content4 = QTextEdit(self.tab2)
        self.content4.setObjectName(u"content4")
        self.content4.setGeometry(QRect(1450, 50, 451, 451))
        self.content4.setFont(font4)
        self.content4.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:rgb(0, 255, 0);")
        self.label_13 = QLabel(self.tab2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(970, 10, 311, 31))
        self.label_13.setFont(font5)
        self.label_13.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_14 = QLabel(self.tab2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(1450, 10, 311, 31))
        self.label_14.setFont(font5)
        self.label_14.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.content5 = QTextEdit(self.tab2)
        self.content5.setObjectName(u"content5")
        self.content5.setGeometry(QRect(10, 550, 451, 451))
        font6 = QFont()
        font6.setFamily(u"Ubuntu")
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        font6.setWeight(50)
        self.content5.setFont(font6)
        self.content5.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:rgb(0, 255, 0);")
        self.label_15 = QLabel(self.tab2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(10, 510, 371, 31))
        self.label_15.setFont(font3)
        self.label_15.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.content6 = QTextEdit(self.tab2)
        self.content6.setObjectName(u"content6")
        self.content6.setGeometry(QRect(490, 550, 451, 451))
        self.content6.setFont(font6)
        self.content6.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:rgb(0, 255, 0);")
        self.label_16 = QLabel(self.tab2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(490, 510, 381, 31))
        self.label_16.setFont(font3)
        self.label_16.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.content7 = QTextEdit(self.tab2)
        self.content7.setObjectName(u"content7")
        self.content7.setGeometry(QRect(970, 550, 451, 451))
        self.content7.setFont(font6)
        self.content7.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:rgb(0, 255, 0);")
        self.content8 = QTextEdit(self.tab2)
        self.content8.setObjectName(u"content8")
        self.content8.setGeometry(QRect(1450, 550, 451, 451))
        self.content8.setFont(font6)
        self.content8.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:rgb(0, 255, 0);")
        self.label_17 = QLabel(self.tab2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(970, 510, 321, 31))
        self.label_17.setFont(font3)
        self.label_17.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_18 = QLabel(self.tab2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(1450, 510, 321, 31))
        self.label_18.setFont(font3)
        self.label_18.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.widget = QWidget(self.tab2)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1921, 1021))
        self.widget.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.tabWidget.addTab(self.tab2, "")
        self.widget.raise_()
        self.content1.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.content2.raise_()
        self.content3.raise_()
        self.content4.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.content5.raise_()
        self.label_15.raise_()
        self.content6.raise_()
        self.label_16.raise_()
        self.content7.raise_()
        self.content8.raise_()
        self.label_17.raise_()
        self.label_18.raise_()
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"background-color: rgb(244, 244, 244);\n"
"font: \"Ubuntu\";")
        self.groupBox_5 = QGroupBox(self.tab)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(20, 20, 731, 611))
        self.groupBox_5.setFont(font3)
        self.label_19 = QLabel(self.groupBox_5)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(30, 60, 31, 31))
        font7 = QFont()
        font7.setPointSize(16)
        font7.setBold(False)
        font7.setItalic(False)
        font7.setWeight(50)
        self.label_19.setFont(font7)
        self.cmd1 = QLineEdit(self.groupBox_5)
        self.cmd1.setObjectName(u"cmd1")
        self.cmd1.setGeometry(QRect(70, 60, 641, 41))
        self.label_20 = QLabel(self.groupBox_5)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(30, 120, 31, 31))
        self.label_20.setFont(font7)
        self.cmd2 = QLineEdit(self.groupBox_5)
        self.cmd2.setObjectName(u"cmd2")
        self.cmd2.setGeometry(QRect(70, 120, 641, 41))
        self.cmd3 = QLineEdit(self.groupBox_5)
        self.cmd3.setObjectName(u"cmd3")
        self.cmd3.setGeometry(QRect(70, 180, 641, 41))
        self.label_21 = QLabel(self.groupBox_5)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(30, 180, 31, 31))
        self.label_21.setFont(font7)
        self.cmd4 = QLineEdit(self.groupBox_5)
        self.cmd4.setObjectName(u"cmd4")
        self.cmd4.setGeometry(QRect(70, 240, 641, 41))
        self.label_22 = QLabel(self.groupBox_5)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(30, 240, 31, 31))
        self.label_22.setFont(font7)
        self.label_23 = QLabel(self.groupBox_5)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(30, 300, 31, 31))
        self.label_23.setFont(font7)
        self.cmd5 = QLineEdit(self.groupBox_5)
        self.cmd5.setObjectName(u"cmd5")
        self.cmd5.setGeometry(QRect(70, 300, 641, 41))
        self.label_24 = QLabel(self.groupBox_5)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(30, 360, 31, 31))
        self.label_24.setFont(font7)
        self.cmd6 = QLineEdit(self.groupBox_5)
        self.cmd6.setObjectName(u"cmd6")
        self.cmd6.setGeometry(QRect(70, 360, 641, 41))
        self.label_25 = QLabel(self.groupBox_5)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(30, 420, 31, 31))
        self.label_25.setFont(font7)
        self.cmd7 = QLineEdit(self.groupBox_5)
        self.cmd7.setObjectName(u"cmd7")
        self.cmd7.setGeometry(QRect(70, 420, 641, 41))
        self.label_26 = QLabel(self.groupBox_5)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(30, 480, 31, 31))
        self.label_26.setFont(font7)
        self.cmd8 = QLineEdit(self.groupBox_5)
        self.cmd8.setObjectName(u"cmd8")
        self.cmd8.setGeometry(QRect(70, 480, 641, 41))
        self.save_btn = QPushButton(self.groupBox_5)
        self.save_btn.setObjectName(u"save_btn")
        self.save_btn.setGeometry(QRect(30, 540, 681, 61))
        self.save_btn.setFont(font5)
        self.save_btn.setStyleSheet(u"background-color: rgb(78, 154, 6);\n"
"color: rgb(255, 255, 255);")
        self.groupBox_6 = QGroupBox(self.tab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(20, 650, 741, 321))
        self.groupBox_6.setFont(font5)
        self.shutdown_btn = QPushButton(self.groupBox_6)
        self.shutdown_btn.setObjectName(u"shutdown_btn")
        self.shutdown_btn.setGeometry(QRect(160, 140, 381, 61))
        self.shutdown_btn.setFont(font5)
        self.shutdown_btn.setStyleSheet(u"background-color: rgb(204, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.tabWidget.addTab(self.tab, "")
        Main.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(Main)
        self.statusBar.setObjectName(u"statusBar")
        Main.setStatusBar(self.statusBar)
        self.btn1.clicked.connect(self.start_thread1)
        self.btn2.clicked.connect(self.start_thread2)
        self.btn3.clicked.connect(self.start_thread3)
        self.btn4.clicked.connect(self.start_thread4)
        self.btn5.clicked.connect(self.start_thread5)
        self.btn6.clicked.connect(self.start_thread6)
        self.btn7.clicked.connect(self.start_thread7)
        self.btn8.clicked.connect(self.start_thread8)
        self.output_str1.connect(self.update1)
        self.output_str2.connect(self.update2)
        self.output_str3.connect(self.update3)
        self.output_str4.connect(self.update4)
        self.output_str5.connect(self.update5)
        self.output_str6.connect(self.update6)
        self.output_str7.connect(self.update7)
        self.output_str8.connect(self.update8)
        self.dis_update.connect(self.camera_view)
        self.force.connect(self.update_force)
        self.retranslateUi(Main)
        self.label_12.setMouseTracking(True)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Main)


    def test(self,event:QMouseEvent):
        print(event.pos())

    def start_thread1(self):
        t1 = th.Thread(target=self.output1)
        t1.start()

    def start_thread2(self):
        t2 = th.Thread(target=self.output2)
        t2.start()

    def start_thread3(self):
        t3 = th.Thread(target=self.output3)
        t3.start()

    def start_thread4(self):
        t4 = th.Thread(target=self.output4)
        t4.start()

    def start_thread5(self):
        t5 = th.Thread(target=self.output5)
        t5.start()

    def start_thread6(self):
        t6 = th.Thread(target=self.output6)
        t6.start()

    def start_thread7(self):
        t7 = th.Thread(target=self.output7)
        t7.start()

    def start_thread8(self):
        t8 = th.Thread(target=self.output8)
        t8.start()


    def output1(self):
        command = self.cmd1.text()
        for path in self.run(command):
            self.output_str1.emit(str(path) + '\n')

    def output2(self):
        command = self.cmd2.text()
        for path in self.run(command):
            self.output_str2.emit(str(path) + '\n')

    def output3(self):
        command = self.cmd3.text()
        for path in self.run(command):
            self.output_str3.emit(str(path) + '\n')

    def output4(self):
        command = self.cmd4.text()
        for path in self.run(command):
            self.output_str4.emit(str(path) + '\n')

    def output5(self):
        command = self.cmd5.text()
        for path in self.run(command):
            self.output_str5.emit(str(path) + '\n')

    def output6(self):
        command = self.cmd6.text()
        for path in self.run(command):
            self.output_str6.emit(str(path) + '\n')

    def output7(self):
        command = self.cmd7.text()
        for path in self.run(command):
            self.output_str7.emit(str(path) + '\n')

    def output8(self):
        command = self.cmd8.text()
        for path in self.run(command):
            self.output_str8.emit(str(path) + '\n')


    def run(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        while True:
            line = process.stdout.readline().rstrip()
            if not line:
                break
            yield line


    @Slot(str)
    def update1(self, str):
        self.content1.insertPlainText(str)

    @Slot(str)
    def update2(self, str):
        self.content2.insertPlainText(str)

    @Slot(str)
    def update3(self, str):
        self.content3.insertPlainText(str)

    @Slot(str)
    def update4(self, str):
        self.content4.insertPlainText(str)

    @Slot(str)
    def update5(self, str):
        self.content5.insertPlainText(str)

    @Slot(str)
    def update6(self, str):
        self.content6.insertPlainText(str)

    @Slot(str)
    def update7(self, str):
        self.content7.insertPlainText(str)

    @Slot(str)
    def update8(self, str):
        self.content8.insertPlainText(str)

    def camera_view(self, c):
        self.label_12.setPixmap(c)
        self.label_12.setScaledContents(True)

    def open_camera(self):
        t = th.Thread(target=self.open_realsense)
        t.start()

    @Slot(str)
    def update_force(self, force):
        if float(force) > 10:
            self.NWarning.setStyleSheet("background-color:red;border-radius:17px;")
        else:
            self.NWarning.setStyleSheet("background-color:rgb(0, 255, 0);border-radius:17px;")
        self.NDisplay.setText(force)

    def force_process(self):
        t1 = th.Thread(target=self.run_roscore)
        t1.start()
        time.sleep(1)
        t2 = th.Thread(target=self.force_out)
        t2.start()

    def force_out(self):
        for path in self.run_force():
            try:
                s = str(path, encoding="utf8")
                js = json.loads(s)
                self.force.emit(js['force'])
            except:
                continue

    def run_roscore(self):
        process = subprocess.Popen(cmd_ros_core, stdout=subprocess.PIPE, shell=True)

    def run_force(self):
        process = subprocess.Popen(cmd_force, stdout=subprocess.PIPE, shell=True)
        while True:
            line = process.stdout.readline().rstrip()
            if not line:
                break
            yield line

    def open_realsense(self):
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, FPS)
        config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, FPS)

        profile = pipeline.start(config)
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        # Color Intrinsics
        intr = color_frame.profile.as_video_stream_profile().intrinsics

        align_to = rs.stream.color
        align = rs.align(align_to)
        while True:
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)

            aligned_depth_frame = aligned_frames.get_depth_frame()
            depth_intr = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
            self.label_12.setting(aligned_depth_frame, depth_intr)
            color_frame = aligned_frames.get_color_frame()
            if not aligned_depth_frame or not color_frame:
                continue
            c = np.asanyarray(color_frame.get_data())
            qimage = QImage(c, 1280, 720, QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(qimage)
            self.dis_update.emit(pixmap)
            time.sleep(DELAY)
        pipeline.stop()

    def retranslateUi(self, Main):
        Main.setWindowTitle(QCoreApplication.translate("Main", u"Avatar", None))
        self.groupBox.setTitle(QCoreApplication.translate("Main", u"\u673a\u68b0\u81c2\u63a7\u5236", None))
        self.btn1.setText(QCoreApplication.translate("Main", u"1. Connect the ur5 step 1", None))
        self.btn2.setText(QCoreApplication.translate("Main", u"2. Connect the ur5 step 2", None))
        self.btn3.setText(QCoreApplication.translate("Main", u"3. Run touch node step 1", None))
        self.btn4.setText(QCoreApplication.translate("Main", u"4. Run touch node step 2", None))
        self.btn5.setText(QCoreApplication.translate("Main", u"5. Run finger serial program", None))
        self.btn6.setText(QCoreApplication.translate("Main", u"6. Run the control program", None))
        self.btn7.setText(QCoreApplication.translate("Main", u"7. XYZ separation", None))
        self.btn8.setText(QCoreApplication.translate("Main", u"Reset orientation", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Main", u"\u529b\u611f\u77e5", None))
        self.label_3.setText(QCoreApplication.translate("Main", u"\u529b\u611f\u77e5\u8bfb\u6570\uff1a", None))
        self.NDisplay.setText(QCoreApplication.translate("Main", u"0 ", None))
        self.label_5.setText(QCoreApplication.translate("Main", u"\u53d7\u529b\u8b66\u544a\uff1a", None))
        self.NWarning.setText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("Main", u"\u53e3\u8154\u5206\u5272", None))
        self.cvSwitch.setText(QCoreApplication.translate("Main", u"\u5173\u95ed", None))
        self.label_11.setText(QCoreApplication.translate("Main", u"\u663e\u793amask\uff1a", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Main", u"\u6444\u50cf\u5934", None))
        self.label_12.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QCoreApplication.translate("Main", u"\u63a7\u5236", None))
        self.label.setText(QCoreApplication.translate("Main", u"1.Connect the ur5 step 1", None))
        self.label_2.setText(QCoreApplication.translate("Main", u"2.Connect the ur5 step 2", None))
        self.label_13.setText(QCoreApplication.translate("Main", u"3. Run touch node step 1", None))
        self.label_14.setText(QCoreApplication.translate("Main", u"4. Run touch node step 2", None))
        self.label_15.setText(QCoreApplication.translate("Main", u"5. Run finger serial program", None))
        self.label_16.setText(QCoreApplication.translate("Main", u"6. Run the control program", None))
        self.label_17.setText(QCoreApplication.translate("Main", u"7. XYZ separation", None))
        self.label_18.setText(QCoreApplication.translate("Main", u"Reset orientation", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QCoreApplication.translate("Main", u"\u8c03\u8bd5", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Main", u"\u673a\u68b0\u81c2\u6307\u4ee4", None))
        self.label_19.setText(QCoreApplication.translate("Main", u"1\uff1a", None))
        self.cmd1.setText(QCoreApplication.translate("Main", u"roslaunch ur_robot_driver ur5_bringup.launch robot_ip:=192.168.103.115", None))
        self.label_20.setText(QCoreApplication.translate("Main", u"2\uff1a", None))
        self.cmd2.setText(QCoreApplication.translate("Main", u"roslaunch ur5_moveit_config ur5_moveit_planning_execution.launch", None))
        self.cmd3.setText(QCoreApplication.translate("Main", u"echo '123qwe' | sudo -S chmod 777 /dev/ttyACM0", None))
        self.label_21.setText(QCoreApplication.translate("Main", u"3\uff1a", None))
        self.cmd4.setText(QCoreApplication.translate("Main", u"roslaunch teleoperation run_touch.launch", None))
        self.label_22.setText(QCoreApplication.translate("Main", u"4\uff1a", None))
        self.label_23.setText(QCoreApplication.translate("Main", u"5\uff1a", None))
        self.cmd5.setText(QCoreApplication.translate("Main", u"roslaunch teleoperation run_serial_control.launch", None))
        self.label_24.setText(QCoreApplication.translate("Main", u"6\uff1a", None))
        self.cmd6.setText(QCoreApplication.translate("Main", u"rosrun teleoperation touch_ctl", None))
        self.label_25.setText(QCoreApplication.translate("Main", u"7\uff1a", None))
        self.cmd7.setText(QCoreApplication.translate("Main", u"python ~/lee/ThroatSwap/src/teleoperation/src/one_xyz_command.py", None))
        self.label_26.setText(QCoreApplication.translate("Main", u"8\uff1a", None))
        self.cmd8.setText(QCoreApplication.translate("Main", u"python ~/lee/ThroatSwap/src/teleoperation/src/orientation_reset.py", None))
        self.save_btn.setText(QCoreApplication.translate("Main", u"\u4fdd\u5b58", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Main", u"\u7cfb\u7edf\u64cd\u4f5c", None))
        self.shutdown_btn.setText(QCoreApplication.translate("Main", u"\u9000\u51fa", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Main", u"\u8bbe\u7f6e", None))
    # retranslateUi

