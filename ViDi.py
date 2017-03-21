#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Program ViDi loads an image or a set of DICOM images to do some operations on them.

This class contains most of the gui functionality while the engine of the program is mostly contained in the ImageView
class.

Basic features of ViDi are:
    - Zoom of image(s)
    - Moving through images of the dataset
    - Hybrid modalities registration (shown as watershed overlay)
    - Change WL and watershed levels and opacity
    - ROI drawing and stats extraction
    - Automatic ROI drawing

Other features are expected in the future:
    - internal dosimetry for radionuclide therapy
    - DQE measurement
    - NORMI-13 automatic feature extraction
    - Mammo density definition and dosimetry
    - 3D multiplanar or mpr imaging

Version:
    - 0.1:  Basic features almost done (circular ROI and automatic ROI definition not implemented. ROI stats not shown)
    - 0.2:  BUG of half of pixel displacement @ ViDiGraphics...corrected
            Define a logger on the user's home directory (not complete)
            circular ROI implemented
            Calculates rois statistics and shows a dialog (todo copy roi statistics)
            Separate stats in an object. Implement a Voi object with many rois (i.e. an organ)
            BUG points of moved rois not updated in scene...corrected

BUGS:
    - Changes in font size and line width when zooming
    - Cursor change when hover a pol. roi even if it is not selected
    - Roi stats values are false!!!

IMPROVEMENTS (other minor features to implement or made "on the fly"):
    - Logger to track bugs and errors (not complete)
    - Window and center choices don't like me!!! => Put an histogram in the dialog and some automatic choices.
    - Export image to other formats
    - Copy/paste rois
    - Roi stats dialog
    - Change mouse operations (left button -> Select/rois, wheel-> move between slices/zoom, right ->WL)


