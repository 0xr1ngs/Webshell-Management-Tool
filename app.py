#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem, QMenu
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from qqwry import QQwry
from functools import partial
from testConnShell import TestConn, scanDir, dns_resolver, formatFileSize, downloadFile
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
        self.tableWidget.doubleClicked.connect(self.shellTableDoubleClicked)

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
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

    def shellTableDoubleClicked(self):
        #计算当前行数
        self.row_num = -1
        for i in self.tableWidget.selectionModel().selection().indexes():
            self.row_num = i.row()
        self.displayShell()


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
            item4 = menu.addAction('查看')
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
            elif action == item3:
                self.tableWidget.removeRow(self.row_num)
            else:
                self.displayWeb(self.tableWidget.item(self.row_num, 0).text())
        else:
            item = menu.addAction('新建')
            action = menu.exec_(self.tableWidget.mapToGlobal(pos))
            if action == item:
                self.add_shell()

    def displayWeb(self, url):
        self.tab_index += 1
        self.new_tab = QtWidgets.QWidget()
        self.new_tab.setObjectName('tab_' + str(self.tab_index))

        self.browser = QWebEngineView()
        self.browser.load(QtCore.QUrl(url))
        self.gridLayout = QtWidgets.QGridLayout(self.new_tab)
        self.gridLayout.addWidget(self.browser, 0, 0)
        self.tabWidget.addTab(self.new_tab, url)
        self.xbutton = QtWidgets.QPushButton("x")
        self.xbutton.setFixedSize(16, 16)
        self.xbutton.clicked.connect(lambda: self.del_tab(self.tab_index))
        self.tabWidget.tabBar().setTabButton(self.tab_index, self.tabWidget.tabBar().RightSide, self.xbutton)
        self.tabWidget.setCurrentIndex(self.tab_index)

    def del_tab(self, index):
        self.tabWidget.removeTab(index)
        self.tab_index -= 1

    def generateFileListMenu(self, data, pos):
        url = data[0]
        password = data[1]
        treeWidget = data[2]
        fileTableWidget = data[3]
        rdata = data[4]
        if treeWidget.currentItem() is None:
            item = data[5]
        else:
            item = treeWidget.currentItem()
        dir = self.parsePath(item, rdata)

        menu = QMenu()
        #计算当前行数
        self.row_num = -1
        for i in fileTableWidget.selectionModel().selection().indexes():
            self.row_num = i.row()

        if self.row_num != -1:
            item1 = menu.addAction('下载文件')
            item2 = menu.addAction('重命名')
            item3 = menu.addAction('删除文件')
            item4 = menu.addAction('更改权限')
            action = menu.exec_(fileTableWidget.mapToGlobal(pos))

            if action == item1:
                try:
                    filename = fileTableWidget.item(self.row_num, 0).text()
                    buffer = downloadFile(url, password, dir + filename)
                    filename = QtWidgets.QFileDialog.getSaveFileName(self, '保存路径', filename)
                    with open(filename[0], 'w') as f:
                        f.write(buffer)
                    QtWidgets.QMessageBox.about(self, "下载成功！", '文件已保存')
                except Exception as e:
                    QtWidgets.QMessageBox.about(self, "下载失败！", str(Exception(e)))
            elif action == item2:
                pass
            elif action == item3:
                pass
            else:
                pass
        else:
            item = menu.addAction('上传文件')
            action = menu.exec_(fileTableWidget.mapToGlobal(pos))
            if action == item:
                pass

    def displayShell(self):
        try:
            url = self.tableWidget.item(self.row_num, 0).text()
            password = self.tableWidget.item(self.row_num, 2).text()
            r = TestConn(url, password)
            rdata = r.split('\n')
            QtWidgets.QMessageBox.about(self, "连接成功！", r)

            self.tab_index += 1
            self.new_tab = QtWidgets.QWidget()
            self.new_tab.setObjectName('tab_' + str(self.tab_index))


            self.gridLayout = QtWidgets.QGridLayout(self.new_tab)
            self.gridLayout.setObjectName("gridLayout")
            fileTableWidget = QtWidgets.QTableWidget(self.new_tab)
            fileTableWidget.setObjectName("fileTableWidget")
            fileTableWidget.setColumnCount(4)
            fileTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            fileTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)



            item = QtWidgets.QTableWidgetItem()
            item.setText("名称")
            fileTableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText("日期")
            fileTableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText("大小")
            fileTableWidget.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText("属性")
            fileTableWidget.setHorizontalHeaderItem(3, item)

            # 更新fileTableWidget
            files = scanDir(url, password, rdata[0] + '/').split('\n')
            files = list(filter(None, files))
            self.updataTable(files, fileTableWidget)


            treeWidget = QtWidgets.QTreeWidget(self.new_tab)
            treeWidget.setObjectName("treeWidget")

            # tree信息初始化
            # 根节点
            self.root = QtWidgets.QTreeWidgetItem(treeWidget)
            self.root.setText(0, rdata[1])
            self.root.setIcon(0, QIcon('D:/Project/Graduation Design/icons/default_folder.svg'))

            # 子节点
            folders = rdata[0][1:].split('/')
            itemStack = [self.root]
            for i in range(len(folders)):
                item = QtWidgets.QTreeWidgetItem(itemStack.pop())
                item.setText(0, folders[i])
                item.setIcon(0, QIcon('D:/Project/Graduation Design/icons/default_folder.svg'))
                itemStack.append(item)

            #更新节点
            treeWidget.clicked.connect(lambda:self.updateTree([url, password, treeWidget, fileTableWidget, rdata]))

            treeWidget.header().setVisible(False)
            treeWidget.header().setHighlightSections(False)
            treeWidget.expandAll()

            self.label = QtWidgets.QLabel(self.new_tab)
            self.label.setMaximumSize(QtCore.QSize(91, 61))
            self.label.setTextFormat(QtCore.Qt.RichText)
            self.label.setScaledContents(False)
            self.label.setObjectName("label")

            self.label_2 = QtWidgets.QLabel(self.new_tab)
            self.label_2.setMaximumSize(QtCore.QSize(91, 61))
            self.label_2.setTextFormat(QtCore.Qt.RichText)
            self.label_2.setScaledContents(False)
            self.label_2.setObjectName("label_2")

            self.gridLayout.addWidget(self.label, 1, 0)
            self.gridLayout.addWidget(self.label_2, 1, 1)
            self.gridLayout.addWidget(treeWidget, 2, 0)
            self.gridLayout.addWidget(fileTableWidget, 2, 1)


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
            fileTableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            fileTableWidget.customContextMenuRequested.connect(partial(self.generateFileListMenu, [url, password, treeWidget,
                                                                                                   fileTableWidget, rdata, item]))
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "连接失败！", str(Exception(e)))

    def updataTable(self, files, fileTableWidget):
        for i in range(len(files) - 1, -1, -1):
            if (files[i].split('\t'))[0].startswith('./') or (files[i].split('\t'))[0].startswith('../'):
                files.remove(files[i])
        fileTableWidget.setRowCount(len(files))
        for i in range(len(files)):
            for j in range(4):
                if j == 2:
                    newItem = QTableWidgetItem(formatFileSize(int(files[i].split('\t')[j]), 2))
                else:
                    newItem = QTableWidgetItem(files[i].split('\t')[j])
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                fileTableWidget.setItem(i, j, newItem)
        fileTableWidget.sortItems(0, QtCore.Qt.AscendingOrder)

    def parsePath(self, item, rdata):
        if item.text(0) == rdata[1]:
            dir = rdata[1]
            if rdata[1] != '/':
                dir += '/'
        else:
            dir = '/'
            dir = '/' + item.text(0) + dir
            while item.parent().text(0) != rdata[1]:
                item = item.parent()
                dir = '/' + item.text(0) + dir
            if rdata[1] != '/':
                dir = rdata[1] + dir
        #print(dir)
        return dir

    def updateTree(self, data):
        url = data[0]
        password = data[1]
        treeWidget = data[2]
        fileTableWidget = data[3]
        rdata = data[4]
        dir = self.parsePath(treeWidget.currentItem(), rdata)

        try:
            # 更新文件列表
            files = scanDir(url, password, dir).split('\n')
            files = list(filter(None, files))
            self.updataTable(files, fileTableWidget)

            # 更新目录列表
            # print(files)

            item = treeWidget.currentItem()
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
                        item = QtWidgets.QTreeWidgetItem(treeWidget.currentItem())
                        item.setText(0, fs[:-1])
                        item.setIcon(0, QIcon('D:/Project/Graduation Design/icons/default_folder.svg'))

            item = treeWidget.currentItem()
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