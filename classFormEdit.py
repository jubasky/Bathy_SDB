# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from class_extQLineEdit import extQLineEdit
from classConfig import Config
from FormEdit import Ui_DialogFormEdit
from class_extQTextEdit import extQTextEdit
import datetime


class FormEdit(QtGui.QWidget, Ui_DialogFormEdit):

    def __init__(self, id, parent=None):
        print(" ---------------- class FormEDit: __init__")
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # definir objecto para configurações de acesso à BD(caminhos, passwd, etc)
        self.Config = Config('config.ini')
        print "classFormEdit id=", id
        # ---------------------------------------- id do registo CDI
        self.Registo_id = id
        # --------------------------------------- flags para evitar repetição de leituras da BD
        self.flag_ler_plataf = False
        self.lista_plataf_tot = []
        self.flag_ler_acesso = False

        self.flag_ler_entidade = False
        self.flag_ler_equip = False
        self.flag_ler_param = False
        # -------------------------------------- inicializar listas auxiliares
        self.lista_param = []
        self.lista_equip = []

        # ----------------------------------------- Averiguar nº de colunas no GridLayout
        n_col = self.gridLayout.columnCount()
        print "ncol=", n_col
        for n in range(0, n_col-1):
            self.gridLayout.setColumnMinimumWidth(n, 140)
            self.gridLayout.setColumnStretch(n, 0)

        # ----------------------------------- criar combo para equipamentos Emodnet (80 registos)
        self.comboBoxEquip = QtGui.QComboBox(self)
        self.comboBoxEquip.setMaximumWidth(300)
        self.comboBoxEquip.setMinimumWidth(0)
        self.comboBoxEquip.setMinimumHeight(27)
        # ----------------------------------- criar combo para parametros Emodnet (80 registos)
        self.comboBoxParam = QtGui.QComboBox(self)
        self.comboBoxParam.setMaximumWidth(400)
        self.comboBoxParam.setMinimumWidth(0)
        self.comboBoxParam.setMinimumHeight(27)

        # ------- mantém combos invisiveis até utilizador clicar botões "Adicionar..."
        self.comboBoxEquip.setVisible(False)
        self.comboBoxParam.setVisible(False)

        # ------------------------------ criar combo para entidades CDI Emodnet (4000 registos)
        self.comboBox_Entidades = QtGui.QComboBox(self)
        self.comboBox_Entidades.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)

        # ------- mantém combo Entidades invisivel até utilizador clicar o widget line_edit
        self.comboBox_Entidades.setVisible(False)

        # ------------------------------------------- Criar widgets textEdit_C (subclass de QTextEdit) com
        # ------------------------------------------- evento click e atributo "name"
        self.textEdit_C_Origem = extQTextEdit(self, 'origem')
        self.textEdit_C_Contacto = extQTextEdit(self, 'contacto')
        self.textEdit_C_Distrib = extQTextEdit(self, 'distrib')
        self.textEdit_C_Org = extQTextEdit(self, 'org')

        # -------------------------------------------- Adicionar widgets especiais
        lay_out = self.gridLayout
        estilo_moldura = "background-color: rgb(250, 250, 250); color: rgb(0, 0, 50); border:2px solid rgb(0, 0, 155);"
        self.textEdit_C_Origem.setStyleSheet(estilo_moldura)
        self.textEdit_C_Origem.setMinimumHeight(40)
        self.textEdit_C_Origem.setMaximumHeight(40)
        self.textEdit_C_Origem.setMinimumWidth(0)
        lay_out.addWidget(self.textEdit_C_Origem, 7, 3)

        self.textEdit_C_Contacto.setStyleSheet(estilo_moldura)
        self.textEdit_C_Contacto.setMinimumHeight(40)
        self.textEdit_C_Contacto.setMaximumHeight(40)
        self.textEdit_C_Contacto.setMinimumWidth(0)
        lay_out.addWidget(self.textEdit_C_Contacto, 7, 1)

        self.textEdit_C_Distrib.setStyleSheet(estilo_moldura)
        self.textEdit_C_Distrib.setMinimumHeight(40)
        self.textEdit_C_Distrib.setMaximumHeight(40)
        self.textEdit_C_Distrib.setMinimumWidth(0)
        lay_out.addWidget(self.textEdit_C_Distrib, 7, 5)

        self.textEdit_C_Org.setStyleSheet(estilo_moldura)
        self.textEdit_C_Org.setMinimumHeight(40)
        self.textEdit_C_Org.setMaximumHeight(40)
        self.textEdit_C_Org.setMinimumWidth(0)
        lay_out.addWidget(self.textEdit_C_Org, 8, 1)

        # -------------------------------------- Ler combos
        self.LerPlataf()
        self.LerAcesso()
        self.ler_entidade()
        self.LerComboEquip()
        self.LerComboParam()

        # ----------------------------------------- atribuir acções a push_buttons
        self.pushButton_Editar.clicked.connect(self.Editar)
        self.pushButton_Gravar.clicked.connect(self.Gravar)

        self.connect(self.textEdit_C_Origem, QtCore.SIGNAL("clicked()"), self.ler_cbos_entidades)
        self.connect(self.textEdit_C_Contacto, QtCore.SIGNAL("clicked()"), self.ler_cbos_entidades)
        self.connect(self.textEdit_C_Distrib, QtCore.SIGNAL("clicked()"), self.ler_cbos_entidades)
        self.connect(self.textEdit_C_Org, QtCore.SIGNAL("clicked()"), self.ler_cbos_entidades)
        self.comboBox_Entidades.currentIndexChanged.connect(self.actualizar_entidade)

        self.connect(self.pushButtonAddEquip, QtCore.SIGNAL("clicked()"), self.MostrarComboEquip)
        self.comboBoxEquip.currentIndexChanged.connect(self.AtribEquip)

        self.connect(self.pushButtonAddParam, QtCore.SIGNAL("clicked()"), self.MostrarComboParam)
        self.comboBoxParam.currentIndexChanged.connect(self.AtribParam)

        self.listWidget_Equip.doubleClicked.connect(self.RemoverEquip)
        self.listWidget_Param.doubleClicked.connect(self.RemoverParam)

        # ---------------- Preparar formulário
        self.SetForm()

        # Ler dados respeitantes ao registo seleccionado pelo utilizador
        self.LerCDI(id)


    def SetForm(self):

        # --------------------------------------- possibilidade de gravar
        self.pushButton_Gravar.setEnabled(False)
        # --------------------------------------- definir listas/Combos
        lista=[]
        self.comboBox_QC_Feito.clear()
        lista.append('True')
        lista.append('False')
        self.comboBox_QC_Feito.addItems(lista)
        self.dateEdit_Rev_Date.setEnabled(False)
        self.comboBox_Plataforma.setEnabled(False)

        # -------------------------------------- Bloquear todos os Widgets
        # -------------------------------------- de introdução de dados
        self.lineEdit_CDI.setEnabled(False)
        self.textEdit_Datum_H.setEnabled(False)
        self.textEdit_Datum_V.setEnabled(False)

        self.lineEdit_Limite_W.setEnabled(False)
        self.lineEdit_Limite_E.setEnabled(False)
        self.lineEdit_Limite_N.setEnabled(False)
        self.lineEdit_Limite_S.setEnabled(False)

        self.lineEdit_ProfMin.setEnabled(False)
        self.lineEdit_ProfMax.setEnabled(False)

        self.dateTimeEdit_Ini.setEnabled(False)
        self.dateTimeEdit_Fim.setEnabled(False)

        self.lineEdit_Cruzeiro.setEnabled(False)
        self.lineEdit_ID_Cruzeiro.setEnabled(False)
        self.lineEdit_Resumo.setEnabled(False)


        self.textEdit_Origem.setEnabled(False)
        self.textEdit_Origem.setVisible(False)
        self.textEdit_C_Origem.setEnabled(False)
        self.textEdit_Contacto.setEnabled(False)
        self.textEdit_Contacto.setVisible(False)
        self.textEdit_C_Contacto.setEnabled(False)
        self.textEdit_Distributor.setEnabled(False)
        self.textEdit_Distributor.setVisible(False)
        self.textEdit_C_Distrib.setEnabled(False)
        self.textEdit_Organizador.setEnabled(False)
        self.textEdit_Organizador.setVisible(False)
        self.textEdit_C_Org.setEnabled(False)

        self.lineEdit_Tamanho.setEnabled(False)
        self.comboBox_Acesso.setEnabled(False)
        self.lineEdit_QC.setEnabled(False)
        self.lineEdit_QC_Obs.setEnabled(False)
        self.comboBox_QC_Feito.setEnabled(False)


        self.pushButtonAddEquip.setEnabled(False)
        self.pushButtonAddParam.setEnabled(False)
        self.listWidget_Equip.setEnabled(False)
        self.listWidget_Param.setEnabled(False)

        self.pushButtonAddEquip.hide()
        self.pushButtonAddParam.hide()

        self.comboBoxParam.setVisible(False)

    # ------------------------------------- Método para ler dados de registo com id= id_CDI
    # ------------------------------------- e popular LineEdit's, ComboBox e Lists
    def LerCDI(self,id_CDI):

        print "classFormEdit LerCDI id=", id_CDI

        # ----------------------Ler texto de queries necessárias para mostrar info completa de cada registo
        self.sql_LerCDI_path = self.Config.Path +"/scripts/sql_ler_cdi_Edit.sql"

        self.sql_LerCDI_Holding_Centre_path = self.Config.Path +"/scripts/sql_ler_cdi_edit_holding_centre.sql"
        self.sql_LerCDI_Distributor_path = self.Config.Path +"/scripts/sql_ler_cdi_edit_distributor.sql"
        self.sql_LerCDI_Collate_Centre_path = self.Config.Path +"/scripts/sql_ler_cdi_edit_collate_centre.sql"
        self.sql_LerCDI_Equip_path = self.Config.Path +"/scripts/sql_ler_cdi_edit_Equip.sql"
        self.sql_LerCDI_Param_path = self.Config.Path + "/scripts/sql_ler_cdi_edit_Param.sql"

        # ------------------------------------------------------------ Ler scripts SQL
        try:
            # -------------------------------------------- Ler script tabela CDI
            with open(self.sql_LerCDI_path, 'r') as f:
                sql_LerCDI =f.read()
            f.close()
            sql_LerCDI = sql_LerCDI.replace("???", str(id_CDI))
            print sql_LerCDI

            # -------------------------------------------- Ler script tabela CDI/Entidade-Holding
            with open(self.sql_LerCDI_Holding_Centre_path, 'r') as f:
                sql_LerCDI_Holding = f.read()
            f.close()
            sql_LerCDI_Holding = sql_LerCDI_Holding.replace("???", str(id_CDI))
            print sql_LerCDI_Holding

            # -------------------------------------------- Ler script tabela CDI/Entidade-Distributor
            with open(self.sql_LerCDI_Distributor_path, 'r') as f:
                sql_LerCDI_Distributor = f.read()
            f.close()
            sql_LerCDI_Distributor = sql_LerCDI_Distributor.replace("???", str(id_CDI))
            print sql_LerCDI_Distributor

            # -------------------------------------------- Ler script CDI/Entidade-Collate
            with open(self.sql_LerCDI_Collate_Centre_path, 'r') as f:
                sql_LerCDI_Collate = f.read()
            f.close()
            sql_LerCDI_Collate = sql_LerCDI_Collate.replace("???", str(id_CDI))
            print sql_LerCDI_Collate

            # -------------------------------------------- Ler script CDI/Equipamento
            with open(self.sql_LerCDI_Equip_path, 'r') as f:
                sql_LerCDI_Equip = f.read()
            f.close()
            sql_LerCDI_Equip = sql_LerCDI_Equip.replace("???", str(id_CDI))
            print sql_LerCDI_Equip

            # -------------------------------------------- Ler script CDI/Param
            with open(self.sql_LerCDI_Param_path, 'r') as f:
                sql_LerCDI_param = f.read()
            f.close()
            sql_LerCDI_param = sql_LerCDI_param.replace("???", str(id_CDI))
            print sql_LerCDI_param

        # --------------------------------------------------------- Em caso de erro, sai da função
        except:
            print('classFormEdit: Problema a ler script SQL')
            return

        # ---------------------------------------- definir objecto psycopg2 (conn) para ligação à BD
        conn = None
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # --------------------------------------- Executar query Ler_CDI_Edit
        cur.execute(sql_LerCDI)
        ver = cur.fetchall()
        # print "ver(1)=" , ver[0][6],ver[0][7]
        if len(ver):
            campos=[]
            for a in ver[0]:
                campos.append(str(a).strip())
            print "leitura OK"
            print "ver = ", ver
            print "campos = ", campos
            # ----------------------------- Preencher Lineedits, etc.
            self.lineEdit_CDI.setText(campos[1])  # CDI descritivo
            self.textEdit_Datum_H.setText(campos[2] + "  " + campos[29])
            self.textEdit_Datum_V.setText(campos[3] + "  " + campos[30])
            self.lineEdit_Limite_W.setText(campos[24])
            self.lineEdit_Limite_E.setText(campos[25])
            self.lineEdit_Limite_N.setText(campos[26])
            self.lineEdit_Limite_S.setText(campos[27])
            self.lineEdit_ProfMin.setText(campos[4])
            self.lineEdit_ProfMax.setText(campos[5])
            datahora  = QtCore.QDateTime.fromString(campos[6][0:19], 'yyyy-MM-dd hh:mm:ss')
            # print "datahora=" , datahora, campos[6][0:19]
            self.dateTimeEdit_Ini.setDateTime(datahora)
            # print "datahora=", datahora, campos[7][0:19]
            datahora = QtCore.QDateTime.fromString(campos[7][0:19], 'yyyy-MM-dd hh:mm:ss')
            self.dateTimeEdit_Fim.setDateTime(datahora)
            # ------------------------ determinar indice de comboBox_Plataforma
            indice = self.comboBox_Plataforma.findText(campos[10] + '  ' + campos[31], QtCore.Qt.MatchFixedString)
            self.comboBox_Plataforma.setCurrentIndex(indice)

            self.lineEdit_Cruzeiro.setText(campos[17])
            self.lineEdit_ID_Cruzeiro.setText(campos[18])
            self.lineEdit_Resumo.setText(campos[9])
            self.textEdit_C_Origem.setText(campos[12] + " " + campos[28])

            self.lineEdit_Tamanho.setText(campos[15])
            # ------------------------ determinar indice de comboBox_Acesso
            indice = self.comboBox_Acesso.findText(campos[16] + '  '+ campos[32], QtCore.Qt.MatchContains)
            self.comboBox_Acesso.setCurrentIndex(indice)
            print "campos[16] + '  ' + campos[32]", campos[16] + '  ' + campos[32]
            self.lineEdit_QC.setText(campos[19])

            self.lineEdit_QC_Obs.setText(campos[21])
            if campos[22] == 'True':
                self.comboBox_QC_Feito.setCurrentIndex(0)
            else:
                self.comboBox_QC_Feito.setCurrentIndex(1)

            datahora = QtCore.QDateTime.fromString(campos[23][0:19], 'yyyy-MM-dd hh:mm:ss')
            self.dateEdit_Rev_Date.setDateTime(datahora)

        else:
            # -------------------------------------------- Erro na ligação
            print "leitura KO"

        # --------------------------------------- Executar query sql_LerCDI_Holding_centre
        cur.execute(sql_LerCDI_Holding)
        ver = cur.fetchall()
        if len(ver):
            print "leitura OK"
            print ver
            campos = []
            for a in ver[0]:
                campos.append(str(a))
            print "leitura OK"
            print "ver = ", ver
            print "campos = ", campos
            self.textEdit_C_Contacto.setText(campos[0] + " " + campos[1])

        else:
            # -------------------------------------------- Erro na ligação
            print "sql_LerCDI_Holding_centre: leitura KO"

        # --------------------------------------- Executar query sql_LerCDI_Distributor
        cur.execute(sql_LerCDI_Distributor)
        ver = cur.fetchall()
        if len(ver):
            print "leitura OK"
            print ver
            campos = []
            for a in ver[0]:
                campos.append(str(a))
            print "leitura OK"
            print "ver = ", ver
            print "campos = ", campos
            self.textEdit_C_Distrib.setText(campos[0] + " " + campos[1])
        else:
            # -------------------------------------------- Erro na ligação
            print "sql_LerCDI_Distributor: leitura KO"

        # --------------------------------------- Executar query sql_LerCDI_Collate
        cur.execute(sql_LerCDI_Collate)
        ver = cur.fetchall()
        if len(ver):
            print "leitura OK"
            print ver
            campos = []
            for a in ver[0]:
                campos.append(str(a))
            print "leitura OK"
            print "ver = ", ver
            print "campos = ", campos
            self.textEdit_C_Org.setText(campos[0] + " - " + campos[1])
        else:
            # -------------------------------------------- Erro na ligação
            print "sql_LerCDI_Collate: leitura KO"

        # --------------------------------------- Executar query sql_LerCDI_Equip
        cur.execute(sql_LerCDI_Equip)
        ver = cur.fetchall()
        if len(ver):
            print "leitura OK"
            print ver

            n_linhas= len(ver)
            campos = [[] for i in range(n_linhas)]
            print "sql_LerCDI_Equip, n_linhas=", n_linhas
            lista_aux=[]
            for i in range(n_linhas):
                for a in ver[i]:
                    campos[i].append(str(a))
            for i in range(n_linhas):
                self.lista_equip.append(campos[i][0] + " " + campos[i][1])
            print "leitura OK"

            self.listWidget_Equip.addItems(self.lista_equip)

        else:
            # -------------------------------------------- Erro na ligação
            print "sql_LerCDI_Equip: leitura KO"

        # --------------------------------------- Executar query sql_LerCDI_Param
        cur.execute(sql_LerCDI_param)
        ver = cur.fetchall()
        if len(ver):
            print "leitura OK"
            print ver

            n_linhas = len(ver)
            campos = [[] for i in range(n_linhas)]
            print "sql_LerCDI_param, n_linhas=", n_linhas
            lista_aux = []
            for i in range(n_linhas):
                for a in ver[i]:
                    campos[i].append(str(a))
            for i in range(n_linhas):
                self.lista_param.append(campos[i][0] + " " + campos[i][1])
            print "leitura OK"

            self.listWidget_Param.addItems(self.lista_param)

        else:
            # -------------------------------------------- Erro na ligação
            print "sql_LerCDI_Equip: leitura KO"


        # --------------------------------------------- Fechar ligação à BD
        if conn:
            print "A fechar ligação !!"
            conn.close()
            conn = None

    # ------------------------------------- Método para activar widgets para edição
    # ------------------------------------- de dados do registo activo (CDI)
    def Editar(self):

        self.dateTimeEdit_Ini.setEnabled(True)
        self.dateTimeEdit_Fim.setEnabled(True)

        self.lineEdit_Cruzeiro.setEnabled(True)
        self.lineEdit_ID_Cruzeiro.setEnabled(True)
        self.comboBox_Plataforma.setEnabled(True)
        self.lineEdit_Resumo.setEnabled(True)

        self.pushButtonAddEquip.setEnabled(True)
        self.pushButtonAddParam.setEnabled(True)
        self.listWidget_Equip.setEnabled(True)
        self.listWidget_Param.setEnabled(True)

        self.pushButtonAddEquip.show()
        self.pushButtonAddParam.show()

        self.textEdit_C_Contacto.setEnabled(True)
        self.textEdit_C_Origem.setEnabled(True)
        self.textEdit_C_Distrib.setEnabled(True)
        self.textEdit_C_Org.setEnabled(True)

        self.lineEdit_Tamanho.setEnabled(True)
        self.comboBox_Acesso.setEnabled(True)
        self.lineEdit_QC.setEnabled(True)
        self.lineEdit_QC_Obs.setEnabled(True)
        self.comboBox_QC_Feito.setEnabled(True)

        self.pushButton_Gravar.setEnabled(True)

    def LerPlataf(self):

        # print ('-------------------------------- LerPlataf')
        if self.flag_ler_plataf:
            return


        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select * FROM plataforma ORDER BY id;")
        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            self.lista_plataf_tot.append(a)
        self.comboBox_Plataforma.clear()
        self.comboBox_Plataforma.addItems(self.lista_plataf_tot)
        self.flag_ler_plataf = True
        conn.close()

    def LerAcesso(self):
        # print ('-------------------------------- LerAcesso)
        if self.flag_ler_acesso:
            return
        lista_aux = []
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select * FROM acesso ORDER BY id;")
        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            lista_aux.append(a)
        self.comboBox_Acesso.clear()
        self.comboBox_Acesso.addItems(lista_aux)
        self.flag_ler_acesso = True
        conn.close()

    def actualizar_entidade(self):
        # ---------- resposta ao evento change do combo
        # ---------  Entidades
        print "actualizar_entidade, comboBoxEnti currentText=", self.comboBox_Entidades.currentText()
        if self.enti == 1:
            self.textEdit_C_Contacto.setText(self.comboBox_Entidades.currentText())
            self.textEdit_C_Contacto.setAlignment(QtCore.Qt.AlignLeft)
            self.textEdit_C_Contacto.setVisible(True)
        elif self.enti == 2:
            self.textEdit_C_Origem.setText(self.comboBox_Entidades.currentText())
            self.textEdit_C_Origem.setAlignment(QtCore.Qt.AlignLeft)
            self.textEdit_C_Origem.setVisible(True)

        elif self.enti == 3:
            self.textEdit_C_Distrib.setText(self.comboBox_Entidades.currentText())
            self.textEdit_C_Distrib.setAlignment(QtCore.Qt.AlignLeft)
            self.textEdit_C_Distrib.setVisible(True)
        elif self.enti == 4:
            self.textEdit_C_Org.setText(self.comboBox_Entidades.currentText())
            self.textEdit_C_Org.setAlignment(QtCore.Qt.AlignLeft)
            self.textEdit_C_Org.setVisible(True)

        self.gridLayout.removeWidget(self.comboBox_Entidades)
        self.comboBox_Entidades.setVisible(False)

    def ler_cbos_entidades(self):

        print('ler combos entidades')
        sender = self.sender()

        print('Sender ===================', sender.name)
        self.comboBox_Entidades.setMinimumHeight(27)
        self.comboBox_Entidades.setVisible(True)

        if sender.name == 'origem':
            self.gridLayout.addWidget(self.comboBox_Entidades, 7, 3, 1, 2)
            self.textEdit_C_Origem.setVisible(False)
            self.enti = 2
            indice = self.comboBox_Entidades.findText(self.textEdit_C_Origem.toPlainText(), QtCore.Qt.MatchFixedString)
        elif sender.name == 'contacto':
            self.gridLayout.addWidget(self.comboBox_Entidades, 7, 1, 1, 2)
            self.textEdit_C_Contacto.setVisible(False)
            self.enti = 1
            indice = self.comboBox_Entidades.findText(self.textEdit_C_Contacto.toPlainText(), QtCore.Qt.MatchFixedString)
        elif sender.name == 'distrib':
            self.gridLayout.addWidget(self.comboBox_Entidades, 7, 5, 1, 2)
            self.textEdit_C_Distrib.setVisible(False)
            self.enti = 3
            indice = self.comboBox_Entidades.findText(self.textEdit_C_Distrib.toPlainText(), QtCore.Qt.MatchFixedString)
        elif sender.name == 'org':
            self.gridLayout.addWidget(self.comboBox_Entidades, 8, 1, 1, 2)
            self.textEdit_C_Org.setVisible(False)
            self.enti = 4
            indice = self.comboBox_Entidades.findText(self.textEdit_C_Org.toPlainText(), QtCore.Qt.MatchFixedString)

        if indice >= 0:
            self.comboBox_Entidades.setCurrentIndex(indice)

    def ler_entidade(self):
        if  self.flag_ler_entidade:
            return
        lista = []
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select id, entidade FROM entidade;")
        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            lista.append(a)
        conn.close()

        self.comboBox_Entidades.clear()
        self.comboBox_Entidades.addItems(lista)

        self.flag_ler_entidade = True


    def LerComboEquip(self):
        print ('-------------------------------- LerComboEquip')
        lista_aux =[]
        if self.flag_ler_equip == True:
            return

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select id, equipamento FROM equipamento ORDER BY id;")

        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            lista_aux.append(a)
        conn.close()

        self.comboBoxEquip.clear()
        self.comboBoxEquip.addItems(lista_aux)

        self.flag_ler_equip = True


    def MostrarComboEquip(self):
        self.gridLayout.addWidget(self.comboBoxEquip, 5, 1, 1, 2)
        self.comboBoxEquip.setVisible(True)

    def AtribEquip(self):
        # --------------------------------- resposta ao evento comboEquip item changes
        if not self.comboBoxEquip.isVisible():
            return

        self.lista_equip.append(self.comboBoxEquip.currentText())
        self.listWidget_Equip.addItem(self.comboBoxEquip.currentText())
        # após copiar texto de combo para a lista de equipamentos,
        # esconde o combo, até se clicar outra vez no botão Equipamento.
        self.gridLayout.removeWidget(self.comboBoxEquip)
        self.comboBoxEquip.setVisible(False)

    def MostrarComboParam(self):
        self.gridLayout.addWidget(self.comboBoxParam, 5, 3, 1, 2)
        self.comboBoxParam.setVisible(True)

    def LerComboParam(self):
        print ('-------------------------------- LerComboParam')
        lista_aux = []
        self.comboBoxParam.setVisible(True)
        if self.flag_ler_param == True:
            return

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select id, parametro FROM parametro ORDER BY id;")

        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            lista_aux.append(a)
        conn.close()

        self.comboBoxParam.clear()
        self.comboBoxParam.addItems(lista_aux)

        self.flag_ler_param = True

    def AtribParam(self):
        # --------------------------------- resposta ao evento comboParam item change
        if not self.comboBoxParam.isVisible():
            return

        self.lista_param.append(self.comboBoxParam.currentText())
        self.listWidget_Param.addItem(self.comboBoxParam.currentText())
        # após copiar texto de combo para a lista de parametros,
        # esconde o combo, até se clicar outra vez no botão Adicionar Parametro.
        self.gridLayout.removeWidget(self.comboBoxParam)
        self.comboBoxParam.setVisible(False)

    def Gravar(self):
        print "Gravar id=", self.Registo_id

        gravar_ok = True

        # -------------------------------------- gravar cdi (metadados correspondentes ao dataset)
        # -------------------------------------- prever possiveis alterações no codigo CDI (descritivo)
        codigo_cdi = self.lineEdit_CDI.text()
        start_date = self.dateTimeEdit_Ini.text()
        end_date = self.dateTimeEdit_Fim.text()

        abstract = self.lineEdit_Resumo.text()

        platform_class = self.comboBox_Plataforma.currentText().split(' ')[0]
        holding_centre = self.textEdit_C_Contacto.toPlainText().split(' ')[0]
        originator = self.textEdit_C_Origem.toPlainText().split(' ')[0]
        distributor = self.textEdit_C_Distrib.toPlainText().split(' ')[0]
        collate_centre = self.textEdit_C_Org.toPlainText().split(' ')[0]
        data_size = str(self.lineEdit_Tamanho.text())
        data_access = self.comboBox_Acesso.currentText().split(' ')[0]
        cruise_name = self.lineEdit_Cruzeiro.text()
        cruise_id = self.lineEdit_ID_Cruzeiro.text()
        qc_desc = str(self.lineEdit_QC.text())
        qc_comment = str(self.lineEdit_QC_Obs.text())

        if self.comboBox_QC_Feito.currentText() == 'True':
            qc_status = True
        else:
            qc_status = False

        qc_date = end_date
        revision_date = str(datetime.datetime.now())

        # ---------------------------------------------------------------------------------
        # ----------------- Info para tabelas cdi_equip
        lista_cdi_equip = []
        for index in xrange(self.listWidget_Equip.count()):
            a, b = self.listWidget_Equip.item(index).text().split(' ', 1)
            lista_cdi_equip.append(a)

        # ---------------------------------------------------------------------------------
        # ----------------- Info para tabelas cdi_param
        lista_cdi_param = []
        for index in xrange(self.listWidget_Param.count()):
            a, b = self.listWidget_Param.item(index).text().split(' ', 1)
            lista_cdi_param.append(a)

        # -------------------------------------------------------- UPDATE info na tabela Cdi
        strSql = "UPDATE cdi SET codigo = '" + codigo_cdi + "', start_date = '" + start_date + "', end_date = '" \
            + end_date + "', abstract = '" + abstract + "', platform_class = " + platform_class + ", holding_centre = " \
            + holding_centre + ", originator = " + originator + ", distributor = " + distributor + ", collate_centre = " \
            + collate_centre + ", data_size = " + data_size +", data_access = '" + data_access + "', cruise_name = '"\
            + cruise_name + "', cruise_id = '" + cruise_id + "', qc_desc = '" + qc_desc + "', qc_date = '"\
            + qc_date + "', qc_comment = '"  + qc_comment + "', qc_status = '" + str(qc_status) + "', revision_date = '" \
            + revision_date + "' WHERE id = " + self.Registo_id + ";"

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("*********  classFormImportFile_class: GravarCDI: strSql=", strSql)
        try:
            cur.execute(strSql)
            print(u'classFormEdit:______________ UPDATE CDI ------ OK')
        except:
            print(u'classFormEdit:______________ UPDATE CDI ------ ERRO!!')
            gravar_ok = False
        finally:
            conn.close()

        if gravar_ok == False:
            return gravar_ok

        # ----------------------------------------- primeiro, apagar todos os registos
        # ----------------------------------------- da tabela cdi_equip relacionados com o CDI em causa
        strSql = "DELETE FROM cdi_equip WHERE cdi =" + self.Registo_id + ";"

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("*********  classFormEdit: DELETE cdi_equip: strSql=", strSql)
        try:
            cur.execute(strSql)
            print(u'classFormEdit:______________ DELETE cdi_equip ------ OK')
        except:
            print(u'classFormEdit:______________ DELETE cdi_equip ------ ERRO!!')
        finally:
            conn.close()
        if gravar_ok == False:
            return gravar_ok

        # ------------- só insere novos registos cdi_equip se existirem equipamentos associados
        if len(lista_cdi_equip) > 0:

            # ------------------------------------------- criar registos cdi_equip
            strSql = "INSERT INTO cdi_equip (cdi, equip_id) VALUES"
            m = len(lista_cdi_equip)
            strValues = ''
            for n in range(m):
                strValues += "(" + self.Registo_id + ", '" + lista_cdi_equip[n] + "')"
                if n == m - 1:
                    strValues += ";"
                else:
                    strValues += ", "
            strSql += strValues

            conn = psycopg2.connect(self.Config.Conn)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            print("*********  classFormEdit: Gravar cdi_equip: strSql=", strSql)
            try:
                cur.execute(strSql)
                print(u'classFormEdit:______________ INSERT cdi_equip ------ OK')
            except:
                print(u'classFormEdit:______________ INSERT cdi_equip ------ ERRO!!')
                gravar_ok = False
            finally:
                conn.close()

            if gravar_ok == False:
                return gravar_ok

        # ----------------------------------------- primeiro, apagar todos os registos
        # ----------------------------------------- da tabela cdi_param relacionados com o CDI em causa
        strSql = "DELETE FROM cdi_param WHERE cdi =" + self.Registo_id + ";"

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("*********  classFormEdit: DELETE cdi_param: strSql=", strSql)
        try:
            cur.execute(strSql)
            print(u'classFormEdit:______________ DELETE cdi_param ------ OK')
        except:
            print(u'classFormEdit:______________ DELETE cdi_param ------ ERRO!!')
        finally:
            conn.close()
        if gravar_ok == False:
            return gravar_ok
        # ------------- só insere novos registos cdi_equip se existirem equipamentos associados
        if len(lista_cdi_param) > 0:

            # ------------------------------------------- criar registos cdi_param
            strSql = "INSERT INTO cdi_param (cdi, param_id) VALUES"
            m = len(lista_cdi_param)
            strValues = ''
            for n in range(m):
                strValues += "(" + self.Registo_id  + ", '" + lista_cdi_param[n] + "')"
                if n == m - 1:
                    strValues += ";"
                else:
                    strValues += ", "

            strSql += strValues

            conn = psycopg2.connect(self.Config.Conn)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            print("*********  classFormEdit: Gravar cdi_param: strSql=", strSql)
            try:
                cur.execute(strSql)
                print(u'classFormEdit:______________ Gravar cdi_param ------ OK')
            except:
                print(u'classFormEdit:______________ Gravar cdi_param ------ ERRO!!')
                gravar_ok = False
            finally:
                conn.close()

        return gravar_ok


    def RemoverParam(self):
        a = self.listWidget_Param.currentRow()
        print "a=", a
        print "len self.lista_param=", len(self.lista_param)

        self.lista_param.remove(self.lista_param[a])
        self.listWidget_Param.clear()
        self.listWidget_Param.addItems(self.lista_param)
        self.listWidget_Param.repaint()

    def RemoverEquip(self):
        a = self.listWidget_Equip.currentRow()
        print a

        self.lista_equip.remove(self.lista_equip[a])
        self.listWidget_Equip.clear()
        self.listWidget_Equip.addItems(self.lista_equip)
        self.listWidget_Equip.repaint()

