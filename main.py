# -*- coding: utf-8 -*-

# --------------------------------- módulo correspondente à gestão do programa principal e da
# --------------------------------- respectiva janela, Ui_Main_Window
import sys
from qgis.gui import *
from qgis.core import *
from PyQt4 import QtGui
from PyQt4 import QtCore

from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QFrame
from PyQt4.QtGui import QDockWidget
from PyQt4.QtCore import *

# ----------------------------------------------- carregar as diferentes classes e "forms", para assegurar
# ----------------------------------------------- as funcionalidades do programa
from main_Window import Ui_Main_Window
from classFormImportFile import FormImportFile
from classFormConnect import FormConnect
from classFormNewDatabase import FormNewDB
from classTreeVMenuProvider import TreeVMenuProvider
from classIdentifyTool import IdentifyTool
from classRectangle import RectangleMapTool

from classPanTool import PanTool
from classConfig import Config
from classFormConfig import FormConfig
# ----------------------------------------------------- importar ícones, etc.
import resources

# ------------------------------------------------------Classe Principal, subclasse de QMainWindow (Qt)
class StartQT4(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # --------------------------------------- implementar a UI definida pela form Main_Window (Qt)
        self.ui = Ui_Main_Window()
        self.ui.setupUi(self)
        # ------------------------------ criar label para mostar latitude, longitude e escala
        # ------------------------------ em self.ui.statusBar
        self.ui.lblXY = QLabel()
        self.ui.lblXY.setFrameStyle(QFrame.Box)
        self.ui.lblXY.setMinimumWidth(170)

        self.ui.lblXY.setFont(QtGui.QFont("Arial", 8))
        self.ui.lblXY.setAlignment(Qt.AlignCenter)
        self.ui.statusbar.setSizeGripEnabled(False)
        self.ui.statusbar.addPermanentWidget(self.ui.lblXY, 0)

        self.ui.lblScale = QLabel()
        self.ui.lblScale.setFrameStyle(QFrame.StyledPanel)
        self.ui.lblScale.setFont(QtGui.QFont("Arial", 8))
        self.ui.lblScale.setMinimumWidth(140)
        self.ui.statusbar.addPermanentWidget(self.ui.lblScale, 0)

        # --------------------------------------------------- inicializar atributos da class
        self.janela = None
        self.filename = ""
        self.file_epsg = ""
        self.fich_transf = ""
        self.preview_filename = ""
        self.lista_cdis = []
        self.cdis_str = ''
        self.first_treeChange = False
        self.lista_cdis_lidos = []
        self.lista_cdis_activos = []
        self.layers = []
        # ---------------------------------------------------- criar canvas (mapa)
        self.canvas = self.ui.widget
        self.canvas.useImageToRender(False)
        self.canvas.cacheMode = True
        self.canvas.enableAntiAliasing(True)
        self.canvas.show()

        # -------------------------------------------- ui.splitter: dimensiona a largura do mapa e do explorador
        m = self.ui.splitter
        m.setSizes([50, 100])

        # ------------------------------------------------------------------------------- Inicializar LegendDock
        self.root = QgsProject.instance().layerTreeRoot()
        self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.canvas)
        self.model = QgsLayerTreeModel(self.root)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag(QgsLayerTreeModel.ShowLegend)

        self.view = QgsLayerTreeView()
        self.view.setModel(self.model)
        self.LegendDock = QDockWidget("Layers", self)
        self.LegendDock.setObjectName("layers")
        self.LegendDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.LegendDock.setWidget(self.view)
        self.LegendDock.setContentsMargins(9, 9, 9, 9)

        # --------------------------------------------------------- adicionar legend dock à janela principal
        self.addDockWidget(Qt.LeftDockWidgetArea, self.LegendDock)

        # ----------------------------------------------------------- definir menu de contexto para TreeView
        self.provider = TreeVMenuProvider(self.view, self.canvas)
        self.view.setMenuProvider(self.provider)
        # -----------------------------------------------------------------------------------------
        # ------------------------  ligação de "sinais" da UI a "slots" da classe
        # -----------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------- Menus
        QtCore.QObject.connect(self.ui.actionImportXYZ, QtCore.SIGNAL("activated()"), self.File_Input)
        QtCore.QObject.connect(self.ui.actionConnect, QtCore.SIGNAL("activated()"), self.Connect_dialog)
        QtCore.QObject.connect(self.ui.actionNew, QtCore.SIGNAL("activated()"), self.CriarDB)
        QtCore.QObject.connect(self.ui.actionConfig, QtCore.SIGNAL("activated()"), self.Config)

        # ------------------------------------------------------------------------------- Mouse move
        self.connect(self.canvas, SIGNAL("xyCoordinates(QgsPoint)"), self.mostrarXY)
        self.connect(self.canvas, SIGNAL("scaleChanged(double)"), self.mostrarEscala)


        # ----------------------------------------------------------------------------- Botões
        self.ui.pushButton_converte.clicked.connect(self.CriarDB)
        self.ui.pushButton_preview.clicked.connect(Preview)

        # --------------------------------------------------------- Activar identify tool & pan tool
        self.IdentifyTool = IdentifyTool(self.canvas, self.provider)
        self.rectTool = RectangleMapTool(self.canvas, self.provider)
        self.panTool = PanTool(self.canvas)

        self.panTool.setAction(self.ui.actionPan)

        # ------------------------------------------------------------ Pan + Identify + Zoom + Mooz
        self.connect(self.ui.actionPan, SIGNAL("triggered()"), self.setPanMode)
        self.connect(self.ui.actionIdentify, SIGNAL("triggered()"), self.setIdentifyMode)
        self.connect(self.ui.actionZoomIn, SIGNAL("triggered()"), self.zoomIn)
        self.connect(self.ui.actionZoomOut, SIGNAL("triggered()"), self.zoomOut)
        self.connect(self.ui.actionSelect, SIGNAL("triggered()"), self.setRectangleMode)

        # --------------------------------------------------------- mostrar mapas + patches
        self.provider.MostrarMapa()

    # ----------------------------------- resposta a click no botão Preview

    def zoomIn(self):
        self.canvas.zoomIn()

    def zoomOut(self):
        self.canvas.zoomOut()

    def setPanMode(self):
        self.ui.actionIdentify.setChecked(False)
        self.ui.actionPan.setChecked(True)
        self.canvas.setMapTool(self.panTool)
        self.ui.actionSelect.setChecked(False)

    def setIdentifyMode(self):
        self.ui.actionPan.setChecked(False)
        self.ui.actionIdentify.setChecked(True)
        self.canvas.setMapTool(self.IdentifyTool)
        self.ui.actionSelect.setChecked(False)

    def setRectangleMode(self):
        self.ui.actionPan.setChecked(False)
        self.ui.actionIdentify.setChecked(False)
        self.ui.actionSelect.setChecked(True)
        self.canvas.setMapTool(self.rectTool)

    def mostrarXY(self, ponto):
        #  ----------------------------------------------------------------- mostrar lat + long na statusBar
        self.ui.lblXY.setText( ("%0.5f" % (ponto.x())) + " | " + ("%0.5f" % (ponto.y())) )

    def mostrarEscala(self, escala):
        #  --------------------------------------------------------------------- mostrar escala na statusBar
        self.ui.lblScale.setText( "Scale 1:" + "%0.0f" % (escala) )

    def Config(self):
        # -------------  Abrir janela para definir configurações do sistema:
        # -------------  caminhos, endereços ip do servidor de dados, utilizdores,
        # -------------  passwords, etc.
        print('Config ------------------')
        self.janela = None
        self.janela = FormConfig()
        self.janela.show()

    def File_Input(self):
        # --------------------------  Carregar classe/janela de importação de dados
        self.janela = None
        self.janela = FormImportFile()
        self.janela.show()
        self.file_epsg = self.janela.epsg

    def Connect_dialog(self):
        # ---------------------- criar formConnect, primeiro, destruir alguma janela pre-existente
        self.janela = None
        self.janela = FormConnect()
        self.janela.show()

    def CriarDB(self):
        # ----------------------------------------------------- carregar janela para criar nova BD
        self.janela = None
        self.janela = FormNewDB()
        self.janela.show()

def Preview():
    print('preview')
    print('---------------------------------')
    for layer in QgsMapLayerRegistry.instance().mapLayers().values():
        a = layer.name()
        print(a)
    print('---------------------------------')

# ----------------------------------------------------------------------------------------
# -------------------------------------------------- Main --------------------------------
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    # ------------------------------------
    Config = Config('config.ini')
    # ---------------------------------------------------- Definir prefixo (path)
    # ---------------------------------------------------- para livrarias PyQGis
    # QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
    QgsApplication.setPrefixPath(Config.PathQ, True)
    print('////////////////////////// QgsApplication.setPrefixPath -------->', QgsApplication.prefixPath())
    QgsApplication.initQgis()

    # ------------------------------------criar a janela principal do programa
    myapp = StartQT4()
    myapp.show()
    myapp.setPanMode()
    app.exec_()
    # ---------------------------- THE END
    # ------------------------------------
    QgsApplication.exitQgis()