# -*- coding: utf-8 -*-
from os.path import isfile
from os.path import getsize

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from FormImportFile import Ui_DialogImport
from converterCSV_WGS84 import ConverterCSV_WGS84
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from class_extQLineEdit import extQLineEdit
from classConfig import Config
import time
import datetime

# ------------------------------------------------------ Classe para gerir importação de dados
class FormImportFile(QtGui.QWidget, Ui_DialogImport):

    def __init__(self, parent=None):
        print(" ---------------- class FormImportFile: __init__")
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        # ------------------------------------------------- Ler constantes a partir de config.ini
        self.Config = Config('config.ini')
        # ----------------------------------------------definir propriedades do objecto
        self.ficheiro_orig = ''
        self.epsg = ''
        self.separador = ''
        self.enti = 0
        self.datasize = 0

        # -------------------------------------------------- definir pasta de scripts :
        self.sql_dir = self.Config.Path + '/scripts/'

        # ------------------------ definir scripts "externos" para funções específicas :
        self.sql_insert_patches = 'sql_insert_into_patches.sql'
        self.sql_insert_patches_info = 'sql_insert_into_patches_info.sql'

        # --------------------------------------- flags, vars aux, etc.
        self.flag_ler_entidades = False
        self.flag_ler_equip = False
        self.flag_ler_plataf = False
        self.flag_ler_acesso = False
        self.flag_ler_datumHoriz = False
        self.flag_ler_datumVert = False
        self.flag_ler_param = False

        self.lista_plataf_tot = []
        self.lista_equip = []
        self.lista_equip_tot = []
        self.lista_acesso_tot = []
        self.lista_param = []
        self.lista_param_tot = []
        self.lista_datumHoriz_tot = []
        self.lista_datumVert_tot = []

        self.dict_equip = {}
        self.dict_plataf = {}
        self.dict_acesso = {}
        self.filename = ""
        self.ignorarLinha = 0
        self.min_patch = 0.0000005

        # -------------------------------------------------- Dimensionar widgets
        self.listWidget_Equip.setMinimumHeight(60)
        n_col = self.gridLayout.columnCount()

        # print("********************************* col count =", n_col)
        for n in range(0, n_col-1):
            self.gridLayout.setColumnMinimumWidth(n, 140)
            self.gridLayout.setColumnStretch(n, 0)

        self.comboBox_Plataf.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)

        # ------------------------------------------- Criar widgets line edit C (subclass de QLineEdit) com
        # ------------------------------------------- evento click e atributo "name"
        self.lineEdit_C_Contacto = extQLineEdit(self, 'contacto')
        self.lineEdit_C_Origem = extQLineEdit(self, 'origem')
        self.lineEdit_C_Distrib = extQLineEdit(self, 'distrib')
        self.lineEdit_C_Org = extQLineEdit(self, 'org')

        # ------------------------------------ acrescentar widget's ao layout da form
        # ----------------------------------- (grid rectangular de campos)
        lay_out = self.gridLayout
        estilo_moldura = "background-color: rgb(250, 250, 250); color: rgb(0, 0, 50); border:2px solid rgb(0, 0, 155);"

        self.lineEdit_C_Contacto.setStyleSheet(estilo_moldura)
        self.lineEdit_C_Contacto.setMinimumHeight(27)
        self.lineEdit_C_Contacto.setMinimumWidth(0)
        lay_out.addWidget(self.lineEdit_C_Contacto, 7, 1, 1, 2)

        self.lineEdit_C_Origem.setStyleSheet(estilo_moldura)
        self.lineEdit_C_Origem.setMinimumHeight(27)
        self.lineEdit_C_Origem.setMinimumWidth(0)

        lay_out.addWidget(self.lineEdit_C_Origem, 7, 3, 1, 2)

        self.lineEdit_C_Distrib.setStyleSheet(estilo_moldura)
        self.lineEdit_C_Distrib.setMinimumHeight(27)
        self.lineEdit_C_Distrib.setMinimumWidth(0)
        lay_out.addWidget(self.lineEdit_C_Distrib, 8, 1, 1, 2)

        self.lineEdit_C_Org.setStyleSheet(estilo_moldura)
        self.lineEdit_C_Org.setMinimumHeight(27)
        self.lineEdit_C_Org.setMinimumWidth(0)
        lay_out.addWidget(self.lineEdit_C_Org, 8, 3, 1, 2)

        # ------------------------------ criar combo para entidades CDI Emodnet (4000 registos)
        self.comboBox_Entidades = QtGui.QComboBox(self)
        self.comboBox_Entidades.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)

        # ------- mantém combo Entidades invisivel até utilizador clicar o widget line_edit
        self.comboBox_Entidades.setVisible(False)

        # ----------------------------------- criar combo para equipamentos Emodnet (80 registos)
        self.comboBoxEquip = QtGui.QComboBox(self)
        self.comboBoxParam = QtGui.QComboBox(self)

        # ------- mantém combo Entidades invisivel até utilizador clicar o widget line_edit
        self.comboBoxEquip.setVisible(False)
        # self.comboBoxEquip.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)

        self.comboBoxParam.setVisible(False)
        # self.comboBoxParam.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)

        # --------------------------------------- criar e atribuir "QValidators"
        validator_dbl = QtGui.QDoubleValidator()
        validator_int = QtGui.QIntValidator()
        self.lineEdit_LongW.setValidator(validator_dbl)
        self.lineEdit_LongE.setValidator(validator_dbl)
        self.lineEdit_LatN.setValidator(validator_dbl)
        self.lineEdit_LatS.setValidator(validator_dbl)
        self.lineEdit_ProfMax.setValidator(validator_dbl)
        self.lineEdit_ProfMin.setValidator(validator_dbl)
        self.lineEdit_Tamanho.setValidator(validator_int)

        # ---------------------------------------------------------Ligar widgets a métodos da classe
        self.lineEdit_cdi.editingFinished.connect(self.validarCdi)

        self.pushButtonAddEquip.clicked.connect(self.LerComboEquip)
        self.pushButtonAddParam.clicked.connect(self.LerComboParam)
        self.comboBoxEquip.currentIndexChanged.connect(self.AtribEquip)
        self.comboBoxParam.currentIndexChanged.connect(self.AtribParam)
        self.listWidget_Equip.doubleClicked.connect(self.RemoverEquip)
        self.listWidgetParam.doubleClicked.connect(self.RemoverParam)

        self.importButton.clicked.connect(self.importar)
        self.pushButtonAbrirFicheiro.clicked.connect(self.File_dialog)
        self.comboBox_Entidades.currentIndexChanged.connect(self.actualizar_entidade)
        self.checkBox_primeira_linha.clicked.connect(self.actualizarIgnorarLinha)
        self.connect(self.lineEdit_C_Contacto, QtCore.SIGNAL("clicked()"), self.ler_cbos_entidades)
        self.connect(self.lineEdit_C_Origem, QtCore.SIGNAL("clicked()"), self.ler_cbos_entidades)
        self.connect(self.lineEdit_C_Distrib, QtCore.SIGNAL("clicked()"), self.ler_cbos_entidades)
        self.connect(self.lineEdit_C_Org, QtCore.SIGNAL("clicked()"), self.ler_cbos_entidades)

        self.connect(self.cboSep, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.ler_linhas)

        # --------------------------------------- ferramenta temporaria para testar projecção
        # --------------------------------------- de coord lat long para cartesianas (metros)
        # ---------------------------------------- em etrs89
        # self.connect(self.lineEdit_C_Origem, QtCore.SIGNAL("clicked()"), self.ler_cbos_entidades))

        # -------------------------------------- inicialmente, desactivar widgets de introdução de dados
        self.DesactivarWidgets()

        # --------------------------------------- num de linhas max. a ler, para mostrar em textEdit
        self.num_lin_amostra = 15

        # --------------------------------------------------------------------- Carregar combos
        lista = ['1 - OK', '2 - KO']
        self.comboBox_Feito.clear()
        self.comboBox_Feito.addItems(lista)
        self.lerDatumHoriz()
        self.cboDatumHz.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.LerPlataf()
        self.LerAcesso()
        self.LerDatumVertical()

        # --------------------------------------------------------- estabelecer opções por defeito
        self.comboBox_Plataf.setCurrentIndex(20)
        self.lista_equip.extend(('156 single-beam echosounders', '157 multi-beam echosounders'))
        self.lista_equip.extend(('POS02 Global Navigation Satellite System receivers', '185 sound velocity sensors'))
        self.listWidget_Equip.addItems(self.lista_equip)

        self.lista_param.extend(('MBAN Bathymetry and Elevation','SVEL Sound velocity and '
                                                                 'travel time in the water column'))
        self.listWidgetParam.addItems(self.lista_param)

        self.comboBox_Acesso.setCurrentIndex(3)

    def LerDatumVertical(self):
        print ('-------------------------------- LerDatumVertical')
        if self.flag_ler_datumVert:
            return
        self.lista_datumVert_tot = []
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select id, datum_v FROM datum_v ORDER BY ordem;")
        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            self.lista_datumVert_tot.append(a)
        conn.close()
        print("--------------------- self.lista_datumVert_tot ")
        self.cboDatumVert.clear()
        self.cboDatumVert.addItems(self.lista_datumVert_tot)
        self.flag_ler_datumVert = True

    def actualizarIgnorarLinha(self):
        self.ignorarLinha = self.checkBox_primeira_linha.checkState()
        print('self.ignorarLinha =', self.ignorarLinha)

    def DesactivarWidgets(self):
        print('DesactivarWidgets')
        self.importButton.setEnabled(False)
        self.groupBox.setEnabled(False)

    def ActivarWidgets(self):
        print('ActivarWidgets')
        self.importButton.setEnabled(True)
        self.groupBox.setEnabled(True)

    def validarCdi(self):
        # ---------------------------------  resposta ao evento lineEdit_cdi.editingFinished()
        # ---------------------------------  verificar se se trata de codigo cdi válido, ie, único na BD
        # ---------------------------------- desactivar eventos do lineEdit_cdi
        self.lineEdit_cdi.blockSignals(True)
        print("Validar Cdi.")
        cdi_codigo = self.lineEdit_cdi.text()
        # ----------------------------------------------------------- ligar à BD
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select codigo FROM cdi WHERE codigo = '" + str(cdi_codigo) + "' ;")
        ver = cur.fetchall()
        if len(ver):
            QMessageBox.about(self, u"Erro no código CDI", u"Código CDI:" + cdi_codigo
                              + u" já existe na base de dados!")
            self.lineEdit_cdi.selectAll()
            self.lineEdit_cdi.setFocus()
            # -------------------------------------------- desactivar botão de importação
            self.importButton.setEnabled(False)
        else:
            # -------------------------------------------- Activar botão de importação
            self.importButton.setEnabled(True)

        conn.close()
        # ------------------------------------- Activar eventos do lineEdit_cdi
        self.lineEdit_cdi.blockSignals(False)

    def lerDatumHoriz(self):
        print ('-------------------------------- LerDatumHoriz')
        if self.flag_ler_datumHoriz:
            return

        self.lista_datumHoriz_tot = []
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select id, datum_h FROM datum_h ORDER BY ordem;")
        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            self.lista_datumHoriz_tot.append(a)
        conn.close()
        print("--------------------- self.lista_datumHoriz_tot ")
        self.cboDatumHz.clear()
        self.cboDatumHz.addItems(self.lista_datumHoriz_tot)
        self.flag_ler_datumHoriz = True

    def LerAcesso(self):
        print ('-------------------------------- LerAcesso')
        if self.flag_ler_acesso:
            return

        self.lista_acesso_tot = []
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select id, acesso FROM acesso ORDER BY id DESC;")
        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            self.lista_acesso_tot.append(a)
        conn.close()

        self.comboBox_Acesso.clear()
        self.comboBox_Acesso.addItems(self.lista_acesso_tot)
        self.flag_ler_acesso = True

    def LerPlataf(self):
        # print ('-------------------------------- LerPlataf')
        if self.flag_ler_plataf:
            return

        self.lista_plataf_tot = []
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select * FROM plataforma ORDER BY id;")
        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            self.lista_plataf_tot.append(a)
        self.comboBox_Plataf.clear()
        self.comboBox_Plataf.addItems(self.lista_plataf_tot)
        self.flag_ler_plataf = True
        conn.close()

    def LerComboParam(self):

        print ('-------------------------------- LerComboEquip')
        self.comboBoxParam.setVisible(True)
        if self.flag_ler_param:
            return

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select id, parametro FROM parametro ORDER BY id;")

        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            self.lista_param_tot.append(a)
        conn.close()

        self.comboBoxParam.clear()
        self.comboBoxParam.addItems(self.lista_param_tot)
        self.comboBoxParam.setMaximumWidth(400)
        self.comboBoxParam.setMinimumWidth(0)
        self.comboBoxParam.setMinimumHeight(27)
        self.gridLayout.addWidget(self.comboBoxParam, 5, 3, 1, 2)
        self.comboBoxParam.setVisible(True)
        self.flag_ler_param = True
        # self.lista_param = []

    def LerComboEquip(self):
        print ('-------------------------------- LerComboEquip')
        self.comboBoxEquip.setVisible(True)
        if self.flag_ler_equip:
            return

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("select id, equipamento FROM equipamento ORDER BY id;")

        ver = cur.fetchall()
        for linha in ver:
            a = str(linha)
            a = a.translate(None, "',()")
            self.lista_equip_tot.append(a)
        conn.close()

        self.comboBoxEquip.clear()
        self.comboBoxEquip.addItems(self.lista_equip_tot)
        self.comboBoxEquip.setMaximumWidth(300)
        self.comboBoxEquip.setMinimumWidth(0)
        self.comboBoxEquip.setMinimumHeight(27)
        self.gridLayout.addWidget(self.comboBoxEquip, 5, 1, 1, 2)
        self.comboBoxEquip.setVisible(True)
        self.flag_ler_equip = True
        # self.lista_equip=[]

    def RemoverParam(self):
        a = self.listWidgetParam.currentRow()
        print('a=',a)
        self.lista_param.remove(self.lista_param[a])
        self.listWidgetParam.clear()
        self.listWidgetParam.addItems(self.lista_param)
        self.listWidgetParam.repaint()

    def RemoverEquip(self):
        a = self.listWidget_Equip.currentRow()
        print('a=', a)
        print(self.lista_equip)
        self.lista_equip.remove(self.lista_equip[a])
        self.listWidget_Equip.clear()
        self.listWidget_Equip.addItems(self.lista_equip)
        self.listWidget_Equip.repaint()

    def AtribParam(self):
        # --------------------------------- resposta ao evento comboEquip item changes
        if not(self.comboBoxParam.isVisible()):
            return
        self.lista_param.append(self.comboBoxParam.currentText())
        self.listWidgetParam.addItem(self.comboBoxParam.currentText())
        # após copiar texto de combo para a lista de parametros,
        # esconde o combo, até se clicar outra vez no botão Parametros.
        self.comboBoxParam.setVisible(False)

    def AtribEquip(self):
        # --------------------------------- resposta ao evento comboEquip item changes
        if not self.comboBoxEquip.isVisible():
            return
        self.lista_equip.append(self.comboBoxEquip.currentText())
        self.listWidget_Equip.addItem(self.comboBoxEquip.currentText())
        # após copiar texto de combo para a lista de equipamentos,
        # esconde o combo, até se clicar outra vez no botão Equipamento.
        self.comboBoxEquip.setVisible(False)

    def actualizar_entidade(self):
        # ---------- resposta ao evento change do combo
        # ---------  Entidades
        print "actualizar_entidade, comboBoxEnti currentText=", self.comboBox_Entidades.currentText()
        if self.enti == 1:
            self.lineEdit_C_Contacto.setText(self.comboBox_Entidades.currentText())
            self.lineEdit_C_Contacto.setAlignment(QtCore.Qt.AlignLeft)
            self.lineEdit_C_Contacto.setCursorPosition(0)
        elif self.enti == 2:
            self.lineEdit_C_Origem.setText(self.comboBox_Entidades.currentText())
            self.lineEdit_C_Origem.setAlignment(QtCore.Qt.AlignLeft)
            self.lineEdit_C_Origem.setCursorPosition(0)
        elif self.enti == 3:
            self.lineEdit_C_Distrib.setText(self.comboBox_Entidades.currentText())
            self.lineEdit_C_Distrib.setAlignment(QtCore.Qt.AlignLeft)
            self.lineEdit_C_Distrib.setCursorPosition(0)
        elif self.enti == 4:
            self.lineEdit_C_Org.setText(self.comboBox_Entidades.currentText())
            self.lineEdit_C_Org.setAlignment(QtCore.Qt.AlignLeft)
            self.lineEdit_C_Org.setCursorPosition(0)
        self.comboBox_Entidades.setVisible(False)

    def ler_entidade(self):
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

    def ler_cbos_entidades(self):
        print('ler combos entidades')
        sender = self.sender()
        indice = -1
        print('Sender ===================', sender.name)
        self.comboBox_Entidades.setMinimumHeight(27)
        self.comboBox_Entidades.setVisible(True)
        if sender.name == 'contacto':
            self.gridLayout.addWidget(self.comboBox_Entidades, 7, 1, 1, 3)
            self.enti = 1
            indice = self.comboBox_Entidades.findText(self.lineEdit_C_Contacto.text(), QtCore.Qt.MatchFixedString)
        elif sender.name == 'origem':
            self.gridLayout.addWidget(self.comboBox_Entidades, 7, 3, 1, 2)
            self.enti = 2
            indice = self.comboBox_Entidades.findText(self.lineEdit_C_Origem.text(), QtCore.Qt.MatchFixedString)
        elif sender.name == 'distrib':
            self.gridLayout.addWidget(self.comboBox_Entidades, 8, 1, 1, 3)
            self.enti = 3
            indice = self.comboBox_Entidades.findText(self.lineEdit_C_Distrib.text(), QtCore.Qt.MatchFixedString)
        elif sender.name == 'org':
            self.gridLayout.addWidget(self.comboBox_Entidades, 8, 3, 1, 2)
            self.enti = 4
            indice = self.comboBox_Entidades.findText(self.lineEdit_C_Org.text(), QtCore.Qt.MatchFixedString)

        if indice >= 0:
            self.comboBox_Entidades.setCurrentIndex(indice)
        if self.flag_ler_entidades:
            return

        self.ler_entidade()
        self.flag_ler_entidades = True

    def File_dialog(self):
        # ------------------------- criar "Dialog" de abertura de ficheiros
        fd = QtGui.QFileDialog(self)
        # -------------- preparar leitura de ficheiros do tipo csv (x,y,z,i)
        a = "Open Csv files"
        b = ''
        c = "CSV Files (*.csv);;All Files (*)"
        self.filename = fd.getOpenFileName(self, a, b, c)
        print ("self.filename=", self.filename)

        # ------------------------------------------- verifica se o path escolhido corresponde a ficheiro válido
        if not (isfile(self.filename)):
            QMessageBox(self, 'Importação', self.filename + ' não corresponde a um ficheiro existente !!!')
            return

        # -------------- verifica se existem separadores ',' ou ';' na primeira linha
        # -------------- do ficheiro a ler e modifica o combo separador de acordo
        m = 0
        separador = ''
        with open(self.filename, 'r') as f:
            for line in f:
                m += 1
                if m == 3:
                    print('line=', line)
                    if line.find(',') > -1:
                        separador = ','
                    elif line.find(';') > -1:
                        separador = ';'
                    break
        # --------------------------------- Desactiva temporariamente os eventos do cboSep
        self.cboSep.blockSignals(True)
        print('separador =', separador)
        if separador == ',':
            print('indice = 2')
            self.cboSep.setCurrentIndex(2)

        elif separador == ';':
            print('indice = 3')
            self.cboSep.setCurrentIndex(3)
        # --------------------------------- Activa  os eventos do cboSep
        self.cboSep.blockSignals(False)

        # ----------------------- Lê as primeiras 10 linhas e activa widgets
        self.ler_linhas()

        # ---------------------------------- guarda o tamnho do ficheiro de dados em Mbytes
        self.datasize = getsize(self.filename)
        self.lineEdit_Tamanho.setText(str((self.datasize/1024)/1024))

    def ler_linhas(self):
        # ----------------------------- ler as primeiras n_p linhas do ficheiro seleccionado
        self.separador = self.cboSep.currentText()
        if self.separador == "SPACE":
            self.separador = " "
        n = 0
        text = ""
        with open(self.filename, 'r') as f:
            for line in f:
                n += 1
                text = text+line
                if n > self.num_lin_amostra:
                    break

        # ------------------------------------- determinar seleccões por defeito nas combo box X Y e Z , etc
        # ------------------------------------- de acordo com o nº de colunas detectado
        self.cboX.clear()
        self.cboY.clear()
        self.cboZ.clear()
        self.cboReflect.clear()
        self.cboR.clear()
        self.cboG.clear()
        self.cboB.clear()

        n_col=0
        list1=[]
        nr = 0
        print("******************************* self.separador = ",self.separador )
        flag_sep_consecutivo = False
        linha = line.strip(' ')
        print("classFormImportFile: ler_linhas  linha)", linha)
        for r in linha:
            # print("nr=", nr, "len(line)=", len(line))
            if r == self.separador and flag_sep_consecutivo is False:
                flag_sep_consecutivo = True
                n_col +=1
                list1.append(str(n_col))
                print("classFormImportFile: ler_linhas  n_col)", n_col)
            else:
                flag_sep_consecutivo = False

        n_col += 1
        list1.append(str(n_col))

        print("classFormImportFile: ler_linhas  n_col final)", n_col)

        # ----------------------------- -preencher widget textEdit com as primeiras (self.num_lin_amostra) linhas
        self.textEdit.setText(text)
        self.lineEdit.setText(self.filename)

        # -------------------------------- preencher widgets QCombo com os indices possíveis.  quantas colunas ?
        self.cboX.addItems(list1)
        self.cboY.setCurrentIndex(0)
        self.cboY.addItems(list1)
        self.cboY.setCurrentIndex(1)
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

        # ---------------------------- ficheiro lido, activar widgets para importar, à excepção do
        # ---------------------------- botão Importar (só é activado quando for introduzido o código CDI
        self.ActivarWidgets()
        self.importButton.setEnabled(False)

    def importar(self):
        # -------------------------------------- Flag para controlar erros na importação
        importar_ok = True
        # ------------------------- Verifica se foram definidas colunas distintas suficientes (x,y,z)
        n1 = self.cboX.currentIndex()
        n2 = self.cboY.currentIndex()
        n3 = self.cboZ.currentIndex()
        n4 = -1
        n5 = -1
        n6 = -1
        n7 = -1
        a1 = self.cboX.currentText()
        a2 = self.cboY.currentText()
        a3 = self.cboZ.currentText()

        if (a1 == a2) or (a1 == a3) or (a2 == a3) or (a1 == '') or (a2 == '') or (a3 == ''):
            QMessageBox.about(self, 'Importar', u'Nº de colunas distintas a importar < 3. Importação cancelada !!!')
            importar_ok = False
            return

        # ------------------- verifica se existe código CDI para os dados a importar
        cdi_codigo = self.lineEdit_cdi.text()
        cdi_codigo = cdi_codigo.strip()

        if len(cdi_codigo) == 0:
            QMessageBox.about(self, 'Importar', u'Código CDI inexistente. Importação terminada.')
            print(u'Erro na importação. Código CDI inexistente.')
            importar_ok = False
            return

        if not(isfile(self.filename)):
            QMessageBox(self.filename, u' inexistente. Importação cancelada.')
            importar_ok = False
            return

        # ----------------------------------- determinar codigo epsg do ficheiro a importar
        aa = self.cboDatumHz.currentText().split(' ', 1)
        epsg_code_1 = aa[0]
        print("------------- classFormImportFile: importar: codigo epsg dos dados a importar: ", epsg_code_1)

        # ------------------------------- definir código epsg de todos os dados na base de dados = wgs84
        epsg_code_2 = u"4326"

        print('------------ > ForImportFile_class: importar; self.filename=', self.filename )

        ficheiro_ascii = self.filename
        ficheiro_formatado = self.Config.Path + "/data/data_temp.bt1"

        # Criar objecto para tarefas de Conversão de coordenadas, lib proj4 & OGR

        conversor = ConverterCSV_WGS84()

        if self.radioButton_pos.isChecked():
            conversor.set_positivo(-1)
        else:
            conversor.set_positivo(1)

        tempo_zero = time.time()
        print('-  FormImportFile_class: importar, fich1=', ficheiro_ascii, 'epsg_1=', epsg_code_1, 'fich_2=', ficheiro_formatado,
              'epsg_2=', epsg_code_2)
        conversor.espacamento = self.lineEdit_Esp.text()
        conversor.converter3(self.ignorarLinha, self.separador, ficheiro_ascii, epsg_code_1, ficheiro_formatado, epsg_code_2, n1, n2, n3, n4, n5, n6, n7)
        tempo_converter = time.time() - tempo_zero
        print('_____________________________________________tempo_converter=', tempo_converter)
        # -------------------------------------------- actualizar valores de bounding box horiz. e vert
        self.lineEdit_LatN.setText("%.7f" % conversor.y_max)
        self.lineEdit_LatS.setText("%.7f" % conversor.y_min)
        self.lineEdit_LongE.setText("%.7f" % conversor.x_max)
        self.lineEdit_LongW.setText("%.7f" % conversor.x_min)
        self.lineEdit_ProfMax.setText("%.7f" % (abs(conversor.z_min)))
        self.lineEdit_ProfMin.setText("%.7f" % (abs(conversor.z_max)))
        self.repaint()

        # ------------------------------------- Gravar tabela CDI (metadados) e recuperar qual o cdi_id (integer)
        # ------------------------------------- do registo
        importar_ok, cdi_id = self.gravarCdi()

        if not importar_ok:
            QMessageBox.about(self, u" ERRO !!!", u'Erro a inserir dados na tabela CDI. Importação terminada!!')
            return

        # ----------------------------------------------------------- apagar dados de importações anteriores
        tempo_zero = time.time()
        self.apagarPontosTemp()
        tempo_apagar_pontos = time.time() - tempo_zero
        print('_____________________________________________tempo_apagar_pontos=', tempo_apagar_pontos)
        tempo_zero = time.time()
        conn = None
        # ---------------------------- Nova forma de importar dados a partir de ficheiro de texto formatado (*.bt1)
        print(" *************** FormImportFile_class:  ficheiro_formatado=", ficheiro_formatado)
        try:
            conn = psycopg2.connect(self.Config.Conn)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            print('ficheiro_formatado ----------->', ficheiro_formatado)
            # ----------------------------------------------------- criar objecto do tipo "file"
            ficheiro_bt = open(ficheiro_formatado, 'r')
            # --------------------------------------------------------- inserir ficheiro completo
            cur.copy_from(ficheiro_bt, 'pontos_temp', columns=('x', 'y', 'z', 'i', 'r', 'g', 'b'), sep=',')
            print('Copiar ', ficheiro_formatado, 'para tabela pontos_temp: ------- OK')
        except:
            print('Copiar ', ficheiro_formatado, 'para tabela pontos_temp: ------- ERRO !!')
            importar_ok = False
        finally:
            conn.close()
            ficheiro_bt.close()

        tempo_importar_pontos = time.time() - tempo_zero
        print('_____________________________________________ tempo_importar_pontos=', tempo_importar_pontos)
        # ---------------------------------------------------------------------------- apagar ficheiro temporario
        # try:
        #     remove(ficheiro_formatado)
        # except:
        #     QMessageBox.about(self,'Importar', 'Erro ao apagar ficheiro temporário ' + ficheiro_formatado)
        # finally:
        #     pass

        # ---------------------------------------------------------------------------- apagar pc_points anterior
        tempo_zero = time.time()

        self.apagarPcPoints()

        tempo_apagar_pc_points = time.time() - tempo_zero
        print('_____________________________________________tempo_apagar_pc_points = ', tempo_apagar_pc_points)

        # ---------------------------------------------------------- criar pc_points
        tempo_zero = time.time()
        conn = None
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        strSql = 'INSERT INTO pc_points (pt) SELECT PC_MakePoint(3, ARRAY[a, bb, c, ' \
                 'intensity, r, g, b]) FROM (SELECT x as a, y as bb, z as c,  10 AS intensity, r ,g, b ' \
                 'FROM pontos_temp) AS values;'
        print("**************************** FormImportFile_class: import:pc_points:  strSql =", strSql)

        try:
            cur.execute(strSql)
            print(u'classFormImportFile:__________________ INSERT INTO pc_points OK !')
        except:
            print(u'classFormImportFile:_________________  INSERT INTO pc_points ERRO !!! ')
            importar_ok = False
        finally:
            conn.close()

        tempo_insert_pc_points = time.time() - tempo_zero
        print('__________________________________________tempo_insert_pc_points = ', tempo_insert_pc_points)

        # --------------------------------------------------Ler script para criar Patches a partir de PC_points
        self.sql_insert_patches ='sql_insert_into_patches.sql'
        with open(self.sql_dir + self.sql_insert_patches, 'r') as f:
            strSql = f.read().decode("utf-8-sig").encode("utf-8")
        f.close()

        # ------------------------------ Ler valor de espacamento medio entre pontos para ajustar tamanho dos patches
        self.esp = self.lineEdit_Esp.text()

        # ------------------------------------ esp dado em metros, utilizar UTM 29N para calcular tamanho de celula
        # ----------------- pt a W de Lisboa: 39ºN, 10ºW
        lat_ini = 39.0
        long_ini = -10.0

        lado = float(self.esp)
        x_lxa, y_lxa = conversor.converter_simples(long_ini,lat_ini,4326,32629)
        x_lxb = x_lxa + lado
        y_lxb = y_lxa + lado
        long_fin, lat_fin = conversor.converter_simples(x_lxb,y_lxb,32629,4326)
        dim_patch = abs(lat_fin-lat_ini)
        dim_patch_longi = abs(long_fin-long_ini)

        # ------------------------------------ arredondar dim_patch para múltiplos de min_patch
        if dim_patch < self.min_patch:
            dim_patch = self.min_patch
            print(" ************** Arredondamento  dim_patch, dim_patch_longi  = ",  dim_patch, dim_patch_longi)
        else:
            n = dim_patch // self.min_patch
            dim_patch = n * self.min_patch
            print(" ************** Arredondamento n, dim_patch = ", n, dim_patch)

        #  substituir codigo do dataset (cdi) na strSql ('-99' no template sql_insert_patches)
        #  por valor correcto,do tipo bigint)

        print("------------ cdi_id =", cdi_id)
        strSql = strSql.replace('-99', cdi_id)
        strSql = strSql.replace('-88', str(dim_patch))
        tempo_zero = time.time()
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("*********  FormImportFile_class: import: strSql=",strSql)
        try:
            cur.execute(strSql)
            print(u'FormImportFile:__________________ INSERT INTO patches -- OK!')
        except:
            print(u'FormImportFile:__________________ INSERT INTO patches -- ERRO!!')
            importar_ok = False
        finally:
            conn.close()

        tempo_insert_patches = time.time() - tempo_zero
        print('__________________________________________ tempo_insert_patches = ', tempo_insert_patches)

        # --------------------------------------------------------------------------- preencher tabela patches_info
        with open(self.sql_dir + self.sql_insert_patches_info, 'r') as f:
            strSql = f.read().decode("utf-8-sig").encode("utf-8")
        f.close()

        #  substituir codigo do dataset (cdi) na strSql ('-99' no template sql_insert_patches_info) por valor correcto,
        # do tipo bigint
        print("------------ cdi_id = ", cdi_id)
        strSql = strSql.replace('-88', "'" + cdi_codigo + "'")
        strSql = strSql.replace('-99', cdi_id)
        strSql = strSql.replace('\n', ' ')
        strSql = strSql.replace('\r', ' ')
        tempo_zero = time.time()
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("*********  FormImportFile_class: import: strSql=",strSql)
        try:
            cur.execute(strSql)
            print(u'FormImportFile:__________________ INSERT INTO patches_info -- OK!')
        except:
            print(u'FormImportFile:__________________ INSERT INTO patches_info -- ERRO!!')
            importar_ok = False
        finally:
            conn.close()

        tempo_insert_patches_info = time.time() - tempo_zero
        print('__________________________________________ tempo_insert_patches_info = ', tempo_insert_patches_info)

        # --------------------------------------------------------- "Aspirar" tabela patches
        strSql = "VACUUM FULL patches;"
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("*********  classFormImportFile_class: import: strSql=",strSql)
        try:
            cur.execute(strSql)
            print(u'classFormImportFile:______________ Importar Vacuum patches ------ OK')
        except:
            print(u'classFormImportFile:______________ Importar Vacuum patches -- ERRO!!')
            importar_ok = False
        finally:
            conn.close()

        tempo_total = tempo_apagar_pontos + tempo_importar_pontos + tempo_apagar_pc_points + \
                      tempo_insert_pc_points + tempo_insert_patches

        # self.apagarPcPoints()

        self.apagarPontosTemp()

        # # --------------------------------------------------------- Analizar BD
        # strSql = "VACUUM FULL;"
        # conn = psycopg2.connect(self.Config.Conn)
        # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # cur = conn.cursor()
        # print("*********  classFormImportFile_class: import: strSql=", strSql)
        # try:
        #     cur.execute(strSql)
        #     print(u'classFormImportFile:______________ VACUUM FULL ------ OK')
        # except:
        #     print(u'classFormImportFile:______________ VACUUM FULL ---- ERRO!!')
        #     importar_ok = False
        # finally:
        #     conn.close()
        #
        # # --------------------------------------------------------- Analizar BD
        # strSql = "ANALYZE;"
        # conn = psycopg2.connect(self.Config.Conn)
        # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # cur = conn.cursor()
        # print("*********  classFormImportFile_class: import: strSql=", strSql)
        # try:
        #     cur.execute(strSql)
        #     print(u'classFormImportFile:______________ ANALYZE DB ------ OK')
        # except:
        #     print(u'classFormImportFile:______________ ANALYZE DB -- ERRO!!')
        #     importar_ok = False
        # finally:
        #     conn.close()

        if importar_ok:
            print('Importação terminada ----------------------- OK')
            QMessageBox.about(self, u"Importação OK, tempo total:", str(tempo_total))
        else:
            print('Importação terminada------------------------ ERRO !!!')
            QMessageBox.about(self, u" ERRO !!!" , u'Importação com erros.')

    def gravarCdi(self):
        # -------------------------------------- gravar cdi (metadados correspondentes ao dataset)
        importar_ok = True
        cdi_id = ''
        codigo_cdi = self.lineEdit_cdi.text()
        lista = self.cboDatumHz.currentText().split(' ')
        datum_h = lista[0]
        lista = self.cboDatumVert.currentText().split(' ')
        datum_v = lista[0]
        # --------------------------------------------------------
        long_w = self.lineEdit_LongW.text()
        long_e = self.lineEdit_LongE.text()
        lat_n = self.lineEdit_LatN.text()
        lat_s = self.lineEdit_LatS.text()
        min_depth = self.lineEdit_ProfMin.text()
        max_depth = self.lineEdit_ProfMax.text()
        area_type = "curve"
        start_date = self.dateTimeEdit_Ini.text()
        end_date = self.dateTimeEdit_Fim.text()
        unid_tempo = "UHOR"
        abstract = self.lineEdit_Resumo.text()
        platform_class = self.comboBox_Plataf.currentText().split(' ')[0]
        holding_centre = self.lineEdit_C_Contacto.text().split(' ')[0]
        originator = self.lineEdit_C_Origem.text().split(' ')[0]
        distributor = self.lineEdit_C_Distrib.text().split(' ')[0]
        collate_center = self.lineEdit_C_Org.text().split(' ')[0]
        data_size = str(self.lineEdit_Tamanho.text())
        data_access = self.comboBox_Acesso.currentText().split(' ')[0]
        cruise_name = self.lineEdit_Cruzeiro.text()
        cruise_id = cruise_name
        qc_desc = str(self.lineEdit_QC.text())
        qc_comment = str(self.lineEdit_Obs.text())
        if self.comboBox_Feito.currentText() == 'OK':
            qc_status = True
        else:
            qc_status = False

        qc_date = end_date
        revision_date = str(datetime.datetime.now())


        # ---------------------------------------------------------------------------------
        # ----------------- Info para tabelas cdi_equip
        lista_equip = []

        for index in xrange(self.listWidget_Equip.count()):
            a, b = self.listWidget_Equip.item(index).text().split(' ',1)
            lista_equip.append(a)

        # ---------------------------------------------------------------------------------
        # ----------------- Info para tabelas cdi_param
        lista_param = []
        for index in xrange(self.listWidgetParam.count()):
            a, b = self.listWidgetParam.item(index).text().split(' ',1)
            lista_param.append(a)

        # -------------------------------------------------------- Gravar info na tabela Cdi
        strSql = "INSERT INTO cdi (codigo, datum_h, datum_v, min_depth, max_depth, area_type, " \
                 "start_date, end_date, unid_tempo, abstract, platform_class, holding_centre, originator, " \
                 "distributor, collate_centre, data_size, data_access, cruise_name, cruise_id, qc_desc, qc_date, " \
                 "qc_comment, qc_status, revision_date, long_w, long_e, lat_n, lat_s) "

        strSql += "VALUES(" + "'" + codigo_cdi + "', " + datum_h + ", '" + datum_v + "', " + min_depth + ", " + max_depth \
                 + ", '" + area_type + "', '" + start_date + "', '" + end_date + "', '" + unid_tempo + "', '" \
                 + abstract + "', '" + platform_class + "', '" + holding_centre + "', '" + originator +  "', '" \
                 + distributor + "', '" + collate_center + "', " + data_size + ", '" + data_access + "', '"  \
                 + cruise_name + "', '" + cruise_id + "', '" + qc_desc + "', '" + qc_date + "', '" \
                 + qc_comment + "', '" + str(qc_status) + "', '" + revision_date + "', " + long_w + ", " + long_e + ", " \
                 + lat_n + ", " + lat_s + ") RETURNING cdi.id;"

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("*********  classFormImportFile_class: GravarCDI: strSql=", strSql)
        try:
            cur.execute(strSql)
            ver = cur.fetchall()
            for linha in ver:
                cdi_id = str(linha)
                cdi_id = cdi_id.translate(None, "',()")
                print "cdi_id=" + cdi_id
            print(u'classFormImportFile:______________ Gravar CDI ------ OK')
        except:
            print(u'classFormImportFile:______________ Gravar CDI ------ ERRO!!')
            importar_ok = False
        finally:
            conn.close()

        # ------------------------------------------- criar registos cdi_equip + cdi_param
        strSql = "INSERT INTO cdi_equip (cdi, equip_id) VALUES"
        m = len(lista_equip)
        strValues = ''
        for n in range(m):
            strValues += "(" + cdi_id +", '" + lista_equip[n] + "')"
            if n == m-1:
                strValues += ";"
            else:
                strValues += ", "
        strSql += strValues

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("*********  classFormImportFile_class: Gravar cdi_equip: strSql=", strSql)
        try:
            cur.execute(strSql)
            print(u'classFormImportFile:______________ Gravar cdi_equip ------ OK')
        except:
            print(u'classFormImportFile:______________ Gravar cdi_equip ------ ERRO!!')
            importar_ok = False
        finally:
            conn.close()

        strSql = "INSERT INTO cdi_param (cdi, param_id) VALUES"
        m = len(lista_param)
        strValues = ''
        for n in range(m):
            strValues += "(" + cdi_id + ", '" + lista_param[n] + "')"
            if n == m-1:
                strValues += ";"
            else:
                strValues += ", "

        strSql += strValues

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("*********  classFormImportFile_class: Gravar cdi_param: strSql=", strSql)
        try:
            cur.execute(strSql)
            print(u'classFormImportFile:______________ Gravar cdi_param ------ OK')
        except:
            print(u'classFormImportFile:______________ Gravar cdi_param ------ ERRO!!')
            importar_ok = False
        finally:
            conn.close()


        return importar_ok, cdi_id

    def apagarPontosTemp(self):
        conn = None
        importar_ok = True
        try:
            conn = psycopg2.connect(self.Config.Conn)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            strSql = 'DELETE FROM pontos_temp;'
            cur.execute(strSql)
            print('classFormImportFile: Importar: ', strSql, ' OK')
        except:
            print('classFormImportFile: Importar: ', strSql, ' ERRO !!!')
            importar_ok = False
        finally:
            conn.close()

        conn = None

        try:
            conn = psycopg2.connect(self.Config.Conn)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            strSql = 'VACUUM FULL pontos_temp';
            cur.execute(strSql)
            print('classFormImportFile: Importar: ', strSql, ' OK')
        except:
            print('classFormImportFile: Importar: ', strSql, ' ERRO !!!')
            importar_ok = False
        finally:
            conn.close()

        return importar_ok

    def apagarPcPoints(self):
        importar_ok = True
        conn = None
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        strSql = 'DELETE FROM pc_points;'
        print("**************************** FormImportFile_class: import: apagar pc_points:  strSql =", strSql)
        try:
            cur.execute(strSql)
            print(u'classFormImportFile:__________________ ', strSql, ' OK !')
        except:
            print(u'classFormImportFile:_________________ ', strSql, ' ERRO !!! ')
            importar_ok = False
        finally:
            conn.close()

        conn = None
        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        strSql = 'VACUUM FULL pc_points;'
        print("**************************** FormImportFile_class: import: apagar pc_points:  strSql =", strSql)
        try:
            cur.execute(strSql)
            print(u'classFormImportFile:__________________ ',strSql,' OK !')
        except:
            print(u'classFormImportFile:_________________ ', strSql, ' ERRO !!! ')
            importar_ok = False
        finally:
            conn.close()

        return importar_ok

    def filtrarCaract(self,a):
        a = a.replace("'", "")
        a = a.replace("(", "")
        a = a.replace(")", "")
        a = a.replace("'", "")
        a = a.replace(",", " ", 1)
        return a
