# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormExportMetadata.ui'
#
# Created: Sun Sep 29 16:46:44 2019
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
        Dialog.resize(900, 427)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(900, 427))
        Dialog.setBaseSize(QtCore.QSize(900, 427))
        self.pushButton_OK = QtGui.QPushButton(Dialog)
        self.pushButton_OK.setGeometry(QtCore.QRect(790, 390, 93, 28))
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.pushButton_Cancel = QtGui.QPushButton(Dialog)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(650, 390, 93, 28))
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.listViewCDI = QtGui.QListView(Dialog)
        self.listViewCDI.setGeometry(QtCore.QRect(10, 40, 361, 371))
        self.listViewCDI.setObjectName(_fromUtf8("listViewCDI"))
        self.lineEdit_Fich_Destino = QtGui.QLineEdit(Dialog)
        self.lineEdit_Fich_Destino.setGeometry(QtCore.QRect(390, 190, 441, 31))
        self.lineEdit_Fich_Destino.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_Fich_Destino.setObjectName(_fromUtf8("lineEdit_Fich_Destino"))
        self.label_listViewCDI = QtGui.QLabel(Dialog)
        self.label_listViewCDI.setGeometry(QtCore.QRect(20, 10, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_listViewCDI.setFont(font)
        self.label_listViewCDI.setObjectName(_fromUtf8("label_listViewCDI"))
        self.pushButton_Sel_Fich_Dest = QtGui.QPushButton(Dialog)
        self.pushButton_Sel_Fich_Dest.setGeometry(QtCore.QRect(850, 190, 31, 31))
        self.pushButton_Sel_Fich_Dest.setObjectName(_fromUtf8("pushButton_Sel_Fich_Dest"))
        self.label_label_Fich_Template = QtGui.QLabel(Dialog)
        self.label_label_Fich_Template.setGeometry(QtCore.QRect(390, 10, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_label_Fich_Template.setFont(font)
        self.label_label_Fich_Template.setObjectName(_fromUtf8("label_label_Fich_Template"))
        self.label_Fich_Template = QtGui.QLabel(Dialog)
        self.label_Fich_Template.setGeometry(QtCore.QRect(390, 40, 441, 31))
        self.label_Fich_Template.setToolTip(_fromUtf8(""))
        self.label_Fich_Template.setWhatsThis(_fromUtf8(""))
        self.label_Fich_Template.setAutoFillBackground(False)
        self.label_Fich_Template.setFrameShape(QtGui.QFrame.Box)
        self.label_Fich_Template.setFrameShadow(QtGui.QFrame.Plain)
        self.label_Fich_Template.setText(_fromUtf8(""))
        self.label_Fich_Template.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_Fich_Template.setObjectName(_fromUtf8("label_Fich_Template"))
        self.pushButton_Sel_Template = QtGui.QPushButton(Dialog)
        self.pushButton_Sel_Template.setGeometry(QtCore.QRect(850, 40, 31, 31))
        self.pushButton_Sel_Template.setToolTip(_fromUtf8(""))
        self.pushButton_Sel_Template.setObjectName(_fromUtf8("pushButton_Sel_Template"))
        self.label_lineEdit_fich_destino = QtGui.QLabel(Dialog)
        self.label_lineEdit_fich_destino.setGeometry(QtCore.QRect(390, 160, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_lineEdit_fich_destino.setFont(font)
        self.label_lineEdit_fich_destino.setObjectName(_fromUtf8("label_lineEdit_fich_destino"))
        self.pushButton_Export = QtGui.QPushButton(Dialog)
        self.pushButton_Export.setGeometry(QtCore.QRect(390, 250, 161, 28))
        self.pushButton_Export.setObjectName(_fromUtf8("pushButton_Export"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton_Cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Exportar Metadata (CDI XML)", None))
        self.pushButton_OK.setText(_translate("Dialog", "&Ok", None))
        self.pushButton_Cancel.setText(_translate("Dialog", "&Cancelar", None))
        self.label_listViewCDI.setText(_translate("Dialog", "CDI - Cruzeiro:", None))
        self.pushButton_Sel_Fich_Dest.setText(_translate("Dialog", "...", None))
        self.label_label_Fich_Template.setText(_translate("Dialog", "Template:", None))
        self.pushButton_Sel_Template.setText(_translate("Dialog", "...", None))
        self.label_lineEdit_fich_destino.setText(_translate("Dialog", "Pasta de destino:", None))
        self.pushButton_Export.setText(_translate("Dialog", "Exportar", None))

