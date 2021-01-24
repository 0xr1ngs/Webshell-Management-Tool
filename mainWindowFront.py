# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindowFront.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 720)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/knife_easyicon.net.svg'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTipDuration(0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.shellTableWidget = QtWidgets.QTableWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shellTableWidget.sizePolicy().hasHeightForWidth())
        self.shellTableWidget.setSizePolicy(sizePolicy)
        self.shellTableWidget.setMinimumSize(QtCore.QSize(256, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.shellTableWidget.setFont(font)
        self.shellTableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shellTableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.shellTableWidget.setAutoFillBackground(False)
        self.shellTableWidget.setAutoScrollMargin(15)
        self.shellTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.shellTableWidget.setRowCount(0)
        self.shellTableWidget.setObjectName("tableWidget")
        self.shellTableWidget.setColumnCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.shellTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.shellTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.shellTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.shellTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.shellTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.shellTableWidget.setHorizontalHeaderItem(5, item)
        self.shellTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.shellTableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.shellTableWidget)
        self.tabWidget.addTab(self.tab, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1012, 23))
        self.menubar.setObjectName("menubar")
        self.menu_shell = QtWidgets.QMenu(self.menubar)
        self.menu_shell.setObjectName("menu_shell")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.genShellPhp = QtWidgets.QAction(MainWindow)
        self.genShellPhp.setObjectName("genShellPhp")
        self.action_shell = QtWidgets.QAction(MainWindow)
        self.action_shell.setObjectName("action_shell")
        self.menu_shell.addAction(self.genShellPhp)
        self.menu.addAction(self.action_shell)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_shell.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Shell管理工具"))
        item = self.shellTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "URL链接"))
        item = self.shellTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "IP地址"))
        item = self.shellTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "密码"))
        item = self.shellTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "物理位置"))
        item = self.shellTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "网站备注"))
        item = self.shellTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "修改时间"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "主页面"))
        self.menu_shell.setTitle(_translate("MainWindow", "生成shell"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.genShellPhp.setText(_translate("MainWindow", "php一句话木马"))
        self.action_shell.setText(_translate("MainWindow", "添加shell"))
