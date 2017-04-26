import logging
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import ui_calculator


class Dosimetry(QDialog, ui_calculator.Ui_Dialog):

    VOI_ROLES = {1: "Source", 2: "Target", 3: "OAR"}

    def __init__(self, vois, patient_data, acq_data, parent=None):
        super(Dosimetry, self).__init__(parent)
        self.setupUi(self)
        self.vois = vois
        self.patient_data = patient_data
        #
        # Additional Gui setups
        #
        self.button_bar.addButton(QPushButton("Continue"), QDialogButtonBox.AcceptRole)
        self.button_bar.accepted.connect(self.accept)
        self.button_bar.rejected.connect(self.reject)
        self.fill_table()
        self.setLayout(self.main_layout)
        self.resize(600, 300)
        self.dt_acquisition_time.setDate(acq_data[0])
        self.dt_acquisition_time.setTime(acq_data[1])
        y = acq_data[0].year()
        m = acq_data[0].month()
        self.dt_admin_time.setDate(acq_data[0].addDays(-1))
        self.dt_admin_time.setTime(QTime(12, 0))

    def fill_table(self):
        rows = len(self.vois)
        self.vois_table.setRowCount(rows)
        self.vois_table.verticalHeader().hide()
        self.vois_table.setColumnCount(6)
        self.vois_table.setHorizontalHeaderLabels(
            ("VOI name", "Source", "Target", "OAR", "Total counts", "Residence time (h)"))
        self.vois_table.resizeColumnsToContents()
        self.vois_table.setColumnWidth(0, 150)
        self.vois_table.setColumnWidth(4, 0)
        for row in range(rows):
            # put the vois label
            item = QTableWidgetItem(self.vois[row].label)
            flags = item.flags()
            flags ^= Qt.ItemIsEditable      # Make flag not editable
            item.setFlags(flags)
            self.vois_table.setItem(row, 0, item)
            for column in range(1, 4):
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Unchecked)
                self.vois_table.setItem(row, column, item)
            s = "{:.5g}".format(self.vois[row].stats.total_counts)
            if QLocale().decimalPoint() == QChar(","):
                s = s.replace(".", ",")
            item = QTableWidgetItem(s)
            flags = item.flags()
            flags ^= Qt.ItemIsEditable  # Make flag not editable
            item.setFlags(flags)
            self.vois_table.setItem(row, 4, item)
        self.vois_table.itemChanged.connect(self.handle_item_changed)
        self.accepted.connect(self.set_roles)

    def handle_item_changed(self, item):
        col = item.column()
        if col == 1:
            w = 150 if item.checkState() else 0
            # Show total counts column
            self.vois_table.setColumnWidth(4, w)
        elif col > 1 and item.checkState():
            c = 3 if col == 2 else 2
            row = item.row()
            self.vois_table.item(row, c).setCheckState(False)

    def set_roles(self):
        rows = len(self.vois)
        for row in range(rows):
            voi_role = 0
            for col in range(1, 4):
                # See voi object flags for more details
                voi_role += (2 ** (col - 1) if self.vois_table.item(row, col).checkState() else 0)
            self.vois[row].set_role(voi_role)