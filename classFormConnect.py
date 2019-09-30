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

        # --------------------------------------------------- Inicializar atributos
        self.strHost = ""
        self.strDb = ""
        self.strUser = ""
        self.strPasswd = ""
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
        self.strHost = self.lineEdit_Host.text()
        self.strDb = self.lineEdit_Db.text()
        self.strUser = self.lineEdit_User.text()
        self.strPasswd = self.lineEdit_Passwd.text()

        print "Ligar-----------------"

        # ------------------------------------------- desactivar indicador de ligação à base de dados em
        self.checkBox.setChecked(False)
        conn = None
        try:
            # -----self.--------------------------------------------------------construir "connection string"
            str_connect="dbname='" + self.strDb + "' user='" + self.strUser + "' host='" + self.strHost + "' password='" \
                        + self.strPasswd + "'"
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
                print "Não foi possível ligar à BD."
        finally:
            if conn:
                conn.close()
            if len(t1)>0:
                self.plainTextEdit.setPlainText(t1)

    def actualizar_config_db(self, novaDB):
        # ------------------------------------- função para actualizar config.ini
        self.Config.Db = novaDB
        # ------------------------------------- falta escrever...


    def GravarConfig(self):
        resultado = False
        try:
            with open(self.pathConfig, 'w') as f:
                f.write(self.User + '\n')
                f.write(self.Passwd + '\n')
                f.write(self.Host + '\n')
                f.write(self.Port + '\n')
                f.write(self.Db + '\n')
                f.write(self.Path + '\n')
                f.write(self.PathQ + '\n')
            f.close()
            resultado = True
        except:
            print('classConstantes -----------------> erro ao gravar Config.ini !!!')
        finally:
            return resultado