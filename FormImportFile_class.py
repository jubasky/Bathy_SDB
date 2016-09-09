# -*- coding: utf-8 -*-
from os.path import isfile
import fileinput
from PyQt4 import QtGui
import csv
from PyQt4.QtGui import *
from FormImportFile import Ui_DialogImport
from converterCSV_WGS84 import ConverterCSV_WGS84
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# ---------------------- Classe para criar FormImportFile
class FormImportFile(QtGui.QWidget, Ui_DialogImport):


    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.ficheiro_orig=''
        self.epsg=""
        self.sql_dir ='c:/MapX/scripts/'
        self.sql_connection = 'sql_connection.sql'
        self.sql_insert_patches ='sql_insert_into_patches.sql'
        print("class FormImportFile: __init__")
        self.convertButton.clicked.connect(self.converter)
        self.importButton.clicked.connect(self.importar)
        self.pushButtonAbrirFicheiro.clicked.connect(self.File_dialog)

        # num de linhas max. a ler, para amostra
        self.n_p = 15

    def File_dialog(self):

        # criar "Dialog" de abertura de ficheiros
        fd = QtGui.QFileDialog(self)
        # preparar leitura de ficheiros do tipo csv (x,y,z,i)
        a="Open Csv files"
        b=''
        c="CSV Files (*.csv);;All Files (*)"
        self.filename = fd.getOpenFileName(self, a, b, c)

        # ler as primeiras n_p linhas do ficheiro seleccionado
        separador=self.cboSep.currentText()
        if isfile(self.filename):
            n=0
            text=""
            for line in fileinput.input([ self.filename ]):
                n+=1
                text=text+line
                if n > self.n_p:
                    break
            print('line=',line)
            n_col=0
            list1=[]

            for r in line:
                if r==separador:
                    n_col +=1
                    list1.append(str(n_col))
            list1.append(str(n_col+1))
            print('line=',line,'n_col=',n_col)
            fileinput.close()
            print('list1=',list1)
            # preencher widget textEdit com as primeiras 10 linhas
            self.textEdit.setText(text)
            self.lineEdit.setText(self.filename)
            self.epsg=  "3763"
            # self.lista_epsg[self.cboDatumHz.currentIndex()]
            print('class FormImportFile: epsg=',self.epsg)
            # preencher widgets QCombo com os indices possiveis
            # quantas colunas ?
            #

            self.cboX.clear()
            self.cboX.addItems(list1)
            self.cboY.setCurrentIndex(0)
            self.cboY.clear()
            self.cboY.addItems(list1)
            self.cboY.setCurrentIndex(1)
            self.cboZ.clear()
            self.cboZ.addItems(list1)
            self.cboZ.setCurrentIndex(2)

            if len(list1)>3:
                self.cboReflect.addItems(list1)
                self.cboReflect.setCurrentIndex(3)
            if len(list1)>4:
                self.cboR.addItems(list1)
                self.cboR.setCurrentIndex(4)
            if len(list1)>5:
                self.cboG.addItems(list1)
                self.cboG.setCurrentIndex(5)
            if len(list1)>6:
                self.cboB.addItems(list1)
                self.cboB.setCurrentIndex(6)


    def converter(self):

        d=ConverterCSV_WGS84()
        list_epsg=['27493','5018','3763', '32629','4326']
        epsg_code_1 =list_epsg[self.cboDatumHz.currentIndex()]

        n1=self.cboX.currentIndex()
        n2=self.cboY.currentIndex()
        n3=self.cboZ.currentIndex()

        print('------------ >filename=', self.filename )

        if isfile(self.filename):
            ficheiro_1 = self.filename
            ficheiro_2 = ficheiro_1[0:-3] + "bt1"
            epsg_code_2 = '4326'
            print('class: FormImportFile: converter, fich1=', ficheiro_1, 'epsg_1=',epsg_code_1,'fich_2=', ficheiro_2)
            d.converter3(ficheiro_1, epsg_code_1, ficheiro_2, epsg_code_2,n1,n2,n3)

    def importar(self):
        print('class: FormImportFIle_class: importar')

        # verifica se os dados estao em wgs84 LL
        if self.cboDatumHz.currentIndex()<>4:
            print(u'Datum diferente de WGS84. Importação terminada !!')
            print(self.cboDatumHz.currentIndex())

            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(u'Datum diferente de WGS84. Importação terminada !!')

            self.msg.setWindowTitle(u'Importação:')
            self.msg.setDetailedText("The details are as follows:")
            self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            self.msg.show()
            print('Importar ------------------------ KO !!')
            return


        # Ler parametros de ligação à BD
        # Ler parametros de ligação à BD
        with open(self.sql_dir + self.sql_connection, 'r') as f:
            str_connect = f.read().decode("utf-8-sig").encode("utf-8")
        f.closed

        # str_connect="dbname='" + b + "' user='" + c + "' host='" + a + "' password='" + d + "'"
        print str_connect
        conn = psycopg2.connect(str_connect)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        strSql = 'DELETE FROM pontos_temp;'
        print(" *************** FormImportFile_class:  self.filename=",self.filename)
        strSql = strSql + "COPY pontos_temp (x, y, z, i, r, g, b) FROM '" + self.filename + "' WITH CSV HEADER;"
        strSql = strSql + "UPDATE pontos_temp SET geom = ST_SetSRID(ST_MakePoint(x,y,z),4326);"
        print("**************************** FormImportFile_class: import: strSql=",strSql)
        try:
            cur.execute(strSql)
        except:
            print(u'FormImportFile Erro:__________________ COPY pontos_temp ')
        finally:
            pass

        cur.close()
        conn.close()


        conn = psycopg2.connect(str_connect)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        strSql = 'DELETE FROM pc_points; INSERT INTO pc_points (pt) SELECT PC_MakePoint(3, ARRAY[a,bb,c,intensity,r,g,b]) FROM (SELECT x as a, y as bb, z as c, 10 AS intensity, r ,g, b FROM pontos_temp) AS values;'


        print("**************************** FormImportFile_class: import: strSql=",strSql)

        try:
            cur.execute(strSql)
        except:
            print(u'FormImportFile Erro:__________________ INSERT INTO pc_points ')
        finally:
            pass

        cur.close()
        conn.close()
        # -------------------------------------------------- criar Patches a partir de PC_points
        # Ler script para criar Patches
        with open(self.sql_dir + self.sql_insert_patches, 'r') as f:
            strSql = f.read().decode("utf-8-sig").encode("utf-8")
        f.closed

        conn = psycopg2.connect(str_connect)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        print("**************************** FormImportFile_class: import: strSql=",strSql)

        try:
            cur.execute(strSql)
        except:
            print(u'FormImportFile Erro:__________________ INSERT INTO patches')
        finally:
            pass

        cur.close()
        conn.close()

        print('Importar ------------------------ OK')
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Importar ------------------------ OK")
        self.msg.setInformativeText("This is additional information")
        self.msg.setWindowTitle("MapX -Info")
        self.msg.setDetailedText("The details are as follows:")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.show()

