


def ler_entidades_1(self):
    # --------------------responde ao evento click() de line_edit_C's relativos a entidades
    print('Ler entidades')
    # self.comboBox_Entidades.setMaximumWidth(200)
    self.gridLayout.addWidget(self.comboBox_Entidades, 5, 1, 1, 2)
    self.comboBox_Entidades.setMinimumHeight(27)
    self.comboBox_Entidades.setVisible(True)
    self.enti = 1
    indice = self.comboBox_Entidades.findText(self.lineEdit_C_Contacto.text(), QtCore.Qt.MatchFixedString)
    if indice >= 0:
        self.comboBox_Entidades.setCurrentIndex(indice)

    if self.flag_ler_entidades:
        return
    self.ler_entidade()
    self.flag_ler_entidades = True


def ler_entidades_2(self):
    # --------------------responde ao evento click() de line_edit_C's relativos a entidades
    print('Ler entidades')
    # self.comboBox_Entidades.setMaximumWidth(0)
    self.gridLayout.addWidget(self.comboBox_Entidades, 5, 3, 1, 2)
    self.comboBox_Entidades.setMinimumHeight(27)
    self.comboBox_Entidades.setVisible(True)
    self.enti = 2
    indice = self.comboBox_Entidades.findText(self.lineEdit_C_Origem.text(), QtCore.Qt.MatchFixedString)
    if indice >= 0:
        self.comboBox_Entidades.setCurrentIndex(indice)

    if self.flag_ler_entidades:
        return
    self.ler_entidade()
    self.flag_ler_entidades = True


def ler_entidades_3(self):
    # --------------------responde ao evento click() de line_edit_C's relativos a entidades
    print('Ler entidades')
    # self.comboBox_Entidades.setMaximumWidth(0)
    self.gridLayout.addWidget(self.comboBox_Entidades, 6, 1, 1, 2)
    self.comboBox_Entidades.setMinimumHeight(27)
    self.comboBox_Entidades.setVisible(True)
    self.enti = 3
    indice = self.comboBox_Entidades.findText(self.lineEdit_C_Distrib.text(), QtCore.Qt.MatchFixedString)
    if indice >= 0:
        self.comboBox_Entidades.setCurrentIndex(indice)

    if self.flag_ler_entidades:
        return

    self.ler_entidade()
    self.flag_ler_entidades = True


def ler_entidades_4(self):
    # --------------------responde ao evento click() de line_edit_C's relativos a entidades
    print('Ler entidades')
    # self.comboBox_Entidades.setMaximumWidth(0)
    self.gridLayout.addWidget(self.comboBox_Entidades, 6, 3, 1, 2)
    self.comboBox_Entidades.setMinimumHeight(27)
    self.comboBox_Entidades.setVisible(True)
    self.enti = 4

    indice = self.comboBox_Entidades.findText(self.lineEdit_C_Org.text(), QtCore.Qt.MatchFixedString)
    if indice >= 0:
        self.comboBox_Entidades.setCurrentIndex(indice)
    if self.flag_ler_entidades:
        return

    self.ler_entidade()
    self.flag_ler_entidades = True