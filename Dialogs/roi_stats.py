import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class RoiStats(QDialog):
    def __init__(self, voi_list, button_list=None, parent=None):
        super(RoiStats, self).__init__(parent)
        #
        # <-------------- Gui definition -------------->
        #
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
        # Attributes
        self.voi_list = voi_list
        self.create_tabs()

    def create_tabs(self):
        i = 0
        for voi in self.voi_list:
            tx = voi.label
            t = QTableWidget()
            self.tab_rois.addTab(t, tx)
            #
            # fill table widgets of the created tabs
            #
            roi_list = voi.roi_list
            headers = ['# slice'] + roi_list[0].stats.values().keys()
            table = self.tab_rois.widget(i)
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            for roi in roi_list:
                row = table.rowCount()
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(str(roi.roi_z)))
                c = 1
                values = roi.stats.values()
                for k in roi.stats.values():
                    # todo: reformat numbers
                    table.setItem(row, c, QTableWidgetItem(str(values[k])))
                    c += 1
            #
            # for table with several rows calculate the total parameters
            #
            if len(roi_list) > 1:
                stats = voi.calculate_stats()
                row = table.rowCount()
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem('TOTAL'))
                c = 1
                values = stats.values()
                for k in roi.stats.values():
                    # todo: reformat numbers
                    table.setItem(row, c, QTableWidgetItem(str(values[k])))
                    c += 1
            i += 1