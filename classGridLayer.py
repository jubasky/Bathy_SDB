__author__ = 'm'

from qgis.core import *

import math

class GridLayer(QgsPluginLayer):
    def __init__(self):
        QgsPluginLayer.__init__(self, "GridLayer", "Grid Layer")

        self.setValid(True)
        self.setCrs(QgsCoordinateReferenceSystem(4326))
        self.setExtent(QgsRectangle(-180, 90, 180, 90))
        self.setCrs(QgsCoordinateReferenceSystem(4326))
        self.setExtent(QgsRectangle(-180, 90, 180, 90))

    def draw(self, renderContext):
        painter = renderContext.painter()
        extent = renderContext.extent()
        xMin = int(math.floor(extent.xMinimum()))
        xMax = int(math.ceil(extent.xMaximum()))
        yMin = int(math.floor(extent.yMinimum()))
        yMax = int(math.ceil(extent.yMaximum()))
        pen = QPen()
        pen.setColor(QColor("light gray"))
        pen.setWidth(1.0)
        painter.setPen(pen)

        mapToPixel = renderContext.mapToPixel()

        for x in range(xMin, xMax+1):
            coord1 = mapToPixel.transform(x, yMin)
            coord2 = mapToPixel.transform(x, yMax)
            painter.drawLine(coord1.x(), coord1.y(),coord2.x(), coord2.y())


        return True