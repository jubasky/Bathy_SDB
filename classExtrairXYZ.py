# -*- coding: utf-8 -*-

from os.path import isfile
from os import walk
from PyQt4.QtGui import QMessageBox
from formExtrairXYZ import Ui_Dialog

from classConfig import Config
from classDB import DB

from qgis.core import *
from PyQt4 import QtGui
from PyQt4.QtCore import *
import glob


# ------------------------------------------------------ Classe para gerir importação de dados
class ExtractXYZ(QtGui.QWidget, Ui_Dialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        print(" ---------------- class CorrigirExportMetadata: __init__")

        # ------------------------------------------------ Iniciar variáveis
        self.pasta_dxf = ''
        self.pasta_destino = ''
        self.lista_cdis = []
        self.lista_codigos = []
        self.lineEdit_bloco.setText('POSIC-SONDA_BL')
        self.bloco = self.lineEdit_bloco.text()
        # --------------------------------------------------- Ler constantes a partir de config.ini
        self.Config = Config('config.ini')

        # ----------------------------------------------   definir modelo básico para listView
        self.model = QtGui.QStandardItemModel(self.listViewCDI)

        # ---------------------------------- ligar botões a métodos
        self.connect(self.pushButton_Abrir_Pasta, SIGNAL("clicked()"), self.File_dialog_Abrir_Pasta)
        self.connect(self.pushButton_Abrir_Pasta_Destino, SIGNAL("clicked()"), self.File_dialog_Abrir_Pasta_Destino)
        self.connect(self.pushButton_Converter, SIGNAL("clicked()"), self.ExtrairDXF)
        self.connect(self.pushButton_Sel, SIGNAL("clicked()"), self.SeleccionarFicheiros)

        self.repaint()

    def ExtrairDXF(self):
        # -------------  percorrer lista de ficheiros dxf (versão 2000)  seleccionados
        # ------------- identificar blocos e respectivos x,y,z
        model = self.listViewCDI.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.checkState() == Qt.Checked:
                print 'item.text()=', item.text()
                ficheiro = item.text()
                f_in = open(ficheiro, 'r')
                ficheiro2 = ficheiro[:len(ficheiro)-3] + 'txt'
                f_out = open(ficheiro2, 'w')

        self.bloco = self.lineEdit_bloco.text()

        print 'self.bloco=', self.bloco

        n = 0
        flag_bloco = False
        linha_out = ''
        linha = f_in.readline()
        while linha:
            linha = f_in.readline()
            str_linha = str(linha).strip()
            if str(self.bloco) == str_linha:
                print linha, n
                linha = f_in.readline()
                str_linha = str(linha).strip()
                linha = f_in.readline()
                str_linha2 = str(linha).strip()

                if str_linha == '100' and  str_linha2 == 'AcDbPoint':
                    n +=1
                    # print 'ponto n=', n
                    # ---------------------- x

                    linha = f_in.readline()
                    linha = f_in.readline()

                    str_linha = str(linha).strip()
                    linha_out += str_linha + ', '
                    # ---------------------- y
                    linha = f_in.readline()
                    linha = f_in.readline()
                    str_linha = str(linha).strip()
                    linha_out += str_linha + ', '
                    # ---------------------- z
                    linha_out.replace('\r','')

                    linha = f_in.readline()
                    linha = f_in.readline()
                    str_linha = str(linha).strip()
                    linha_out += str_linha + '\n'
                    f_out.write(linha_out)
                    # print linha_out
                    linha_out = ''

        f_in.close()
        f_out.close()
        print 'terminado.'

    def SeleccionarFicheiros(self):

        model = self.listViewCDI.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == Qt.Unchecked:
                item.setCheckState(Qt.Checked)
            elif item.isCheckable() and item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)

    def MostrarDXF(self, caminho):
        print "MostrarDXF"
        lista_ficheiros = glob.glob(caminho + "*.dxf")
        print 'caminho=', caminho
        print 'lista_ficheiros=', lista_ficheiros
        n = 0
        #  ---------------------criar um item para cada ficheiro xml
        for f in lista_ficheiros:
            item = QtGui.QStandardItem(f)

            # adicionar checkbox
            item.setCheckable(True)

            # adicionar o item ao modelo
            self.model.appendRow(item)
            n += 1

        # Aplicar o modelo à ListView
        self.listViewCDI.setModel(self.model)
        self.label_Num_Ficheiros.setText(u'Nº ficheiros: ' + str(n))

    def File_dialog_Abrir_Pasta(self):
        # ------------------------- criar "Dialog" de abertura de ficheiros
        # ------------------------- para seleccionar pasta de leitura de ficheiros a corrigir
        fd = QtGui.QFileDialog(self)
        # -------------- preparar filtro para ficheiros do tipo dxf
        a = "Open DXF files"
        b = 'c:/'
        c = "DXF Files (*.dxf);;All Files (*)"
        d =  fd.getOpenFileNameAndFilter (self, "Escolher pasta", b, c)
        print ("self.File_dialog_Abrir_Pasta=", self.pasta_dxf)
        # -------------------------------------------------------- actualiza Label com novo path + ficheiro
        self.lineEdit_Lista_Ficheiros.setText(self.pasta_dxf)
        self.lineEdit_Lista_Ficheiros.setToolTip(self.pasta_dxf)
        lista_aux =  d[0].split('/')
        m = len(lista_aux)-1
        n = 0
        caminho = ''
        for linha in lista_aux:
            if n < m:
                caminho += linha + '/'
                n +=1
        print 'caminho =', caminho
        self.pasta_dxf = caminho
        self.MostrarDXF(self.pasta_dxf)

    def File_dialog_Abrir_Pasta_Destino(self):
        # ------------------------- criar "Dialog" de abertura de ficheiros
        # ------------------------- para seleccionar pasta de destino de ficheiros corrigidos
        fd = QtGui.QFileDialog(self)
        # -------------- preparar filtro para ficheiros do tipo xml
        a = "Open XML files"
        b = 'c:/MapX/xml/'
        c = "XML Files (*.xml);;All Files (*)"
        d = fd.getExistingDirectory(self, "Escolher pasta de destinor", "c:/MapX/xml/", QtGui.QFileDialog.ShowDirsOnly)
        self.pasta_destino = d
        print ("self.File_dialog_Abrir_Pasta_Destino=", self.pasta_destino)

        # -------------------------------------------------------- actualiza Label com novo path + ficheiro
        self.lineEdit_Pasta_Destino.setText(d)
        self.lineEdit_Pasta_Destino.setToolTip(d)


