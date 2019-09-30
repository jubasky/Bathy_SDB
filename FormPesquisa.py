# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formPesquisa.ui'
#
# Created: Sun Sep 29 15:15:48 2019
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

class Ui_FormPesquisa(object):
    def setupUi(self, FormPesquisa):
        FormPesquisa.setObjectName(_fromUtf8("FormPesquisa"))
        FormPesquisa.resize(825, 360)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FormPesquisa.sizePolicy().hasHeightForWidth())
        FormPesquisa.setSizePolicy(sizePolicy)
        FormPesquisa.setMaximumSize(QtCore.QSize(3000, 360))
        self.layoutWidget = QtGui.QWidget(FormPesquisa)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 781, 261))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_LatMax = QtGui.QLabel(self.layoutWidget)
        self.label_LatMax.setObjectName(_fromUtf8("label_LatMax"))
        self.gridLayout.addWidget(self.label_LatMax, 1, 2, 1, 1)
        self.lineEdit_LatMax = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_LatMax.sizePolicy().hasHeightForWidth())
        self.lineEdit_LatMax.setSizePolicy(sizePolicy)
        self.lineEdit_LatMax.setObjectName(_fromUtf8("lineEdit_LatMax"))
        self.gridLayout.addWidget(self.lineEdit_LatMax, 1, 3, 1, 1)
        self.label_LatMin = QtGui.QLabel(self.layoutWidget)
        self.label_LatMin.setObjectName(_fromUtf8("label_LatMin"))
        self.gridLayout.addWidget(self.label_LatMin, 1, 0, 1, 1)
        self.label_LongMin = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_LongMin.sizePolicy().hasHeightForWidth())
        self.label_LongMin.setSizePolicy(sizePolicy)
        self.label_LongMin.setObjectName(_fromUtf8("label_LongMin"))
        self.gridLayout.addWidget(self.label_LongMin, 0, 0, 1, 1)
        self.label_LongMax = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_LongMax.sizePolicy().hasHeightForWidth())
        self.label_LongMax.setSizePolicy(sizePolicy)
        self.label_LongMax.setObjectName(_fromUtf8("label_LongMax"))
        self.gridLayout.addWidget(self.label_LongMax, 0, 2, 1, 1)
        self.lineEdit_LatMin = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_LatMin.sizePolicy().hasHeightForWidth())
        self.lineEdit_LatMin.setSizePolicy(sizePolicy)
        self.lineEdit_LatMin.setObjectName(_fromUtf8("lineEdit_LatMin"))
        self.gridLayout.addWidget(self.lineEdit_LatMin, 1, 1, 1, 1)
        self.lineEdit_LongMax = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_LongMax.sizePolicy().hasHeightForWidth())
        self.lineEdit_LongMax.setSizePolicy(sizePolicy)
        self.lineEdit_LongMax.setObjectName(_fromUtf8("lineEdit_LongMax"))
        self.gridLayout.addWidget(self.lineEdit_LongMax, 0, 3, 1, 1)
        self.lineEdit_LongMin = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_LongMin.sizePolicy().hasHeightForWidth())
        self.lineEdit_LongMin.setSizePolicy(sizePolicy)
        self.lineEdit_LongMin.setObjectName(_fromUtf8("lineEdit_LongMin"))
        self.gridLayout.addWidget(self.lineEdit_LongMin, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.listWidget = QtGui.QListWidget(self.layoutWidget)
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 160))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.pushButtonCancel = QtGui.QPushButton(FormPesquisa)
        self.pushButtonCancel.setGeometry(QtCore.QRect(10, 320, 120, 28))
        self.pushButtonCancel.setMaximumSize(QtCore.QSize(120, 16777215))
        self.pushButtonCancel.setBaseSize(QtCore.QSize(120, 0))
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.pushButtonOk = QtGui.QPushButton(FormPesquisa)
        self.pushButtonOk.setGeometry(QtCore.QRect(680, 320, 120, 28))
        self.pushButtonOk.setMaximumSize(QtCore.QSize(120, 16777215))
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))

        self.retranslateUi(FormPesquisa)
        QtCore.QMetaObject.connectSlotsByName(FormPesquisa)

    def retranslateUi(self, FormPesquisa):
        FormPesquisa.setWindowTitle(_translate("FormPesquisa", "Pesquisa", None))
        self.label_LatMax.setText(_translate("FormPesquisa", "Lat Max:", None))
        self.label_LatMin.setText(_translate("FormPesquisa", "Lat Min:", None))
        self.label_LongMin.setText(_translate("FormPesquisa", "Long Min:", None))
        self.label_LongMax.setText(_translate("FormPesquisa", "LongMax:", None))
        self.pushButtonCancel.setText(_translate("FormPesquisa", "&Cancel", None))
        self.pushButtonOk.setText(_translate("FormPesquisa", "Ok", None))

