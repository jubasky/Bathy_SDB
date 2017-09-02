from PyQt4 import QtGui
class ComboBox(QtGui.QComboBox):
    def showPopup(self):
        self.insertItem(0, 'Added')
        super(ComboBox, self).showPopup()
