#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem, QMenu
from PyQt5 import QtCore, QtWidgets
from qqwry import QQwry
from testConnShell import dns_resolver
import mainWindowFront, addShell, genShellPhp

class mainCode(QMainWindow, mainWindowFront.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        mainWindowFront.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.tab_index = 0
        self.row_num = -1
        self.genShellPhp.triggered.connect(self.gen_shell_php)
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)

    def gen_shell_php(self):
        dg = QDialog()
        shellPhp = genShellPhp.Ui_Dialog()
        shellPhp.setupUi(dg)
        dg.exec()

    def add_shell(self):
        dg = addShell.Ui_dialog()
        dg.signal_url_password.connect(self.deal_emit_slot)
        dg.exec()

    #处理窗口关闭前传过来的URL
    def deal_emit_slot(self, data):
        url = data[0]
        password = data[1]
        memo = data[2]
        if self.row_num == -1:
            self.index = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(self.index + 1)
        else:
            self.index = self.row_num

        #添加URL
        newItem = QTableWidgetItem(url)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(self.index, 0, newItem)

        #添加IP
        ip= dns_resolver(url)
        newItem = QTableWidgetItem(ip)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(self.index, 1, newItem)

        #添加密码
        newItem = QTableWidgetItem(password)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(self.index, 2, newItem)

        #添加物理地址
        q = QQwry()
        q.load_file('D:\Project\Graduation Design\qqwry.dat')
        try:
            res = q.lookup(ip)
            addr = res[0] + ' ' + res[1]
        except:
            addr = ''
        newItem = QTableWidgetItem(addr)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(self.index, 3, newItem)

        #添加备注
        newItem = QTableWidgetItem(memo)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(self.index, 4, newItem)

    def generateMenu(self, pos):
        menu = QMenu()
        #计算当前行数
        self.row_num = -1
        for i in self.tableWidget.selectionModel().selection().indexes():
            self.row_num = i.row()

        if self.row_num != -1:
            item1 = menu.addAction('打开')
            item2 = menu.addAction('编辑')
            item3 = menu.addAction('删除')
            action = menu.exec_(self.tableWidget.mapToGlobal(pos))

            if action == item1:
                self.tab_index += 1
                self.new_tab = QtWidgets.QWidget()
                self.new_tab.setObjectName('tab_'+str(self.tab_index))
                self.tabWidget.addTab(self.new_tab, self.tableWidget.item(self.row_num, 1).text())
                self.xbutton = QtWidgets.QPushButton("x")
                self.xbutton.setFixedSize(16, 16)
                self.xbutton.clicked.connect(lambda: self.del_tab(self.tab_index))
                self.tabWidget.tabBar().setTabButton(self.tab_index, self.tabWidget.tabBar().RightSide, self.xbutton)
                self.tabWidget.setCurrentIndex(self.tab_index)

            elif action == item2:
                dg = addShell.Ui_dialog()
                dg.pushButton.setText("保存")

                dg.lineEdit.setText(self.tableWidget.item(self.row_num, 0).text())
                dg.lineEdit_2.setText(self.tableWidget.item(self.row_num, 2).text())
                dg.lineEdit_3.setText(self.tableWidget.item(self.row_num, 4).text())
                dg.signal_url_password.connect(self.deal_emit_slot)

                dg.exec()
            else:
                self.tableWidget.removeRow(self.row_num)
        else:
            item = menu.addAction('新建')
            action = menu.exec_(self.tableWidget.mapToGlobal(pos))
            if action == item:
                self.add_shell()

    def del_tab(self, index):
        self.tabWidget.removeTab(index)
        self.tab_index -= 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mc = mainCode()
    mc.show()
    sys.exit(app.exec_())