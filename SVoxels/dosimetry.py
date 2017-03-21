from PyQt4.QtGui import *
from PyQt4.QtCore import *


class VoisRole(QDialog):

    ROLES = {1: "Source", 2: "Target", 3: "OAR"}

    def __init__(self, vois, parent=None):
        super(VoisRole, self).__init__(parent)
        self.vois = vois
        l = QVBoxLayout(self)
        self.table = QTableWidget()
        l.addWidget(self.table)
        button_bar = QDialogButtonBox(QDialogButtonBox.Cancel)
        # Add a button for clear all selections
        bt_cont = QPushButton("Continue")
        button_bar.addButton(bt_cont, QDialogButtonBox.AcceptRole)
        l.addWidget(button_bar)
        button_bar.accepted.connect(self.accept)
        button_bar.rejected.connect(self.reject)
        self.fill_table()
        self.resize(550, 200)

    def fill_table(self):
        rows = len(self.vois)
        self.table.setRowCount(rows)
        self.table.verticalHeader().hide()
        self.table.setColumnCount(5)
        for row in range(rows):
            # put the vois label
            item = QTableWidgetItem(self.vois[row].label)
            self.table.setItem(row, 0, item)
            for column in range(1, 4):
                item = QTableWidgetItem(self.ROLES[column])
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Unchecked)
                self.table.setItem(row, column, item)
        self.table.itemChanged.connect(self.handle_item_changed)
        self.accepted.connect(self.set_roles)

    def handle_item_changed(self, item):
        col = item.column()
        if col > 1 and item.checkState():
            c = 3 if col == 2 else 2
            row = item.row()
            self.table.item(row, c).setCheckState(False)

    def set_roles(self):
        rows = len(self.vois)
        for row in range(rows):
            voi_role = 0
            for col in range(1, 4):
                # See voi object flags for more details
                voi_role += (2 ** (col - 1) if self.table.item(row, col).checkState() else 0)
            self.vois[row].set_role(voi_role)