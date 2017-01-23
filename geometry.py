import math

__author__ = "M.A. Peinado"
__copyright__ = "2016, M.A. Peinado"
__credits__ = ["Miguel A. Peinado"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "M.A. Peinado"
__email__ = "miguel.peinado@sespa.es"
__status__ = "prototype"


def complement2(self, memory_value, base):
    """
    Get the negative value with a 2-complement given by the first parameter
    in a binary length defined by the second parameter:
    - Direct means: from memory value to negative value C2(a,16)=-[not(a-1) & 0xffff]
    - Inverse means: from  negative value C2 to memory value C2(b,16)= [not(-b) & 0xffff]+1
    :param memory_value: value to do the 2-complement
    :param base: Binary length of the base
    :return: Direct 2-complement
    """
    return -(~(memory_value-1) & (2**base - 1))


def distance2_qt(point1, point2):
    """
    :param point1: QPointF instance with point 1
    :param point2: QPointF instance with point 2
    :return: square of euclidean distance between points
    """
    return (point1.x() - point2.x())**2 + (point1.y() - point2.y())**2


def distance2(x1, y1, x2, y2):
    """
        :param x1, y1: coordinates of point 1
        :param x2, y2: coordinates of point 2
        :return: square of euclidean distance between points
    """
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def dist_to_segment(point, start, end):
    l = distance2_qt(start, end)
    u = ((point.x() - start.x()) * (end.x() - start.x()) + (point.y() - start.y()) * (end.y() - start.y())) / l
    if u <= 0:
        return False, distance2_qt(point, start)
    elif u >=1:
        return False, distance2_qt(point, end)
    else:
        px = start.x() + u * (end.x() - start.x())
        py = start.y() + u * (end.y() - start.y())
        return True, distance2(px, py, point.x(), point.y())


def centroid_qt(polygon):
    from PyQt4.QtCore import QPointF
    """Determine the centroid of a QPolygon"""
    x = 0.
    y = 0.
    n = polygon.count()
    for i in range(n):
        x += polygon.at(i).x()
        y += polygon.at(i).y()
    x /= n
    y /= n
    return QPointF(x, y)


def area_qt(roi, roi_type):
    """Gets the area of a roi """
    sum = 0.0
    # Duck typing for poligonal rois...must pass something to distinguish between ellipses and rectangles
    if roi_type == "polygon":
        n = roi.count()
        pol = roi
        pol.insert(0, roi.at(n - 1))
        for i in range(n):
            p = pol.at(i)
            p2 = pol.at(i+1)
            sum += (p.x() * p2.y() -p2.x() * p.y())
        return abs(sum / 2.)
    elif roi_type == "ellipse":
        print roi.width(), roi.height()
        return roi.width()* roi.height() * math.pi / 4.