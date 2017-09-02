__author__ = 'm'
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWidget,QLineEdit,QApplication
from PyQt4.QtCore import SIGNAL

class extQLineEdit(QLineEdit):
    def __init__(self,parent):
        QLineEdit.__init__(self,parent)
    def mousePressEvent(self,QMouseEvent):
        self.emit(SIGNAL('clicked()'))