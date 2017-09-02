# -*- coding: utf-8 -*-
from qgis.gui import *
from PyQt4.QtCore import *
class PanTool(QgsMapTool):

    def __init__(self, window):
        QgsMapTool.__init__(self, window)
        self.setCursor(Qt.OpenHandCursor)
        self.dragging = False

    def canvasMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragging = True
            self.canvas().panAction(event)

    def canvasReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.canvas().panActionEnd(event.pos())
            self.dragging = False

