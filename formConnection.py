# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formConnection.ui'
#
# Created: Tue Oct 13 21:51:22 2015
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

class Ui_FormConnection(object):
    def setupUi(self, FormConnection):
        FormConnection.setObjectName(_fromUtf8("FormConnection"))
        FormConnection.resize(432, 338)
        self.gridLayout = QtGui.QGridLayout(FormConnection)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_1 = QtGui.QLineEdit(FormConnection)
        self.lineEdit_1.setObjectName(_fromUtf8("lineEdit_1"))
        self.gridLayout.addWidget(self.lineEdit_1, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(FormConnection)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(FormConnection)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.checkBox = QtGui.QCheckBox(FormConnection)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 4, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(FormConnection)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 2, 1, 1)
        self.label_2 = QtGui.QLabel(FormConnection)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(FormConnection)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.label_1 = QtGui.QLabel(FormConnection)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(FormConnection)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(FormConnection)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.plainTextEdit = QtGui.QPlainTextEdit(FormConnection)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.gridLayout.addWidget(self.plainTextEdit, 5, 0, 1, 3)

        self.retranslateUi(FormConnection)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FormConnection.close)
        QtCore.QMetaObject.connectSlotsByName(FormConnection)

    def retranslateUi(self, FormConnection):
        FormConnection.setWindowTitle(_translate("FormConnection", "Form", None))
        self.lineEdit_1.setText(_translate("FormConnection", "localhost", None))
        self.label_3.setText(_translate("FormConnection", "User:", None))
        self.lineEdit_3.setText(_translate("FormConnection", "postgres", None))
        self.checkBox.setText(_translate("FormConnection", "Success!", None))
        self.label_2.setText(_translate("FormConnection", "Database:", None))
        self.lineEdit_4.setText(_translate("FormConnection", "juba", None))
        self.label_1.setText(_translate("FormConnection", "Host:", None))
        self.lineEdit_2.setText(_translate("FormConnection", "lidar", None))
        self.label_4.setText(_translate("FormConnection", "Passwd:", None))

