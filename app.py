#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem, QMenu
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from qqwry import QQwry
from functools import partial
from testConnShell import *
import pathlib
import mainWindowFront, addShell, genShellPhp
import os, time, json, re

class mainCode(QMainWindow, mainWindowFront.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        mainWindowFront.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.tab_index = 0
        self.row_num = -1
        self.index = -1
        self.init_table()
        self.genShellPhp.triggered.connect(self.gen_shell_php)
        self.shellTableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.shellTableWidget.doubleClicked.connect(self.shellTableDoubleClicked)

    def init_table(self):
        current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(current_path + "/cache/db.json", "r") as f:
            d = json.load(f)
            for index, data in d.items():
                self.shellTableWidget.setRowCount(int(index) + 1)
                # 添加URL
                newItem = QTableWidgetItem(data["URL链接"])
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.shellTableWidget.setItem(int(index), 0, newItem)

                # 添加IP
                newItem = QTableWidgetItem(data["IP地址"])
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.shellTableWidget.setItem(int(index), 1, newItem)

                # 添加密码
                newItem = QTableWidgetItem(data["密码"])
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.shellTableWidget.setItem(int(index), 2, newItem)

                # 添加物理地址
                newItem = QTableWidgetItem(data["物理位置"])
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.shellTableWidget.setItem(int(index), 3, newItem)

                # 添加备注
                newItem = QTableWidgetItem(data["网站备注"])
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.shellTableWidget.setItem(int(index), 4, newItem)

                # 添加时间
                newItem = QTableWidgetItem(data["修改时间"])
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.shellTableWidget.setItem(int(index), 5, newItem)

        self.shellTableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.shellTableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
    def closeEvent(self, Event):
        if self.index != -1:
            js = {}
            current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
            for i in range(self.index + 1):
                data = {}
                data["URL链接"] = self.shellTableWidget.item(i, 0).text()
                data["IP地址"] = self.shellTableWidget.item(i, 1).text()
                data["密码"] = self.shellTableWidget.item(i, 2).text()
                data["物理位置"] = self.shellTableWidget.item(i, 3).text()
                data["网站备注"] = self.shellTableWidget.item(i, 4).text()
                data["修改时间"] = self.shellTableWidget.item(i, 5).text()
                js[i] = data

            with open(current_path + "/cache/db.json", "w") as f:
                json.dump(js, f)
                #print("加载入文件完成...")
        Event.accept()

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
            self.index = self.shellTableWidget.rowCount()
            self.shellTableWidget.setRowCount(self.index + 1)
        else:
            self.index = self.row_num

        #添加URL
        newItem = QTableWidgetItem(url)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.shellTableWidget.setItem(self.index, 0, newItem)

        #添加IP
        ip= dns_resolver(url)
        newItem = QTableWidgetItem(ip)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.shellTableWidget.setItem(self.index, 1, newItem)

        #添加密码
        newItem = QTableWidgetItem(password)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.shellTableWidget.setItem(self.index, 2, newItem)

        #添加物理地址
        q = QQwry()
        q.load_file(os.path.dirname(__file__) + '/qqwry.dat')
        try:
            res = q.lookup(ip)
            addr = res[0] + ' ' + res[1]
        except:
            addr = ''
        newItem = QTableWidgetItem(addr)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.shellTableWidget.setItem(self.index, 3, newItem)

        #添加备注
        newItem = QTableWidgetItem(memo)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.shellTableWidget.setItem(self.index, 4, newItem)
        # 添加时间
        newItem = QTableWidgetItem(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.shellTableWidget.setItem(self.index, 5, newItem)

        self.shellTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.shellTableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.shellTableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

    def shellTableDoubleClicked(self):
        #计算当前行数
        self.row_num = -1
        for i in self.shellTableWidget.selectionModel().selection().indexes():
            self.row_num = i.row()
        self.displayShell()


    def generateMenu(self, pos):
        menu = QMenu()
        #计算当前行数
        self.row_num = -1
        for i in self.shellTableWidget.selectionModel().selection().indexes():
            self.row_num = i.row()

        if self.row_num != -1:
            item1 = menu.addAction('打开')
            item2 = menu.addAction('编辑')
            item3 = menu.addAction('删除')
            item4 = menu.addAction('查看')
            action = menu.exec_(self.shellTableWidget.mapToGlobal(pos))

            if action == item1:
                self.displayShell()

            elif action == item2:
                dg = addShell.Ui_dialog()
                dg.pushButton.setText("保存")

                dg.lineEdit.setText(self.shellTableWidget.item(self.row_num, 0).text())
                dg.lineEdit_2.setText(self.shellTableWidget.item(self.row_num, 2).text())
                dg.lineEdit_3.setText(self.shellTableWidget.item(self.row_num, 4).text())
                dg.signal_url_password.connect(self.deal_emit_slot)

                dg.exec()
            elif action == item3:
                self.shellTableWidget.removeRow(self.row_num)
            elif action == item4:
                self.displayWeb(self.shellTableWidget.item(self.row_num, 0).text())
        else:
            item = menu.addAction('新建')
            action = menu.exec_(self.shellTableWidget.mapToGlobal(pos))
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
        # 当前选择文件的目录
        dir = self.parsePath(item, rdata)

        menu = QMenu()
        #计算当前行数
        self.row_num = -1
        for i in fileTableWidget.selectionModel().selection().indexes():
            self.row_num = i.row()

        if self.row_num != -1:
            if fileTableWidget.item(self.row_num, 0).text().endswith('/'):
                # 文件夹
                pass
            else:
                # 文件
                item1 = menu.addAction('下载文件')
                item2 = menu.addAction('重命名')
                item3 = menu.addAction('删除文件')
                item4 = menu.addAction('更改权限')
                action = menu.exec_(fileTableWidget.mapToGlobal(pos))

                if action == item1:
                    try:
                        filename = fileTableWidget.item(self.row_num, 0).text()
                        buffer = downloadFile(url, password, dir + filename)
                        file = QtWidgets.QFileDialog.getSaveFileName(self, '保存路径', filename)
                        if file[0] != '':
                            with open(file[0], 'w', encoding='utf-8') as f:
                                f.write(buffer)
                            QtWidgets.QMessageBox.about(self, "下载成功！", '文件已保存')
                    except Exception as e:
                        QtWidgets.QMessageBox.about(self, "下载失败！", str(Exception(e)))
                elif action == item2:
                    try:
                        rfilename = fileTableWidget.item(self.row_num, 0).text()
                        dfilename, ok = QtWidgets.QInputDialog.getText(self, '重命名', '更改后的文件名：')
                        if ok:
                            if renameFile(url, password, dir + rfilename, dir + dfilename) == '1':
                                QtWidgets.QMessageBox.about(self, "重命名成功！", '文件已重命名')
                            else:
                                QtWidgets.QMessageBox.about(self, "重命名失败！", '可能没有权限')
                            # 更新文件目录
                            files = scanDir(url, password, dir).split('\n')
                            files = list(filter(None, files))
                            self.updataTable(files, fileTableWidget)
                    except Exception as e:
                        QtWidgets.QMessageBox.about(self, "重命名失败！", str(Exception(e)))
                elif action == item3:
                    try:
                        file = fileTableWidget.item(self.row_num, 0).text()
                        reply = QtWidgets.QMessageBox.question(self, '删除文件', "确定要删除该文件吗？", QtWidgets.QMessageBox.Yes
                                                               | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
                        if reply == QtWidgets.QMessageBox.Yes:
                            if deleteFile(url, password, dir + file) == '1':
                                QtWidgets.QMessageBox.about(self, "删除成功！", '文件已删除')
                            else:
                                QtWidgets.QMessageBox.about(self, "删除失败！", '可能没有权限')
                            # 更新文件目录
                            files = scanDir(url, password, dir).split('\n')
                            files = list(filter(None, files))
                            self.updataTable(files, fileTableWidget)
                    except Exception as e:
                        QtWidgets.QMessageBox.about(self, "删除文件失败！", str(Exception(e)))
                elif action == item4:
                    try:
                        file = fileTableWidget.item(self.row_num, 0).text()
                        rmode = fileTableWidget.item(self.row_num, 3).text()
                        nmode, ok = QtWidgets.QInputDialog.getText(self, '更改权限', '更改为：', text = rmode)
                        if ok:
                            searchObj = re.search( '^0[0-7][0-7][0-7]$', nmode)
                            if searchObj is None:
                                raise Exception('输入不合法')
                            if chmodFile(url, password, dir + file, nmode) == '1':
                                QtWidgets.QMessageBox.about(self, "更改成功！", '权限已经更改')
                            else:
                                QtWidgets.QMessageBox.about(self, "更改失败！", '更改权限失败！')
                            # 更新文件目录
                            files = scanDir(url, password, dir).split('\n')
                            files = list(filter(None, files))
                            self.updataTable(files, fileTableWidget)
                    except Exception as e:
                        QtWidgets.QMessageBox.about(self, "更改权限失败！", str(Exception(e)))
        else:
            item11 = menu.addAction('上传文件')
            item12 = menu.addAction('刷新目录')
            action = menu.exec_(fileTableWidget.mapToGlobal(pos))
            if action == item11:
                try:
                    filePath= QtWidgets.QFileDialog.getOpenFileName(self, '选择文件')
                    if filePath[0] != '':
                        with open(filePath[0], encoding='utf-8') as f:
                            buffer = f.read()
                        r = uploadFile(url, password, buffer, dir + os.path.basename(filePath[0]))
                        if r == '1':
                            QtWidgets.QMessageBox.about(self, "上传成功！", '文件已上传')
                            # 更新文件目录
                            files = scanDir(url, password, dir).split('\n')
                            files = list(filter(None, files))
                            self.updataTable(files, fileTableWidget)
                        else:
                            QtWidgets.QMessageBox.about(self, "上传失败！", '可能没有权限')

                except Exception as e:
                    QtWidgets.QMessageBox.about(self, "上传失败！", str(Exception(e)))
            elif action == item12 :
                # 更新文件目录
                files = scanDir(url, password, dir).split('\n')
                files = list(filter(None, files))
                self.updataTable(files, fileTableWidget)

    def displayShell(self):
        try:
            url = self.shellTableWidget.item(self.row_num, 0).text()
            password = self.shellTableWidget.item(self.row_num, 2).text()
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
            treeWidget.setStyle(QtWidgets.QStyleFactory.create("windows"))

            # tree信息初始化
            # 根节点
            self.root = QtWidgets.QTreeWidgetItem(treeWidget)
            if not rdata[1].endswith(':'):
                self.root.setText(0, rdata[1])
                self.root.setIcon(0,
                                  QIcon(os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_root_folder_opened.svg'))
            else:
                #处理windows路径
                r = rdata[1].split(':')[:-1]
                for i in r:
                    if i == rdata[0][0]:
                        self.root.setText(0, i+':/')
                        self.root.setIcon(0, QIcon(
                            os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_root_folder_opened.svg'))
                    else:
                        root = QtWidgets.QTreeWidgetItem(treeWidget)
                        root.setText(0, i + ':/')
                        root.setIcon(0, QIcon(
                            os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_root_folder_opened.svg'))


            # 子节点
            if rdata[0][1] != ':':
                folders = rdata[0][1:].split('/')
            else:
                # 处理windows
                folders = rdata[0][3:].split('/')
            itemStack = [self.root]
            for i in range(len(folders)):
                item = QtWidgets.QTreeWidgetItem(itemStack.pop())
                item.setText(0, folders[i])

                if i == len(folders) - 1:
                    item.setIcon(0, QIcon(os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_folder.svg'))
                else:
                    item.setIcon(0, QIcon(os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_folder_opened.svg'))

                itemStack.append(item)

            # 更新节点
            treeWidget.clicked.connect(lambda:self.updateTree([url, password, treeWidget, fileTableWidget, rdata]))
            # 处理展开的Icon
            treeWidget.itemExpanded.connect(self.treeExpaned)
            treeWidget.itemCollapsed.connect(self.treeCollapsed)

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
            #调整比例
            self.gridLayout.setColumnStretch(0, 1)
            self.gridLayout.setColumnStretch(1, 2)


            self.label.setText(
                "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">目录列表</span></p></body></html>")
            self.label_2.setText(
                "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">文件列表</span></p></body></html>")

            self.tabWidget.addTab(self.new_tab, self.shellTableWidget.item(self.row_num, 1).text())
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

    def treeExpaned(self, item):
        if item is not None:
            if item.parent() is None:
                item.setIcon(0, QIcon(
                    os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_root_folder_opened.svg'))
            else:
                item.setIcon(0, QIcon(os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_folder_opened.svg'))

    def treeCollapsed(self, item):
        if item is not None:
            if item.parent() is None:
                item.setIcon(0, QIcon(
                    os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_root_folder.svg'))
            else:
                item.setIcon(0, QIcon(os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_folder.svg'))

    def updataTable(self, files, fileTableWidget):
        for i in range(len(files) - 1, -1, -1):
            if (files[i].split('\t'))[0].startswith('./') or (files[i].split('\t'))[0].startswith('../'):
                files.remove(files[i])
        fileTableWidget.setRowCount(len(files))
        for i in range(len(files)):
            for j in range(4):
                content = files[i].split('\t')[j]
                if j == 2:
                    try:
                        newItem = QTableWidgetItem(formatFileSize(int(content), 2))
                    except:
                        newItem = QTableWidgetItem(content)
                elif j == 0:
                    fileType = os.path.splitext(content)[1][1:]
                    icon = os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/file_type_' + fileType + '.svg'
                    iconFile = pathlib.Path(icon)
                    if iconFile.is_file():
                        newItem = QTableWidgetItem(QIcon(icon), content)
                    elif content.endswith('/'):
                        icon = os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_folder.svg'
                        newItem = QTableWidgetItem(QIcon(icon), content)
                    else:
                        icon = os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_file.svg'
                        newItem = QTableWidgetItem(QIcon(icon), content)
                else:
                    newItem = QTableWidgetItem(content)
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                fileTableWidget.setItem(i, j, newItem)
        fileTableWidget.sortItems(0, QtCore.Qt.AscendingOrder)

    def parsePath(self, item, rdata):
        if not rdata[1].endswith(':'):
            # linux
            # 是否为根目录
            if item.text(0) == rdata[1]:
                dir = rdata[1]
            else:
                dir = '/'
                dir = '/' + item.text(0) + dir
                while item.parent().text(0) != rdata[1]:
                    item = item.parent()
                    dir = '/' + item.text(0) + dir
            #print(dir)
            return dir

        else:
            # windows
            if item.text(0).endswith(':/'):
                dir = item.text(0)
            else:
                dir = '/'
                dir = '/' + item.text(0) + dir
                while not item.parent().text(0).endswith(':/'):
                    item = item.parent()
                    dir = '/' + item.text(0) + dir
                item = item.parent()
                dir = item.text(0)[:2] + dir
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
                        if item.isExpanded():
                            item.setIcon(0, QIcon(os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_folder_opened.svg'))
                        else:
                            item.setIcon(0, QIcon(os.path.dirname(os.path.realpath(sys.argv[0])) + '/icons/default_folder.svg'))

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