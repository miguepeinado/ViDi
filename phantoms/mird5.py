import numpy as np
from PyQt4.QtCore import QObject, pyqtSignal
from volumes import *
from specials import *


# todo: transform print in signals. Must change phantom to a QObject
def phantom(lut, gender='F', voxel_size=None, fov_size=None, array_size=None):
    """
    :param lut:
    :param gender:
    :param voxel_size: numpy array with (x, y, z) voxel size in mm
    :param fov_size:
    :param array_size:
    :return _phantom: is the 3D of th Cristy phantom as defined in mird report #5
    """
    a = voxel_size is not None
    b = fov_size is not None
    c = array_size is not None
    # Only two out of the three conditions can be true
    if ((a and b) and c) or not ((a and (b or c)) or (b and c)):
        raise ValueError("Two out of the three dimension values must be not null")
    if not a:
        voxel_size = fov_size / array_size
    elif not b:
        fov_size = voxel_size * array_size
    elif not c:
        array_size = fov_size / voxel_size
    # change array size (z planes are in the first dimensions as
    # inherited from the ViDi scheme, Why????)
    array_size = array_size[::-1]
    z_zero, y_zero, x_zero = array_size / 2.
    dx, dy, dz = voxel_size
    _phantom = np.zeros(shape=array_size, dtype=np.float32) - lut['air']
    gender = gender.capitalize()
    #
    # B.2: Exterior
    #
    if 'body' in lut:
        # trunk
        center = np.array([0, 0])
        semiaxis = np.array([200, 100])
        z_range = [0, 700]
        units = 1000 + lut['body']
        trunk = z_cylinder(center, semiaxis, z_range, units, voxel_size, array_size)
        _phantom += trunk
        # head...has two parts
        center = np.array([0, 0])
        semiaxis = np.array([70, 100])
        z_range = [700, 855]
        head1 = z_cylinder(center, semiaxis, z_range, units, voxel_size, array_size)
        _phantom += head1
        center = np.array([0, 0, 855])
        semiaxis = np.array([70, 100, 85])
        head2 = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        z_bottom = int(round(855. / dz) + z_zero)
        head2[:z_bottom, :, :] = 0
        _phantom += head2
        # legs...it's a little bit different as the change as z function
        _phantom += legs(units, voxel_size, array_size)
        print "body...done"
        # Add genitalia for males
        if gender=='M':
            pass

    #
    # B.3. Now define all the organs inside...(-,-)
    #

    # B.3.1. Skeletal system..2B done

    # B.3.2. Bone marrow..2B done

    # B.3.3. Adrenals
    if 'adrenals' in lut:
        # left kidney...
        center = np.array([45, 65, 380])
        semiaxis = np.array([15, 5, 50])
        units = 1000 + lut['adrenals']
        l_adrenal = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        z_bottom = int(round(380. / dz) + z_zero)
        l_adrenal[:z_bottom, :, :] = 0
        _phantom += l_adrenal
        # right kidney
        center = np.array([-45, 65, 380])
        r_adrenal = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        r_adrenal[:z_bottom, :, :] = 0
        _phantom += r_adrenal
        print "adrenals...done"

    # B.3.4. Brain
    if 'brain' in lut:
        center = np.array([0, 0, 865])
        semiaxis = np.array([60, 90, 65])
        units = 1000 + lut['brain']
        brain = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        _phantom += brain
        print "brain...done"

    # B.3.5. Urinary bladder
    if 'bladder' in lut:
        center = np.array([0, -45, 80])
        semiaxis = np.array([49.58, 34.58, 34.58])
        units = 1000 + lut['bladder'][0]
        bladder = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        semiaxis = np.array([47.06, 32.06, 32.06])
        content = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        bladder -= content
        _phantom += bladder
        units = 1000 + lut['bladder'][1]
        content = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        _phantom += content
        print "bladder...done"

    # B.3.6. GI tract and contents...2B done
    if 'stomach' in lut:
        # ...stomach and contents
        center = np.array([80, -40, 350])
        semiaxis = np.array([40, 30, 80])
        units = 1000 + lut['stomach'][0]
        stomach = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        semiaxis = np.array([33.87, 23.87, 73.87])
        content = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        stomach -= content
        _phantom += stomach
        units = 1000 + lut['stomach'][1]
        content = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        _phantom += content
        print "stomach...done"

    if "intestine" in lut:
        # ...small intenstine...(don't considered as is defined as freely moving in a volume)
        # center = np.array([0, -38])
        # semiaxis = np.array([113, 113])
        # z_range = [170, 270]
        # units = 1000 + lut['intestine'][0]
        # small_int = z_cylinder(center, semiaxis, z_range, units, voxel_size, array_size)
        # y_back = int(round(-48.6/dy) + y_zero)
        # y_front = int(round(22 / dy) + y_zero)
        # small_int[:, :y_back, :] = 0
        # small_int[:, y_front:, :] = 0
        # _phantom += small_int
        # ...Upper large intestine 1: ascending colon
        # center = np.array([-85, -23.6])
        # semiaxis = np.array([25, 25])
        # z_range = [144.5, 240]
        # units = 1000 + lut['intestine'][0]
        # uli1 = z_cylinder(center, semiaxis, z_range, units, voxel_size, array_size)
        # semiaxis = np.array([17.915, 17.915])
        # content = z_cylinder(center, semiaxis, z_range, units, voxel_size, array_size)
        # uli1 -= content
        # _phantom += uli1
        # units = 1000 + lut['intestine'][1]
        # content = z_cylinder(center, semiaxis, z_range, units, voxel_size, array_size)
        # _phantom += content
        # # ...Upper large intestine 2: transverse colon
        # center = np.array([-23.6, 255])
        # semiaxis = np.array([25, 15])
        # x_range = [-105, 105]
        # units = 1000 + lut['intestine'][0]
        # uli2 = x_cylinder(center, semiaxis, x_range, units, voxel_size, array_size)
        # semiaxis = np.array([19.73, 9.73])
        # content = x_cylinder(center, semiaxis, x_range, units, voxel_size, array_size)
        # uli2 -= content
        # _phantom += uli2
        # units = 1000 + lut['intestine'][1]
        # content = x_cylinder(center, semiaxis, x_range, units, voxel_size, array_size)
        # _phantom += content
        # # ...Lower large intestine 1: descending colon
        units = (1000 + lut['intestine'][0], 1000 + lut['intestine'][1])
        # _phantom += lli1(units, voxel_size, array_size)
        # ...Lower large intestine 2: sigmoid colon
        _phantom += lli2(units, voxel_size, array_size)
        print "intestine...done"
        return _phantom

    # B.3.7. Heart...2B done

    # B.3.8. Kidneys
    if 'kidneys' in lut:
        # left kidney...
        center = np.array([60, 60, 325])
        semiaxis = np.array([45, 15, 55])
        units = 1000 + lut['kidneys']
        l_kidney = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        x_left = int(round(30./dx) + x_zero)
        l_kidney[:,:,:x_left] = 0
        _phantom += l_kidney
        # right kidney
        center = np.array([-60, 60, 325])
        r_kidney = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        x_right = int(round(-30. / dx) + x_zero)
        r_kidney[:, :, x_right:] = 0
        _phantom += r_kidney
        print "kidneys...done"

    # B.3.9. Liver
    if 'liver' in lut:
        center = np.array([0, 0])
        semiaxis = np.array([165, 80])
        z_range = [270, 430]
        units = 1000 + lut['liver']
        liver = z_cylinder(center, semiaxis,z_range, units, voxel_size, array_size)
        # Now get cutted by the plane x/35+y/45-z/43<=-1
        slices, rows, cols = np.ogrid[0:array_size[0], 0:array_size[1], 0:array_size[2]]
        # Beware with the inequalities: A z is in the other direction inequalities must be reversed
        mask = (cols - x_zero) / 350 * dx + (rows - y_zero) / 450 * dy - (slices - z_zero) / 430 * dz > -1
        liver[mask] = 0
        _phantom += liver
        print "liver...done"

    # B.3.10. Lungs
    if 'lungs' in lut:
        # left lung...
        center = np.array([85, 0, 435])
        semiaxis = np.array([50, 75, 240])
        units = 1000 + lut['lungs']
        l_lung = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        # define the anterior section to remove...
        center[0] = 25
        ant_section = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        # ...only the intersection with the lung...
        mask = np.where(l_lung == 0)
        ant_section[mask] = 0
        # ...and only positive y axis
        ant_section[:, int(y_zero):, :] = 0
        l_lung -= ant_section
        z_bottom = int(round(435. / dz) + z_zero)
        l_lung[:z_bottom, :, :] = 0
        _phantom += l_lung
        # right lung
        center = np.array([-85, 0, 435])
        semiaxis = np.array([50, 75, 240])
        r_lung = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        # define the anterior section to remove...
        center[0] = -25
        ant_section = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        # ...only the intersection with the lung...
        mask = np.where(r_lung == 0)
        ant_section[mask] = 0
        # ...and only positive y axis
        ant_section[:, int(y_zero):, :] = 0
        r_lung -= ant_section
        r_lung[:z_bottom, :, :] = 0
        _phantom += r_lung
        print "lungs...done"

    # B.3.11. Ovaries
    if 'ovaries' in lut and gender=='F':
        center = np.array([60, 0, 150])
        semiaxis = np.array([10, 5, 20])
        units = 1000 + lut['ovaries']
        l_ovary = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        _phantom += l_ovary
        center = np.array([-60, 0, 150])
        r_ovary = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        _phantom += r_ovary
        print "ovaries...done"

    # B.3.12. Pancreas
    if 'pancreas' in lut:
        center = np.array([0, 0, 370])
        semiaxis = np.array([150, 10, 30])
        units = 1000 + lut['pancreas']
        pancreas = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        x_left = int(x_zero)
        pancreas[:, :,:x_left] = 0
        x_right = int(round(30./dx) + x_zero)
        z_bottom = int(round(370. / dz) + z_zero)
        pancreas[:z_bottom, :, x_right:] = 0
        _phantom += pancreas
        print "pancreas...done"

    # B.3.13. Skin...no analytical definition: 2 mm thickness extending over the entire exterior of the phantom

    # B.3.14. Spleen
    if 'spleen' in lut:
        center = np.array([110, 30, 370])
        semiaxis = np.array([35, 20, 60])
        units = 1000 + lut['spleen']
        spleen = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        _phantom += spleen
        print "spleen...done"

    # B.3.15. Testicles
    if 'testicles' in lut and gender == 'M':
        center = np.array([13, 8, 23])
        semiaxis = np.array([13, 15, 23])
        units = 1000 + lut['testicles']
        l_testicle = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        _phantom += l_testicle
        center = np.array([-13, 8, 23])
        r_testicle = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        _phantom += r_testicle
        print "testicles...done"

    # B.3.16. Thymus
    if 'thymus' in lut:
        center = np.array([-20, -60, 605])
        semiaxis = np.array([30, 5, 40])
        units = 1000 + lut['thymus']
        thymus = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        _phantom += thymus
        print "thymus...done"

    # B.3.17. Thyroid...2B done

    # B.3.18. Uterus
    if 'uterus' in lut and gender == 'F':
        center = np.array([0, -20, 140])
        semiaxis = np.array([25, 50, 15])
        units = 1000 + lut['uterus']
        uterus = ellipsoid(center, semiaxis, units, voxel_size, array_size)
        y_back = int(round(-45./dy) + y_zero)
        uterus[:, :y_back, :] = 0
        _phantom += uterus
        print "uterus...done"

    # phantom reflection on z axis
    _phantom[:, :, :] = _phantom[::-1, :, :]
    return _phantom
