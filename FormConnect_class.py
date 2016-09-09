# -*- coding: utf-8 -*-
# --------- Classe para ligar a base de dados
import psycopg2
from PyQt4 import QtGui
from formConnection import Ui_FormConnection

class FormConnect(QtGui.QWidget,Ui_FormConnection):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.window4 = None
        self.checkBox.setChecked(False)
        self
    def ligar(self):


        # ler os parâmetros a partir das caixas de texto ("Qt line edits")
        #
        a = self.lineEdit_1.text()
        b = self.lineEdit_2.text()
        c = self.lineEdit_3.text()
        d = self.lineEdit_4.text()
        t1=''
        print "Ligar-----------------"
        # colocar indicador de ligação à base de dados em desactivado
        self.checkBox.setChecked(False)
        try:
            # construir "connection string"
            # conn = psycopg2.connect("dbname='lidar' user='postgres' host='localhost' password='juba'")
            str_connect="dbname='" + b + "' user='" + c + "' host='" + a + "' password='" + d + "'"
            print str_connect
            conn = psycopg2.connect(str_connect)

            # indicador de ligação à base de dados activado
            self.checkBox.setChecked(True)
            cur = conn.cursor()

            cur.execute("SELECT * FROM spatial_ref_sys WHERE spatial_ref_sys.srtext LIKE '%Lisbon%';")
            #cur.execute('SELECT PostGIS_full_version();')
            ver = cur.fetchall()
            t1=''
            for linha in ver:
                t1 = t1 + str(linha[1]) + ' ' + str(linha[2]) + ' ' + str(linha[3]) +'\n'
            print t1
        except:
            if conn:
                print('ligado!, com erros... -------------------------------------')
            else:
                print "I am unable to connect to the database"


        finally:
            if conn:
                conn.close()

            if len(t1)>0:
                self.plainTextEdit.setPlainText(t1)

