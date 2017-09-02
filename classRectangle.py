from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import QMessageBox
from classFormPesquisa import FormPesquisa

class RectangleMapTool(QgsMapToolEmitPoint):

    def __init__(self, canvas, tv):
        self.canvas = canvas
        self.tv = tv

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setOpacity(.4)
        self.rubberBand.setWidth(1)
        self.reset()
        self.rect_mouse_up = False
        self.Identif = QgsMapToolIdentify
        self.janela = None

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QGis.Polygon)

    def canvasPressEvent(self, e):
        r = self.rectangle()
        checkPoint = self.toMapCoordinates(e.pos())
        x1 = checkPoint.x()
        y1 = checkPoint.y()
        if r is not None and self.rect_mouse_up:
            print(x1, y1, self.startPoint.x(), self.endPoint.x() ,self.startPoint.y(), self.endPoint.y() )
            if (x1 >= r.xMinimum() and x1 <= r.xMaximum()) and (y1 >= r.yMinimum() and y1 <= r.yMaximum()):
                print "dentro do Rectangle:",x1,y1, r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum()
                self.rect_mouse_up = False
                self.janela = None
                self.janela = FormPesquisa(self.tv)
                self.janela.set_cantos(self.startPoint.x(), self.endPoint.x() ,self.startPoint.y(), self.endPoint.y())

                self.janela.show()


                return

        # print "Fora do Rectangle:", x1, y1, r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum()
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showRect(self.startPoint, self.endPoint)



    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        r = self.rectangle()
        self.rect_mouse_up = True
        if r is not None:
            print "Rectangle:", r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum()

        if e.button() == Qt.RightButton:
            print "right"
            if r is not None:
                print "Rectangle:", r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum()
        else:
            print "left"
            if r is not None:
                print "Rectangle:", r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum()

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return

        self.endPoint = self.toMapCoordinates(e.pos())
        self.showRect(self.startPoint, self.endPoint)

    def showRect(self, startPoint, endPoint):
        self.rubberBand.reset(QGis.Polygon)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return

        point1 = QgsPoint(startPoint.x(), startPoint.y())
        point2 = QgsPoint(startPoint.x(), endPoint.y())
        point3 = QgsPoint(endPoint.x(), endPoint.y())
        point4 = QgsPoint(endPoint.x(), startPoint.y())

        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)    # true to update canvas
        self.rubberBand.show()

    def rectangle(self):
        if self.startPoint is None or self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            return None

        return QgsRectangle(self.startPoint, self.endPoint)

    def deactivate(self):
        super(RectangleMapTool, self).deactivate()
        self.emit(SIGNAL("deactivated()"))