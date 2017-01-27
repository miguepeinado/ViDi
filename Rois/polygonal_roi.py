from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QPointF
from label import LabelItem
import MyTools.geometry as geometry


class RoiPol(QGraphicsPolygonItem):
    # todo: Copy/paste rois
    def __init__(self, origin, text=None, parent=None, scene=None):
        super(RoiPol, self).__init__(parent, scene)
        # some gui tweaks
        self.myOutlineColor = Qt.yellow
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        p = QPolygonF()
        p.append(origin)
        self.setPolygon(p)
        self.outer_polygon = QPolygonF()
        self._label = LabelItem(text, self, scene)
        self._label.setDefaultTextColor(self.myOutlineColor)
        self._label.setVisible(False)
        self.mass_center = None
        self.edit_points = None
        self.point_edited = None
        self.moving = None
        self.roi_z = None
        self.stats = {}
        self._is_selected = False
        # Static values must be placed here beacuse they are complex objects
        self.DEL_POINT_CURSOR = QCursor(QPixmap(":/Cursors/pictures/del-point-cursor.svg"))
        self.ADD_POINT_CURSOR = QCursor(QPixmap(":/Cursors/pictures/add-point-cursor.svg"), 18.3, 17.7)
        self.DEFAULT_CURSOR = QCursor(QPixmap(":/Cursors/pictures/arrow-cursor.svg"), 17.0, 3.0)
        self.setCursor(self.DEFAULT_CURSOR)
