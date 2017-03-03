import sys
from PyQt4 import QtCore, QtGui
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter


# From http://stackoverflow.com/questions/29992771/combining-pyqt-and-matplotlib:
# "When combining matplotlib in PyQt, don't use the matlab-like interface of
#  the pyplot module at all. Use the matplotlib classes directly."
class DoseReport(QtGui.QMainWindow):
    def __init__(self, vois, parent=None):
        super(DoseReport, self).__init__(parent)

        self.figure = Figure()  # don't use matplotlib.pyplot at all!
        self.canvas = FigureCanvas(self.figure)
        # use addToolbar to add toolbars to the main window directly!
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.addToolBar(self.toolbar)
        self.main_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.main_widget.setLayout(layout)
        self.plot(vois)

    def plot(self, vois):
        # create an axis
        ax = self.figure.add_subplot(111)
        # Tweak axes:
        ax.grid(True)
        ax.set_title('Dose Volume histograms')
        ax.set_xlabel('Dose (mGy)')
        ax.set_ylabel('Volume (% of total)')
        # ...Create the formatter using the function to_percent. This multiplies all the
        # default labels by 100, making them all percentages
        # (from http://matplotlib.org/examples/pylab_examples/histogram_percent_demo.html)
        formatter = FuncFormatter(self.to_percent)
        self.figure.gca().yaxis.set_major_formatter(formatter)
        # don't repaint at each plot call
        ax.hold(True)
        # plot data
        for v in vois:
            l = str(v.label)
            print "-->", l
            ax.hist(v.doses().values(), normed=True, cumulative=-1, histtype='step', label=l)
        # refresh canvas
        ax.legend(loc='lower left')
        self.canvas.draw()

    def to_percent(self, y, position):
        # Ignore the passed in position. This has the effect of scaling the default
        # tick locations.
        s = str(100 * y)

        # The percent symbol needs escaping in latex
        if matplotlib.rcParams['text.usetex'] is True:
            return s + r'$\%$'
        else:
            return s + '%'
