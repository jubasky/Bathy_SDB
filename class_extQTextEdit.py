from PyQt4.QtGui import QTextEdit
from PyQt4.QtCore import SIGNAL


class extQTextEdit(QTextEdit):

    def __init__(self, parent, name):
        QTextEdit.__init__(self, parent)
        self.name = name
    def mousePressEvent(self, QMouseEvent):
        self.emit(SIGNAL('clicked()'))