#
# <------------------- Reimplemented methods -------------->
#

    def boundingRect(self):
        return self.polygon().boundingRect()

    def shape(self):
        path = QPainterPath()
        path.addPolygon(self.outer_polygon)
        path.closeSubpath()
        return path

    def paint(self, painter, option, widget):
        pen = QPen(self.myOutlineColor)
        zoom = self.scene().zoom
        side = 5./zoom
        pen.setWidthF(2./zoom)
        painter.setPen(pen)
        if option.state & QStyle.State_Selected:
            if self.is_editing():
                for p in self.polygon():
                    painter.drawEllipse(p, 3./zoom, 3./zoom)
                painter.setBrush(QBrush(self.myOutlineColor))
                list_of_points = [QPointF(self.mass_center.x()-side, self.mass_center.y()),
                                  QPointF(self.mass_center.x(), self.mass_center.y()-side),
                                  QPointF(self.mass_center.x()+side, self.mass_center.y()),
                                  QPointF(self.mass_center.x(), self.mass_center.y()+side)]
                pol = QPolygonF(list_of_points)
                painter.drawPolygon(pol)
                painter.setBrush(QBrush())
            pen.setStyle(Qt.DotLine)
            self._is_selected = True
        else:
            self._is_selected = False

        painter.setPen(pen)
        painter.drawPolygon(self.polygon())
        f = self._label.font()
        f.setPointSize(round(10./zoom))
        self._label.setFont(f)

    #
    # <---------------------- Events -------------------->
    #
    def mousePressEvent(self, event):
        self.point_edited = self.point_at_cursor(event.pos())
        shift_is_pressed = (event.modifiers() == Qt.ShiftModifier)
        # Determine if cursor is near to the center
        self.moving = (geometry.distance2_qt(self.mass_center, event.pos()) <= 16)
        # Determine if cursor is near to a point
        if self.point_edited is None:
            if self.moving and shift_is_pressed:
                # Erase the whole roi
                self.scene().ROIs.remove(self)
                self.scene().removeItem(self)
            # Determine if cursor is near to a segment
            add_point_in_segment_n = self.near_segment(event.pos())
            if add_point_in_segment_n is not None:
                pol = self.polygon()
                pol.insert(add_point_in_segment_n, event.pos())
                self.setPolygon(pol)
                self.set_outer_polygon()
                self.update()
                self.point_edited = add_point_in_segment_n
                self.setCursor(QCursor(Qt.SizeAllCursor))
        else:
            if shift_is_pressed:
                pol = self.polygon()
                pol.remove(self.point_edited)
                self.setPolygon(pol)
                self.set_outer_polygon()
                self.update()
                self.setCursor(self.DEFAULT_CURSOR)
        super(RoiPol, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Used when moving the roi or a single point"""
        if self.point_edited is not None:
            shift_is_pressed = (event.modifiers() == Qt.ShiftModifier)
            if not shift_is_pressed:
                # todo: avoid point movement outside image
                self.replace(self.point_edited, event.pos())
        elif self.moving:
            # todo: avoid roi movement outside image
            super(RoiPol, self).mouseMoveEvent(event)

    def hoverMoveEvent(self, event):
        if self.is_editing() and self.isSelected():
            shift_is_pressed = (event.modifiers() == Qt.ShiftModifier)
            near_center = (geometry.distance2_qt(self.mass_center, event.pos()) <= 16)
            near_vertex = (self.point_at_cursor(event.pos()) is not None)
            near_border = self.near_segment(event.pos())
            if near_center:
                if shift_is_pressed:
                    self.setCursor(QCursor(self.DEL_POINT_CURSOR))
                else:
                    self.setCursor(QCursor(Qt.SizeAllCursor))
            elif near_vertex:
                if shift_is_pressed:
                    self.setCursor(QCursor(self.DEL_POINT_CURSOR))
                else:
                    self.setCursor(QCursor(Qt.SizeAllCursor))
            elif near_border is not None:
                self.setCursor(QCursor(self.ADD_POINT_CURSOR))
            else:
                self.setCursor(self.DEFAULT_CURSOR)


#
# <---------------------- Functions -------------------->
#

#
# <--------------------- override ---------------------->
#
    def __str__(self):
        r = self.boundingRect()
        p = r.bottomRight() - self.mass_center
        return "polygonal roi {} with points {}".format(self.get_text(), [p for p in self.polygon()])

    def add_point(self, point):
        pol = self.polygon()
        pol.append(point)
        self.setPolygon(pol)
        self.set_outer_polygon()
        self.update()

    def default_label_pos(self):
        r = self.boundingRect()
        r.translate(5, -10)
        p = r.topRight()
        self._label.setVisible(True)
        self._label.setPos(p)

    def edit_points(self, edit):
        self.edit_points = edit
        self.update()

    def get_text(self):
        return str(self._label.toPlainText())

    def is_editing(self):
        view = self.scene().views()[0]
        return view.left_operation == view.OP_SELECT

    def is_selected(self):
        return self._is_selected

    def near_segment(self, point):
        pol = self.polygon()
        n_points = pol.count()-1
        for i in range(-1, n_points):
            in_segment, distance2 = geometry.dist_to_segment(point, pol[i], pol[i + 1])
            if in_segment and distance2 <= 9:
                return i+1
        return None

    def point_at_cursor(self, point):
        for p in self.polygon():
            if geometry.distance2_qt(point, p) <= 16:
                return self.polygon().indexOf(p)
        return None

    def replace(self, index, point):
        pol = self.polygon()
        pol.replace(index, point)
        self.setPolygon(pol)
        self.set_outer_polygon()
        self.update()

    def set_outer_polygon(self):
        """
            Define the outer polygon used for shape and for dragging points.
            Store the result in self.outer_polygon
        """
        pol = self.polygon()
        self.mass_center = geometry.centroid_qt(pol)
        t = QTransform().translate(-self.mass_center.x(), -self.mass_center.y())
        pol = t.map(pol)
        t = QTransform().scale(1.1, 1.1)
        pol = t.map(pol)
        t = QTransform().translate(self.mass_center.x(), self.mass_center.y())
        self.outer_polygon = t.map(pol)

    def set_text(self, text):
        self._label.setPlainText(text)

    def set_z(self, z):
        self.roi_z = z

    def set_stats(self, stats):
        self.stats = stats