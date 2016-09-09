# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormNewDatabase.ui'
#
# Created: Tue Aug 30 02:05:10 2016
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

class Ui_FormNewDatabase(object):
    def setupUi(self, FormNewDatabase):
        FormNewDatabase.setObjectName(_fromUtf8("FormNewDatabase"))
        FormNewDatabase.resize(400, 350)
        FormNewDatabase.setMinimumSize(QtCore.QSize(400, 350))
        FormNewDatabase.setMaximumSize(QtCore.QSize(400, 350))
        FormNewDatabase.setBaseSize(QtCore.QSize(400, 350))
        # FormNewDatabase.setSizeGripEnabled(False)
        self.buttonBox = QtGui.QDialogButtonBox(FormNewDatabase)
        self.buttonBox.setGeometry(QtCore.QRect(40, 310, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.groupBox = QtGui.QGroupBox(FormNewDatabase)
        self.groupBox.setGeometry(QtCore.QRect(160, 200, 231, 101))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 20, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.textNome = QtGui.QTextEdit(self.groupBox)
        self.textNome.setGeometry(QtCore.QRect(80, 10, 141, 31))
        self.textNome.setObjectName(_fromUtf8("textNome"))
        self.textOwner = QtGui.QTextEdit(self.groupBox)
        self.textOwner.setGeometry(QtCore.QRect(80, 50, 141, 31))
        self.textOwner.setObjectName(_fromUtf8("textOwner"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 41, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox_2 = QtGui.QGroupBox(FormNewDatabase)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 20, 381, 161))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.lineEdit_1 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_1.setGeometry(QtCore.QRect(60, 20, 113, 20))
        self.lineEdit_1.setObjectName(_fromUtf8("lineEdit_1"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 20, 113, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_3 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(60, 60, 113, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_4 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(240, 60, 113, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 31, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(30, 60, 31, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(191, 20, 46, 13))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(199, 60, 41, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.textEdit = QtGui.QTextEdit(self.groupBox_2)
        self.textEdit.setGeometry(QtCore.QRect(10, 90, 341, 61))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(FormNewDatabase)
        QtCore.QMetaObject.connectSlotsByName(FormNewDatabase)

    def retranslateUi(self, FormNewDatabase):
        FormNewDatabase.setWindowTitle(_translate("FormNewDatabase", "Dialog", None))
        self.label.setText(_translate("FormNewDatabase", "Nome:", None))
        self.label_2.setText(_translate("FormNewDatabase", "Owner:", None))
        self.groupBox_2.setTitle(_translate("FormNewDatabase", "GroupBox", None))
        self.label_3.setText(_translate("FormNewDatabase", " host", None))
        self.label_4.setText(_translate("FormNewDatabase", "user", None))
        self.label_5.setText(_translate("FormNewDatabase", "dbname", None))
        self.label_6.setText(_translate("FormNewDatabase", "psswd", None))

