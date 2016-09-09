__author__ = 'm'


class GridLayer(QgsPluginLayer):
    def __init__(self):
        QgsPluginLayer.__init__(self, "GridLayer", "Grid Layer")
        self.setValid(True)