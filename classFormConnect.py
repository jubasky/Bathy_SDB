# -*- coding: utf-8 -*-
# --------- Classe para testar ligação a base de dados
import psycopg2
from PyQt4 import QtGui
from formConnection import Ui_FormConnection
from classConfig import Config

class FormConnect(QtGui.QWidget,Ui_FormConnection):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.pathConfig = 'config.ini'

        # --------------------------------------------------- Ler constantes a partir de config.ini
        self.Config = Config('config.ini')

        self.lineEdit_Host.setText(self.Config.Host)
        self.lineEdit_Db.setText(self.Config.Db)
        self.lineEdit_User.setText(self.Config.User)
        self.lineEdit_Passwd.setText(self.Config.Passwd)

        self.checkBox.setChecked(False)
        self.pushButtonLigar.clicked.connect(self.ligar)

        self.repaint()

    def ligar(self):
        # ---------------------------------------------ler os parâmetros a partir das caixas de texto
        strHost = self.lineEdit_Host.text()
        strDb = self.lineEdit_Db.text()
        strUser = self.lineEdit_User.text()
        strPasswd = self.lineEdit_Passwd.text()
        print "Ligar-----------------"

        # ------------------------------------------- desactivar indicador de ligação à base de dados em
        self.checkBox.setChecked(False)
        conn = None
        try:
            # --------------------------------------------------------------construir "connection string"
            str_connect="dbname='" + strDb + "' user='" + strUser + "' host='" + strHost + "' password='" \
                        + strPasswd + "'"
            print str_connect
            conn = psycopg2.connect(str_connect)
            # ------------------------------------ activar indicador de ligação à base de dados
            self.checkBox.setChecked(True)
            cur = conn.cursor()
            cur.execute('SELECT version();')
            ver = cur.fetchall()
            t1=''
            for linha in ver:
                t1 = t1 + str(linha[0])
            print t1

            # ---------------------------- em caso de sucesso na ligação à base de dados
            # ---------------------------- modificar config.ini para definir esta bd como a inicial
            self.actualizar_config_db(strDb)
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

    def actualizar_config_db(self, novaDB):
        # ------------------------------------- função para actualizar config.ini
        self.Config.Db = novaDB
        # ------------------------------------- falta escrever...

