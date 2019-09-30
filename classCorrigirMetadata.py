# -*- coding: utf-8 -*-

from os.path import isfile
from os import walk
from PyQt4.QtGui import QMessageBox
from formCorrigirMetadata import Ui_Dialog

from classConfig import Config
from classDB import DB

from qgis.core import *
from PyQt4 import QtGui
from PyQt4.QtCore import *


# ------------------------------------------------------ Classe para gerir importação de dados
class CorrigeMetadata(QtGui.QWidget, Ui_Dialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        print(" ---------------- class CorrigirExportMetadata: __init__")

        # ------------------------------------------------ Iniciar variáveis
        self.pasta_xml = ''
        self.pasta_destino = ''
        self.lista_cdis = []
        self.lista_codigos = []

        # _____________________________________________________ Preencher combo Box's
        Lista=['0: Unknown or > 500m', '1: between 500m and 50m', '2: between 50m and 20m ',
               '3: < 20m ' ]
        self.comboBox_Horiz.addItems(Lista)

        Lista = ['0: Unknown, plummet, leadline', '1: SBES Low Frequency, SDB', '2: MBES low frequency',
                 '3: Lidar, SBES High Frequency', '4: MBES High frequency']
        self.comboBox_Vert.addItems(Lista)

        Lista = ['0: Purpose  unknown ', '1: Transit/opportunity',
                 '2: Bathymetric/morphologic survey',
                 '3: Hydrographic survey']
        self.comboBox_Purpose.addItems(Lista)

        # -------------------------------------- estabelecer valores por defeito para as combos
        self.comboBox_Horiz.setCurrentIndex(3)
        self.comboBox_Vert.setCurrentIndex(3)
        self.comboBox_Purpose.setCurrentIndex(3)

        # --------------------------------------------------- Ler constantes a partir de config.ini
        self.Config = Config('config.ini')

        # ----------------------------------------------   definir modelo básico para listView
        self.model = QtGui.QStandardItemModel(self.listViewCDI)

        # ---------------------------------- ligar botões a métodos
        self.connect(self.pushButton_Abrir_Pasta, SIGNAL("clicked()"), self.File_dialog_Abrir_Pasta)
        self.connect(self.pushButton_Abrir_Pasta_Destino, SIGNAL("clicked()"), self.File_dialog_Abrir_Pasta_Destino)
        self.connect(self.pushButtonCorrigir, SIGNAL("clicked()"), self.GravarMetadadosCorrigidos)
        self.connect(self.pushButton_Sel, SIGNAL("clicked()"), self.SeleccionarFicheiros)

        self.repaint()

    def SeleccionarFicheiros(self):

        model = self.listViewCDI.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == Qt.Unchecked:
                item.setCheckState(Qt.Checked)
            elif item.isCheckable() and item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)

    def MostrarXML(self, caminho):
        print "MostrarXML"
        lista_ficheiros = []
        for (caminho, pastas, ficheiros) in walk(caminho):
            lista_ficheiros.extend(ficheiros)
            break

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
        # -------------- preparar filtro para ficheiros do tipo xml
        caminho = self.LerIni_Fic_Input()

        # -------------- preparar filtro para ficheiros do tipo xml
        a = "Open XML files"
        c = "XML Files (*.xml);;All Files (*)"
        d =  fd.getExistingDirectory (self, "Escolher pasta", caminho, QtGui.QFileDialog.ShowDirsOnly)
        self.pasta_xml = d
        print ("self.File_dialog_Abrir_Pasta=", self.pasta_xml)

        # -------------------------------------------------------- actualiza Label com novo path + ficheiro
        self.lineEdit_Lista_Ficheiros.setText(d)
        self.lineEdit_Lista_Ficheiros.setToolTip(d)

        self.MostrarXML(d)

        self.GravarIni_Fich_Input(d)

    def File_dialog_Abrir_Pasta_Destino(self):
        # ------------------------- criar "Dialog" de abertura de ficheiros
        # ------------------------- para seleccionar pasta de destino de ficheiros corrigidos
        fd = QtGui.QFileDialog(self)
        # -------------- preparar filtro para ficheiros do tipo xml
        caminho = self.LerIni_Fic_Output()

        self.pasta_destino = caminho
        d = fd.getExistingDirectory(self, "Escolher pasta de destinor", caminho, QtGui.QFileDialog.ShowDirsOnly)
        self.GravarIni_Fich_Output(d)
        print ("self.File_dialog_Abrir_Pasta_Destino=", d)

        # -------------------------------------------------------- actualiza Label com novo path + ficheiro
        self.lineEdit_Pasta_Destino.setText(d)
        self.lineEdit_Pasta_Destino.setToolTip(d)

    def LerIni_Fic_Input(self):
        # -------------- ler ultima localização utilizada (c:/MapX/caminhos/folder_xml.ini)
        lista = []
        try:
            f_in = open('c:/MapX/caminhos/folder_xml_in.ini', 'r')
            for linha in f_in:
                lista.append(linha)
            f_in.close()
        except:
            pass
        print 'lista=', lista

        caminho = ''
        if len(lista) > 0:
            caminho = lista[0]
            print 'caminho = ', caminho

        return caminho

    def GravarIni_Fich_Input(self, caminho):
        # -------------------- actualiza ficheiro *.ini
        try:
            f_in = open('c:/MapX/caminhos/folder_xml_in.ini', 'w')
            f_in.write(caminho)
            f_in.close()
        except:
            pass

    def LerIni_Fic_Output(self):
        # -------------- ler ultima localização utilizada (c:/MapX/caminhos/folder_xml.ini)
        lista = []
        try:
            f_in = open('c:/MapX/caminhos/folder_xml_out.ini', 'r')
            for linha in f_in:
                lista.append(linha)
            f_in.close()
        except:
            pass
        print 'lista=', lista

        caminho = ''
        if len(lista) > 0:
            caminho = lista[0]
            print 'caminho = ', caminho

        return caminho

    def GravarIni_Fich_Output(self, caminho):
        # -------------------- actualiza ficheiro *.ini
        try:
            f_in = open('c:/MapX/caminhos/folder_xml_out.ini', 'w')
            f_in.write(caminho)
            f_in.close()
        except:
            pass

    def GravarMetadadosCorrigidos(self):

        lista_QI=[]
        lista_QI.append(self.comboBox_Horiz.currentText()[0])
        lista_QI.append(self.comboBox_Vert.currentText()[0] )
        lista_QI.append(self.comboBox_Purpose.currentText()[0])
        print lista_QI

        model = self.listViewCDI.model()
        for index in range(model.rowCount()):
            item = model.item(index)

            if item.isCheckable() and item.checkState() == Qt.Checked:
                nome_fich = str(item.text())
                sucesso = self.Set_QIndex_and_XYZ(nome_fich, self.pasta_destino, lista_QI)

    def Set_QIndex(self, ficheiro, pasta_destino, lista):

        print(u'Set_QIndex:', ficheiro, pasta_destino, lista)
        fich_destino = pasta_destino + "//" + ficheiro
        print(u'destino:', fich_destino)
        # -------------------------------- Abrir ficheiro para copiar
        # -------------------------------- info original, acrescentando
        # -------------------------------- Indices de Qualidade (QI)
        f_in = open(self.pasta_xml+'//'+ ficheiro, 'r')
        ft_in = open(self.Config.Path + '/xml/template_qi.xml', 'r')
        f_out = open(fich_destino, 'w')
        n = 0
        pesquisa = '<gmd:lineage>'

        for line in f_in:
            n += 1
            str_text = line
            # ---------------------------------- se a linha começar por '<gmd:lineage>'
            # ---------------------------------- acabámos de passar o bloco de Info de Qualidade
            if str_text.find(pesquisa) > -1:
                m = 0

                # ------------------------ escreve mais três registos com info de Qualidade
                for linha in ft_in:

                    m += 1
                    if m < 23:
                        f_out.write(linha)
                    elif m == 23:
                        # substituir codigo de QI_Horizontal
                        inicio = linha.find('<gco:CharacterString>')
                        str_espacos = ''
                        str_espacos += ' ' * inicio
                        novo_codigo = str_espacos + '<gco:CharacterString>' + str(lista[0]) + '</gco:CharacterString>'
                        f_out.write(novo_codigo)
                        f_out.write('\n')

                    elif m > 23 and m < 54:
                        f_out.write(linha)
                    elif m == 54:
                        # substituir codigo de QI_Vertical
                        inicio = linha.find('<gco:CharacterString>')
                        str_espacos = ''
                        str_espacos += ' ' * inicio
                        novo_codigo = str_espacos + '<gco:CharacterString>' + str(lista[1]) + '</gco:CharacterString>'
                        f_out.write(novo_codigo)
                        f_out.write('\n')
                    elif m > 54 and m < 85:
                        f_out.write(linha)
                    elif m == 85:
                        # substituir texto de QI_Purpose
                        # encontrar   <gco:CharacterString>
                        inicio = linha.find('<gco:CharacterString>')
                        str_espacos = ''
                        str_espacos += ' ' * inicio
                        novo_codigo = str_espacos + '<gco:CharacterString>' + str(lista[2]) + '</gco:CharacterString>'
                        f_out.write(novo_codigo)
                        f_out.write('\n')

                    elif m > 85:
                        f_out.write(linha)
                        espacos = len(linha)-len(linha.strip())

                # escreve a linha original (inicio do ultimo bloco de informação)
                str_espacos = ''
                str_espacos += ' ' * abs(espacos-3)
                # f_out.write(str_text)
                f_out.write(str_espacos + '<gmd:lineage>\n')

            else:

                f_out.write(str_text)

        f_in.close()
        ft_in.close()
        f_out.close()

        del f_in
        del f_out
        del ft_in

    def Set_QIndex_and_XYZ(self, ficheiro, pasta_destino, lista):

        print(u'Set_QIndex:', ficheiro, pasta_destino, lista)
        fich_destino = pasta_destino + "//" + ficheiro
        print(u'destino:', fich_destino)

        # -------------------------------- Abrir ficheiro para copiar
        # -------------------------------- info original, acrescentando
        # -------------------------------- Indices de Qualidade (QI)
        f_in = open(self.pasta_xml+'//'+ ficheiro, 'r')
        ft_in = open(self.Config.Path + '/xml/template_qi.xml', 'r')
        ff_in = open(self.Config.Path + '/xml/template_format.xml', 'r')
        f_out = open(fich_destino, 'w')
        n = 0
        pesquisa = '<gmd:lineage>'
        pesquisa2 = '<gmd:distributionFormat>'
        pesquisa3 = 'codeListValue="LAB32"'
        contador = 0
        flag_format = False

        for line in f_in:
            n += 1
            str_text = line
            # ---------------------------------- se a linha começar por '<gmd:lineage>'
            # ---------------------------------- acabámos de passar o bloco de Info de Qualidade
            if str_text.find(pesquisa) > -1:
                m = 0
                # ------------------------ escreve mais três registos com info de Qualidade
                for linha in ft_in:
                    m += 1
                    if m < 23:
                        f_out.write(linha)
                    elif m == 23:
                        # substituir codigo de QI_Horizontal
                        inicio = linha.find('<gco:CharacterString>')
                        str_espacos = ''
                        str_espacos += ' ' * inicio
                        novo_codigo = str_espacos + '<gco:CharacterString>' + str(lista[0]) + '</gco:CharacterString>'
                        f_out.write(novo_codigo)
                        f_out.write('\n')

                    elif m > 23 and m < 54:
                        f_out.write(linha)

                    elif m == 54:
                        # substituir codigo de QI_Vertical
                        inicio = linha.find('<gco:CharacterString>')
                        str_espacos = ''
                        str_espacos += ' ' * inicio
                        novo_codigo = str_espacos + '<gco:CharacterString>' + str(lista[1]) + '</gco:CharacterString>'
                        f_out.write(novo_codigo)
                        f_out.write('\n')
                    elif m > 54 and m < 85:
                        f_out.write(linha)
                    elif m == 85:
                        # substituir texto de QI_Purpose
                        # encontrar   <gco:CharacterString>
                        inicio = linha.find('<gco:CharacterString>')
                        str_espacos = ''
                        str_espacos += ' ' * inicio
                        novo_codigo = str_espacos + '<gco:CharacterString>' + str(lista[2]) + '</gco:CharacterString>'
                        f_out.write(novo_codigo)
                        f_out.write('\n')

                    elif m > 85:
                        f_out.write(linha)
                        espacos = len(linha)-len(linha.strip())

                # escreve a linha original (inicio do ultimo bloco de informação)
                str_espacos = ''
                str_espacos += ' ' * abs(espacos-3)
                # f_out.write(str_text)
                f_out.write(str_espacos + '<gmd:lineage>\n')

            elif str_text.find(pesquisa2) > -1:
                flag_format = True

                # ------------------- escreve conteudo de template_format.xml
                for linha_f in ff_in:
                    f_out.write(str(linha_f))

            elif str_text.find(pesquisa3) > -1:
                f_out.write('<sdn:SDN_DeviceCategoryCode codeSpace="SeaDataNet"  codeListValue="185"  codeList="http://vocab.nerc.ac.uk/isoCodelists/sdnCodelists/cdicsrCodeList.xml#SDN_DeviceCategoryCode" >sound velocity sensors</sdn:SDN_DeviceCategoryCode>\n')

            elif flag_format and contador < 9:
                contador += 1

            # .------------------------------------------ Actualizar Revision date
            elif n == 171:
                f_out.write('                           <gco:Date>2017-10-16</gco:Date>\n')

            else:
                flag_format = False
                contador = 0

                f_out.write(str_text)

        f_in.close()
        ft_in.close()
        ff_in.close()
        f_out.close()

        del f_in
        del f_out
        del ft_in
        del ff_in

        return True