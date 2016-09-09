# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formT.ui'
#
# Created: Sun Oct 18 01:43:23 2015
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

class Ui_formT(object):
    def setupUi(self, formT):
        formT.setObjectName(_fromUtf8("formT"))
        formT.resize(495, 434)
        self.widgetMap = QgsMapCanvas(formT)
        self.widgetMap.setGeometry(QtCore.QRect(80, 70, 341, 291))
        self.widgetMap.setObjectName(_fromUtf8("widgetMap"))

        self.retranslateUi(formT)
        QtCore.QMetaObject.connectSlotsByName(formT)

    def retranslateUi(self, formT):
        formT.setWindowTitle(_translate("formT", "Form", None))

from qgis.gui import QgsMapCanvas
