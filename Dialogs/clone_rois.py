from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import ui_CloneRois


class CloneRois(QDialog, ui_CloneRois.Ui_Dialog):
    """Dialog for clone selected rois"""
    update_images = pyqtSignal()

    def __init__(self, txt, limits, parent=None):
        # Invoke parent's method
        super(CloneRois, self).__init__(parent)
        #
        # <------------------------ Gui setup ----------------------->
        #
        self.setupUi(self)
        self.lb_rois.setText(txt)
        self.spb_from_slice.setMinimum(limits[0])
        self.spb_from_slice.setMaximum(limits[1])
        self.spb_from_slice.setValue(limits[0])
        self.spb_to_slice.setMinimum(limits[0])
        self.spb_to_slice.setMaximum(limits[1])
        self.spb_to_slice.setValue(limits[1])

    def get_range(self):
        return self.spb_from_slice.value(), self.spb_to_slice.value()