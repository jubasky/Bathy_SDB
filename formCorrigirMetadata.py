# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formCorrigirMetadata.ui'
#
# Created: Thu Oct 05 20:39:21 2017
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(630, 560)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(630, 560))
        Dialog.setMaximumSize(QtCore.QSize(630, 560))
        self.pushButtonOk = QtGui.QPushButton(Dialog)
        self.pushButtonOk.setGeometry(QtCore.QRect(530, 520, 93, 28))
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.pushButtonCancel = QtGui.QPushButton(Dialog)
        self.pushButtonCancel.setGeometry(QtCore.QRect(390, 520, 93, 28))
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.label_1 = QtGui.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(10, 30, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_1.setFont(font)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.listViewCDI = QtGui.QListView(Dialog)
        self.listViewCDI.setGeometry(QtCore.QRect(10, 110, 271, 401))
        self.listViewCDI.setObjectName(_fromUtf8("listViewCDI"))
        self.pushButton_Abrir_Pasta = QtGui.QPushButton(Dialog)
        self.pushButton_Abrir_Pasta.setGeometry(QtCore.QRect(250, 70, 31, 31))
        self.pushButton_Abrir_Pasta.setObjectName(_fromUtf8("pushButton_Abrir_Pasta"))
        self.pushButtonCorrigir = QtGui.QPushButton(Dialog)
        self.pushButtonCorrigir.setGeometry(QtCore.QRect(530, 480, 93, 28))
        self.pushButtonCorrigir.setObjectName(_fromUtf8("pushButtonCorrigir"))
        self.label2 = QtGui.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(320, 120, 81, 16))
        self.label2.setObjectName(_fromUtf8("label2"))
        self.label2_2 = QtGui.QLabel(Dialog)
        self.label2_2.setGeometry(QtCore.QRect(320, 180, 81, 16))
        self.label2_2.setObjectName(_fromUtf8("label2_2"))
        self.label2_3 = QtGui.QLabel(Dialog)
        self.label2_3.setGeometry(QtCore.QRect(320, 240, 81, 16))
        self.label2_3.setObjectName(_fromUtf8("label2_3"))
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(320, 310, 291, 151))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.comboBox_Horiz = QtGui.QComboBox(Dialog)
        self.comboBox_Horiz.setGeometry(QtCore.QRect(420, 120, 181, 22))
        self.comboBox_Horiz.setObjectName(_fromUtf8("comboBox_Horiz"))
        self.comboBox_Vert = QtGui.QComboBox(Dialog)
        self.comboBox_Vert.setGeometry(QtCore.QRect(420, 180, 181, 22))
        self.comboBox_Vert.setObjectName(_fromUtf8("comboBox_Vert"))
        self.lineEdit_Lista_Ficheiros = QtGui.QLineEdit(Dialog)
        self.lineEdit_Lista_Ficheiros.setGeometry(QtCore.QRect(10, 71, 231, 31))
        self.lineEdit_Lista_Ficheiros.setObjectName(_fromUtf8("lineEdit_Lista_Ficheiros"))
        self.label_Num_Ficheiros = QtGui.QLabel(Dialog)
        self.label_Num_Ficheiros.setGeometry(QtCore.QRect(20, 520, 251, 16))
        self.label_Num_Ficheiros.setText(_fromUtf8(""))
        self.label_Num_Ficheiros.setObjectName(_fromUtf8("label_Num_Ficheiros"))
        self.pushButton_Sel = QtGui.QPushButton(Dialog)
        self.pushButton_Sel.setGeometry(QtCore.QRect(290, 480, 93, 28))
        self.pushButton_Sel.setObjectName(_fromUtf8("pushButton_Sel"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(310, 30, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_Pasta_Destino = QtGui.QLineEdit(Dialog)
        self.lineEdit_Pasta_Destino.setGeometry(QtCore.QRect(310, 70, 261, 31))
        self.lineEdit_Pasta_Destino.setObjectName(_fromUtf8("lineEdit_Pasta_Destino"))
        self.pushButton_Abrir_Pasta_Destino = QtGui.QPushButton(Dialog)
        self.pushButton_Abrir_Pasta_Destino.setGeometry(QtCore.QRect(580, 70, 31, 31))
        self.pushButton_Abrir_Pasta_Destino.setObjectName(_fromUtf8("pushButton_Abrir_Pasta_Destino"))
        self.comboBox_Purpose = QtGui.QComboBox(Dialog)
        self.comboBox_Purpose.setGeometry(QtCore.QRect(420, 240, 181, 22))
        self.comboBox_Purpose.setObjectName(_fromUtf8("comboBox_Purpose"))
        self.label2_4 = QtGui.QLabel(Dialog)
        self.label2_4.setGeometry(QtCore.QRect(320, 290, 81, 16))
        self.label2_4.setObjectName(_fromUtf8("label2_4"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "QI Index", None))
        self.pushButtonOk.setText(_translate("Dialog", "&Ok", None))
        self.pushButtonCancel.setText(_translate("Dialog", "&Cancel", None))
        self.label_1.setText(_translate("Dialog", "Ficheiros a corrigir:", None))
        self.pushButton_Abrir_Pasta.setText(_translate("Dialog", "...", None))
        self.pushButtonCorrigir.setText(_translate("Dialog", "Co&rrigir", None))
        self.label2.setText(_translate("Dialog", "QI_Horizontal", None))
        self.label2_2.setText(_translate("Dialog", " QI_Vertical", None))
        self.label2_3.setText(_translate("Dialog", "QI_Purpose", None))
        self.pushButton_Sel.setText(_translate("Dialog", "Sel. Todos", None))
        self.label_2.setText(_translate("Dialog", "Pasta de destino:", None))
        self.pushButton_Abrir_Pasta_Destino.setText(_translate("Dialog", "...", None))
        self.label2_4.setText(_translate("Dialog", "QI_Notes", None))

