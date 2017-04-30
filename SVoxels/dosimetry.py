import logging
import re
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import ui_calculator


class Dosimetry(QDialog, ui_calculator.Ui_Dialog):

    VOI_ROLES = {1: "Source", 2: "Target", 3: "OAR"}

    def __init__(self, vois, patient_data, acq_data, parent=None):
        super(Dosimetry, self).__init__(parent)
        self.setupUi(self)
        self.vois = vois
        self.rows = len(self.vois)
        self.patient_data = patient_data
        self.f_quant = 0
        self.residence_time = []
        self.time_lapse = 0
        #
        # Additional Gui setups
        #
        self.button_bar.addButton(QPushButton("Continue"), QDialogButtonBox.AcceptRole)
        self.button_bar.accepted.connect(self.verify_accept)
        self.fill_table()
        self.setLayout(self.main_layout)
        self.resize(600, 300)
        self.dt_acquisition_time.setDate(acq_data[0])
        self.dt_acquisition_time.setTime(acq_data[1])
        y = acq_data[0].year()
        m = acq_data[0].month()
        self.dt_admin_time.setDate(acq_data[0].addDays(-1))
        self.dt_admin_time.setTime(QTime(12, 0))
        # Must put a reg ex validator for f_quant textbox
        v = QRegExpValidator(QRegExp('-?\d+\.?\d*(?:[Ee]\ *[-+]?\d+)?'))
        self.tx_f_quant.setValidator(v)

    def fill_table(self):
        self.vois_table.setRowCount(self.rows)
        self.vois_table.verticalHeader().hide()
        self.vois_table.setColumnCount(6)
        self.vois_table.setHorizontalHeaderLabels(
            ("VOI name", "Source", "Target", "OAR", "Total counts", "Residence time (h)"))
        self.vois_table.resizeColumnsToContents()
        self.vois_table.setColumnWidth(0, 150)
        self.vois_table.setColumnWidth(4, 0)
        for row in range(self.rows):
            # put the vois label
            item = QTableWidgetItem(self.vois[row].label)
            flags = item.flags()
            flags ^= Qt.ItemIsEditable      # Make flag not editable
            item.setFlags(flags)
            self.vois_table.setItem(row, 0, item)
            # Put the checkboxes
            for column in range(1, 4):
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Unchecked)
                self.vois_table.setItem(row, column, item)
            # Put the total counts column
            s = "{:.5g}".format(self.vois[row].stats.total_counts)
            if QLocale().decimalPoint() == QChar(","):
                s = s.replace(".", ",")
            item = QTableWidgetItem(s)
            flags = item.flags()
            flags ^= Qt.ItemIsEditable  # Make flag not editable
            item.setFlags(flags)
            self.vois_table.setItem(row, 4, item)
            # Put the last column item (workaround to set a validator)

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

    def verify_accept(self):
        # 1. Verify if injection date is previous to acquisition date
        self.time_lapse = self.dt_admin_time.dateTime().secsTo(self.dt_acquisition_time.dateTime())
        print self.time_lapse
        # 2. Verify quantification factor is not zero and valid:
        self.f_quant, is_ok = self.tx_f_quant.text().toDouble()
        if  not is_ok or self.f_quant == 0:
            QMessageBox.critical(self, "VALUE ERROR", "Quantification factor must be a valid not null value")
            return
        # 3. Verify all the vois have valid residence time values
        for row in range(self.rows):
            it = self.vois_table.item(row, 5)                   # cellWidget(row, 5)
            tau, is_ok = it.data(Qt.DisplayRole).toDouble()     # it.text().toDouble()
            if is_ok and tau != 0:
                self.residence_time.append(tau)
            else:
                QMessageBox.critical(self, "VALUE ERROR", "residence time for voi '{}'\n"
                                                          " must be a valid not null value".format(self.vois[row].label))
                return
        self.accept()
