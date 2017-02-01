from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QPointF, QRectF
from label import LabelItem
import geometry


class RoiCirc(QGraphicsEllipseItem):
    # todo: Copy/paste rois
    def __init__(self, center, text=None, parent=None, scene=None):
        super(RoiCirc, self).__init__(parent, scene)
        # some gui tweaks
        self.myOutlineColor = Qt.yellow
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.mass_center = center
        self._label = LabelItem(text, self, scene)
        self._label.setDefaultTextColor(self.myOutlineColor)
        self._label.setVisible(False)
        self.edit_points = None
        self.point_edited = None
        self.moving = False
        self.roi_z = None
        self.stats = {}
        self._is_selected = False
        # Static values must be placed here beacuse they are complex objects
        self.DEL_POINT_CURSOR = QCursor(QPixmap(":/Cursors/pictures/del-point-cursor.svg"))
        self.DEFAULT_CURSOR = QCursor(QPixmap(":/Cursors/pictures/arrow-cursor.svg"), 17.0, 3.0)
        self.setCursor(self.DEFAULT_CURSOR)
#
# <------------------- Reimplemented methods -------------->
#

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
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
                p = self.boundingRect().bottomRight()
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
                painter.setPen(pen)
                painter.drawRect(self.boundingRect())
            pen.setStyle(Qt.SolidLine)
            self._is_selected = True
        else:
            self._is_selected = False
        painter.setPen(pen)
        painter.drawEllipse(self.boundingRect())
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
        if self.moving and shift_is_pressed:
            # Erase the whole roi
            self.scene().ROIs.remove(self)
            self.scene().removeItem(self)
        super(RoiCirc, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.point_edited:
            shift_is_pressed = (event.modifiers() == Qt.ShiftModifier)
            if not shift_is_pressed:
                # todo: avoid point movement outside image
                self.resize(event.pos())
        elif self.moving:
            # todo: avoid roi movement outside image
            super(RoiCirc, self).mouseMoveEvent(event)

    def hoverMoveEvent(self, event):
        if self.is_editing() and self.isSelected():
            shift_is_pressed = (event.modifiers() == Qt.ShiftModifier)
            near_center = (geometry.distance2_qt(self.mass_center, event.pos()) <= 9)
            near_vertex = self.point_at_cursor(event.pos())
            if near_center or near_vertex:
                if near_center and shift_is_pressed:
                    self.setCursor(QCursor(self.DEL_POINT_CURSOR))
                else:
                    self.setCursor(QCursor(Qt.SizeAllCursor))
            else:
                self.setCursor(self.DEFAULT_CURSOR)

#
# <--------------------- override ---------------------->
#
    def __str__(self):
        r = self.boundingRect()
        p = r.bottomRight() - self.mass_center
        return "ellipse roi %s with center (%f, %f) and semi-axes (%f, %f)" % \
               (self.get_text(), self.mass_center.x(), self.mass_center.y(), p.x(), p.y())
#
# <---------------------- Functions -------------------->
#

    def resize(self, point):
        delta_x = abs(self.mass_center.x() - point.x())
        delta_y = abs(self.mass_center.y() - point.y())
        p1 = self.mass_center - QPointF(delta_x, delta_y)
        p2 = self.mass_center + QPointF(delta_x, delta_y)
        r = QRectF(p1, p2)
        self.setRect(r)
        self.update()

    def default_label_pos(self):
        r = self.boundingRect()
        r.translate(5, -10)
        p = r.topRight()
        self._label.setVisible(True)
        self._label.setPos(p)

    def get_text(self):
        return str(self._label.toPlainText())

    def is_editing(self):
        view = self.scene().views()[0]
        return view.left_operation == view.OP_SELECT

    def is_selected(self):
        return self._is_selected

    def point_at_cursor(self, point):
        r = self.boundingRect()
        p = r.bottomRight()
        return geometry.distance2_qt(point, p) <= 16

    def set_text(self, text):
        self._label.setPlainText(text)

    def set_z(self, z):
        self.roi_z = z

    def set_stats(self, stats):
        self.stats = stats