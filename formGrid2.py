# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formGrid2.ui'
#
# Created: Sun Aug 28 00:36:45 2016
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

class Ui_formGrid(object):
    def setupUi(self, formGrid):
        formGrid.setObjectName(_fromUtf8("formGrid"))
        formGrid.resize(861, 735)
        self.centralwidget = QtGui.QWidget(formGrid)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widgetMap = QgsMapCanvas(self.centralwidget)
        self.widgetMap.setObjectName(_fromUtf8("widgetMap"))
        self.gridLayout.addWidget(self.widgetMap, 0, 0, 1, 5)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 4, 1, 1, QtCore.Qt.AlignRight)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        formGrid.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(formGrid)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 861, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        formGrid.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(formGrid)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        formGrid.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(formGrid)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        formGrid.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(formGrid)
        QtCore.QMetaObject.connectSlotsByName(formGrid)

    def retranslateUi(self, formGrid):
        formGrid.setWindowTitle(_translate("formGrid", "MainWindow", None))
        self.pushButton.setText(_translate("formGrid", "PushButton", None))
        self.pushButton_2.setText(_translate("formGrid", "PushButton", None))
        self.toolBar.setWindowTitle(_translate("formGrid", "toolBar", None))

from qgis.gui import QgsMapCanvas
