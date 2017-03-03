#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
v 0.1:  Almost operative
v 0.2:  Half-pixel displacement of overlay...fixed
        Black spots on images
"""
import logging
import numpy as np
from PyQt4.QtCore import *
from PyQt4 import QtGui
from Dialogs import *
from Rois import *
import SVoxels

__author__ = "M.A. Peinado"
__copyright__ = "2016, M.A. Peinado"
__credits__ = ["Miguel A. Peinado"]
__license__ = "GPL"
__version__ = "0.2"
__maintainer__ = "M.A. Peinado"
__email__ = "peinadomiguel@sespa.es"
__status__ = "Prototyping"


class ImageView(QtGui.QGraphicsView):
    """
    Attributes
        - image: DicomImage object
    """
    OP_SELECT = 0
    OP_MIDDLE_CHANGE_Z = 1
    OP_MIDDLE_ZOOM = 2
    OP_WL = 3
    OP_ROI_POL = 4
    OP_ROI_CIRC = 5
    WL_RANGE = 256
    # Custom signals
    selected = pyqtSignal(int)
    change_slice = pyqtSignal(int)
    view_updated = pyqtSignal(QString)
    load_overlay = pyqtSignal(bool)
    roi_finished = pyqtSignal(bool)

    def __init__(self, id_number, parent=None):
        super(ImageView, self).__init__(parent)
        self.setMouseTracking(True)
        self.id_number = id_number
        scene = ImageScene()
        self.image = None
        self.overlay_image = None
        # self.overlay_scaling_factor = []
        self.setScene(scene)
        self.VOIs = []
        self.mid_operation = self.OP_MIDDLE_CHANGE_Z
        self.left_operation = self.OP_SELECT
        self._auto_roi = False
        self.roi = None
        self.x_cursor = None
        self.y_cursor = None
        self.isSelected = False
        self.CURSOR_ZOOM = QtGui.QCursor(QtGui.QPixmap(":/Cursors/pictures/zoom-cursor.svg"))
        self.CURSOR_CHANGE_SLICE = QtGui.QCursor(QtGui.QPixmap(":/Cursors/pictures/change-slice-cursor.svg"))
        self.CURSOR_WL = QtGui.QCursor(QtGui.QPixmap(":/Cursors/pictures/WL-cursor.svg"))
        self.CURSOR_ADD_POINT = QtGui.QCursor(QtGui.QPixmap(":/Cursors/pictures/add-point-cursor.svg"), 18.3, 17.7)
        self.DEFAULT_CURSOR = QtGui.QCursor(QtGui.QPixmap(":/Cursors/pictures/arrow-cursor.svg"), 17.0, 3.0)
        self.setCursor(self.DEFAULT_CURSOR)

#
# <---------------- Paint management ------------------->
#
    def paintEvent(self, event):
        # todo: do that without style sheets
        if self.isSelected:
            self.setStyleSheet("QGraphicsView {border: 2px ridge rgb(0,255,0);\
                               background-color: rgb(0, 0, 0); color: rgb(0,192,0);}")
        else:
            self.setStyleSheet("QGraphicsView {border: 1px solid rgb(0,192,0); \
                               background-color: rgb(0, 0, 0); color: rgb(0,192,0);}")
        super(ImageView, self).paintEvent(event)

#
# <---------------- Events ------------------->
#
# def resizeEvent(self, event):
# Resize would be useful to avoid scroll bars but shows a weird behaviour when loading the image
    def wheelEvent(self, event):
        if self.scene().pixmap is None:
            return
        num_degrees = event.delta() / 8.0
        num_steps = num_degrees / 15.0
        if self.mid_operation == self.OP_MIDDLE_ZOOM:
            # Must set cursor on viewport to properly update cursor
            self.viewport().setCursor(self.CURSOR_ZOOM)
            factor = pow(1.125, num_steps)
            z1 = self.scene().zoom * factor
            if z1 < 0.2:
                z1 = 0.2
                factor = 1.
            elif z1 > 10:
                z1 = 10.
                factor = 1.
            self.scene().zoom = z1
            self.scale(factor, factor)
            txt = "zooming: %0.1fx" % z1
            self.view_updated.emit(txt)
        elif self.mid_operation == self.OP_MIDDLE_CHANGE_Z:
            if not self.image.is_sequence:
                txt = "data set is not a sequence"
                self.view_updated.emit(txt)
                return
            self.viewport().setCursor(self.CURSOR_CHANGE_SLICE)
            if num_steps > 0:
                n_z, pixmap = self.image.next_image()
            else:
                n_z, pixmap = self.image.prev_image()
            self.scene().set_pixmap(self.image.pixmap())
            z = self.image.get_slice_location()
            txt = "slice %i/%i" % ((n_z + 1), self.image.attributes['n_images'])
            txt2 = "Change slice (n, z)=({},{})".format(n_z, z)
            if self.overlay_image is not None:
                #     change z for rois visibility
                p = self.image.to_ref_frame([QPointF(0, 0)])
                txt2 += " -> ref frame: {}".format(str(p))
                p, n_z = self.overlay_image.from_ref_frame(p)
                z = self.overlay_image.slice_locations[n_z]
                txt2 += " -> overlay frame {}, {} (z={})".format(str(p[0]), n_z, z)
                self.update_overlay_image()
                txt += " ({}/{} in overlay)".format((n_z + 1), self.overlay_image.attributes['n_images'])
            # Set roi visibility depending on roi_z
            print (txt2)
            [r.setVisible(n_z == r.roi_z) for r in self.scene().ROIs]
            self.view_updated.emit(txt)

    def mousePressEvent(self, event):
        self.isSelected = True
        self.selected.emit(self.id_number)
        if self.scene().pixmap is None:
            super(ImageView, self).mousePressEvent(event)
            return
        # Limit roi drawing to the image
        limit_x = self.image.attributes['cols']
        limit_y = self.image.attributes['rows']
        mouse_point = self.mapToScene(event.pos())
        if 0 <= mouse_point.x() < limit_x and 0 <= mouse_point.y() < limit_y:
            if event.button() == Qt.LeftButton:
                if self.left_operation == self.OP_ROI_POL:
                    if self.roi is None:
                        txt = "--- roi %i ---" % (len(self.scene().ROIs)+1)
                        if self._auto_roi:
                            pass    # floodfill with point
                        else:
                            self.roi = RoiPol(mouse_point, txt, scene=self.scene())
                            self.roi.setSelected(True)
                    else:
                        self.roi.add_point(mouse_point)
                    event.ignore()
                    return
                elif self.left_operation == self.OP_ROI_CIRC:
                    if self.roi is None:
                        txt = "--- roi %i ---" % (len(self.scene().ROIs) + 1)
                        if self._auto_roi:
                            pass  # floodfill with point
                        else:
                            self.roi = RoiCirc(mouse_point, txt, scene=self.scene())
                            self.roi.setSelected(True)
                    event.ignore()
            elif event.button() == Qt.RightButton:
                self.viewport().setCursor(self.CURSOR_WL)
                self.x_cursor = event.pos().x()
                self.y_cursor = event.pos().y()
                return
        super(ImageView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.scene().pixmap is None:
            super(ImageView, self).mouseMoveEvent(event)
            return
        # the returned value for event.button() is always Qt.NoButton for mouse move events -> must use buttons
        if event.buttons() == Qt.RightButton:
            dx = event.pos().x() - self.x_cursor
            dy = event.pos().y() - self.y_cursor
            new_center = self.image.attributes['center'] + dx / float(self.width()) * self.WL_RANGE
            c_inf, c_sup = self.image.pixel_thresholds()
            if new_center < c_inf:
                new_center = c_inf
            if new_center > c_sup:
                new_center = c_sup
            new_window = self.image.attributes['window'] + dy / float(self.height()) * self.WL_RANGE
            # todo: Overlays the histogram and WL line
            if new_window < 1:
                new_window = 1
            # Ensure the window don't exceeds limits (why?)
            # w_sup = min(abs(new_center - c_inf), abs(new_center - c_sup))/2
            # if new_window > w_sup:
            #     new_window = w_sup
            self.image.attributes['center'] = new_center
            self.image.attributes['window'] = new_window
            #
            #
            self.scene().set_pixmap(self.image.pixmap())
            self.x_cursor = event.pos().x()
            self.y_cursor = event.pos().y()
            txt = "window: %i, center: %i" % (new_window, new_center)
            self.view_updated.emit(txt)
            return
        if self.left_operation == self.OP_SELECT:
            self.viewport().setCursor(self.DEFAULT_CURSOR)
            p = self.mapToScene(event.pos())
            val = self.image.value_at(p.x(), p.y())
            val = str(val)
            self.view_updated.emit("(%i,%i) %s" % (p.x(), p.y(), val))
            # if something is selected must propagate events
            if len(self.scene().selectedItems()) > 0:
                super(ImageView, self).mouseMoveEvent(event)
            # self.viewport().setCursor(self.DEFAULT_CURSOR)
        elif self.left_operation == self.OP_ROI_POL or self.left_operation == self.OP_ROI_CIRC:
            # Limit roi drawing to the image
            limit_x = self.image.attributes['cols']
            limit_y = self.image.attributes['rows']
            mouse_point = self.mapToScene(event.pos())
            if 0 <= mouse_point.x() < limit_x and 0 <= mouse_point.y() < limit_y:
                self.viewport().setCursor(self.CURSOR_ADD_POINT)
                if self.left_operation == self.OP_ROI_CIRC and self.roi is not None:
                    self.roi.resize(mouse_point)
            else:
                self.viewport().setCursor(self.DEFAULT_CURSOR)
            val = self.image.value_at(mouse_point.x(), mouse_point.y())
            val = str(val)
            self.view_updated.emit("(%i,%i) %s" % (mouse_point.x(), mouse_point.y(), val))

    def mouseDoubleClickEvent(self, event):
        if self.scene().pixmap is None:
            super(ImageView, self).mouseDoubleClickEvent(event)
            return
        if event.button() == Qt.LeftButton:
            if self.left_operation != self.OP_SELECT and self.roi is not None:
                # todo: Reassign z values when rois already exist and an overlay is added
                if self.overlay_image is not None:
                    p = self.image.to_ref_frame([QPointF(0, 0)])
                    _, n_z = self.overlay_image.from_ref_frame(p)
                    print "---> overlay z for roi", n_z
                else:
                    n_z = self.image.current_index
                self.roi.set_z(n_z)
                self.roi.default_label_pos()
                # Is list of rois worth?. Yes, for roi copy/paste operation
                self.scene().ROIs.append(self.roi)
                self.roi_finished.emit(True)
                print self.roi
                self.roi = None
                self.left_operation = self.OP_SELECT
                self.viewport().setCursor(self.DEFAULT_CURSOR)
            elif self.left_operation == self.OP_SELECT:
                super(ImageView, self).mouseDoubleClickEvent(event)
        elif event.button() == Qt.RightButton:
            dlg = WLDialog(self.image, self.overlay_image, self.parent())
            dlg.update_images.connect(self.update_dicom_image)
            if self.overlay_image is not None:
                dlg.update_images.connect(self.update_overlay_image)
            if dlg.exec_() == dlg.Rejected:
                self.image.attributes['window'] = dlg.window0
                self.image.attributes['center'] = dlg.center0
                self.update_dicom_image()
                if self.overlay_image is not None:
                    self.overlay_image.alpha = dlg.alpha0
                    self.overlay_image.lower_value = dlg.low0
                    self.overlay_image.upper_value = dlg.high0
                    self.update_overlay_image()
            return

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.x_cursor = None
            self.y_cursor = None
            self.viewport().setCursor(self.DEFAULT_CURSOR)
        else:
            super(ImageView, self).mouseReleaseEvent(event)

#
# <-------------- End of event processing ----------------->
#
# <----------------------- Slots -------------------------->
#

    def set_operation(self, button, operation):
        if button == 0:
            self.left_operation = operation
            self.scene().clearSelection()
        elif button == 1:
            self.mid_operation = operation

#
# <----------------------- Methods -------------------------->
#

    def set_auto_roi(self, auto_roi):
        QtGui.QMessageBox.warning(None, "Floodfill auto roi", "It Does Nothing yet!!!")
        self._auto_roi = auto_roi
        print self._auto_roi

    def set_image(self, image):
        #
        self.image = image
        # self.image.pixmap_update.connect(self.update_dicom_image)
        pxm = self.image.pixmap()
        self.scene().set_pixmap(pxm)

    def set_overlay_image(self, image):
        # Verify if overlay and image have the same Frame UID and the same orientation (Data sets must be coplanar)
        try:
            if image.attributes['frame_uid'] != self.image.attributes['frame_uid']:
                self.scene().switch_overlay_item.view_overlay = False
                raise ValueError("Can't correlate, the frames of reference of the image and overlay are not the same")
            if not np.array_equal(self.image.attributes['cosines'], image.attributes['cosines']):
                self.scene().switch_overlay_item.view_overlay = False
                raise ValueError("Can't correlate, the dataset have not the same orientation")
        except AttributeError:

            txt = "No reference coordinate system or image orientation tag are present.\n"
            txt +=  "Base/overlay matching are not safe and will be done at your own risk.\n"
            print txt
            pass
        self.overlay_image = image
        # self.overlay_image.pixmap_update.connect(self.update_overlay_image)
        p = self.image.to_ref_frame([QPointF(0, 0)])
        _, nz2 = self.overlay_image.from_ref_frame(p)
        overlay_origin = self.overlay_image.attributes['origin']
        p2, _ = self.image.from_ref_frame([overlay_origin])
        p2 = p2[0]
        sc_o = self.overlay_image.attributes['pixel_spacing']
        sc_i = self.image.attributes['pixel_spacing']
        zx = sc_o[0] / sc_i[0]
        zy = sc_o[1] / sc_i[1]
        # Fix half of pixel displacement on overlay
        # p2 += QPointF((1.-zx)/2., (1.-zy)/2.)
        p2 += QPointF(- zx / 2., - zy / 2.)
        # self.overlay_scaling_factor = [zx, zy]
        # print "overlay_scaling_factor", self.overlay_scaling_factor
        pixmap = self.overlay_image.pixmap_for_index(nz2)
        self.scene().set_overlay(pixmap, p2, zx, zy)
        # todo here if there are rois -> erase all
        pass

    def update_dicom_image(self):
        self.scene().set_pixmap(self.image.pixmap())

    def update_overlay_image(self):
        # 1. Pass origin of the actual slice to reference and after to overlay coordinate system
        p = self.image.to_ref_frame([QPointF(0, 0)])
        _, nz2 = self.overlay_image.from_ref_frame(p)
        self.scene().set_overlay(self.overlay_image.pixmap_for_index(nz2))
        return nz2

    def get_vois(self, get_stats=True):
        """Define all the VOIs actually in image(s) from the rois already defined and all its statistics"""
        self.VOIs = []
        for r in self.scene().ROIs:
            tx = r.get_text()
            v_o_i = next((v for v in self.VOIs if v.label == tx), None)
            if v_o_i is not None:
                v_o_i.append(r)
            else:
                self.VOIs.append(Voi(tx, r))
            if get_stats:
                pol, roi_type, px = self.roi_info_4_stats(r)
                stats = statistics.calculate(pol, roi_type, px)
                r.set_stats(stats)

    def roi_info_4_stats(self, r):
            logging.info("retrieving stats for {0}".format(r.get_text()))
            if self.overlay_image is not None:
                px = self.overlay_image.pixel_values_for_index(r.roi_z)
                if isinstance(r, RoiPol):
                    p = self.image.to_ref_frame(r.polygon(), 0)
                    pf, _ = self.overlay_image.from_ref_frame(p)
                    roi_type = "polygon"
                    pol = QtGui.QPolygonF(pf)
                else:
                    rect = r.boundingRect()
                    p1 = rect.topLeft()
                    p2 = rect.bottomRight()
                    p = self.image.to_ref_frame([p1, p2], 0)
                    pf, _ = self.overlay_image.from_ref_frame(p)
                    roi_type = "ellipse"
                    pol = QRectF(pf[0], pf[1])
            else:
                px = self.image.pixel_values_for_index(r.roi_z)
                if isinstance(r, RoiPol):
                    pol = r.mapToScene(r.polygon())
                    roi_type = "polygon"
                else:
                    pol = r.mapRectToScene(r.boundingRect())
                    roi_type = "ellipse"
            return pol, roi_type, px

    def show_stats(self):
        if len(self.scene().ROIs) == 0:
            return
        self.get_vois()
        dlg = RoiStats(self.VOIs)
        dlg.exec_()

    def dosimetry(self):
        if len(self.scene().ROIs) == 0:
            return
        self.get_vois()
        dlg = SVoxels.VoisRole(self.VOIs)
        if dlg.exec_() == dlg.Accepted:
            # Get pixel values
            px_values = self.overlay_image.pixel_values() if self.overlay_image is not None \
                                                          else self.image.pixel_values()
            f_quant = 5.80786e-5  # [MBq/count]
            # Parse file with s-factors  [mGy/(MBq·s)]
            s_values = SVoxels.s_value_parser("177Lu", 4.42)
            # Compute all sources indices (mixed, no need of getting each source indices separately)
            source_indices = []
            for v in self.VOIs:
                if v.get_role() & Voi.SOURCE_ROLE:
                    for r_source in v.roi_list:
                        pol, roi_type, _ = self.roi_info_4_stats(r_source)
                        source_indices += SVoxels.roi2indices(pol, roi_type, r_source.roi_z)
            # Compute all target indices (separately for each voi. Must store total doses and DVH)
            for v in self.VOIs:
                target_indices = []
                if v.get_role() > Voi.SOURCE_ROLE:
                    for r_target in v.roi_list:
                        pol, roi_type, _ = self.roi_info_4_stats(r_target)
                        target_indices += SVoxels.roi2indices(pol, roi_type, r_target.roi_z)
                doses = {}      # Needed? We only need total organ doses. Can make DVH on the fly?
                for tix in target_indices:
                    for six in source_indices:
                        # Get 3D distances (z index is stored in first position!!)
                        dist_3d = (abs(tix[1] - six[1]), abs(tix[2] - six[2]), abs(tix[0] - six[0]))
                        # Multiply s-factor with counts on pixel and quantification factor
                        # Be careful...pixel values are indexed with z index in first position!!!
                        try:
                            d = s_values[dist_3d] * px_values[six] * f_quant
                        except IndexError:
                            d = s_values[(5, 5, 5)] * px_values[six] * f_quant
                        # Add to doses
                        try:
                            doses[tix] += d
                        except KeyError:
                            # index key does not exists => must create first
                            doses[tix] = d
                    # Must store doses: Can discard keys (target voxel position) when all sources have been computed
                    # Prefer to keep them if isodoses curves are drawed later
                v.set_doses(doses)
                # Total dose
                d = SVoxels.DoseReport(self.VOIs)
                d.show()

    def show_info(self, show):
        self.scene()._draw_general_info = show

    def clone_rois(self):
        rois = []
        txt = "Clone roi(s):"
        for r in self.scene().ROIs:
            if r.is_selected():
                rois.append(r)
                txt += "\n  -> {0}".format(r.get_text())
        if len(rois) == 0:
            QtGui.QMessageBox.critical(None, "Clone Rois", "Please select one or several rois to clone.")
            return
        upper_limit = len(self.overlay_image.slice_locations if self.overlay_image is not None
                          else self.image.slice_locations)
        # todo: Limit the rois to the extent of image when overlay exceeds the limits of the image
        dlg = CloneRois(txt, (1, upper_limit))
        if dlg.exec_() == dlg.Accepted:
            slice_range = dlg.get_range()
            print slice_range
            # Be aware to don't copy rois in their own slice
            scene_rois = self.scene().ROIs
            for r in rois:
                z0 = r.roi_z
                txt = r.get_text()
                print z0, txt
                for i in range(slice_range[0], slice_range[1]):
                    # Be aware to don't copy rois in their own slice
                    if z0 != i:
                        # QWidget does not support copy method so must take a workaround
                        # (kinda complex stuff with bindings to C++ original objects)
                        # r2 = copy.copy(r)
                        if isinstance(r, RoiPol):
                            # Create a new object
                            p = r.polygon()
                            r2 = RoiPol(p[0], text=txt, scene=self.scene())
                            # ...copy its shape
                            r2.setPolygon(p)
                            r2.set_outer_polygon()
                        else:
                            # Create a new object
                            r2 = RoiCirc(r.mass_center, text=txt, scene=self.scene())
                            # ...copy its size
                            r2.setRect(r.rect())
                        r2.default_label_pos()
                        r2.set_z(i)
                        print r2.is_selected()
                        r2.setVisible(False)
                        scene_rois.append(r2)
                        logging.info("clone roi {} from position {} to position {}".format(r.get_text(), z0, i))


class ImageScene(QtGui.QGraphicsScene):
    def __init__(self, pixmap=None, overlay=None):
        self.pixmap = pixmap
        self.overlay = overlay
        w = pixmap.width() if pixmap is not None else 0
        h = pixmap.height() if pixmap is not None else 0
        super(ImageScene, self).__init__(0, 0, w, h)
        self.ROIs = []
        self.stats = []
        self.zoom = 1.
        self._draw_general_info = False
        self.switch_overlay_item = SwitchOverlay(scene=self)
        self.switch_overlay_item.setVisible(False)
        self.overlay_item = QtGui.QGraphicsPixmapItem(scene=self)

    def drawBackground(self, painter, rect):
        if self.pixmap is not None:
            painter.drawPixmap(-.5, -.5, self.pixmap)
        super(ImageScene, self).drawBackground(painter, rect)

    def drawForeground(self, painter, rect):
        if self.pixmap is not None:
            view = self.views()[0]
            if self._draw_general_info:
                # Adjust size to avoid zoom effect
                intended_size = 12.
                interline_space = intended_size * 1.5
                font = painter.font()
                point_size = intended_size/self.zoom
                font.setPointSizeF(point_size)
                painter.setFont(font)
                x = 5
                y = interline_space
                point = view.mapToScene(QPoint(x, y))
                painter.drawText(point, "Zoom: %0.1f" % self.zoom)
                y += interline_space
                point = view.mapToScene(QPoint(x, y))
                info = view.image.get_info()
                txt = "slice z = {0:.1f}".format(info['z'])
                if info['total'] > 1:
                    txt += " ({0}/{1})".format(info['index'] + 1, info['total'])
                txt_wl = "w ={0:.0f} / c={1:.0f}".format(info['window'] + 1, info['center'])
                painter.drawText(point, txt)
                if view.overlay_image is not None:
                    y += interline_space
                    point = view.mapToScene(QPoint(x, y))
                    info = view.overlay_image.get_info()
                    txt = "overlay z = {0:.1f}".format(info['z'])
                    if info['total'] > 1:
                        txt += " ({0}/{1})".format(info['index'] + 1, info['total'])
                    painter.drawText(point, txt)

                y += interline_space
                point = view.mapToScene(QPoint(x, y))
                painter.drawText(point, txt_wl)
            self.switch_overlay_item.setVisible(True)
            # Draw the folded right upper corner
            w = view.width() - 1
            s = float(self.switch_overlay_item.side)
            v = view.verticalScrollBar().width() if view.verticalScrollBar().isVisible() else 0
            p = view.mapToScene(QPoint(w-s-v, 0))
            self.switch_overlay_item.setPos(p)
        super(ImageScene, self).drawForeground(painter, rect)

    def erase_pixmap(self):
        self.pixmap = None

    def make_overlay_visible(self, is_visible):
        if is_visible:
            if self.overlay is None:
                view = self.views()[0]
                view.load_overlay.emit(True)
            else:
                self.overlay_item.setVisible(True)
        elif self.overlay is not None:
            self.overlay_item.setVisible(False)

    def set_pixmap(self, pixmap):
        if self.pixmap is None:
            w = float(pixmap.width())
            h = float(pixmap.height())
            self.setSceneRect(0, 0, w, h)
            view = self.views()[0]
            view_w = view.width()
            view_h = view.height()
            factor_w = view_w/w
            factor_h = view_h/h
            factor = factor_w if factor_w < factor_h else factor_h
            view.resetMatrix()
            self.zoom = factor
            view.scale(self.zoom, self.zoom)
        self.pixmap = pixmap
        self.update()

    def set_overlay(self, overlay_pixmap, p=None, zx=None, zy=None):
        self.overlay = overlay_pixmap
        self.overlay_item.setPixmap(self.overlay)
        # Must translate and scale overlay
        if p is not None:
            self.overlay_item.setPos(p.x(), p.y())
        if zx is not None and zy is not None:
            self.overlay_item.scale(zx, zy)
        self.overlay_item.setZValue(-1000)


class SwitchOverlay(QtGui.QGraphicsItem):

    def __init__(self, parent=None, scene=None):
        super(SwitchOverlay, self).__init__(parent, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setToolTip("Click to show/hide overlay image")
        self.view_overlay = False
        self.side = 12.

    def mousePressEvent(self, event):
        super(SwitchOverlay, self).mousePressEvent(event)
        self.view_overlay = not self.view_overlay
        # Quick 'n' dirty solution to avoid signaling
        self.scene().make_overlay_visible(self.view_overlay)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(Qt.white)
        zoom = self.scene().zoom
        pen.setWidth(1./zoom)
        side = self.side/zoom
        list_of_points = [QPointF(0, 0), QPointF(side, side), QPointF(0, side), QPointF(0, 0)]
        pol = QtGui.QPolygonF(list_of_points)
        # if option.state & QtGui.QStyle.State_Selected:
        if self.view_overlay:
            color = painter.pen().color()
            brush = QtGui.QBrush(color)
            painter.setBrush(brush)
            painter.drawPolygon(pol)
        else:
            painter.setBrush(Qt.NoBrush)
            painter.drawPolygon(pol)

    def boundingRect(self):
        return QRectF(0, 0, self.side, self.side)