"""
import sys
import os
import logging
from PyQt4 import QtCore
from PyQt4 import QtGui
import ui_ViDi
import ViDiGraphics
import MyDicom

__author__ = "M.A. Peinado"
__copyright__ = "2016, M.A. Peinado"
__credits__ = ["Miguel A. Peinado"]
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "M.A. Peinado"
__email__ = "miguel.peinado@sespa.es"
__status__ = "Beta testing"


class ViDi(QtGui.QMainWindow, ui_ViDi.Ui_MainWindow):
    """ Load GUI and manages user interaction as:
        - loading images
        - Mouse operation
    """
    # todo: icon and operability of show info action
    # todo: action for help (documentation)
    OP_SELECT = 0
    OP_CHANGE_SLICES = 1
    OP_WL = 2
    OP_ZOOM = 3

    def __init__(self, parent=None):
        # Invoke parent's method
        super(ViDi, self).__init__(parent)
        #
        # <------------------------ Gui setup ----------------------->
        #
        self.setupUi(self)
        # Additional GUI tweaks
        self.setWindowIcon(QtGui.QIcon(":Others/pictures/ViDi.svg"))
        self.tb_tools.setVisible(False)
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        f = self.progress_bar.font()
        f.setWeight(QtGui.QFont.Bold)
        self.progress_bar.setFont(f)
        self.progress_bar.setStyleSheet("::chunk { background: \
                                        qlineargradient( x1: 0, y1: 0.5, x2: 1, y2: 0.5, \
                                        stop: 0 green, stop: 1 white);}")
        self.status_bar = self.statusBar()
        self.resize(800, 720)
        self.tb_files.setStyleSheet("QToolButton:hover { border-style: solid;\
                            border: 2px solid green; border-radius: 10px;\
                            background: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0.2 green, stop:1 black);}\
                            QToolButton:pressed { border-style: solid;\
                            border: 2px solid rgb(128,255,128); }\
                            QToolButton:checked {border-style: solid;\
                            border: 2px solid rgb(128,255,128);  border-radius: 10px;\
                            background: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0.2 'green', stop:1 'gray'); }")

        # Add view(s)
        w = QtGui.QWidget()
        l = QtGui.QHBoxLayout()

        self.view = ViDiGraphics.ImageView(0, self)
        l.addWidget(self.view)
        w.setLayout(l)
        self.setCentralWidget(w)
        #
        # <------------------------------ Signals ----------------------------->
        #
        self.view.view_updated.connect(self.show_message)
        self.view.load_overlay.connect(self.load_overlay)
        self.act_open_file.triggered.connect(self.load_image)
        self.act_show_info.triggered.connect(self.view.show_info)
        self.tb_edit.actionTriggered.connect(self.set_operation)
        self.view.roi_finished.connect(self.uncheck_rois)
        self.act_roi_auto.triggered.connect(self.view.set_auto_roi)
        self.act_clone_rois.triggered.connect(self.view.clone_rois)
        self.act_get_stats.triggered.connect(self.view.show_stats)
        self.act_dosimetry.triggered.connect(self.view.dosimetry)
        #
        # <----------------------------- Attributes --------------------------->
        #
        self._current_dir = os.getcwd()
        from os.path import expanduser
        home = expanduser("~")
        self.show_message("Log file created in " + home)
        logging.basicConfig(format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                            datefmt='%m-%d %H:%M', filename=home + '/ViDi.log',
                            filemode='w', level=logging.INFO)
        logging.info('ViDi started')
        # Install exception handler
        # sys.excepthook = self.exception_handler

#
# <------------------------------ Slots ----------------------------->
#
    def load_overlay(self):
        self.load_image(is_overlay=True)

    def load_image(self, is_overlay=False):
        """Loads the file name(s) of an image or sequence of images"""
        logging.info("Ready to load file(s) as " + ("overlay" if is_overlay else "image"))
        d = QtGui.QFileDialog()
        d.setWindowTitle('Load image or sequence of images')
        d.setDirectory(self._current_dir)
        d.setFileMode(QtGui.QFileDialog.ExistingFiles)
        d.setFilter("DICOM files (*.ima *.dcm);;All files (*.*)")
        if d.exec_() == d.Accepted:
            fn = d.selectedFiles()
            files = [str(f) for f in d.selectedFiles()]
            # Must reinitialize all the graphics
            # self.view.scene().erase_pixmap()
            if len(files) > 0:
                self.status_bar.clearMessage()
                self.progress_bar.setMaximum(len(files))
                self.status_bar.addWidget(self.progress_bar)
                th = MyDicom.ImageLoader(files, is_overlay=is_overlay)
                th.updated.connect(self.progress_bar.setValue)
                if is_overlay:
                    th.completed.connect(self.load_overlay_completed)
                else:
                    th.first_loaded.connect(self.first_image_loaded)
                    th.completed.connect(self.load_image_completed)
                th.start()

    def first_image_loaded(self, image):
        self.view.set_image(image[0])      # Unwrap the dicom image

    def load_image_completed(self):
        """Slot to process the signal of the image loader in MyDicom"""
        self.tb_edit.setEnabled(True)
        self.act_hybrid.setEnabled(True)
        self.status_bar.removeWidget(self.progress_bar)

    def load_overlay_completed(self, overlay_image):
        """Slot to process the signal of the image loader in MyDicom for an overlay"""
        # overlay_image[0].is_overlay = True
        # overlay_image[0].lower_value = overlay_image[0].get_min_value()
        # overlay_image[0].upper_value = overlay_image.get_max_value()
        self.view.set_overlay_image(overlay_image[0])
        self.status_bar.removeWidget(self.progress_bar)

    def set_operation(self, action):
        """Change the operation in the view (See ViDiGraphics)"""
        if action == self.act_zoom:
            self.view.set_operation(1, self.view.OP_MIDDLE_ZOOM if self.act_zoom.isChecked()
                                    else self.view.OP_MIDDLE_CHANGE_Z)
        elif action == self.act_roi_pol:
            self.view.set_operation(0, self.view.OP_ROI_POL if self.act_roi_pol.isChecked()
                                    else self.view.OP_SELECT)
            self.act_roi_circ.setChecked(False)
            # what if uncheck action when roi not yet finished??
        elif action == self.act_roi_circ:
            self.view.set_operation(0, self.view.OP_ROI_CIRC if self.act_roi_circ.isChecked()
                                    else self.view.OP_SELECT)
            self.act_roi_pol.setChecked(False)

    def show_message(self, txt):
        """Show message in status bar"""
        self.status_bar.showMessage(txt)

    def uncheck_rois(self):
        for a in self.tb_edit.actions():
            if a != self.act_zoom and a != self.act_tools:
                a.setChecked(False)

    @staticmethod
    def exception_handler(type, value, tb):
        logging.exception("Uncaught exception: {0}".format(str(value)))

# Autolauncher
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    c = ViDi()
    c.show()
    app.exec_()
