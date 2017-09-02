# -*- coding: utf-8 -*-
# --------- Classe para ligar a base de dados
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from FormNewDatabase import Ui_FormNewDatabase
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from classConfig import Config


class FormNewDB(QtGui.QWidget, Ui_FormNewDatabase):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # --------------------------------------------------- Ler constantes a partir de config.ini
        self.Config = Config('config.ini')
        self.sql_dir = self.Config.Path + '/scripts/'
        print('-------------------->', self.sql_dir)

        # ----------------------------------------------------------------- definir nome do script de criação de BD
        self.sql_create_db='sql_create_db.sql'
        # ----------------------------------------------------------------------- preencher caixas de texto da Form
        self.lineEdit_host.setText(self.Config.Host)
        # -----------------------------BD por defeito, necessária para primeira conexão para criar nova BD
        self.lineEdit_db.setText('postgres')
        # --------------------------------------- preencher restantes parâmetros
        self.lineEdit_user.setText(self.Config.User)
        self.lineEdit_passwd.setText(self.Config.Passwd)
        self.lineEdit_owner.setText('postgres')
        # --------------------------------------- limpar nome da nova BD, utilizador tem que preencher !!
        self.lineEdit_nova.setText('')

        self.pushButtonCriar.clicked.connect(self.CriarDB)

    def filtrar(self, texto):

        filtrado = texto.replace('\n', ' ')
        filtrado = filtrado.replace('\r', ' ')
        filtrado = filtrado.replace('\\', '/')
        filtrado = filtrado.replace('\\\\', '/')
        filtrado = filtrado.replace('C:/MapX', self.Config.Path)
        filtrado = filtrado.replace('c:/MapX', self.Config.Path)

        return filtrado

    def CriarDB(self):

        # ler os parâmetros a partir das caixas de texto ("Qt line edits")
        str_Host = self.lineEdit_host.text()
        str_Db = self.lineEdit_db.text()
        str_User = self.lineEdit_user.text()
        str_passwd = self.lineEdit_passwd.text()

        print "Ligar-----------------"

        # ----------------------------------------------construir "connection string" para BD inicial (postgres)
        str_connect="dbname='" + str_Db + "' user='" + str_User + "' host='" + str_Host + "' password='" \
                    + str_passwd + "'"
        print str_connect
        conn = None
        conn = psycopg2.connect(str_connect)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # -------------------------------------------------------------------------  CRIAR NOVA BASE DADOS
        nova = self.lineEdit_nova.text()
        t1 = ''
        erro = False
        try:
            cur.execute('DROP DATABASE IF EXISTS ' + nova)
            cur.execute('CREATE DATABASE ' + nova)
            self.textEdit.append(u'classFormNewDatabase: CREATE DATABASE --- OK')
            t1 = u'CREATE DATABASE --- OK'
        except Exception, e:
            t1 = u'CREATE DATABASE --- ERRO ' + str(e) + ' ' + nova
            erro = True
        finally:
            self.textEdit.append(t1)
            conn.close()

        # self.repaint()
        # if erro:
        #     QMessageBox.about(self, u'Criar BD', u'Erro ao criar BD' + nova)
        #     return

        # -----------------------------------------------------------------  Construir strConnect para nova BD
        str_connect="dbname='" + nova + "' user='" + str_User + "' host='" + str_Host + "' password='" \
                    + str_passwd + "'"
        print str_connect
        conn = None
        erro = False
        t1 = ''
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute('SELECT version();')
            ver = cur.fetchone()
            for linha in ver:
                t1 += linha + '\n'
            t1 += u'Ligação OK.'
        except Exception, e:
            t1 += u'Não foi possível ligar à base de dados ' + nova + ' !!!  Erro: ' + str(e)
            erro = True
        finally:
            self.textEdit.append(t1)

        self.repaint()
        if erro:
            if conn:
                conn.close()
            QMessageBox.about(self, u'Criar BD', u'Erro a ligar a nova BD ' + nova + 'Erro: ' + str(e))
            return

        # ------------------------Criar Tabelas, Views, Funções a partir de script "/MapX/scripts/sql_create_db.sql"
        with open(self.sql_dir+self.sql_create_db, 'r') as f:
            read_data = f.read().decode("utf-8-sig").encode("utf-8")
        # ------------------------------------- Limpar read_data  de caracteres de formatação etc.
        strSql = self.filtrar(read_data)
        print("classFormNewDatabase - criar db - read_data filtrado = ",strSql)
        erro = False
        t1 = ''
        try:
            cur.execute(strSql)
            t1 = u'classFormNewDatabase Criar database -- OK'
        except Exception, e:
            erro = True
            t1 = u'classFormNewDatabase Erro: criar tabelas  ' + nova + ' Erro: ' + str(e)
            print(u'classFormNewDatabase Erro: criar tabelas ', nova)
        finally:
            conn.close()
            self.textEdit.append(t1)
        self.repaint()
        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabelas na nova BD ' + nova + ' ' +  str(e))
            return

        # ----------------------------------------------------------  Importação de dados para tabelas auxiliares

        # -------------------------------------------------------------------- Tabela parametro
        t1 = 'Tabela: parametro. --- >'
        conn = None
        erro = False
        ficheiro = self.Config.Path + '/scripts/parametros_SDN_P02_93.csv'
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            ff = open(ficheiro, 'r')
            cur.copy_from(ff, 'parametro', columns=('id', 'parametro'), sep=',')
            t1 += u' Importação OK.'
        except Exception, e:
            t1 += u' Erro a importar de ' + ficheiro + ' ' + str(e)
            erro = True
        finally:
            if conn:
                conn.close()
            ff.close()
            self.textEdit.append(t1)

        self.repaint()
        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabela "parametro"'
                                                 u' a partir de ' + ficheiro + ' ' + str(e))
            return

        # -------------------------------------------r------------------------  Tabela unid_tempo
        t1 = u"Tabela: unid_tempo. --- >"
        conn = None
        erro = False
        ficheiro = self.Config.Path + '/scripts/unid_tempo_SDN_L26_1.csv'
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            ff = open(ficheiro, 'r')
            cur.copy_from(ff, 'unid_tempo', columns=('id', 'unid_tempo'), sep=',')
            t1 += u' Importação OK.'
        except Exception, e:
            t1 += u' Erro a importar de ' + ficheiro + ' ' + str(e)
            erro = True
        finally:
            if conn:
                conn.close()
            ff.close()
            self.textEdit.append(t1)

        self.repaint()
        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabela "unid_tempo"'
                                                 u' a partir de ' + ficheiro + ' ' + str(e))
            return


        # -------------------------------------------------------------------  Tabela Entidades
        t1 = u"Tabela: entidade. --- >"
        conn = None
        erro = False
        ficheiro = self.Config.Path + '/scripts/entidades.csv'
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            ff = open(ficheiro, 'r')
            cur.copy_from(ff, 'entidade', columns=('id', 'entidade'), sep=',')
            t1 += u' Importação OK.'
        except Exception, e:
            t1 += u' Erro a importar de ' + ficheiro + ' ' + str(e)
            erro = True
        finally:
            if conn:
                conn.close()
            ff.close()
            self.textEdit.append(t1)

        self.repaint()
        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabela "entidade"'
                                                 u' a partir de ' + ficheiro + ' ' + str(e))
            return

        # ----------------------------------------------------------- tabela equipamento
        t1 = u"Tabela: equipamento. --- >"
        conn = None
        erro = False
        ficheiro = self.Config.Path + '/scripts/equipamentos_SDN_L05_55.csv'
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            ff = open(ficheiro, 'r')
            cur.copy_from(ff, 'equipamento', columns=('id', 'equipamento'), sep=',')
            t1 += u'Importação OK.'
        except Exception, e:
            t1 += u'Erro a importar de ' + ficheiro + ' ' + str(e)
            erro = True
        finally:
            if conn:
                conn.close()
            ff.close()
            self.textEdit.append(t1)

        self.repaint()
        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabela "equipamento" a'
                                                 u' partir de ' + ficheiro + ' ' + str(e))
            return

        # ----------------------------------------------------------------  tabela plataforma
        t1 = u"Tabela: plataforma. --- >"
        conn = None
        erro = False
        ficheiro = self.Config.Path + '/scripts/platform_categ_SDN_L06_13.csv'
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            ff = open(ficheiro, 'r')
            cur.copy_from(ff, 'plataforma', columns=('id', 'platform_class'), sep=',')
            t1 += u' Importação OK.'
        except Exception, e:
            t1 += u' Erro a importar de ' + ficheiro + ' ' + str(e)
            erro = True
        finally:
            if conn:
                conn.close()
            ff.close()
            self.textEdit.append(t1)

        self.repaint()
        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabela plataforma a'
                                                 u' partir de ' + ficheiro + ' ' + str(e))
            return

        # ------------------------------------------------------------------- preencher tabela acesso
        t1 = u"Tabela: acesso. --- >"
        conn = None
        ficheiro = self.Config.Path + '/scripts/access_SDN_L08_3.csv'
        erro = False
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            ff = open(ficheiro, 'r')
            cur.copy_from(ff, 'acesso', columns=('id', 'acesso'), sep=',')
            t1 += u'Importação OK.'
        except Exception, e:
            t1 += u'Erro a importar de ' + ficheiro +  ' ' + str(e)
            erro = True
        finally:
            if conn:
                conn.close()
            ff.close()
            self.textEdit.append(t1)

        self.repaint()
        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabela "acesso" a '
                                                 u'partir de ' + ficheiro + ' ' + str(e))
            return

        # --------------------------------------------------------------------- preencher tabela datum_h
        t1 = u"Tabela: datum_h. --- >"
        conn = None
        ficheiro = self.Config.Path + '/scripts/coordinate_SDN_L10_3.csv'
        erro = False
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            ff = open(ficheiro, 'r')
            # --------------------------------------------------------- inserir ficheiro completo
            cur.copy_from(ff, 'datum_h', columns=('id', 'datum_h', 'ordem'), sep=',')
            t1 += u' Importação OK.'
        except Exception, e:
            t1 += u' Erro a importar de ' + ficheiro  + ' ' + str(e)
            erro = True
        finally:
            if conn:
                conn.close()
            ff.close()
            self.textEdit.append(t1)

        self.repaint()

        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabela "datum_h" '
                                                 u'a partir de ' + ficheiro + ' ' + str(e))
            return

        #
        # --------------------------------------------------------------------- preencher tabela datum_v
        t1 = u"Tabela: datum_v. --- >"
        conn = None
        ficheiro = self.Config.Path + '/scripts/v_datum_SDN_L11_8.csv'
        erro = False
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            ff = open(ficheiro, 'r')
            # --------------------------------------------------------- inserir ficheiro completo
            cur.copy_from(ff, 'datum_v', columns=('id', 'datum_v', 'ordem'), sep=',')
            t1 += u' Importação OK.'
        except Exception, e:
            t1 += u' Erro a importar de ' + ficheiro + ' ' + str(e)
            erro = True
        finally:
            if conn:
                conn.close()
            ff.close()
            self.textEdit.append(t1)

        self.repaint()

        # -------------------------------------------------------------------  Tabela Formato
        t1 = u"Tabela: formato. --- >"
        conn = None
        erro = False
        ficheiro = self.Config.Path + '/scripts/data_format_SDN_L24_7.csv'
        try:
            conn = psycopg2.connect(str_connect)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            ff = open(ficheiro, 'r')
            cur.copy_from(ff, 'formato', columns=('id', 'formato'), sep=',')
            t1 += u' Importação OK.'
        except Exception, e:
            t1 += u' Erro a importar de ' + ficheiro + ' ' + str(e)
            erro = True
        finally:
            if conn:
                conn.close()
            ff.close()
            self.textEdit.append(t1)

        self.repaint()
        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabela "entidade"'
                                                 u' a partir de ' + ficheiro + ' ' + str(e))
            return

        if erro:
            QMessageBox.about(self, u'Criar BD', u'Erro a criar tabela "datum_v" '
                                                 u'a partir de ' + ficheiro + ' ' + str(e))

        else:
            self.textEdit.append(u'Importação de tabelas --> OK.')
            QMessageBox.about(self, u'Criar BD', u'Nova BD criada: ' + nova + u' --> OK. Importação de tabelas --> OK.')



