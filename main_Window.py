# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Fri Mar 17 00:23:28 2017
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
        Main_Window.resize(972, 646)
        self.centralwidget = QtGui.QWidget(Main_Window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineEdit_MapInfo = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_MapInfo.setMinimumSize(QtCore.QSize(0, 32))
        self.lineEdit_MapInfo.setObjectName(_fromUtf8("lineEdit_MapInfo"))
        self.verticalLayout.addWidget(self.lineEdit_MapInfo)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QgsMapCanvas(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(500, 200))
        self.widget.setMaximumSize(QtCore.QSize(100000, 100000))
        self.widget.setBaseSize(QtCore.QSize(0, 0))
        self.widget.setStyleSheet(_fromUtf8("border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.widget_2 = QtGui.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(20, 10, 211, 221))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_preview = QtGui.QPushButton(self.centralwidget)
        self.pushButton_preview.setObjectName(_fromUtf8("pushButton_preview"))
        self.horizontalLayout.addWidget(self.pushButton_preview)
        self.pushButton_converte = QtGui.QPushButton(self.centralwidget)
        self.pushButton_converte.setObjectName(_fromUtf8("pushButton_converte"))
        self.horizontalLayout.addWidget(self.pushButton_converte)
        self.pushButton_cancel = QtGui.QPushButton(self.centralwidget)
        self.pushButton_cancel.setEnabled(True)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        Main_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Main_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 972, 26))
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
        self.toolBar.setMinimumSize(QtCore.QSize(0, 40))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        Main_Window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionImportXYZ = QtGui.QAction(Main_Window)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/mActionExplore.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImportXYZ.setIcon(icon)
        self.actionImportXYZ.setObjectName(_fromUtf8("actionImportXYZ"))
        self.actionExit = QtGui.QAction(Main_Window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/mActionNew.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionImport = QtGui.QAction(Main_Window)
        self.actionImport.setIcon(icon)
        self.actionImport.setObjectName(_fromUtf8("actionImport"))
        self.actionPreview = QtGui.QAction(Main_Window)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Map_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreview.setIcon(icon2)
        self.actionPreview.setObjectName(_fromUtf8("actionPreview"))
        self.actionNew = QtGui.QAction(Main_Window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/mActionExit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon3)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionEdit = QtGui.QAction(Main_Window)
        self.actionEdit.setObjectName(_fromUtf8("actionEdit"))
        self.actionConnect = QtGui.QAction(Main_Window)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/mActionZoomOut.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnect.setIcon(icon4)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.action_GeoSearch = QtGui.QAction(Main_Window)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/witch.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_GeoSearch.setIcon(icon5)
        self.action_GeoSearch.setObjectName(_fromUtf8("action_GeoSearch"))
        self.actionDataSearch = QtGui.QAction(Main_Window)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/abob.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDataSearch.setIcon(icon6)
        self.actionDataSearch.setObjectName(_fromUtf8("actionDataSearch"))
        self.actionPan = QtGui.QAction(Main_Window)
        self.actionPan.setCheckable(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/mActionPan.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPan.setIcon(icon7)
        self.actionPan.setObjectName(_fromUtf8("actionPan"))
        self.actionZoomIn = QtGui.QAction(Main_Window)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/mActionZoomIn.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon8)
        self.actionZoomIn.setObjectName(_fromUtf8("actionZoomIn"))
        self.actionZoomOut = QtGui.QAction(Main_Window)
        self.actionZoomOut.setIcon(icon4)
        self.actionZoomOut.setObjectName(_fromUtf8("actionZoomOut"))
        self.actionIdentify = QtGui.QAction(Main_Window)
        self.actionIdentify.setCheckable(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/mActionIdentify.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionIdentify.setIcon(icon9)
        self.actionIdentify.setObjectName(_fromUtf8("actionIdentify"))
        self.actionConfig = QtGui.QAction(Main_Window)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/selec_1.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConfig.setIcon(icon10)
        self.actionConfig.setObjectName(_fromUtf8("actionConfig"))
        self.actionSelect = QtGui.QAction(Main_Window)
        self.actionSelect.setCheckable(True)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/polig_5.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelect.setIcon(icon11)
        self.actionSelect.setObjectName(_fromUtf8("actionSelect"))
        self.menuFile.addAction(self.actionImportXYZ)
        self.menuFile.addAction(self.actionConfig)
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
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)
        self.toolBar.addAction(self.actionPan)
        self.toolBar.addAction(self.actionIdentify)
        self.toolBar.addAction(self.actionSelect)
        self.toolBar.addAction(self.actionImportXYZ)

        self.retranslateUi(Main_Window)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), Main_Window.close)
        QtCore.QObject.connect(self.pushButton_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Main_Window.close)
        QtCore.QMetaObject.connectSlotsByName(Main_Window)

    def retranslateUi(self, Main_Window):
        Main_Window.setWindowTitle(_translate("Main_Window", "MapX", None))
        self.pushButton_preview.setText(_translate("Main_Window", "Preview", None))
        self.pushButton_converte.setText(_translate("Main_Window", "Converter para LL WGS84 ", None))
        self.pushButton_cancel.setText(_translate("Main_Window", "Cancelar", None))
        self.menuFile.setTitle(_translate("Main_Window", "&File", None))
        self.menuView.setTitle(_translate("Main_Window", "&View", None))
        self.menuAbout.setTitle(_translate("Main_Window", "&About", None))
        self.menuDatabase.setTitle(_translate("Main_Window", "&Database", None))
        self.toolBar.setWindowTitle(_translate("Main_Window", "toolBar", None))
        self.actionImportXYZ.setText(_translate("Main_Window", "&ImportXYZ", None))
        self.actionExit.setText(_translate("Main_Window", "E&xit", None))
        self.actionImport.setText(_translate("Main_Window", "Importar", None))
        self.actionImport.setToolTip(_translate("Main_Window", "Importar ficheiro csv", None))
        self.actionPreview.setText(_translate("Main_Window", "Preview", None))
        self.actionPreview.setToolTip(_translate("Main_Window", "Ver mapa dos dados", None))
        self.actionNew.setText(_translate("Main_Window", "&New", None))
        self.actionEdit.setText(_translate("Main_Window", "&Edit", None))
        self.actionConnect.setText(_translate("Main_Window", "&Connect", None))
        self.action_GeoSearch.setText(_translate("Main_Window", "GeoSearch", None))
        self.actionDataSearch.setText(_translate("Main_Window", "&DataSearch", None))
        self.actionPan.setText(_translate("Main_Window", "Pan", None))
        self.actionZoomIn.setText(_translate("Main_Window", "ZoomIn", None))
        self.actionZoomOut.setText(_translate("Main_Window", "ZoomOut", None))
        self.actionIdentify.setText(_translate("Main_Window", "Identify", None))
        self.actionConfig.setText(_translate("Main_Window", "&Config", None))
        self.actionSelect.setText(_translate("Main_Window", "&Select", None))
        self.actionSelect.setToolTip(_translate("Main_Window", "Definir área rectg.", None))

from qgis.gui import QgsMapCanvas
import resources_rc
