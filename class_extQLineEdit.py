from PyQt4.QtGui import QLineEdit
from PyQt4.QtCore import SIGNAL


class extQLineEdit(QLineEdit):

    def __init__(self, parent, name):
        QLineEdit.__init__(self, parent)
        self.name = name
    def mousePressEvent(self, QMouseEvent):
        self.emit(SIGNAL('clicked()'))
