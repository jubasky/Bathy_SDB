# -*- coding: utf-8 -*-

from os.path import isfile

from PyQt4.QtGui import QMessageBox
from FormExportMetadata import Ui_Dialog
from classConfig import Config
from classDB import DB

from qgis.core import *
from PyQt4 import QtGui
from PyQt4.QtCore import *

import xml.etree.ElementTree as ET


# ------------------------------------------------------ Classe para gerir exporação de metadados
class ExportMetadata(QtGui.QWidget, Ui_Dialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        print(" ---------------- class ExportMetadata: __init__")
        self.lista_cdis = []
        self.lista_codigos = []
        self.metadados = []

        # --------------------------------------------------- Ler constantes a partir de config.ini
        self.Config = Config('config.ini')

        # ----------------------------------------------   definir modelo básico para listView
        model = QtGui.QStandardItemModel(self.listViewCDI)

        # ------------------------------------------------ Iniciar variáveis
        self.filename_template = ''
        self.filename_save = ''


        # ------------------------ Ler lista de paises e codigos
        self.LerListaPaises()

        # ----------------------------------------------- criar lista de cdis
        self.lista_cdis, self.lista_codigos = self.LerCdis()
        print self.lista_cdis
        print self.lista_codigos

        n = 0
        # ---------------------criar um item com codigo e descrição para cada cruzeiro
        for cdi in self.lista_cdis:
            item = QtGui.QStandardItem(cdi + ' - ' + self.lista_codigos[n])

            # adicionar checkbox
            item.setCheckable(True)

            # adicionar o item ao modelo
            model.appendRow(item)
            n += 1

        # Aplicar o modelo à ListView
        self.listViewCDI.setModel(model)
        self.repaint()

        self.label_Fich_Template.setText('C:/Dados_bat/EMODNET/Set_2017/Templates/3288_SB_TEMPLATE_POL.xml')
        self.lineEdit_Fich_Destino.setText('C:/Dados_bat/EMODNET/Set_2017/Teste_Export_XML/')



        # ---------------------------------- ligar botões a métodos
        self.connect(self.pushButton_OK, SIGNAL("clicked()"), self.GravarMetadados)
        self.connect(self.pushButton_Sel_Template, SIGNAL("clicked()"), self.File_dialog_template)
        self.connect(self.pushButton_Sel_Fich_Dest, SIGNAL("clicked()"), self.File_dialog_save)
        self.connect(self.pushButton_Export, SIGNAL("clicked()"), self.GravarMetadados)


    def GravarMetadados(self):

        print "GravarMetaDados"
        # for cdi in self.lista_cdis:
        str_cdi=[]
        model = self.listViewCDI.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == Qt.Checked:
                print "item.text()=",item.text()
                str_cdi = item.text().split('-')
                #
                print "str_cdi[0]=", str_cdi[0]
                print "str_cdi[1]=", str_cdi[1]
                self.LerMeta(str_cdi[0])
                self.GravarXML(str_cdi[0])

    def File_dialog_template(self):
        # ------------------------- criar "Dialog" de abertura de ficheiros
        # ------------------------- para seleccionar "template"
        fd = QtGui.QFileDialog(self)
        # -------------- preparar filtro para ficheiros do tipo xml
        a = "Open XML files"
        b = 'c:/MapX/xml/'
        c = "XML Files (*.xml);;All Files (*)"
        self.filename_template = fd.getOpenFileName(self, a, b, c)
        print ("self.filename_template=", self.filename_template)
        mensagem = self.filename_template

        # ------------------------------------------- verifica se o path escolhido corresponde a ficheiro válido
        if not (isfile(self.filename_template)):
            mensagem += ' não corresponde a um ficheiro existente !!!'
            QMessageBox(self, 'Exportar metadados: ', mensagem)
            return
        else:
            # -------------------------------------------------------- actualiza Label com novo path + ficheiro
            self.label_Fich_Template.setText(self.filename_template)

    def File_dialog_save(self):
        # ------------------------- criar "Dialog" de abertura de ficheiros
        # ------------------------- para seleccionar "template"
        fd = QtGui.QFileDialog(self)
        # -------------- preparar filtro para ficheiros do tipo xml
        a = "Open XML files"
        b = 'c:/MapX/xml/'
        c = "XML Files (*.xml);;All Files (*)"
        self.filename_save = fd.getExistingDirectory (self, "Open a folder", "", QtGui.QFileDialog.ShowDirsOnly)
        print ("self.filename_save=", self.filename_save)

        # -------------------------------------------------------- actualiza Label com novo path + ficheiro
        self.lineEdit_Fich_Destino.setText(self.filename_save)

    def LerCdis(self):
        print "ler cdis"
        ligacao = DB()

        ligacao.set_connection(self.Config.Conn)
        ligacao.ligar()
        resultado = ligacao.ler_sql("SELECT id, codigo FROM patches_info ORDER BY id")
        lista_cdi = []
        lista_cod = []
        for linha in resultado:
            a = str(linha)
            a = a.replace("'", "")
            a = a.replace("(", "")
            a = a.replace(")", "")
            campos = a.split(",")
            lista_cdi.append(campos[0])
            lista_cod.append(campos[1])

        ligacao.desligar()
        ligacao = None

        return lista_cdi, lista_cod

    def LerMeta(self,cdi):

        # ----------------------------- Função para ler metadados a partir da base de dados.
        # ----------------------------- Compõe o nome do ficheiro xml a criar a partir do campo
        # ----------------------------- "codigo" e do codigo EDMO do dono dos dados
        ligacao = DB()

        ligacao.set_connection(self.Config.Conn)
        ligacao.ligar()
        str_sql = "SELECT cdi.id, cdi.codigo, cdi.min_depth, "
        str_sql += "cdi.max_depth, cdi.start_date, cdi.end_date, cdi.unid_tempo, "
        str_sql += "cdi.abstract, cdi.platform_class, cdi.holding_centre, cdi.originator, cdi.distributor, "
        str_sql += "cdi.collate_centre, cdi.data_size, cdi.data_access, cdi.cruise_name, "
        str_sql += "cdi.cruise_id, cdi.qc_desc, cdi.qc_date, cdi.qc_comment, cdi.qc_status, "
        str_sql += "cdi.revision_date, cdi.long_w, cdi.long_e, cdi.lat_n, cdi.lat_s "
        str_sql += "FROM cdi  "
        str_sql += "WHERE cdi.id = " + cdi + ";"
        print str_sql

        resultado = ligacao.ler_sql(str_sql)
        campos = []
        for a in resultado[0]:
            campos.append(str(a).strip())

        ligacao.desligar()
        ligacao = None

        print "----------------- campos = " , campos

        self.nome_fich = campos[1]
        print "----------------------- self.nome_fich = ", self.nome_fich

        # ----------------------------------------- tratar campos de data/hora
        datahora = QDateTime.fromString(campos[4][0:19], 'yyyy-MM-dd hh:mm:ss').toString('yyyy/MM/dd hh:mm:ss')
        print "campos[4] antes=" , campos[4]
        campos[4] = datahora.strip('u')
        print  "campos[4] depois=" , campos[4]

        datahora = QDateTime.fromString(campos[5][0:19], 'yyyy-MM-dd hh:mm:ss').toString('yyyy/MM/dd hh:mm:ss')
        print "campos[5] antes=", campos[5]
        campos[5] = datahora.strip('u')
        print "campos[5] depois=", campos[5]

        datahora = QDateTime.fromString(campos[18][0:19], 'yyyy-MM-dd hh:mm:ss').toString('yyyy/MM/dd hh:mm:ss')
        print "campos[18] antes=", campos[18]
        campos[18] = datahora.strip('u')
        print "campos[18] depois=", campos[18]

        datahora = QDateTime.fromString(campos[21][0:19], 'yyyy-MM-dd hh:mm:ss').toString('yyyy/MM/dd hh:mm:ss')
        print "campos[21] antes=", campos[21]
        campos[21] = datahora.strip('u')
        print "campos[21] depois=", campos[21]

        self.metadados = campos
        print "self.metadados = ",self.metadados

        # ler info de Entidades

        self.Lista_Contacto = self.LerXML(campos[9])
        print "Lista_Contacto=", self.Lista_Contacto

        self.Lista_Origem = self.LerXML(campos[10])
        print "Lista_Origem=", self.Lista_Origem

        self.Lista_Distrib = self.LerXML(campos[11])
        print "Lista_Distrib=", self.Lista_Distrib

        self.Lista_Collate = self.LerXML(campos[12])
        print "Lista_Collate=", self.Lista_Collate


    def GravarXML(self, cdi):
        fich_template = self.label_Fich_Template.text()
        fich_xml = self.lineEdit_Fich_Destino.text()  + self.nome_fich + '.xml'
        print "fich_xml=", fich_xml
        f = open(fich_template, 'r')
        t = open(fich_xml, 'w')

        n = 0

        for line in f:
            n += 1
            str_text = unicode(line)
            texto = ''

            if n == 6:
                # ------------------------------------- Codigo CDI descritivo = nome_dataset
                # --------------------------Prever correcção de nomes com sufixo do IPMA (3288)
                nome_dataset =string.replace(self.metadados[1], "3288_", "")

                str_text = string.replace(str_text, "SB_TEMPLATE_POL", nome_dataset)
                print(n,str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 23:
                # -------------------------------- Dados datacentre "collate"
                texto = '"'+ self.Lista_Collate[0] + '" '
                texto += '>' + self.Lista_Collate[1]

                str_text = string.replace(str_text, '"4" >Dove Marine Laboratory, University of Newcastle upon Tyne', texto)
                print(n,str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 30:
                # -------------------------------- Dados datacentre "collate" - morada
                texto2 = u"Hi!"
                texto2 = self.Lista_Collate[4]

                str_text = string.replace(str_text, 'Cullercoats   ', texto2)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 33:
                # -------------------------------- Dados datacentre "collate"
                texto2 = u"Hi!"
                texto2 = self.Lista_Collate[5]

                str_text = string.replace(str_text, 'North Shields', texto2)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 36:
                # -------------------------------- Dados datacentre "collate"
                if self.Lista_Collate[7] == None:
                    texto2 =  ''
                else:
                    texto2 = self.Lista_Collate[7]

                str_text = string.replace(str_text, 'NE30 4PZ', texto2)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 39:
                # -------------------------------- Dados datacentre "collate": País e Codigo de País
                if self.Lista_Collate[8] == None:
                    texto2 =  ''
                else:
                    texto2 = self.Lista_Collate[8]
                    texto2 = texto2.strip()
                    # --------------- determinar codigo de pais em função do nome
                    codigo_pais = self.ListaPaises[texto2]

                str_text = string.replace(str_text, 'United Kingdom', texto2)
                str_text = string.replace(str_text, 'GB', codigo_pais)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 42:
                # -------------------------------- Dados datacentre "distributor: email"
                if self.Lista_Collate[9] == None:
                    texto2 =  ''
                else:
                    texto2 = self.Lista_Collate[9]

                str_text = string.replace(str_text, 'sdn-userdesk@seadatanet.org', texto2)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 153:
                str_text = string.replace(str_text, "SB_TEMPLATE_POL", nome_dataset)
                t.write(str_text)

            elif n == 156:
                str_text = string.replace(str_text, "SB_TEMPLATE_POL", nome_dataset)
                t.write(str_text)

            elif n == 171:
                str_text = string.replace(str_text, "SB_TEMPLATE_POL", nome_dataset)
                t.write(str_text)

            elif n == 178:
                # -------------------------------- Dados datacentre "originator"
                texto = '"' + self.Lista_Origem[0] + '" '
                texto += '>' + self.Lista_Origem[1]
                str_text = string.replace(str_text, '"2" >University of Cambridge Department of Earth Sciences',
                                          texto)
                t.write(str_text.encode('utf-8'))

            elif n== 185:
                # -------------------------------- Dados datacentre "originator" - morada
                texto = u'olá'
                texto = self.Lista_Origem[4]
                str_text = string.replace(str_text, 'Downing Street  ', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n== 188:
                # -------------------------------- Dados datacentre "originator" - cidade
                texto = self.Lista_Origem[5]
                str_text = string.replace(str_text, 'Cambridge', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))
            elif n == 191:
                # -------------------------------- Dados datacentre "originator" - Cod Postal
                texto = self.Lista_Origem[7]
                str_text = string.replace(str_text, 'CB2 3EQ', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))
            elif n == 194:
                # -------------------------------- Dados datacentre "originator": País e Codigo de País
                if self.Lista_Origem[8] == None:
                    texto = ''
                else:
                    texto = self.Lista_Origem[8]
                    texto = texto.strip()
                    # --------------- determinar codigo de pais em função do nome
                    codigo_pais = self.ListaPaises[texto]

                str_text = string.replace(str_text, 'United Kingdom', texto)
                str_text = string.replace(str_text, 'GB', codigo_pais)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 197:
                # -------------------------------- Dados datacentre "originator: email"
                if self.Lista_Origem[9] == None:
                    texto = ''
                else:
                    texto = self.Lista_Origem[9]

                str_text = string.replace(str_text, 'jaj2@cam.ac.uk', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 218:
                # ----------------------------------------- Resumo (abstract)
                a = "Abstract"
                abstract_dataset = self.metadados[7]
                str_text = string.replace(str_text, a, abstract_dataset)
                t.write(str_text)

            elif n == 204:
                # -------------------------------- Dados datacentre "originator: Online resource"
                texto = ''
                str_text = string.replace(str_text, 'http://www.esc.cam.ac.uk', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 223:
                # -------------------------------- Dados datacentre "contacto"
                texto = '"' + self.Lista_Contacto[0] + '" '
                texto += '>' + self.Lista_Contacto[1]
                str_text = string.replace(str_text, '"2475" >University of Duisburg-Essen, Applied Zoology/Hydrobiology',
                                          texto)
                t.write(str_text.encode('utf-8'))

            elif n == 230:
                # -------------------------------- Dados datacentre "contacto" - telef
                if self.Lista_Contacto[2] == None:
                    texto = ''
                else:
                    texto =  self.Lista_Contacto[2]

                str_text = string.replace(str_text,'+49-201-183 3189', texto)
                t.write(str_text.encode('utf-8'))
            elif n == 233:
                # -------------------------------- Dados datacentre "contacto" - fax
                if self.Lista_Contacto[3] == None:
                    texto = ''
                else:
                    texto =  self.Lista_Contacto[3]

                str_text = string.replace(str_text,'+49-201-183 2179', texto)
                t.write(str_text.encode('utf-8'))
            elif n == 240:
                # -------------------------------- Dados datacentre "contacto" - Morada
                if self.Lista_Contacto[4] == None:
                    texto = ''
                else:
                    texto = self.Lista_Contacto[4]

                str_text = string.replace(str_text, 'Universitaetsstrasse 5', texto)
                t.write(str_text.encode('utf-8'))
            elif n == 243:
                # -------------------------------- Dados datacentre "contacto" - Cidade
                if self.Lista_Contacto[5] == None:
                    texto = ''
                else:
                    texto = self.Lista_Contacto[5]

                str_text = string.replace(str_text, 'Essen', texto)
                t.write(str_text.encode('utf-8'))
            elif n == 246:
                # -------------------------------- Dados datacentre "contacto" - Cod Postal
                if self.Lista_Contacto[7] == None:
                    texto = ''
                else:
                    texto = self.Lista_Contacto[7]

                str_text = string.replace(str_text, '45141', texto)
                t.write(str_text.encode('utf-8'))
            elif n == 249:
                # -------------------------------- Dados datacentre "contacto": País e Codigo de País
                if self.Lista_Contacto[8] == None:
                    texto = ''
                else:
                    texto = self.Lista_Contacto[8]
                    texto = texto.strip()
                    # --------------- determinar codigo de pais em função do nome
                    codigo_pais = self.ListaPaises[texto]

                str_text = string.replace(str_text, 'Germany', texto)
                str_text = string.replace(str_text, 'DE', codigo_pais)
                t.write(str_text.encode('utf-8'))

            elif n == 252:
                # -------------------------------- Dados datacentre "contacto: email"
                if self.Lista_Contacto[9] == None:
                    texto = ''
                else:
                    texto = self.Lista_Contacto[9]

                str_text = string.replace(str_text, 'sdn-userdesk@seadatanet.org', texto)
                t.write(str_text.encode('utf-8'))
            elif n == 259:
                # -------------------------------- Dados datacentre "contato: Online resource"
                texto = ''
                str_text = string.replace(str_text, 'http://www.uni-due.de/hydrobiology/', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 452:
                # ------------------------------------ nome cruzeiro
                a = "TEMPLATE_NAME"
                str_text = string.replace(str_text, a, self.metadados[15])
                t.write(str_text.encode('utf-8'))

            elif n == 455:
                # ------------------------------------ ID cruzeiro
                a = "TEMPLATE_ID"
                str_text = string.replace(str_text, a, self.metadados[16])
                t.write(str_text.encode('utf-8'))

            elif n == 460:
                # ----------------------------------- data ini cruzeiro
                nova_data = self.metadados[4]
                nova_data = string.replace(nova_data,'/','-')
                str_text = string.replace(str_text, "2004-09-28", nova_data[0:10])
                t.write(str_text)

            elif n == 491:
                # ----------------------------------------------------------- mbr_w
                nova_data = self.metadados[22]
                str_text = string.replace(str_text, "-10.0", nova_data)
                t.write(str_text)

            elif n == 494:
                nova_data = self.metadados[23]
                str_text = string.replace(str_text, "-6.5", nova_data)
                t.write(str_text)
            elif n == 497:
                nova_data = self.metadados[24]
                str_text = string.replace(str_text, "34.1", nova_data)
                t.write(str_text)
            elif n == 500:
                nova_data = self.metadados[25]
                str_text = string.replace(str_text, "36.1", nova_data)
                t.write(str_text)

            elif n == 514:
                # ---------------------------------------- bounding box
                # '                                          <gml:posList>'
                x_min = self.metadados[22]
                y_min = self.metadados[24]
                x_max = self.metadados[23]
                y_max = self.metadados[25]

                str_poligono = '                                          <gml:posList>'
                str_poligono += x_min + ' ' + y_max + ' '
                str_poligono += x_min + ' ' + y_min + ' '
                str_poligono += x_max + ' ' + y_min + ' '
                str_poligono += x_max + ' ' + y_max + ' '
                str_poligono += x_min + ' ' + y_max + '</gml:posList>' + '\n'

                t.write(str_poligono)

                # n_linhas = 0
                # # --------------- inserir polig_nome_dataset.txt
                # ff = open(self.path_trab2 + 'polig_' + nome_fich + '.txt', 'r')
                # for linha in ff:
                #     t.write('<gml:posList>' + linha + '</gml:posList>')
                #     n_linhas += 1
                # ff.close
                # print("n. de fiadas inseridas=", n_linhas)

            elif n == 527:
                # ---------------------------------------------------- data ini
                nova_data = self.metadados[4]
                nova_data = string.replace(nova_data, '/', '-')
                a = nova_data[0:10] + 'T' + nova_data[11:21]
                str_text = string.replace(str_text, "2004-09-28T00:00:00", a)
                t.write(str_text)

            elif n == 528:
                # ---------------------------------------------------- data Fim
                nova_data = self.metadados[5]
                nova_data = string.replace(nova_data, '/', '-')
                a = nova_data[0:10] + 'T' + nova_data[11:21]

                str_text = string.replace(str_text, "2004-10-07T00:00:00", a)
                t.write(str_text)

            elif n == 536:
                # -------------------------------....................--- minimum depth
                a = self.metadados[2]
                b= int(float(a))
                nova_data = str(b)
                str_text = string.replace(str_text, "704", nova_data)
                t.write(str_text)
            elif n == 539:
                # ........................................................maximum depth
                a = self.metadados[3]
                b = int(float(a))
                nova_data = str(b)
                str_text = string.replace(str_text, "5189", nova_data)
                t.write(str_text)
            elif n == 590:
                # -------------------------------- Dados datacentre "distributor"
                texto = '"' + self.Lista_Distrib[0] + '" '
                texto += '>' + self.Lista_Distrib[1]
                str_text = string.replace(str_text,'"3" >Culterty Field Station, University of Aberdeen', texto)
                t.write(str_text.encode('utf-8'))

            elif n == 607:
                # -------------------------------- Dados datacentre "distributor" - morada
                if self.Lista_Distrib[4] == None:
                    texto = ''
                else:
                    texto = self.Lista_Distrib[4]

                str_text = string.replace(str_text, 'Newburgh  ', texto)
                t.write(str_text.encode('utf-8'))

            elif n == 610:
                # -------------------------------- Dados datacentre "distributor" - cidade
                if self.Lista_Distrib[5] == None:
                    texto = ''
                else:
                    texto = self.Lista_Distrib[5]

                str_text = string.replace(str_text, 'Aberdeen', texto)
                t.write(str_text.encode('utf-8'))
            elif n == 613:
                # -------------------------------- Dados datacentre "distributor" - cod_postal
                if self.Lista_Distrib[7] == None:
                    texto = ''
                else:
                    texto = self.Lista_Distrib[7]

                str_text = string.replace(str_text, 'AB25 3AA', texto)
                t.write(str_text.encode('utf-8'))

            elif n == 616:
                # -------------------------------- Dados datacentre "distributor" - pais + codigo
                if self.Lista_Distrib[8] == None:
                    texto = ''
                else:
                    texto = self.Lista_Distrib[8]
                    texto = texto.strip()
                    # --------------- determinar codigo de pais em função do nome
                    codigo_pais = self.ListaPaises[texto]

                str_text = string.replace(str_text, 'United Kingdom', texto)
                str_text = string.replace(str_text, 'GB', codigo_pais)
                t.write(str_text.encode('utf-8'))

            elif n == 619:
                # -------------------------------- Dados datacentre "distributor: email"
                if self.Lista_Distrib[9] == None:
                    texto = ''
                else:
                    texto = self.Lista_Distrib[9]

                str_text = string.replace(str_text, 'sdn-userdesk@seadatanet.org', texto)
                t.write(str_text.encode('utf-8'))

            elif n == 626:
                # -------------------------------- Dados datacentre "distributor: Online resource"
                texto = ''
                str_text = string.replace(str_text, 'http://www.abdn.ac.uk/zoology/cfs.htm', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 642:
                # ------------------------------------------- Tamanho em MB
                texto = self.metadados[13]
                if int(texto)<1:
                    texto ='1'

                str_text = string.replace(str_text, '9177', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 708:
                # ------------------------------------------  QC name
                # QC_NAME
                texto = self.metadados[17]
                str_text = string.replace(str_text, 'QC_NAME', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            elif n == 713:
                # ------------------------------------------  QC date
                # QC_NAME
                nova_data = self.metadados[18]
                nova_data = string.replace(nova_data, '/', '-')
                a = nova_data[0:10]
                str_text = string.replace(str_text, '2001-01-01', a)
                t.write(str_text.encode('utf-8'))

            elif n == 723:
                # ------------------------------------------  QC comment
                # QC_NAME
                if self.metadados[19] == None:
                    texto = ''
                else:
                    texto = self.metadados[19]

                str_text = string.replace(str_text, 'QC_COMMENT', texto)
                print(n, str_text)
                t.write(str_text.encode('utf-8'))

            else:
                t.write(str_text)

        f.close
        t.close

        del f
        del t
        # del ff

        print("Acabei !!!!")



    def LerXML(self, entidade_id):
        Lista_Entidade = []
        nome_ficheiro = self.Config.Path + "/scripts/SDN_EDMO_CORRIGIDO.xml"
        # print "nome_ficheiro = ", nome_ficheiro

        tree = ET.parse(nome_ficheiro)
        root = tree.getroot()
        # print(root[0][0]).attrib
        n=0
        for child in root:

            # print " ------------------------------------------------"
            # print child.tag, child.attrib, child.text
            # print (child[0]).tag, (child[0]).attrib['SDNIdent'], (child[0]).text
            c= (child[0]).attrib['SDNIdent']
            c=string.strip(c)

            if c == 'SDN:EDMO::' + entidade_id:
                Lista_Entidade.append(entidade_id)
                Lista_Entidade.append((child[0]).text)
                # ------------------------ Telefone + fax
                for a in child[1][0]:
                    # voiceNum = a.find('voiceNum').text
                    # print a.tag, a.attrib, a.text
                    Lista_Entidade.append(a.text)

                # ------------------- Morada
                for a in child[1][1]:
                    # print a.tag, a.attrib, a.text
                    Lista_Entidade.append(a.text)

                break

        return Lista_Entidade

    def LerListaPaises(self):
        # --------------------- definir dictonario para info de paises (nome + codigo)
        self.ListaPaises = {}

        # encoding = 'utf-8'
        with open(self.Config.Path + '/scripts/Lista_Paises.txt') as f:

            print "LerListaPaises"

            for line in f:
                str_text = str(line)
                a= str_text.split(';')
                self.ListaPaises[a[0]] = a[1].strip('\n')

        f.close

        print len(self.ListaPaises),self.ListaPaises
        del f
