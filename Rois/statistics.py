from PyQt4.QtGui import QPolygonF
from PyQt4.QtCore import Qt, QPointF
import MyTools.geometry as geometry


class Stats:
    def __init__(self):
        self.area = None
        self.total_points = None
        self.total_counts = None
        self.minimum_value = None
        self.maximum_value = None
        self.mean = None
        self.variance = None

    def values(self):
        return {'area': self.area, 'min_value': self.minimum_value, 'max_value': self.maximum_value, 'mean': self.mean,
                'variance': self.variance, 'total_counts': self.total_counts, 'total_points': self.total_points}


def calculate(roi, roi_type, pixel_array):

    def inside(r, point):
        if roi_type == "polygon":
            return r.containsPoint(point, Qt.OddEvenFill)
        elif roi_type == "ellipse":
            d = ((point.x() - p_center.x()) / a) ** 2 + ((point.y() - p_center.y()) / b) ** 2 <= 1
            return d
        else:
            return True     # for rectangles points are always inside

    stats = Stats()
    if roi_type == "polygon":
        rect = roi.boundingRect()
    elif roi_type == "ellipse":
        rect = roi
        a = rect.width() / 2.
        b = rect.height() / 2.

    p1 = rect.topLeft()
    p2 = rect.bottomRight()
    if roi_type == "ellipse":
        p_center = p1 + QPointF(a, b)
        print "ellipse ", p_center, (a, b)
    j_min = int(round(p1.x()))
    j_max = int(round(p2.x()))
    i_min = int(round(p1.y()))
    i_max = int(round(p2.y()))
    print "intervals", j_min, j_max, i_min, i_max
    sum1 = 0
    sum2 = 0
    n = 0
    max_value = -1.e7
    min_value = 1.e7
    for i in range(i_min, i_max + 1):
        for j in range(j_min, j_max + 1):
            if inside(roi, QPointF(j, i)):
                px_value = pixel_array[i, j]
                sum1 += px_value
                sum2 += px_value ** 2
                n += 1
                if px_value > max_value:
                    max_value = px_value
                if px_value < min_value:
                    min_value = px_value
                # pixel_array[i, j] = 1000.
    stats.minimum_value = min_value
    stats.maximum_value = max_value
    if n > 0:
        stats.mean = float(sum1) / float(n)
        stats.variance = float(sum2) / float(n) - stats.mean ** 2
    else:
        raise ValueError("ROI seems to be empty!")
    # Change area calculation for ellipses
    stats.area = geometry.area_qt(roi, roi_type)
    stats.total_counts = sum1
    stats.total_points = n
    return stats
