# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formExtrairXYZ.ui'
#
# Created: Sun Oct 08 02:39:16 2017
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
        self.pushButton_Converter = QtGui.QPushButton(Dialog)
        self.pushButton_Converter.setGeometry(QtCore.QRect(530, 480, 93, 28))
        self.pushButton_Converter.setObjectName(_fromUtf8("pushButton_Converter"))
        self.label2_2 = QtGui.QLabel(Dialog)
        self.label2_2.setGeometry(QtCore.QRect(320, 180, 81, 16))
        self.label2_2.setObjectName(_fromUtf8("label2_2"))
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(320, 260, 241, 151))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
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
        self.lineEdit_bloco = QtGui.QLineEdit(Dialog)
        self.lineEdit_bloco.setGeometry(QtCore.QRect(320, 210, 241, 22))
        self.lineEdit_bloco.setObjectName(_fromUtf8("lineEdit_bloco"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "DXF -> XYZ", None))
        self.pushButtonOk.setText(_translate("Dialog", "&Ok", None))
        self.pushButtonCancel.setText(_translate("Dialog", "&Cancel", None))
        self.label_1.setText(_translate("Dialog", "Ficheiro a ler:", None))
        self.pushButton_Abrir_Pasta.setText(_translate("Dialog", "...", None))
        self.pushButton_Converter.setText(_translate("Dialog", "Converter", None))
        self.label2_2.setText(_translate("Dialog", "bloco (dwg):", None))
        self.pushButton_Sel.setText(_translate("Dialog", "Sel. Todos", None))
        self.label_2.setText(_translate("Dialog", "Pasta de destino:", None))
        self.pushButton_Abrir_Pasta_Destino.setText(_translate("Dialog", "...", None))

