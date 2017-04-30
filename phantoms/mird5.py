import sys
import numpy as np
from PyQt4.QtGui import *
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def MirdPhantom(ct_shape):
    dx = 1.0
    dy = 1.0
    dz = 5.0
    # FOV is 51,2x51,2 cm2
    # z length is [-100, 100]
    z_zero = int(1000./dz)
    shape = ( 2*z_zero, int(512./dy), int(512./dx))
    phantom = np.zeros(shape, dtype=np.float32)
    labels =  np.ndarray(shape, dtype='a10')
    #
    # Trunk: solid elliptical cylinder centered in (0,0) with semiaxis (200, 100) for z in [0, +700]
    #
    z_min = z_zero - int(700./dz)
    z_max = z_zero
    y_semiaxis = 100.
    x_semiaxis = 200.
    slice = np.zeros(shape[1:], dtype=np.float32) - 1000
    slice_labels = np.ndarray(shape[1:], dtype='a10')
    rows, cols = np.ogrid[0:shape[2], 0:shape[1]]
    mask = (rows - shape[2] / 2.) * (rows - shape[2] / 2.) / y_semiaxis ** 2 * dx ** 2 +\
           (cols - shape[1] / 2.) * (cols - shape[1] / 2.) / x_semiaxis ** 2 * dy ** 2 <= 1
    slice[mask] = 0
    slice_labels[mask]="trunk"
    for z in range(z_min, z_max + 1):
        phantom[z, :, :] = slice
        labels[z, :, :] = slice_labels
    #
    # Head: solid elliptical cilinder centered in (0,0) with semiaxis (70, 100) for z in [+700, +855]...
    #
    z_min = z_zero - int(855. / dz)
    z_max = z_zero - int(700. / dz)
    y_semiaxis = 100.
    x_semiaxis = 70.
    slice = np.zeros(shape[1:], dtype=np.float32) - 1000
    slice_labels = np.ndarray(shape[1:], dtype='a10')
    rows, cols = np.ogrid[0:shape[2], 0:shape[1]]
    mask = (rows - shape[2] / 2.) * (rows - shape[2] / 2.) / y_semiaxis ** 2 * dx ** 2 + \
           (cols - shape[1] / 2.) * (cols - shape[1] / 2.) / x_semiaxis ** 2 * dy ** 2 <= 1
    slice[mask] = 0
    slice_labels[mask] = "head"
    for z in range(z_min, z_max + 1):
        phantom[z, :, :] = slice
        labels[z, :, :] = slice_labels
    # ...topped by half an ellipsoid
    z_min = z_zero - int(940. / dz)
    z_max = z_zero - int(855. / dz)
    z_semiaxis = 85.5
    y_semiaxis = 100.
    x_semiaxis = 70.
    z_center = z_max
    for z in range(z_min, z_max + 1):
        slice = np.zeros(shape[1:], dtype=np.float32) - 1000
        slice_labels = np.ndarray(shape[1:], dtype='a10')
        rows, cols = np.ogrid[0:shape[2], 0:shape[1]]
        mask = (rows - shape[2] / 2.) * (rows - shape[2] / 2.) / y_semiaxis ** 2 * dx ** 2 + \
               (cols - shape[1] / 2.) * (cols - shape[1] / 2.) / x_semiaxis ** 2 * dy ** 2 + \
               (z - z_center) * (z -z_center) / z_semiaxis ** 2 * dz ** 2 <= 1
        slice[mask] = 0
        slice_labels[mask] = "head"
        phantom[z, :, :] = slice
        labels[z, :, :] = slice_labels
    #
    # Legs: frustrum of two circular cones
    #
    z_min = z_zero + 1
    z_max = z_zero + int(800. / dz)
    x_center = int(100. / dx)
    for z in range(z_min, z_max + 1):
        x_center *= -1
        slice = np.zeros(shape[1:], dtype=np.float32) - 1000
        slice_labels = np.ndarray(shape[1:], dtype='a10')
        rows, cols = np.ogrid[0:shape[2], 0:shape[1]]
        mask = (rows - shape[2] / 2.) * (rows - shape[2] / 2.) * dy ** 2 +\
               (cols - x_center - shape[1] / 2.) * (cols - x_center - shape[1] / 2.) * dx ** 2 <= \
               (200. - z * dz / 10.) ** 2
        slice[mask] = 0
        slice_labels[mask] = "right leg"
        x_center *= -1
        mask = (rows - shape[2] / 2.) * (rows - shape[2] / 2.) * dy ** 2 + \
               (cols - x_center - shape[1] / 2.) * (cols - x_center - shape[1] / 2.) * dx ** 2 <= \
               (200. - z * dz / 10.) ** 2
        slice[mask] = 0
        slice_labels[mask] = "left leg"
        phantom[z, :, :] = slice
        labels[z, :, :] = slice_labels
    #
    # The whole phantom...
    #
    return phantom


class ShowPhantom(QMainWindow):
    def __init__(self, parent=None):
        super(ShowPhantom, self).__init__(parent)
        # Gui setup
        self.figure = Figure()  # don't use matplotlib.pyplot at all!
        self.canvas = FigureCanvas(self.figure)
        # self.ax = self.figure.add_subplot(111)
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
        # Phantom values
        self.phantom = MirdPhantom(0)
        self.z = self.phantom.shape[0] / 2
        self.plot()

    def plot(self):
        # create an axis
        self.ax = self.figure.add_subplot(111)
        self.ax.hold(False)
        # plot data
        slice = self.phantom[self.z, :, :]
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