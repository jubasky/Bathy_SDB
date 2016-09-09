from qgis.gui import *
from qgis.core import *
from PyQt4 import QtGui
from PyQt4 import QtCore

from formGrid2 import Ui_formGrid
from classDB_Admin import DB_Admin


class GridForm(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # ------------- implementar a UI definida pela form Grid (Qt)
        self.ui = Ui_formGrid()
        self.ui.setupUi(self)

        canvas =  self.ui.widgetMap
        canvas.useImageToRender(False)
        canvas.show()

        # ---------------  mostrar inicialmente um mapa global
        shapefile = "C:/data/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp"
        layer1 = QgsVectorLayer(shapefile, "world", "ogr")

        QgsMapLayerRegistry.instance().addMapLayer(layer1)
        QgsMapLayerRegistry.instance().addMapLayer(layer1)
        canvas.setExtent(layer1.extent())
        canvas.setLayerSet([ QgsMapCanvasLayer(layer1)])

        # CRIA  objecto de acesso a adados
        a = DB_Admin()
        a.ligar()
        b = a.ler_sql('SELECT * FROM spatial_ref_sys LIMIT 10;')
        t1=''
        for linha in b:
            t1 = t1 + str(linha[1]) + ' ' + str(linha[2]) + ' ' + str(linha[3]) +'\n'
        print t1
        a.desligar()
        a = None

