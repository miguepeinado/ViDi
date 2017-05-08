import sys
import numpy as np
from PyQt4.QtGui import *
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
from mird5 import phantom


class ShowPhantom(QMainWindow):
    def __init__(self, parent=None):
        super(ShowPhantom, self).__init__(parent)
        # Gui setup
        self.figure = Figure()  # don't use matplotlib.pyplot at all!
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        act_up = QAction(QIcon().fromTheme("go-up"), "up", self.toolbar)
        act_up.triggered.connect(self.slice_up)
        act_down = QAction(QIcon().fromTheme("go-down"), "down", self.toolbar)
        act_down.triggered.connect(self.slice_down)
        act_10up = QAction(QIcon().fromTheme("go-top"), "10up", self.toolbar)
        act_10up.triggered.connect(self.slice_10up)
        act_10down = QAction(QIcon().fromTheme("go-bottom"), "10down", self.toolbar)
        act_10down.triggered.connect(self.slice_10down)
        self.toolbar.addAction(act_up)
        self.toolbar.addAction(act_down)
        self.toolbar.addAction(act_10up)
        self.toolbar.addAction(act_10down)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.main_widget.setLayout(layout)
        #
        # Phantom values
        #
        voxel_size = np.array([1, 1, 5])
        fov_size = np.array([512, 512, 2000])
        # HU values from https://en.wikipedia.org/wiki/Hounsfield_scale
        hu_values = {'air': -1000, 'body': 0, 'adrenals': 25, 'bladder': (50, 10), 'brain': 40, 'kidneys': 30, 'liver': 60,
                     'lungs': -500, 'ovaries':25, 'pancreas': 25, 'spleen': 50, 'stomach': (500, 20), 'thymus': 50, 'uterus': 100}
        hu_values = {'air': -1000, 'body': 0, 'intestine': (500, 20)}
        self.phantom = phantom(hu_values, "f", voxel_size, fov_size)
        self.z = self.phantom.shape[0] / 2
        self.plot()

    def plot(self):
        # create an axis
        self.ax = self.figure.add_subplot(111)
        # plot data
        slice = self.phantom[self.z, :, :]
        if np.any(slice): print "--->", self.z
        self.ax.imshow(slice)
        # refresh canvas
        self.canvas.draw()
        bar = self.statusBar()
        bar.showMessage('z: {}'.format(self.z))

    def slice_up(self, pushed):
        self.z -= 1
        if self.z < 0:
            self.z = 0
        self.plot()

    def slice_down(self, pushed):
        self.z += 1
        if self.z == self.phantom.shape[0]:
            self.z -= 1
        self.plot()

    def slice_10up(self, pushed):
        self.z -= 10
        if self.z < 0:
            self.z = 0
        self.plot()

    def slice_10down(self, pushed):
        self.z += 10
        if self.z == self.phantom.shape[0]:
            self.z = self.phantom.shape[0] - 1
        self.plot()

# Autolaucher
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ShowPhantom()
    w.show()
    app.exec_()