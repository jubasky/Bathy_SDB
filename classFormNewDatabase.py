# -*- coding: utf-8 -*-
# --------- Classe para ligar a base de dados
from PyQt4 import QtGui
from FormNewDatabase import Ui_FormNewDatabase
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import fileinput


class FormNewDB(QtGui.QWidget,Ui_FormNewDatabase):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.window4 = None
        self.sql_dir = 'c:/MapX/scripts/'
        self.sql_create_db='sql_create_db.sql'

    def criar(self):


        # ler os parâmetros a partir das caixas de texto ("Qt line edits")
        self.lineEdit_1.setText('localhost')
        self.lineEdit_2.setText('postgres')
        self.lineEdit_3.setText('postgres')
        self.lineEdit_4.setText('juba')
        a = self.lineEdit_1.text()
        b = self.lineEdit_2.text()
        c = self.lineEdit_3.text()
        d = self.lineEdit_4.text()
        t1=''
        print "Ligar-----------------"



        # construir "connection string"
        # conn = psycopg2.connect("dbname='lidar' user='postgres' host='localhost' password='juba'")
        str_connect="dbname='" + b + "' user='" + c + "' host='" + a + "' password='" + d + "'"
        print str_connect
        conn = None
        conn = psycopg2.connect(str_connect)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        nova='teste'
        # ----------------------------------------------------------------------------------------- CRIAR BASE DADOS
        try:
            cur.execute('CREATE DATABASE ' + nova)

        except:
            print('Erro -------------------------------- CRIAR DB')
        finally:
            cur.close()
            conn.close()
        # ---------------------------------------------------------------------------- Ligar a base dados por defeito
        str_connect="dbname='" + nova + "' user='" + c + "' host='" + a + "' password='" + d + "'"
        print str_connect
        conn = None
        conn = psycopg2.connect(str_connect)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
                # --------------------------------------------------------------------- Testar Ligação
        # #cur.execute("SELECT * FROM spatial_ref_sys WHERE spatial_ref_sys.srtext LIKE '%Lisbon%';")
        cur.execute("select version();")
        ver = cur.fetchall()
        t1=''
        m=0
        n=0
        for linha in ver:
            n += 1
            for aa in linha:
                t1 = t1 + str(aa) +'\n'
                m += 1
        print t1,n,m
        # --------------------------------------------------------------------- extensão postgis
        try:
            strSql="create extension postgis;"
            cur.execute(strSql)
        except:
            print(u'Erro ao criar  extensão postgis ___________________________')
        finally:
            pass
        # --------------------------------------------------------------------- extensão postgis_topology
        try:
            strSql="create extension postgis_topology;"
            cur.execute(strSql)
        except:
            print(u'Erro ao criar  extensão postgis_topology ___________________________')
        finally:
            pass
        # --------------------------------------------------------------------- extensão pointcloud
        try:
            strSql="create extension pointcloud;"
            cur.execute(strSql)
        except:
            print('Erro ao criar  extensao pointcloud ___________________________')
        finally:
            pass
        # --------------------------------------------------------------------- extensão postgis_postgis
        try:
            strSql="create extension pointcloud_postgis;"
            cur.execute(strSql)
        except:
            print(u'Erro ao criar  extensão pointcloud_postgis ___________________________')

        finally:
            pass
        # ------------------------------------------------------------ criar novo tipo de point para PointCloud
        self.sql_dir='c:/MapX/scripts/'
        self.sql_criar_pointcloud_3='sql_criar_pointcloud_3.sql'
        read_data=''

        with open(self.sql_dir+self.sql_criar_pointcloud_3, 'r') as f:
            read_data = f.read().decode("utf-8-sig").encode("utf-8")

        f.closed

        print("classFormNewDatabase - read_data =",read_data)
        #  Limpar read_data  de caracteres de formatação etc.
        cc=read_data.replace('\n','')
        cc=cc.replace('      ', '')
        print("classFormNewDatabase - read_data filtrado=",cc)
        try:

            cur.execute(cc)
        except:
            print(u'classFormNewDatabase Erro: criar novo tipo de point para PointCloud ')

        finally:
            pass

        # -------------------------------------------------------------------- Criar tabela pontos_temp
        self.sql_create_table_pontos_temp='sql_create_table_pontos_temp.sql'

        with open(self.sql_dir+self.sql_create_table_pontos_temp, 'r') as f:
            read_data = f.read().decode("utf-8-sig").encode("utf-8")
        f.closed

        print("classFormNewDatabase - read_data =",read_data)
        #  Limpar read_data  de caracteres de formatação etc.
        cc=read_data.replace('\n',' ')
        cc=cc.replace('      ', '')
        cc=cc.replace('\\', ' ')

        print("classFormNewDatabase - read_data filtrado=",cc)

        try:
            cur.execute(cc)
        except:
            print(u'classFormNewDatabase Erro: criar pontos_temp ')
        finally:
            pass


        cur.close()
        conn.close()


    def criar2(self):


        # ler os parâmetros a partir das caixas de texto ("Qt line edits")
        self.lineEdit_1.setText('localhost')
        self.lineEdit_2.setText('postgres')
        self.lineEdit_3.setText('postgres')
        self.lineEdit_4.setText('juba')
        a = self.lineEdit_1.text()
        b = self.lineEdit_2.text()
        c = self.lineEdit_3.text()
        d = self.lineEdit_4.text()
        t1=''
        print "Ligar-----------------"



        # construir "connection string"
        # conn = psycopg2.connect("dbname='lidar' user='postgres' host='localhost' password='juba'")
        str_connect="dbname='" + b + "' user='" + c + "' host='" + a + "' password='" + d + "'"
        print str_connect
        conn = None
        conn = psycopg2.connect(str_connect)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        nova='teste'
        # ----------------------------------------------------------------------------------------- CRIAR BASE DADOS
        try:
            cur.execute('CREATE DATABASE ' + nova)

        except:
            print('Erro -------------------------------- CRIAR DB')
        finally:
            cur.close()
            conn.close()
        # ---------------------------------------------------------------------------- Ligar a base dados por defeito
        str_connect="dbname='" + nova + "' user='" + c + "' host='" + a + "' password='" + d + "'"
        print str_connect
        conn = None
        conn = psycopg2.connect(str_connect)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
                # --------------------------------------------------------------------- Testar Ligação
        # #cur.execute("SELECT * FROM spatial_ref_sys WHERE spatial_ref_sys.srtext LIKE '%Lisbon%';")
        cur.execute("select version();")
        ver = cur.fetchall()
        t1=''
        m=0
        n=0
        for linha in ver:
            n += 1
            for aa in linha:
                t1 = t1 + str(aa) +'\n'
                m += 1
        print t1,n,m

        # -------------------------------------------------------------------- Criar db


        with open(self.sql_dir+self.sql_create_db, 'r') as f:
            read_data = f.read().decode("utf-8-sig").encode("utf-8")
        f.closed

        print("classFormNewDatabase - read_data =",read_data)
        #  Limpar read_data  de caracteres de formatação etc.
        cc=read_data.replace('\n',' ')
        cc=cc.replace('      ', '')
        cc=cc.replace('\\', ' ')

        print("classFormNewDatabase - read_data filtrado=",cc)

        try:
            cur.execute(cc)
        except:
            print(u'classFormNewDatabase Erro: criar dbp ')
        finally:
            pass


        cur.close()
        conn.close()
