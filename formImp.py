# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formImp.ui'
#
# Created: Tue Aug 25 15:41:45 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_formImp(object):
    def setupUi(self, formImp):
        formImp.setObjectName(_fromUtf8("formImp"))
        formImp.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(formImp)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(formImp)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.pushButton_cancel = QtGui.QPushButton(formImp)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.pushButton_ok = QtGui.QPushButton(formImp)
        self.pushButton_ok.setObjectName(_fromUtf8("pushButton_ok"))
        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.retranslateUi(formImp)
        QtCore.QObject.connect(self.pushButton_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), formImp.close)
        QtCore.QMetaObject.connectSlotsByName(formImp)

    def retranslateUi(self, formImp):
        formImp.setWindowTitle(_translate("formImp", "Import CSV", None))
        self.label.setText(_translate("formImp", "Olá", None))
        self.pushButton_cancel.setText(_translate("formImp", "Cancel", None))
        self.pushButton_ok.setText(_translate("formImp", "Ok", None))

