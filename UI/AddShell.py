# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addShell.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import Core.php.ConnectToShellPhp as phpCore
import Core.jsp.ConnectToShellJsp as jspCore

class Ui_dialog(QtWidgets.QDialog):
    signalDgData = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setObjectName("dialog")
        self.resize(400, 400)
        self.setMinimumSize(QtCore.QSize(400, 400))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 5, 0, 1, 4)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 4, 3, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 2)
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 4, 0, 1, 2)
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 2, 1, 1)

        '''
        测试连接稳定性
        '''
        self.pushButton_2.clicked.connect(self.testConn)
        '''
        添加数据
        '''
        self.pushButton.clicked.connect(self.close)

        self.comboBox.activated[str].connect(self.handelComboChanged)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.lineEdit, self.pushButton)
        self.setTabOrder(self.pushButton, self.pushButton_2)
        self.setTabOrder(self.pushButton_2, self.textBrowser)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "添加shell"))
        self.label_2.setText(_translate("dialog", "密码"))
        self.pushButton.setText(_translate("dialog", "添加"))
        self.label_3.setText(_translate("dialog", "备注"))
        self.comboBox.setItemText(0, _translate("dialog", "PHP"))
        self.comboBox.setItemText(1, _translate("dialog", "JSP"))
        self.pushButton_2.setText(_translate("dialog", "测试连接"))
        self.label.setText(_translate("dialog", "URL链接"))
        self.checkBox.setText(_translate("dialog", "流量加密"))
        self.label_4.setText(_translate("dialog", "脚本类型"))
    '''
    关闭窗口时发送信号，传递数据
    '''
    def closeEvent(self, event):

        if not hasattr(self.sender(), 'text'):
            event.accept()
        else:
            try:
                self.signalDgData.emit([self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.checkBox.isChecked(), self.comboBox.currentText()])
                event.accept()
            except Exception as e:
                self.textBrowser.setText('添加失败！\n' + str(Exception(e)))
                event.ignore()

    '''
    JSP不支持流量加密
    '''

    def handelComboChanged(self):
        if self.comboBox.currentText() == 'JSP':
            self.checkBox.setChecked(False)
            self.checkBox.setEnabled(False)
        else:
            self.checkBox.setEnabled(True)


    def testConn(self):
        url = self.lineEdit.text()
        passWord = self.lineEdit_2.text()
        try:
            if self.checkBox.isChecked():
                useRSA = '是'
            else:
                useRSA = '否'
            if self.comboBox.currentText() == "PHP":
                r = phpCore.TestConn(url, passWord, useRSA)
            else:
                r = jspCore.TestConn(url, passWord)
            self.textBrowser.setText('连接成功！\n' + r)
        except Exception as e:
            self.textBrowser.setText('连接失败！\n' + str(Exception(e)))