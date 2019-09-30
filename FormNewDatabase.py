# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormNewDatabase.ui'
#
# Created: Thu Sep 26 10:49:06 2019
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
        FormNewDatabase.resize(600, 500)
        FormNewDatabase.setMinimumSize(QtCore.QSize(600, 500))
        FormNewDatabase.setMaximumSize(QtCore.QSize(600, 500))
        FormNewDatabase.setBaseSize(QtCore.QSize(600, 350))
        # FormNewDatabase.setSizeGripEnabled(False)
        self.groupBox = QtGui.QGroupBox(FormNewDatabase)
        self.groupBox.setGeometry(QtCore.QRect(100, 320, 301, 131))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(22, 42, 46, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(24, 83, 41, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_nova = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_nova.setGeometry(QtCore.QRect(90, 40, 181, 25))
        self.lineEdit_nova.setMinimumSize(QtCore.QSize(0, 24))
        self.lineEdit_nova.setObjectName(_fromUtf8("lineEdit_nova"))
        self.lineEdit_owner = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_owner.setGeometry(QtCore.QRect(90, 80, 181, 25))
        self.lineEdit_owner.setMinimumSize(QtCore.QSize(0, 24))
        self.lineEdit_owner.setObjectName(_fromUtf8("lineEdit_owner"))
        self.groupBox_2 = QtGui.QGroupBox(FormNewDatabase)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 20, 571, 281))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.lineEdit_host = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_host.setGeometry(QtCore.QRect(59, 20, 161, 25))
        self.lineEdit_host.setObjectName(_fromUtf8("lineEdit_host"))
        self.lineEdit_db = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_db.setGeometry(QtCore.QRect(370, 20, 191, 25))
        self.lineEdit_db.setObjectName(_fromUtf8("lineEdit_db"))
        self.lineEdit_user = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_user.setGeometry(QtCore.QRect(59, 60, 161, 25))
        self.lineEdit_user.setObjectName(_fromUtf8("lineEdit_user"))
        self.lineEdit_passwd = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_passwd.setGeometry(QtCore.QRect(370, 60, 191, 25))
        self.lineEdit_passwd.setObjectName(_fromUtf8("lineEdit_passwd"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(15, 20, 30, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(16, 60, 31, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(236, 25, 131, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(300, 60, 60, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.textEdit = QtGui.QTextEdit(self.groupBox_2)
        self.textEdit.setGeometry(QtCore.QRect(10, 90, 551, 181))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.pushButtonCriar = QtGui.QPushButton(FormNewDatabase)
        self.pushButtonCriar.setGeometry(QtCore.QRect(30, 460, 91, 31))
        self.pushButtonCriar.setObjectName(_fromUtf8("pushButtonCriar"))
        self.pushButtonSair = QtGui.QPushButton(FormNewDatabase)
        self.pushButtonSair.setGeometry(QtCore.QRect(470, 460, 111, 31))
        self.pushButtonSair.setObjectName(_fromUtf8("pushButtonSair"))

        self.retranslateUi(FormNewDatabase)
        QtCore.QObject.connect(self.pushButtonSair, QtCore.SIGNAL(_fromUtf8("clicked()")), FormNewDatabase.close)
        QtCore.QMetaObject.connectSlotsByName(FormNewDatabase)

    def retranslateUi(self, FormNewDatabase):
        FormNewDatabase.setWindowTitle(_translate("FormNewDatabase", "Criar BD", None))
        self.groupBox.setTitle(_translate("FormNewDatabase", "Nova base de dados:", None))
        self.label.setText(_translate("FormNewDatabase", "Nome:", None))
        self.label_2.setText(_translate("FormNewDatabase", "Owner:", None))
        self.label_3.setText(_translate("FormNewDatabase", "Host:", None))
        self.label_4.setText(_translate("FormNewDatabase", "User:", None))
        self.label_5.setText(_translate("FormNewDatabase", "Base de dados inicial:", None))
        self.label_6.setText(_translate("FormNewDatabase", "Password:", None))
        self.pushButtonCriar.setText(_translate("FormNewDatabase", "&Criar BD", None))
        self.pushButtonSair.setText(_translate("FormNewDatabase", "&Sair", None))

