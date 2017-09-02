# -*- coding: utf-8 -*-
from qgis.gui import *
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import *
# ----------------------------------------------------- Identificador de "features" por click


class IdentifyTool(QgsMapToolIdentify):

    def __init__(self, window, tv):
        QgsMapToolIdentify.__init__(self, window)
        self.window = window
        self.tv = tv

    def canvasReleaseEvent(self, event):

        if event.button() == Qt.RightButton:
            menu = QtGui.QMenu()
            quitAction = menu.addAction("Ver pontos")
            action = menu.exec_(self.window.mapToGlobal(QPoint(event.pos().x(), event.pos().y())))

            found_features = self.identify(event.x(), event.y(), self.TopDownStopAtFirst, self.VectorLayer)
            if len(found_features) > 0:
                feature = found_features[0].mFeature
                info = []

                prof = str(feature.attribute("prof"))
                num_pts = str(feature.attribute("n"))
                id_found = str(feature.attribute("id"))
                cdi_found = str(feature.attribute("cdi"))

                info.append('id=' + id_found)
                info.append('cdi=' + cdi_found)
                info.append('prof med.=' + prof)
                info.append('npts='  + num_pts)
                # QMessageBox.about(self.window, "Info", "\n".join(info))
                self.tv.lerPontos(cdi_found, id_found)
                self.window.refresh()

            return


        #  -------- Left Button
        found_features = self.identify(event.x(), event.y(), self.TopDownStopAtFirst, self.VectorLayer)
        if len(found_features) > 0:
            feature = found_features[0].mFeature
            info = []
            try:
                codigo_found = str(feature.attribute("codigo"))
                info.append('cod_cdi=' + codigo_found)

                id_found = str(feature.attribute("id"))
                info.append('id=' + id_found)

                prof = str(feature.attribute("prof"))
                info.append('prof med.=' + prof)

                num_pts = str(feature.attribute("n"))
                info.append('npts=' + num_pts)


                point = self.window.getCoordinateTransform().toMapCoordinates(event.x(), event.y())
                # print(point)
                latitude = point[1]
                longitude = point[0]

                info.append("Lat/Long: %0.5f, %0.5f" % (latitude, longitude))

            except:
                pass
            finally:
                pass
            if len(info)>0:
                QMessageBox.about(self.window, "Info", "\n".join(info))

    def canvasMoveEvent(self, event):
        pass


