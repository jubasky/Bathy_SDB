# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormConfig.ui'
#
# Created: Sun Jan 15 01:42:09 2017
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

class Ui_FormConfig(object):
    def setupUi(self, FormConfig):
        FormConfig.setObjectName(_fromUtf8("FormConfig"))
        FormConfig.resize(520, 500)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FormConfig.sizePolicy().hasHeightForWidth())
        FormConfig.setSizePolicy(sizePolicy)
        FormConfig.setMinimumSize(QtCore.QSize(520, 500))
        FormConfig.setMaximumSize(QtCore.QSize(520, 500))
        FormConfig.setBaseSize(QtCore.QSize(503, 247))
        FormConfig.setSizeGripEnabled(False)
        self.pushButton_Ok = QtGui.QPushButton(FormConfig)
        self.pushButton_Ok.setGeometry(QtCore.QRect(420, 460, 93, 28))
        self.pushButton_Ok.setObjectName(_fromUtf8("pushButton_Ok"))
        self.pushButton_Cancel = QtGui.QPushButton(FormConfig)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(290, 460, 93, 28))
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.widget = QtGui.QWidget(FormConfig)
        self.widget.setGeometry(QtCore.QRect(10, 12, 501, 438))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.widget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_host = QtGui.QLabel(self.groupBox)
        self.label_host.setObjectName(_fromUtf8("label_host"))
        self.gridLayout.addWidget(self.label_host, 0, 0, 1, 1)
        self.lineEdit_Host = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Host.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_Host.setBaseSize(QtCore.QSize(0, 25))
        self.lineEdit_Host.setObjectName(_fromUtf8("lineEdit_Host"))
        self.gridLayout.addWidget(self.lineEdit_Host, 0, 1, 1, 1)
        self.label_Port = QtGui.QLabel(self.groupBox)
        self.label_Port.setObjectName(_fromUtf8("label_Port"))
        self.gridLayout.addWidget(self.label_Port, 1, 0, 1, 1)
        self.lineEdit_Port = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Port.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_Port.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lineEdit_Port.setObjectName(_fromUtf8("lineEdit_Port"))
        self.gridLayout.addWidget(self.lineEdit_Port, 1, 1, 1, 1)
        self.label_Db = QtGui.QLabel(self.groupBox)
        self.label_Db.setObjectName(_fromUtf8("label_Db"))
        self.gridLayout.addWidget(self.label_Db, 2, 0, 1, 1)
        self.lineEdit_Db = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Db.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_Db.setBaseSize(QtCore.QSize(0, 25))
        self.lineEdit_Db.setObjectName(_fromUtf8("lineEdit_Db"))
        self.gridLayout.addWidget(self.lineEdit_Db, 2, 1, 1, 1)
        self.label_nome = QtGui.QLabel(self.groupBox)
        self.label_nome.setObjectName(_fromUtf8("label_nome"))
        self.gridLayout.addWidget(self.label_nome, 3, 0, 1, 1)
        self.lineEdit_User = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_User.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_User.setBaseSize(QtCore.QSize(0, 25))
        self.lineEdit_User.setObjectName(_fromUtf8("lineEdit_User"))
        self.gridLayout.addWidget(self.lineEdit_User, 3, 1, 1, 1)
        self.label_password = QtGui.QLabel(self.groupBox)
        self.label_password.setObjectName(_fromUtf8("label_password"))
        self.gridLayout.addWidget(self.label_password, 4, 0, 1, 1)
        self.lineEdit_Passwd = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Passwd.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_Passwd.setBaseSize(QtCore.QSize(0, 25))
        self.lineEdit_Passwd.setObjectName(_fromUtf8("lineEdit_Passwd"))
        self.gridLayout.addWidget(self.lineEdit_Passwd, 4, 1, 1, 1)
        self.label_path = QtGui.QLabel(self.groupBox)
        self.label_path.setObjectName(_fromUtf8("label_path"))
        self.gridLayout.addWidget(self.label_path, 5, 0, 1, 1)
        self.lineEdit_PathScripts = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_PathScripts.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_PathScripts.setBaseSize(QtCore.QSize(0, 25))
        self.lineEdit_PathScripts.setObjectName(_fromUtf8("lineEdit_PathScripts"))
        self.gridLayout.addWidget(self.lineEdit_PathScripts, 5, 1, 1, 1)
        self.pushButton_path = QtGui.QPushButton(self.groupBox)
        self.pushButton_path.setMinimumSize(QtCore.QSize(28, 0))
        self.pushButton_path.setMaximumSize(QtCore.QSize(28, 16777215))
        self.pushButton_path.setObjectName(_fromUtf8("pushButton_path"))
        self.gridLayout.addWidget(self.pushButton_path, 5, 2, 1, 1)
        self.label_PrefixPath = QtGui.QLabel(self.groupBox)
        self.label_PrefixPath.setObjectName(_fromUtf8("label_PrefixPath"))
        self.gridLayout.addWidget(self.label_PrefixPath, 6, 0, 1, 1)
        self.lineEdit_QPath = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_QPath.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_QPath.setBaseSize(QtCore.QSize(0, 25))
        self.lineEdit_QPath.setObjectName(_fromUtf8("lineEdit_QPath"))
        self.gridLayout.addWidget(self.lineEdit_QPath, 6, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.pushButton_testConn = QtGui.QPushButton(self.widget)
        self.pushButton_testConn.setObjectName(_fromUtf8("pushButton_testConn"))
        self.verticalLayout.addWidget(self.pushButton_testConn)
        self.textBrowser = QtGui.QTextBrowser(self.widget)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 150))
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 150))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi(FormConfig)
        QtCore.QObject.connect(self.pushButton_Cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), FormConfig.close)
        QtCore.QObject.connect(self.pushButton_Ok, QtCore.SIGNAL(_fromUtf8("clicked()")), FormConfig.accept)
        QtCore.QMetaObject.connectSlotsByName(FormConfig)

    def retranslateUi(self, FormConfig):
        FormConfig.setWindowTitle(_translate("FormConfig", "Configuração", None))
        self.pushButton_Ok.setText(_translate("FormConfig", "OK", None))
        self.pushButton_Cancel.setText(_translate("FormConfig", "Cancel", None))
        self.label_host.setText(_translate("FormConfig", "Host", None))
        self.label_Port.setText(_translate("FormConfig", "Port", None))
        self.label_Db.setText(_translate("FormConfig", "Base dados", None))
        self.label_nome.setText(_translate("FormConfig", "Utilizador", None))
        self.label_password.setText(_translate("FormConfig", "Password", None))
        self.label_path.setText(_translate("FormConfig", "Loc. Scripts", None))
        self.pushButton_path.setText(_translate("FormConfig", "...", None))
        self.label_PrefixPath.setText(_translate("FormConfig", "QGis Prefix Path", None))
        self.pushButton_testConn.setText(_translate("FormConfig", "Testar ligação à BD", None))

