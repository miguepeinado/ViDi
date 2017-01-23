import sys
import os
from PyQt4 import QtCore
from PyQt4 import QtGui
import ui_ViDi
import ViDiGraphics
import MyDicom

class Prueba(QtGui.QFrame):
    def __init__(self, parent=None):
        super(Prueba, self).__init__(parent)
        l = QtGui.QGridLayout()
        for i in range(256):
            r = i // 16
            c = i % 16
            lb = MyLabel(str(i))
            col = QtGui.QColor().fromRgb(i, i, i)
            col = QtGui.QColor().fromHsl((255 - i), 255, 128, 92)
            lb.set_color(col)
            l.addWidget(lb, r, c, 1, 1)
        self.setLayout(l)

class MyLabel(QtGui.QLabel):
    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self._color = None

    def set_color(self, color):
        self._color = color
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        w = self.size().width()
        h = self.size().height()
        qp.fillRect(0, 0, w, h, self._color)
        super(MyLabel, self).paintEvent(event)

# Autolauncher
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    c = Prueba()
    c.show()
    app.exec_()
