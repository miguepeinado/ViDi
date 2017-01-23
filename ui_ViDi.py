# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ViDi.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(943, 675)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Otros/resources/ViDi.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(25.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(414, 489))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gv_images = QtGui.QGraphicsView(self.centralwidget)
        self.gv_images.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gv_images.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gv_images.setObjectName(_fromUtf8("gv_images"))
        self.horizontalLayout.addWidget(self.gv_images)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.tb_files = QtGui.QToolBar(MainWindow)
        self.tb_files.setMovable(False)
        self.tb_files.setIconSize(QtCore.QSize(36, 36))
        self.tb_files.setObjectName(_fromUtf8("tb_files"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tb_files)
        self.tb_edit = QtGui.QToolBar(MainWindow)
        self.tb_edit.setEnabled(False)
        self.tb_edit.setMovable(True)
        self.tb_edit.setIconSize(QtCore.QSize(36, 36))
        self.tb_edit.setObjectName(_fromUtf8("tb_edit"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tb_edit)
        self.tb_rois = QtGui.QToolBar(MainWindow)
        self.tb_rois.setEnabled(True)
        self.tb_rois.setIconSize(QtCore.QSize(36, 36))
        self.tb_rois.setObjectName(_fromUtf8("tb_rois"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tb_rois)
        self.tb_tools = QtGui.QToolBar(MainWindow)
        self.tb_tools.setIconSize(QtCore.QSize(36, 36))
        self.tb_tools.setObjectName(_fromUtf8("tb_tools"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tb_tools)
        self.actExit = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/exit.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actExit.setIcon(icon1)
        self.actExit.setObjectName(_fromUtf8("actExit"))
        self.act_zoom = QtGui.QAction(MainWindow)
        self.act_zoom.setCheckable(True)
        self.act_zoom.setEnabled(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/zoom.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_zoom.setIcon(icon2)
        self.act_zoom.setObjectName(_fromUtf8("act_zoom"))
        self.actWL = QtGui.QAction(MainWindow)
        self.actWL.setCheckable(True)
        self.actWL.setEnabled(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/WL.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actWL.setIcon(icon3)
        self.actWL.setObjectName(_fromUtf8("actWL"))
        self.act_change_slice = QtGui.QAction(MainWindow)
        self.act_change_slice.setCheckable(True)
        self.act_change_slice.setChecked(False)
        self.act_change_slice.setEnabled(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/change-slice.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_change_slice.setIcon(icon4)
        self.act_change_slice.setObjectName(_fromUtf8("act_change_slice"))
        self.act_settings = QtGui.QAction(MainWindow)
        self.act_settings.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/settings.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_settings.setIcon(icon5)
        self.act_settings.setObjectName(_fromUtf8("act_settings"))
        self.act_hybrid = QtGui.QAction(MainWindow)
        self.act_hybrid.setCheckable(True)
        self.act_hybrid.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/hbrid.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_hybrid.setIcon(icon6)
        self.act_hybrid.setObjectName(_fromUtf8("act_hybrid"))
        self.act_roi_pol = QtGui.QAction(MainWindow)
        self.act_roi_pol.setCheckable(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/new-pol-roi.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_roi_pol.setIcon(icon7)
        self.act_roi_pol.setObjectName(_fromUtf8("act_roi_pol"))
        self.act_roi_circ = QtGui.QAction(MainWindow)
        self.act_roi_circ.setCheckable(True)
        self.act_roi_circ.setEnabled(True)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/new-circ-roi.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_roi_circ.setIcon(icon8)
        self.act_roi_circ.setObjectName(_fromUtf8("act_roi_circ"))
        self.act_roi_auto = QtGui.QAction(MainWindow)
        self.act_roi_auto.setCheckable(True)
        self.act_roi_auto.setEnabled(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/auto-roi.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_roi_auto.setIcon(icon9)
        self.act_roi_auto.setObjectName(_fromUtf8("act_roi_auto"))
        self.act_get_stats = QtGui.QAction(MainWindow)
        self.act_get_stats.setEnabled(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/roi-stats.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_get_stats.setIcon(icon10)
        self.act_get_stats.setObjectName(_fromUtf8("act_get_stats"))
        self.act_select = QtGui.QAction(MainWindow)
        self.act_select.setCheckable(True)
        self.act_select.setChecked(True)
        self.act_select.setEnabled(True)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/select.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_select.setIcon(icon11)
        self.act_select.setObjectName(_fromUtf8("act_select"))
        self.act_rotate_cw = QtGui.QAction(MainWindow)
        self.act_rotate_cw.setObjectName(_fromUtf8("act_rotate_cw"))
        self.act_rotate_ccw = QtGui.QAction(MainWindow)
        self.act_rotate_ccw.setObjectName(_fromUtf8("act_rotate_ccw"))
        self.act_normi13 = QtGui.QAction(MainWindow)
        self.act_normi13.setEnabled(False)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/normi-13.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_normi13.setIcon(icon12)
        self.act_normi13.setObjectName(_fromUtf8("act_normi13"))
        self.act_tools = QtGui.QAction(MainWindow)
        self.act_tools.setCheckable(True)
        self.act_tools.setEnabled(True)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/tools.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_tools.setIcon(icon13)
        self.act_tools.setObjectName(_fromUtf8("act_tools"))
        self.act_open_file = QtGui.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/open-file.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_open_file.setIcon(icon14)
        self.act_open_file.setObjectName(_fromUtf8("act_open_file"))
        self.act_open_3D = QtGui.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/Open-3D.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_open_3D.setIcon(icon15)
        self.act_open_3D.setObjectName(_fromUtf8("act_open_3D"))
        self.act_dosimetry = QtGui.QAction(MainWindow)
        self.act_dosimetry.setObjectName(_fromUtf8("act_dosimetry"))
        self.act_internal_dosimetry = QtGui.QAction(MainWindow)
        self.act_internal_dosimetry.setObjectName(_fromUtf8("act_internal_dosimetry"))
        self.act_show_info = QtGui.QAction(MainWindow)
        self.act_show_info.setCheckable(True)
        self.act_show_info.setChecked(False)
        self.act_show_info.setObjectName(_fromUtf8("act_show_info"))
        self.act_clone_rois = QtGui.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(_fromUtf8(":/Actions/pictures/clone-rois.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_clone_rois.setIcon(icon16)
        self.act_clone_rois.setObjectName(_fromUtf8("act_clone_rois"))
        self.tb_files.addAction(self.act_open_file)
        self.tb_files.addSeparator()
        self.tb_files.addAction(self.act_settings)
        self.tb_files.addAction(self.act_show_info)
        self.tb_files.addSeparator()
        self.tb_files.addAction(self.actExit)
        self.tb_edit.addAction(self.act_select)
        self.tb_edit.addAction(self.act_change_slice)
        self.tb_edit.addAction(self.act_zoom)
        self.tb_edit.addAction(self.actWL)
        self.tb_edit.addSeparator()
        self.tb_edit.addAction(self.act_tools)
        self.tb_rois.addAction(self.act_roi_auto)
        self.tb_rois.addAction(self.act_roi_pol)
        self.tb_rois.addAction(self.act_roi_circ)
        self.tb_rois.addAction(self.act_clone_rois)
        self.tb_rois.addAction(self.act_get_stats)
        self.tb_tools.addAction(self.act_internal_dosimetry)
        self.tb_tools.addAction(self.act_normi13)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.act_tools, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.tb_tools.setVisible)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ViDi - Visor Dicom", None))
        self.tb_files.setWindowTitle(_translate("MainWindow", "Toolbar: General", None))
        self.tb_edit.setWindowTitle(_translate("MainWindow", "Toolbar: VIew", None))
        self.tb_rois.setWindowTitle(_translate("MainWindow", "Toolbar: ROIs", None))
        self.tb_tools.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actExit.setText(_translate("MainWindow", "Exit", None))
        self.actExit.setToolTip(_translate("MainWindow", "Exit program", None))
        self.act_zoom.setText(_translate("MainWindow", "Zoom", None))
        self.act_zoom.setToolTip(_translate("MainWindow", "Zoom image", None))
        self.actWL.setText(_translate("MainWindow", "Window/Level", None))
        self.actWL.setToolTip(_translate("MainWindow", "Change Window/Level", None))
        self.act_change_slice.setText(_translate("MainWindow", "Change image", None))
        self.act_change_slice.setToolTip(_translate("MainWindow", "Navigate between images", None))
        self.act_settings.setText(_translate("MainWindow", "Settings", None))
        self.act_settings.setToolTip(_translate("MainWindow", "Program settings", None))
        self.act_hybrid.setText(_translate("MainWindow", "Hybrid imagesx", None))
        self.act_hybrid.setToolTip(_translate("MainWindow", "Overlays images for a hybrid modality", None))
        self.act_roi_pol.setText(_translate("MainWindow", "Draw roi", None))
        self.act_roi_pol.setToolTip(_translate("MainWindow", "Draw polygonal roi", None))
        self.act_roi_circ.setText(_translate("MainWindow", "Draw circular roi", None))
        self.act_roi_circ.setToolTip(_translate("MainWindow", "Draw circular roi", None))
        self.act_roi_auto.setText(_translate("MainWindow", "Automatic roi", None))
        self.act_roi_auto.setToolTip(_translate("MainWindow", "Automatically defines a roi", None))
        self.act_get_stats.setText(_translate("MainWindow", "Roi stats", None))
        self.act_get_stats.setToolTip(_translate("MainWindow", "Get roi statistics", None))
        self.act_select.setText(_translate("MainWindow", "Select", None))
        self.act_select.setToolTip(_translate("MainWindow", "selection tool", None))
        self.act_rotate_cw.setText(_translate("MainWindow", "Rotate CW", None))
        self.act_rotate_cw.setToolTip(_translate("MainWindow", "Rotate image(s) 90º clockwise", None))
        self.act_rotate_ccw.setText(_translate("MainWindow", "Rotate CCW", None))
        self.act_rotate_ccw.setToolTip(_translate("MainWindow", "Rotate image(s) 90º counter clockwise", None))
        self.act_normi13.setText(_translate("MainWindow", "Normi 13", None))
        self.act_normi13.setToolTip(_translate("MainWindow", "Automatic analysis of normi 13 phantom", None))
        self.act_tools.setText(_translate("MainWindow", "Tools", None))
        self.act_open_file.setText(_translate("MainWindow", "open image(s)", None))
        self.act_open_file.setToolTip(_translate("MainWindow", "Open a single or serie of image(s)", None))
        self.act_open_3D.setText(_translate("MainWindow", "open 3D image", None))
        self.act_open_3D.setToolTip(_translate("MainWindow", "open 3D image (in one or several files)", None))
        self.act_dosimetry.setText(_translate("MainWindow", "internal dosimetry", None))
        self.act_dosimetry.setToolTip(_translate("MainWindow", "Opens internal dosimetry tool", None))
        self.act_internal_dosimetry.setText(_translate("MainWindow", "Internal dosimetry", None))
        self.act_show_info.setText(_translate("MainWindow", "show info", None))
        self.act_clone_rois.setText(_translate("MainWindow", "clone roi(s)", None))
        self.act_clone_rois.setToolTip(_translate("MainWindow", "Clone selected roi(s) to other slices", None))

import icons_rc
