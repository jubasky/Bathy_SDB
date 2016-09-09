# -*- coding: utf-8 -*-

# módulo correspondente à gestão do programa principal e da
# respectiva janela window1 (Qt), Ui_Main_Window

import sys
import os
from qgis.gui import *
from qgis.core import *
from PyQt4 import QtGui
from PyQt4 import QtCore

# carregar as diferentes "forms", para assegurar
# as funcionalidades do programa
#
from main_Window import Ui_Main_Window
from FormImportFile_class import FormImportFile
from FormConnect_class import FormConnect

from formImp import Ui_formImp
from converterCSV_WGS84 import ConverterCSV_WGS84

from classFormNewDatabase import FormNewDB

from classGridLayer import GridLayer
from classDB_Admin import DB_Admin

class Mensagem(QtGui.QWidget, Ui_formImp):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        a = ConverterCSV_WGS84
        self.label.text = a.ficheiro



class StartQT4(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # ------------- implementar a UI definida pela form Main_Window (Qt)
        self.ui = Ui_Main_Window()
        self.ui.setupUi(self)

        # ------------- inicializar objectos windows1...windows4
        # -------------
        self.window1 = None
        self.window2 = None
        self.window3 = None
        self.window4 = None

        # ---------------- inicializar atributos da class
        self.filename = ""
        self.file_epsg = ""

        self.fich_transf = ""
        self.preview_filename = ""


        # ------------------------------------------------------------------------------
        # ------------------------  ligação de "sinais" da UI a "slots" da classe
        # ------------------------------------------------------------------------------
        # ------------ Menus:
        QtCore.QObject.connect(self.ui.actionImportXYZ, QtCore.SIGNAL("activated()"), self.File_Input)
        QtCore.QObject.connect(self.ui.actionConnect, QtCore.SIGNAL("activated()"), self.Connect_dialog)
        QtCore.QObject.connect(self.ui.actionNew, QtCore.SIGNAL("activated()"), self.CriarDB)

        # ------------ Botões
        self.ui.pushButton_preview.clicked.connect(self.ver_resumo)
        self.ui.pushButton_converte.clicked.connect(self.CriarDB)

        # --------------- mapa global
        shapefile = "C:/data/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp"
        self.layer1 = QgsVectorLayer(shapefile, "world", "ogr")

        # --------- começar o programa mostrando ao utilizador
        # --------- um mapa base
        self.Mostrar_mapa_base()

    def ver_resumo(self):
        print("ver_resumo, FILE=", self.window2.filename)
        # coloca o nome do ficheiro csv  a ler a partir de uma
        # propriedade da form de Importação de Dados anteriormente mostrada

        self.filename=self.window2.filename
        self.file_epsg=self.window2.epsg
        print("filename=",self.filename)
        print("file_epsg=",self.window2.epsg)

        if os.path.isfile(self.filename):
            b=ConverterCSV_WGS84()


            # AAAAAAAAAAAAAKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKLLLLLLLLLLLLLLLLLLLLLLLLLLL
            b.resumo2(self.filename,int(self.file_epsg),4326)

            self.preview_filename=b.fich_sample
            print "preview_filename=" , self.preview_filename
            self.Mostrar_mapa()

    def converte(self):
        # coloca o nome do ficheiro csv  a ler a partir de uma
        # propriedade da form de Importação de Dados
        self.filename=self.window2.filename
        print("StartQT4: converte")
        if os.path.isfile(self.filename):
            print("StartQT4: converte, filename=",self.filename )
            self.fich_transf=self.filename[0:-3] + "bt1"
            #----------------------- ---- Criar form ConverterCSV_WGS84
            b=ConverterCSV_WGS84()
            b.set_ficheiro_csv(self.filename)
            b.converter(self.filename, 3763, self.fich_transf, 4326)

    def Mostrar_mapa(self):
        canvas =  self.ui.widget
        canvas.useImageToRender(False)
        canvas.show()

        # ------------- Ler dados a partir de ficheiro csv(x,y,z)
        uri = "file:///" + self.preview_filename
        uri = uri + "?type=csv&xField=x&yField=y&spatialIndex=no&subsetIndex=no&watchFile=no"
        print uri
        layer = QgsVectorLayer(uri, self.preview_filename, "delimitedtext")

        if not layer.isValid():
            raise IOError("Ficheiro invalido.")

        QgsMapLayerRegistry.instance().addMapLayer(layer)
        QgsMapLayerRegistry.instance().addMapLayer(self.layer1)
        canvas.setExtent(layer.extent())
        canvas.setLayerSet([ QgsMapCanvasLayer(layer),QgsMapCanvasLayer(self.layer1)])

    def Mostrar_mapa_base(self):
        canvas =  self.ui.widget
        canvas.useImageToRender(False)
        canvas.show()

        QgsMapLayerRegistry.instance().addMapLayer(self.layer1)
        canvas.setExtent(self.layer1.extent())
        canvas.setLayerSet([ QgsMapCanvasLayer(self.layer1)])



    def File_Input(self):
        # ------------------- criar FormInputFile ------
        self.window2 = None
        if self.window2 is None:
            self.window2 = FormImportFile()

        self.window2.show()
        print("file_input",)

        self.file_epsg=self.window2.epsg


    def Connect_dialog(self):
        # ---------------------------------------------------------------------
        # ------------------- criar formConnect -------------------------------
        # ------------------- primeiro, destruir alguma window3 pre-existente
        self.window3 = None
        if self.window3 is None:
            self.window3 = FormConnect()
        self.window3.show()
        self.window3.ligar()


    # ----------------- carregar janela para definição de grid (partições)
    def CriarDB(self):

        self.bb=FormNewDB()
        self.bb.show()
        self.bb.criar2()

if __name__ == '__main__':
    QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
    QgsApplication.initQgis()
    app = QtGui.QApplication(sys.argv)
    # ------------------------------------
    # criar a janela principal do programa
    myapp = StartQT4()
    myapp.show()
    # ------------------------------------
    sys.exit(app.exec_())
    QgsApplication.exitQgis()