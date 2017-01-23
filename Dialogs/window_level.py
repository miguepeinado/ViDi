
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_WLDialog


class WLDialog(QDialog, ui_WLDialog.Ui_Dialog):
    """Dialog for adjusting window/level for images and overlays"""
    update_images = pyqtSignal()

    def __init__(self, image, overlay,parent=None):
        # Invoke parent's method
        super(WLDialog, self).__init__(parent)
        self.image = image
        #
        # <------------------------ Gui setup ----------------------->
        #
        self.setupUi(self)
        # set intervals for controls
        c_inf, c_sup = self.image.pixel_thresholds()
        self.sld_center.setMinimum(c_inf)
        self.sld_center.setMaximum(c_sup)
        self.spb_center.setMinimum(c_inf)
        self.spb_center.setMaximum(c_sup)
        # No need to change lower limit of window associated controls
        self.sld_window.setMaximum(c_sup)
        self.spb_window.setMaximum(c_sup)
        # set signals for update images
        self.sld_center.valueChanged.connect(self.update_center)
        self.sld_window.valueChanged.connect(self.update_window)
        # set control values
        self.center0 = self.image.attributes['center']
        self.center = self.center0
        self.window0 = self.image.attributes['window']
        self.sld_center.setValue(self.center0)
        self.sld_window.setValue(self.window0)
        if overlay is not None:
            self.overlay = overlay
            self.enable_controls()
            self.sld_min_value.setMinimum(self.overlay.lowest_value)
            self.sld_min_value.setMaximum(self.overlay.highest_value)
            self.spb_min_value.setMinimum(self.overlay.lowest_value)
            self.spb_min_value.setMaximum(self.overlay.highest_value)
            self.sld_min_value.setValue(self.overlay.low_value)
            self.low0 = self.overlay.low_value
            self.high0 = self.overlay.high_value
            self.sld_max_value.setMinimum(self.overlay.lowest_value)
            self.sld_max_value.setMaximum(self.overlay.highest_value)
            self.spb_max_value.setMinimum(self.overlay.lowest_value)
            self.spb_max_value.setMaximum(self.overlay.highest_value)
            self.sld_max_value.setValue(self.overlay.high_value)
            self.alpha0 = self.overlay.alpha
            self.sld_alpha.setValue(self.alpha0)
            # some signals to control intervals
            self.sld_min_value.valueChanged.connect(self.update_low_value)
            self.sld_max_value.valueChanged.connect(self.update_high_value)
            self.sld_alpha.valueChanged.connect(self.update_alpha)

    def update_center(self, new_center):
        self.center = new_center
        self.image.attributes['center'] = new_center
        self.update_window(self.sld_window.value())
        self.update_images.emit()

    def update_window(self, new_window):
        # See notes about window and center choices
        # w_sup = min(abs(self.center - self.sld_center.minimum()), abs(self.center - self.sld_center.maximum()))
        # if new_window > w_sup:
        #     self.sld_window.setValue(w_sup)
        #     new_window = w_sup
        self.image.attributes['window'] = new_window
        self.update_images.emit()

    def update_low_value(self, new_low_value):
        if new_low_value > self.sld_max_value.value():
            self.sld_min_value.setValue(self.sld_max_value.value())
        self.overlay.set_threshold(new_low_value, self.sld_max_value.value())
        self.update_images.emit()

    def update_high_value(self, new_high_value):
        if new_high_value < self.sld_min_value.value():
            self.sld_min_value.setValue(self.sld_min_value.value())
        self.overlay.set_threshold(self.sld_min_value.value(), new_high_value)
        self.update_images.emit()

    def update_alpha(self, new_alpha):
        self.overlay.set_alpha(new_alpha)
        self.update_images.emit()

    def enable_controls(self):
        self.lb_overlay.setEnabled(True)
        self.sld_min_value.setEnabled(True)
        self.spb_min_value.setEnabled(True)
        self.sld_max_value.setEnabled(True)
        self.spb_max_value.setEnabled(True)
        self.sld_alpha.setEnabled(True)
        self.spb_alpha.setEnabled(True)