# -*- coding: utf-8 -*-
# --------- Classe para testar ligação a base de dados
import psycopg2
from PyQt4 import QtGui
from FormConfig import Ui_FormConfig
from classConfig import Config
from PyQt4.QtGui import QMessageBox
import os.path


class FormConfig(QtGui.QDialog, Ui_FormConfig):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.pathConfig = 'config.ini'

        # --------------------------------------------------- Ler constantes a partir de config.ini
        self.Config = Config('config.ini')

        self.lineEdit_Host.setText(self.Config.Host)
        self.lineEdit_Db.setText(self.Config.Db)
        self.lineEdit_Port.setText(self.Config.Port)
        self.lineEdit_User.setText(self.Config.User)
        self.lineEdit_Passwd.setText(self.Config.Passwd)
        self.lineEdit_PathScripts.setText(self.Config.Path)
        self.lineEdit_QPath.setText(self.Config.PathQ)

        # --------------------------------------------------- definir propriedades da classe
        self.PathScripts = self.Config.Path

        # --------------------------------------------------- ligar botões a funções
        self.pushButton_path.clicked.connect(self.abrirPath)
        self.pushButton_testConn.clicked.connect(self.ligar)
        self.pushButton_Ok.clicked.connect(self.actualizarConfig)

        # ------------------------------------------- inicialmente, desactivar botão OK, só após teste de ligação
        #  ------------------------------------------ bem sucedido é que pode ficar activado
        self.pushButton_Ok.setEnabled(False)
        self.repaint()

    def abrirPath(self):

        # ------------------------- criar "Dialog" de abertura de ficheiros
        fd = QtGui.QFileDialog(self)
        # -------------- preparar leitura de ficheiros do tipo csv (x,y,z,i)
        a = "Open files"
        b = ''
        c = "All Files (*)"
        tempStr = str(fd.getExistingDirectory())
        tempStr = tempStr.replace('\\', '/')

        if os.path.isdir(tempStr):
            self.lineEdit_PathScripts.setText(tempStr)
        else:
            # -- não altera pathSCRIPTS
            QMessageBox.about(self, u'Actualizar', 'Caminho inválido !!!')

        print ("self.PathScripts = ", self.PathScripts)

    def ligar(self):
        # ---------------------------------------------ler os parâmetros a partir das caixas de texto
        strHost = self.lineEdit_Host.text()
        strDb = self.lineEdit_Db.text()
        strUser = self.lineEdit_User.text()
        strPasswd = self.lineEdit_Passwd.text()
        print "Ligar-----------------"
        conn = None
        try:
            # --------------------------------------------------------------construir "connection string"
            str_connect="dbname='" + strDb + "' user='" + strUser + "' host='" + strHost + "' password='" \
                        + strPasswd + "'"
            print('classFormConfig: ligar()', str_connect)
            conn = psycopg2.connect(str_connect)
            # ------------------------------------ activar indicador de ligação à base de dados
            cur = conn.cursor()
            cur.execute('SELECT version();')
            ver = cur.fetchall()
            t1=''
            for linha in ver:
                t1 += str(linha[0]) + '\n'
            print t1

            t1 += '\n' + u"Ligação à Base de dados efectuada com sucesso.\n"
            if self.Alteracoes():
                t1 += u"Clique em OK para actualizar configuração" +'\n'
                t1 += u"e re-inicie o programa para utilizar nova configuração."

            # ----------------------------------------- Activar botão OK
            self.pushButton_Ok.setEnabled(True)

        except:
            print "Não foi possível ligar à BD"
            t1 = u"Não foi possível ligar à BD/Host !!"
            self.pushButton_Ok.setEnabled(False)

        finally:
            if conn:
                conn.close()
            if len(t1)>0:
                self.textBrowser.setText(t1)

    def actualizarConfig(self):
        # ------------------------------------- função para actualizar config.ini
        if self.configAlterada() :
            if self.Config.GravarConfig():
                QMessageBox.about(self, u'Actualizar', 'Config.ini actualizado !')
            else:
                QMessageBox.about(self, u'Actualizar', 'Erro a actualizar Config.ini !!!')

    def configAlterada(self):
        alterado = False
        if self.Config.Host != self.lineEdit_Host.text():
            alterado = True
            self.Config.Host = self.lineEdit_Host.text()
        if self.Config.Db != self.lineEdit_Db.text():
            self.Config.Db = self.lineEdit_Db.text()
            alterado = True
        if self.Config.Port != self.lineEdit_Port.text():
            self.Config.Port = self.lineEdit_Port.text()
            alterado = True
        if self.Config.User != self.lineEdit_User.text():
            self.Config.User = self.lineEdit_User.text()
            alterado = True
        if self.Config.Passwd != self.lineEdit_Passwd.text():
            self.Config.Passwd = self.lineEdit_Passwd.text()
            alterado = True
        if self.Config.Path != self.lineEdit_PathScripts.text():
            strTemp = str(self.lineEdit_PathScripts.text())
            self.Config.Path = strTemp.replace('\\', '/')
            alterado = True
        if self.Config.PathQ != self.lineEdit_QPath.text():
            strTemp = str(self.lineEdit_QPath.text())
            self.Config.PathQ = strTemp.replace('\\', '/')
            alterado = True

        return alterado

    def Alteracoes(self):
        alterado = False
        if self.Config.Host != self.lineEdit_Host.text():
            alterado = True
        if self.Config.Db != self.lineEdit_Db.text():
            alterado = True
        if self.Config.Port != self.lineEdit_Port.text():
            alterado = True
        if self.Config.User != self.lineEdit_User.text():
            alterado = True
        if self.Config.Passwd != self.lineEdit_Passwd.text():
            alterado = True
        if self.Config.Path != self.lineEdit_PathScripts.text():
            alterado = True
        if self.Config.PathQ != self.lineEdit_QPath.text():
            alterado = True

        return alterado