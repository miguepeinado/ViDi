from statistics import Stats


class Voi:

    SOURCE_ROLE = 1
    TARGET_ROLE = 2
    OAR_ROLE = 4

    def __init__(self, label, roi_s):
        self.label = label
        # Duck typing for vois defined from a single roi
        try:
            len(roi_s)
            self.roi_list = roi_s
        except TypeError:
            self.roi_list = []
            self.roi_list.append(roi_s)
        self._role = 0
        self.stats = Stats()
        self._voxel_doses = None

    def set_role(self, role):
        self._role = role

    def get_role(self):
        return self._role

    def append(self, roi):
        self.roi_list.append(roi)

    def calculate_stats(self):
        min_value = 1.e7
        max_value = -1.e7
        area = 0
        total_points = 0
        total_counts = 0
        mean = 0
        variance = 0
        for roi in self.roi_list:
            area += roi.stats.area
            if roi.stats.maximum_value > max_value:
                max_value = roi.stats.maximum_value
            if roi.stats.minimum_value < min_value:
                min_value = roi.stats.minimum_value
            total_points += roi.stats.total_points
            total_counts += roi.stats.total_counts
            mean += roi.stats.mean * roi.stats.total_points
            variance += (roi.stats.variance + roi.stats.mean ** 2) * roi.stats.total_points
        self.stats.area = area
        self.stats.maximum_value = max_value
        self.stats.minimum_value = min_value
        self.stats.total_points = total_points
        self.stats.total_counts = total_counts
        self.stats.mean = mean / total_points
        self.stats.variance = variance / total_points - self.stats.mean ** 2
        return self.stats

    def set_doses(self, voxel_doses):
        self._voxel_doses = voxel_doses

    def doses(self):
        return self._voxel_doses
