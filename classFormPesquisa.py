# -*- coding: utf-8 -*-
# --------- Classe para gerir form de pesquisa
import psycopg2

from PyQt4.QtCore import Qt
from PyQt4 import QtGui
from PyQt4.QtGui import QApplication

from FormPesquisa import Ui_FormPesquisa
from classDB import DB
from classConfig import Config


class FormPesquisa(QtGui.QDialog, Ui_FormPesquisa):

    def __init__(self,tv, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.x1 = 0.0
        self.x2 = 0.0
        self.y1 = 0.0
        self.y2 = 0.0
        self.Config = Config('config.ini')
        self.tv = tv

        # --------------------------------------------------- ligar botões a funções
        self.pushButtonOk.clicked.connect(self.iniciarPesquisa)

        self.db_acess = DB()
        self.db_acess.set_connection(self.Config.Conn)
        self.db_acess.ligar()
        ver = self.db_acess.ler_sql("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = 'cdi';")

        self.db_acess.desligar()
        self.db_acess = None
        lista = []
        for linha in ver:
            a = str(linha)

            a = a.translate(None, "',()")
            b = a.split(' ')
            lista.append(b[0] + ' (' + b[1]+')')
        self.listWidget.addItems(lista)

        print ("version = ", psycopg2.__version__)


    def iniciarPesquisa(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        print('iniciar pesquisa')
        self.db_acess = DB()
        self.db_acess.set_connection(self.Config.Conn)
        self.db_acess.ligar()
        strSql = "delete from patches_sel;"
        self.db_acess.execute_sql(strSql)

        strSql = "INSERT INTO patches_sel SELECT  cdi, id, pa FROM patches WHERE PC_Intersects(pa, ST_SetSRID(ST_MakePolygon(ST_GeomFromText('LINESTRING("
        strSql += str(self.x1) + " " + str(self.y1) + ", " + str(self.x2) + " " + str(self.y1) +  ", "
        strSql +=  str(self.x2) + " " + str(self.y2) + ", "
        strSql += str(self.x1) + " " + str(self.y2) + ", " + str(self.x1) + " " + str(self.y1) +")')),4326));"
        print strSql

        self.db_acess.execute_sql(strSql)
        self.db_acess.desligar()
        self.db_acess = None

        self.tv.mostrarResultado()
        QApplication.restoreOverrideCursor()
        self.close()

    def set_cantos(self, x1,x2,y1,y2):
        print("FormPesquisa x1=",x1)
        self.lineEdit_LongMin.setText(str(x1))
        self.lineEdit_LongMax.setText(str(x2))
        self.lineEdit_LatMin.setText(str(y1))
        self.lineEdit_LatMax.setText(str(y2))
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.repaint()



