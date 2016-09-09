# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Mon Aug 22 21:49:43 2016
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

class Ui_Main_Window(object):
    def setupUi(self, Main_Window):
        Main_Window.setObjectName(_fromUtf8("Main_Window"))
        Main_Window.resize(552, 436)
        self.centralwidget = QtGui.QWidget(Main_Window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QgsMapCanvas(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 1000))
        self.widget.setStyleSheet(_fromUtf8("border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 3)
        self.pushButton_preview = QtGui.QPushButton(self.centralwidget)
        self.pushButton_preview.setObjectName(_fromUtf8("pushButton_preview"))
        self.gridLayout.addWidget(self.pushButton_preview, 2, 0, 1, 1)
        self.pushButton_converte = QtGui.QPushButton(self.centralwidget)
        self.pushButton_converte.setObjectName(_fromUtf8("pushButton_converte"))
        self.gridLayout.addWidget(self.pushButton_converte, 2, 1, 1, 1)
        self.pushButton_cancel = QtGui.QPushButton(self.centralwidget)
        self.pushButton_cancel.setEnabled(True)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.gridLayout.addWidget(self.pushButton_cancel, 2, 2, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMaximumSize(QtCore.QSize(1677, 30))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 3)
        Main_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Main_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 552, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        self.menuDatabase = QtGui.QMenu(self.menubar)
        self.menuDatabase.setObjectName(_fromUtf8("menuDatabase"))
        Main_Window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Main_Window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Main_Window.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(Main_Window)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        Main_Window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionImportXYZ = QtGui.QAction(Main_Window)
        self.actionImportXYZ.setObjectName(_fromUtf8("actionImportXYZ"))
        self.actionExit = QtGui.QAction(Main_Window)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionImportar = QtGui.QAction(Main_Window)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Map_flag.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImportar.setIcon(icon)
        self.actionImportar.setObjectName(_fromUtf8("actionImportar"))
        self.actionPreview = QtGui.QAction(Main_Window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Map_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreview.setIcon(icon1)
        self.actionPreview.setObjectName(_fromUtf8("actionPreview"))
        self.actionNew = QtGui.QAction(Main_Window)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionEdit = QtGui.QAction(Main_Window)
        self.actionEdit.setObjectName(_fromUtf8("actionEdit"))
        self.actionConnect = QtGui.QAction(Main_Window)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.action_GeoSearch = QtGui.QAction(Main_Window)
        self.action_GeoSearch.setObjectName(_fromUtf8("action_GeoSearch"))
        self.actionDataSearch = QtGui.QAction(Main_Window)
        self.actionDataSearch.setObjectName(_fromUtf8("actionDataSearch"))
        self.menuFile.addAction(self.actionImportXYZ)
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.action_GeoSearch)
        self.menuView.addAction(self.actionDataSearch)
        self.menuDatabase.addAction(self.actionConnect)
        self.menuDatabase.addAction(self.actionNew)
        self.menuDatabase.addAction(self.actionEdit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.toolBar.addAction(self.actionImportar)
        self.toolBar.addAction(self.actionPreview)

        self.retranslateUi(Main_Window)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), Main_Window.close)
        QtCore.QObject.connect(self.pushButton_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Main_Window.close)
        QtCore.QMetaObject.connectSlotsByName(Main_Window)

    def retranslateUi(self, Main_Window):
        Main_Window.setWindowTitle(_translate("Main_Window", "Bathy Map", None))
        self.pushButton_preview.setText(_translate("Main_Window", "Preview", None))
        self.pushButton_converte.setText(_translate("Main_Window", "Converter para LL WGS84 ", None))
        self.pushButton_cancel.setText(_translate("Main_Window", "Cancelar", None))
        self.menuFile.setTitle(_translate("Main_Window", "File", None))
        self.menuView.setTitle(_translate("Main_Window", "View", None))
        self.menuAbout.setTitle(_translate("Main_Window", "About", None))
        self.menuDatabase.setTitle(_translate("Main_Window", "Database", None))
        self.toolBar.setWindowTitle(_translate("Main_Window", "toolBar", None))
        self.actionImportXYZ.setText(_translate("Main_Window", "ImportXYZ", None))
        self.actionExit.setText(_translate("Main_Window", "Exit", None))
        self.actionImportar.setText(_translate("Main_Window", "Importar", None))
        self.actionImportar.setToolTip(_translate("Main_Window", "Importar ficheiro csv", None))
        self.actionPreview.setText(_translate("Main_Window", "Preview", None))
        self.actionPreview.setToolTip(_translate("Main_Window", "Ver mapa dos dados", None))
        self.actionNew.setText(_translate("Main_Window", "New", None))
        self.actionEdit.setText(_translate("Main_Window", "Edit", None))
        self.actionConnect.setText(_translate("Main_Window", "Connect", None))
        self.action_GeoSearch.setText(_translate("Main_Window", "GeoSearch", None))
        self.actionDataSearch.setText(_translate("Main_Window", "DataSearch", None))

from qgis.gui import QgsMapCanvas
import resources_rc
