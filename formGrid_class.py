# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from formGrid import Ui_formGrid

class formGrid(QtGui.QWidget, Ui_formGrid):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

    def MostraMapa(self):
        canvas =  self.widgetMap
        canvas.useImageToRender(False)
        canvas.show()

        # --------------- mapa global
        shapefile = "C:/data/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp"
        layer1 = QgsVectorLayer(shapefile, "world", "ogr")

        QgsMapLayerRegistry.instance().addMapLayer(layer1)
        # QgsMapLayerRegistry.instance().addMapLayer(layer1)
        canvas.setExtent(layer1.extent())
        canvas.setLayerSet([ QgsMapCanvasLayer(layer1)])
