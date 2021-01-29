#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QApplication
from UI import mainWindowFront
import sys

class mainCode(QMainWindow, mainWindowFront.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        mainWindowFront.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.initTable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mc = mainCode()
    mc.show()
    sys.exit(app.exec_())