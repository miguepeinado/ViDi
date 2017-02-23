"""Functions related with s-voxel dosimetry"""


def roi2indices(roi, roi_type, k):
    """Return the pixels inside a roi as a list of their indices"""
    from PyQt4.QtCore import Qt, QPointF

    def inside(r, point):
        if roi_type == "polygon":
            return r.containsPoint(point, Qt.OddEvenFill)
        elif roi_type == "ellipse":
            d = ((point.x() - p_center.x()) / a) ** 2 + ((point.y() - p_center.y()) / b) ** 2 <= 1
            return d
        else:
            return True     # for rectangles points are always inside

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
    j_min = int(round(p1.x()))
    j_max = int(round(p2.x()))
    i_min = int(round(p1.y()))
    i_max = int(round(p2.y()))
    index_list = []
    # todo: Consider the possibility of vois that already contains other vois
    for i in range(i_min, i_max + 1):
        for j in range(j_min, j_max + 1):
            if inside(roi, QPointF(j, i)):
                # z index is in the first position!!!
                index_list.append((k, i, j))
    return index_list


def s_value_parser(isotope, vx_size):
    """returns the s-voxel values for the isotope and voxel size"""
    import csv
    import numpy as np
    from PyQt4.QtCore import QDir

    # todo: Verify if changes in directory file is necessary
    # todo: Retrieve from url if file does not exist
    data_dir = QDir.currentPath() + "/SVoxels/"
    print data_dir
    file_name = QDir.currentPath() + "/SVoxels/{}{}mmsoft.txt".format(isotope, vx_size)
    index_value_pair = []
    with open(file_name, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter='\t', quotechar='\'')
        i = 0
        for row in reader:
            if i > 1:
                ix = (int(row[0]), int(row[1]), int(row[2]))
                index_value_pair.append([ix, float(row[3])])
            i += 1
    # shape is last index read + 1 in each dimension
    shape = np.array(ix) + np.array([1, 1, 1])
    s_values = np.ndarray(shape)
    for iv in index_value_pair:
        s_values[iv[0]] = iv[1]
    return s_values