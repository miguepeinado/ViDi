import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def legs(value, voxel_size, array_size):
    """
    Legs: frustrum of two circular cones
    :param value:
    :param voxel_size: numpy array with (x, y, z) voxel size in mm
    :param array_size:
    :return: the array with the legs
    """
    z_zero, y_zero, x_zero = array_size / 2.
    dx, dy, dz = voxel_size
    z_min = int(z_zero + 1)
    z_max =  int(z_zero + round(800. / dz))
    x_center = int(100. / dx)
    dummy = np.zeros(array_size, dtype=np.float32)
    for z in range(z_min, z_max + 1):
        x_center *= -1
        slice = np.zeros(array_size[1:], dtype=np.float32)
        rows, cols = np.ogrid[0:array_size[1], 0:array_size[2]]
        mask = (rows - y_zero) * (rows - y_zero) * dy ** 2 +\
               (cols - x_center - x_zero) * (cols - x_center - x_zero) * dx ** 2 <= \
               (200. - z * dz / 10.) ** 2
        slice[mask] = value
        x_center *= -1
        mask = (rows - y_zero) * (rows - y_zero) * dy ** 2 + \
               (cols - x_center - x_zero) * (cols - x_center - x_zero) * dx ** 2 <= \
               (200. - z * dz / 10.) ** 2
        slice[mask] = value
        dummy[2*int(z_zero) - z, :, :] = slice
    return dummy


def lli1(values, voxel_size, array_size):
    """
    Descendig colon: elliptical prism with axis not vertical
    :param values:
    :param voxel_size: numpy array with (x, y, z) voxel size in mm
    :param array_size:
    :return: the array with the legs
    """
    z_zero, y_zero, x_zero = array_size / 2.
    dx, dy, dz = voxel_size
    z_min = int(z_zero + round(87.2 / dz))
    z_max =  int(z_zero + round(240. / dz))
    dummy = np.zeros(array_size, dtype=np.float32)
    ax = 0.28 / 15.28
    ay = 2.5 / 15.28
    x_center = (90 + ax * (87.2 - 240)) / dx
    dx_center = ax * dz / dx
    y_center = 0
    dy_center = -ay * dz / dy
    rows, cols = np.ogrid[0:array_size[1], 0:array_size[2]]
    for z in range(z_min, z_max + 1):
        slice = np.zeros(array_size[1:], dtype=np.float32)
        # Wall
        x_semiaxis, y_semiaxis = [18.8, 21.3]
        mask = (rows - y_center - y_zero) * (rows - y_center - y_zero) / y_semiaxis **2 * dy ** 2 + \
               (cols - x_center - x_zero) * (cols - x_center - x_zero) / x_semiaxis **2 * dx ** 2 <= 1
        slice[mask] = values[0]
        # Contents
        x_semiaxis, y_semiaxis = [15.8, 13.4]
        mask = (rows - y_center - y_zero) * (rows - y_center - y_zero) / y_semiaxis ** 2 * dy ** 2 + \
               (cols - x_center - x_zero) * (cols - x_center - x_zero) / x_semiaxis ** 2 * dx ** 2 <= 1
        slice[mask] = values[1]
        dummy[z, :, :] = slice
        x_center += dx_center
        y_center += dy_center
    return dummy


def lli2(values, voxel_size, array_size):
    """
    Descending colon: elliptical prism with axis not vertical
    :param values:
    :param voxel_size: numpy array with (x, y, z) voxel size in mm
    :param array_size:
    :return: the array with the legs
    """
    z_zero, y_zero, x_zero = array_size / 2.
    dx, dy, dz = voxel_size
    x0 = int(x_zero + round(30 / dx))
    z0 = int(z_zero + round(87.2 / dz))
    sigmoid = np.zeros(array_size, dtype=np.float32)
    slices, rows, cols = np.ogrid[0:array_size[0], 0:array_size[1], 0:array_size[2]]
    mask = (((cols - x0) * (cols - x0) * dx ** 2 + (slices - z0) * (slices - z0) * dz ** 2) ** .5
            - 57.2) ** 2 + (rows - y_zero) * (rows - y_zero) * dy ** 2 <= 15.7 ** 2
    sigmoid[mask] = values[0]
    mask = (((cols - x0) * (cols - x0) * dx ** 2 + (slices - z0) * (slices - z0) * dz ** 2) ** .5
            - 57.2) ** 2 + (rows - y_zero) * (rows - y_zero) * dy ** 2 <= 9.1 ** 2
    sigmoid[mask] = values[1]
    sigmoid[:, :, :x0] = 0
    sigmoid[z0:, :, :] = 0
    # Second half of the sigmoid
    sigmoid2 = np.zeros(array_size, dtype=np.float32)
    mask2 = (((cols - x0) * (cols - x0) * dx ** 2 + (slices - z0) * (slices - z0) * dz ** 2) ** .5
            - 57.2) ** 2 + (rows - y_zero) * (rows - y_zero) * dy ** 2 <= 15.7 ** 2
    sigmoid2[mask2] == values[0]
    # mask = (((cols - x0) * (cols - x0) * dx ** 2 + (slices - z_zero) * (slices - z_zero) * dz ** 2) ** .5
    #         - 30) ** 2 + (rows - y_zero) * (rows - y_zero) * dy ** 2 <= 9.1 ** 2
    # sigmoid2[mask] = 0
    # sigmoid2[:, :, x0:] = 0
    # sigmoid2[:int(z_zero), :, :] = 0
    # sigmoid += sigmoid2
    z, y, x = sigmoid2.nonzero()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, zdir='z', c='red')
    plt.show()
    return sigmoid
