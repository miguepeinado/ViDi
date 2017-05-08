import numpy as np


def ellipsoid(center, semiaxis, value, voxel_size, array_size):
    """
    :param center: (x, y, z) coordinates of the center of the ellipsoid
    :param semiaxis: (x, y, z) dimensions (in mm) of the ellipsoid.
    :param value
    :param voxel_size: numpy array with (x, y, z) voxel size in mm
    :param fov_size:
    :param array_size:
    :return: The array with the ellipsoid
    """
    # center in mm => convert to voxels
    center = np.round(center / voxel_size, decimals=0)
    x_center, y_center, z_center = center
    z_zero, y_zero, x_zero = array_size / 2.
    dx, dy, dz = voxel_size
    x_semiaxis, y_semiaxis, z_semiaxis = semiaxis
    dummy = np.zeros(array_size , dtype=np.float32)
    # slice_labels = np.ndarray(shape[1:], dtype='a10')
    slices, rows, cols = np.ogrid[0:array_size [0], 0:array_size [1], 0:array_size [2]]
    mask = (slices - z_zero - z_center) * (slices - z_zero - z_center) / z_semiaxis ** 2 * dz ** 2 + \
           (cols - x_zero - x_center) * (cols - x_zero - x_center) / x_semiaxis ** 2 * dx ** 2 + \
           (rows - y_zero - y_center) * (rows - y_zero - y_center) / y_semiaxis ** 2 * dy ** 2 <= 1
    dummy[mask] = value
    return dummy


def z_cylinder(center, semiaxis, z_range, value, voxel_size, array_size):
    """
    :param center: (x, y) coordinates of the center of the ellipsoid
    :param semiaxis: (x, y) dimensions (in mm) of the ellipsoid.
    :param z_range: Start and end (in mm) of the elliptical cylinder
    :param value:
    :param voxel_size: numpy array with (x, y, z) voxel size in mm
    :param fov_size:
    :param array_size:
    :return: The array with the elliptical cylinder
    """
    z_zero, y_zero, x_zero = array_size / 2.
    dx, dy, dz = voxel_size
    # center in mm => convert to voxels
    center = np.round(center / voxel_size[:2], decimals=0)
    x_center, y_center = center
    # z range in mm => convert to voxels
    z_min, z_max = np.round(z_range / dz + z_zero, decimals=0)
    x_semiaxis, y_semiaxis = semiaxis
    dummy = np.zeros(array_size, dtype=np.float32)
    slice = np.zeros(array_size[1:], dtype=np.float32)
    rows, cols = np.ogrid[ 0:array_size[1], 0:array_size[2]]
    mask = (cols - x_zero - x_center) * (cols - x_zero - x_center) / x_semiaxis ** 2 * dx ** 2 + \
           (rows - y_zero - y_center) * (rows - y_zero - y_center) / y_semiaxis ** 2 * dy ** 2 <= 1
    slice[mask] = value
    for z in range(int(z_min), int(z_max + 1)):
        dummy[z, :, :] = slice
    return dummy


def x_cylinder(center, semiaxis, x_range, value, voxel_size, array_size):
    """
    :param center: (z, y) coordinates of the center of the ellipsoid
    :param semiaxis: (z, y) dimensions (in mm) of the ellipsoid.
    :param x_range: Start and end (in mm) of the elliptical cylinder
    :param value:
    :param voxel_size: numpy array with (x, y, z) voxel size in mm
    :param array_size:
    :return: The array with the elliptical cylinder
    """
    dx, dy, dz = voxel_size
    z_zero, y_zero, x_zero = array_size / 2.
    # center in mm => convert to voxels
    y_center = np.round(center[0] / dy, decimals=0)
    z_center = np.round(center[1] / dz, decimals=0)
    # z range in mm => convert to voxels
    x_min, x_max = np.round(x_range / dx + x_zero, decimals=0)
    y_semiaxis, z_semiaxis = semiaxis
    dummy = np.zeros(array_size, dtype=np.float32)
    sagital = np.zeros(array_size[:2], dtype=np.float32)
    slice, rows = np.ogrid[ 0:array_size[0], 0:array_size[1]]
    mask = (slice - z_zero - z_center) * (slice - z_zero - z_center) / z_semiaxis ** 2 * dz ** 2 + \
           (rows - y_zero - y_center) * (rows - y_zero - y_center) / y_semiaxis ** 2 * dy ** 2 <= 1
    sagital[mask] = value
    for x in range(int(x_min), int(x_max + 1)):
        dummy[:, :, x] = sagital
    return dummy