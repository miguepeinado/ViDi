import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class RoiStats(QDialog):
    def __init__(self, roi_list, button_list=None, parent=None):
        super(RoiStats, self).__init__(parent)
        #
        # <-------------- Gui definition -------------->
        #
        self.roi_list = roi_list
        l = QVBoxLayout()
        self.tab_rois = QTabWidget()
        l.addWidget(self.tab_rois)
        self.button_box = QDialogButtonBox()
        if button_list is None:
            self.button_box.addButton(QDialogButtonBox.Ok)
            self.button_box.accepted.connect(self.accept)
        else:
            for bt in button_list:
                self.button_box.addButton(bt, QDialogButtonBox.AcceptRole)
            self.button_box.addButton(QDialogButtonBox.Cancel)
            self.button_box.rejected.connect(self.reject)
        l.addWidget(self.button_box)
        self.setLayout(l)
        self.create_tabs()

    def create_tabs(self):
        label_list = []
        #
        # Define the list with different roi labels
        #
        for roi in self.roi_list:
            tx = roi.get_text()
            if tx not in label_list:
                label_list.append(tx)
                t = QTableWidget()
                self.tab_rois.addTab(t, tx)
        #
        # fill table widgets of the created tabs
        #
        used = [-1] * len(self.roi_list)
        n = self.tab_rois.count()
        headers = ['# slice'] + self.roi_list[0].stats.keys()
        for i in range(n):
            tx = str(self.tab_rois.tabText(i))
            table = self.tab_rois.widget(i)
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            j = 0
            for roi in self.roi_list:
                if used[j] < 0:
                    if roi.get_text() == tx:
                        row = table.rowCount()
                        table.insertRow(row)
                        table.setItem(row, 0, QTableWidgetItem(str(roi.roi_z)))
                        for c in range(1, len(headers)):
                            key = roi.stats.keys()[c - 1]
                            # todo: reformat numbers
                            table.setItem(row, c, QTableWidgetItem(str(roi.stats[key])))
                        used[j] = i
                j += 1
        #
        # for table with several rows calculate the whole parameters
        #
        for i in range(n):
            table = self.tab_rois.widget(i)
            if table.rowCount() > 1:
                row = table.rowCount()
                table.insertRow(row)
                print "total scores for ", str(self.tab_rois.tabText(i))
                min_value = 1.e7
                max_value = -1.e7
                area = 0
                total_points = 0
                total_counts = 0
                mean = 0
                variance = 0
                j = 0
                for roi in self.roi_list:
                    if i == used[j]:
                        area += roi.stats['area']
                        if roi.stats['max_value'] > max_value:
                            max_value = roi.stats['max_value']
                        if roi.stats['min_value'] < min_value:
                            min_value = roi.stats['min_value']
                        total_points += roi.stats['total_points']
                        total_counts += roi.stats['total_counts']
                        mean += roi.stats['mean'] * roi.stats['total_points']
                        variance += (roi.stats['variance'] * roi.stats['total_points'] + roi.stats['mean'] ** 2)
                    j += 1
                mean /= total_points
                variance = variance / total_points - mean ** 2
                table.setItem(row, 0, QTableWidgetItem('TOTAL'))
                table.setItem(row, 1, QTableWidgetItem(str(area)))
                table.setItem(row, 2, QTableWidgetItem(str(max_value)))
                table.setItem(row, 3, QTableWidgetItem(str(min_value)))
                table.setItem(row, 4, QTableWidgetItem(str(variance)))
                table.setItem(row, 5, QTableWidgetItem(str(total_points)))
                table.setItem(row, 6, QTableWidgetItem(str(total_counts)))
                table.setItem(row, 7, QTableWidgetItem(str(mean)))