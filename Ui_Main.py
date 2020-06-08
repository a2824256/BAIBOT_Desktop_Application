# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import threading as th
import multiprocessing as mp
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, Signal, Slot)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2 import QtCore
from PySide2.QtWidgets import *
import os


class Ui_Main(QObject):
    output_str = QtCore.Signal(str)

    def setupUi(self, Main):
        if not Main.objectName():
            Main.setObjectName(u"Main")
        Main.resize(800, 600)
        Main.setStyleSheet(u"QTabBar::tab{\n"
"	background-color: rgb(0, 175, 255);\n"
"	color:white;\n"
"}\n"
"QTabWidget::tab-bar{\n"
"        alignment:left;\n"
"}\n"
"QTabBar::tab:selected{\n"
"	border-color: white;\n"
"	background: white;\n"
"	color:black\n"
"}")
        self.centralwidget = QWidget(Main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background:rgb(0, 175, 255);")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 800, 581))
        self.tabWidget.setStyleSheet(u"QTabWidget::pane{border-width:0px;\n"
"border-style: outset;background-color: rgb(255, 255, 255);\n"
"}\n"
"QTabBar::tab{border-bottom-color: #C2C7CB;\n"
"             border-top-left-radius: 0px;\n"
"             border-top-right-radius: 0px;\n"
"             max-width: 100px; min-width:100px; min-height:40px;\n"
"             font:20px Times New Roman;\n"
"             padding: 0px;\n"
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
        self.pushButton = QPushButton(self.tab1)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 10, 141, 51))
        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QWidget()
        self.tab2.setObjectName(u"tab2")
        self.tab2.setStyleSheet(u"background-color: rgb(244, 244, 244);")
        self.textEdit = QTextEdit(self.tab2)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 10, 331, 411))
        self.textEdit.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:white;")
        self.tabWidget.addTab(self.tab2, "")
        Main.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(Main)
        self.statusBar.setObjectName(u"statusBar")
        Main.setStatusBar(self.statusBar)
        self.pushButton.clicked.connect(self.start_thread)
        self.output_str.connect(self.update)
        # QObject.connect(self.output_str,self.update)
        self.retranslateUi(Main)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Main)

    def start_thread(self):
        t1 = th.Thread(target=self.output)
        print("start")
        t1.start()

    def output(self):
        val = os.popen("python /Users/alexleung/Documents/Avatar/test.py")
        for temp in val.readlines():
            self.output_str.emit(temp)

    @Slot(str)
    def update(self,str):
        print(str)
        self.textEdit.insertPlainText(str)


    # setupUi

    def retranslateUi(self, Main):
        Main.setWindowTitle(QCoreApplication.translate("Main", u"Avatar", None))
        self.pushButton.setText(QCoreApplication.translate("Main", u"\u6267\u884c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QCoreApplication.translate("Main", u"\u63a7\u5236", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QCoreApplication.translate("Main", u"\u8c03\u8bd5", None))
    # retranslateUi

