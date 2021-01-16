#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem, QMenu
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from qqwry import QQwry
from testConnShell import TestConn, scanDir, dns_resolver, formatFileSize

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
                self.displayShell()

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

    def displayShell(self):
        try:
            self.url = self.tableWidget.item(self.row_num, 0).text()
            self.password = self.tableWidget.item(self.row_num, 2).text()
            r = TestConn(self.url, self.password)
            self.data = r.split('\n')
            QtWidgets.QMessageBox.about(self, "连接成功！", r)

            self.tab_index += 1
            self.new_tab = QtWidgets.QWidget()
            self.new_tab.setObjectName('tab_' + str(self.tab_index))

            self.gridLayout_2 = QtWidgets.QGridLayout(self.new_tab)
            self.gridLayout_2.setObjectName("gridLayout_2")
            self.gridLayout = QtWidgets.QGridLayout()
            self.gridLayout.setObjectName("gridLayout")
            self.tableWidget_2 = QtWidgets.QTableWidget(self.new_tab)
            self.tableWidget_2.setObjectName("tableWidget_2")
            self.tableWidget_2.setColumnCount(4)
            self.tableWidget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

            item = QtWidgets.QTableWidgetItem()
            item.setText("名称")
            self.tableWidget_2.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText("日期")
            self.tableWidget_2.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText("大小")
            self.tableWidget_2.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText("属性")
            self.tableWidget_2.setHorizontalHeaderItem(3, item)

            # 更新tableWidget_2
            files = scanDir(self.url, self.password, self.data[0] + '/').split('\n')
            files = list(filter(None, files))
            self.updataTable(files)



            self.gridLayout.addWidget(self.tableWidget_2, 1, 1, 1, 1)
            self.treeWidget = QtWidgets.QTreeWidget(self.new_tab)
            self.treeWidget.setObjectName("treeWidget")

            # tree信息初始化
            # 根节点
            self.root = QtWidgets.QTreeWidgetItem(self.treeWidget)
            self.root.setText(0, self.data[1])
            self.root.setIcon(0, QIcon('D:/Project/Graduation Design/icons/default_folder.svg'))

            # 子节点
            folders = self.data[0][1:].split('/')
            itemStack = [self.root]
            for i in range(len(folders)):
                item = QtWidgets.QTreeWidgetItem(itemStack.pop())
                item.setText(0, folders[i])
                item.setIcon(0, QIcon('D:/Project/Graduation Design/icons/default_folder.svg'))
                itemStack.append(item)

            #更新节点
            self.treeWidget.clicked.connect(self.updateTree)

            self.treeWidget.header().setVisible(False)
            self.treeWidget.header().setHighlightSections(False)
            self.treeWidget.expandAll()
            self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 1)
            self.label = QtWidgets.QLabel(self.new_tab)
            self.label.setMaximumSize(QtCore.QSize(91, 61))
            self.label.setTextFormat(QtCore.Qt.RichText)
            self.label.setScaledContents(False)
            self.label.setObjectName("label")
            self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
            self.label_2 = QtWidgets.QLabel(self.new_tab)
            self.label_2.setMaximumSize(QtCore.QSize(91, 61))
            self.label_2.setTextFormat(QtCore.Qt.RichText)
            self.label_2.setScaledContents(False)
            self.label_2.setObjectName("label_2")
            self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
            self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
            self.label.setText(
                "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">目录列表</span></p></body></html>")
            self.label_2.setText(
                "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">文件列表</span></p></body></html>")

            self.tabWidget.addTab(self.new_tab, self.tableWidget.item(self.row_num, 1).text())
            self.horizontalLayout.addWidget(self.tabWidget)
            self.xbutton = QtWidgets.QPushButton("x")
            self.xbutton.setFixedSize(16, 16)
            self.xbutton.clicked.connect(lambda: self.del_tab(self.tab_index))
            self.tabWidget.tabBar().setTabButton(self.tab_index, self.tabWidget.tabBar().RightSide, self.xbutton)
            self.tabWidget.setCurrentIndex(self.tab_index)
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "连接失败！", str(Exception(e)))

    def updataTable(self, files):
        for i in range(len(files) - 1, -1, -1):
            if (files[i].split('\t'))[0].startswith('./') or (files[i].split('\t'))[0].startswith('../'):
                files.remove(files[i])
        self.tableWidget_2.setRowCount(len(files))
        for i in range(len(files)):
            for j in range(4):
                if j == 2:
                    newItem = QTableWidgetItem(formatFileSize(int(files[i].split('\t')[j]), 2))
                else:
                    newItem = QTableWidgetItem(files[i].split('\t')[j])
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget_2.setItem(i, j, newItem)

    def updateTree(self):
        item = self.treeWidget.currentItem()
        if item.text(0) == self.data[1]:
            dir = self.data[1]
            if self.data[1] != '/':
                dir += '/'
        else:
            dir = '/'
            dir = '/' + item.text(0) + dir
            while item.parent().text(0) != self.data[1]:
                item = item.parent()
                dir = '/' + item.text(0) + dir
            if self.data[1] != '/':
                dir = self.data[1] + dir
        #print(dir)

        try:
            # 更新文件列表
            files = scanDir(self.url, self.password, dir).split('\n')
            files = list(filter(None, files))
            self.updataTable(files)

            # 更新目录列表
            # print(files)

            item = self.treeWidget.currentItem()
            childL = []
            childCount = item.childCount()
            for i in range(childCount):
                childL.append(item.child(i).text(0))

            # print(childL)
            fname = []
            for f in files:
                fs = f.split('\t')[0]
                if fs.endswith('/'):
                    fname.append(fs[:-1])
                    if fs[:-1] not in childL:
                        item = QtWidgets.QTreeWidgetItem(self.treeWidget.currentItem())
                        item.setText(0, fs[:-1])
                        item.setIcon(0, QIcon('D:/Project/Graduation Design/icons/default_folder.svg'))

            item = self.treeWidget.currentItem()
            for i in range(childCount - 1, -1, -1):
                if item.child(i).text(0) not in fname:
                    item.removeChild(item.child(i))
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "连接失败！", str(Exception(e)))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mc = mainCode()
    mc.show()
    sys.exit(app.exec_())