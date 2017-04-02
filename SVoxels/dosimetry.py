import logging
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSql import *
import ui_patient


class Dosimetry(QDialog):

    VOI_ROLES = {1: "Source", 2: "Target", 3: "OAR"}

    def __init__(self, vois, patient_data, parent=None):
        super(Dosimetry, self).__init__(parent)
        self.vois = vois
        self.patient_data = patient_data
        #
        # Additional Gui setups
        #
        l = QVBoxLayout(self)
        self.fr_patient = PatientFrame(self)
        l.addWidget(self.fr_patient)
        self.fr_patient.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.fr_patient.setLayout(self.fr_patient.grid_layout)
        self.fr_patient.setMinimumHeight(200)
        self.table = QTableWidget()
        l.addWidget(self.table)
        button_bar = QDialogButtonBox(QDialogButtonBox.Cancel)
        button_bar.rejected.connect(self.close_db)
        # Add a button for clear all selections in the table
        button_bar.addButton(QPushButton("Continue"), QDialogButtonBox.AcceptRole)
        l.addWidget(button_bar)
        button_bar.accepted.connect(self.accept)
        button_bar.rejected.connect(self.reject)
        #
        # Database connection and models
        #
        db_path = './SVoxels/DataBase.sqlite'
        self.db_connect = QSqlDatabase.addDatabase('QSQLITE')
        self.db_connect.setDatabaseName(db_path)
        if not self.db_connect.open():
            logging.error("Database Error: %s" % self.bdConect.lastError().text())
            return
        else:
            logging.info("Dosimetry database opened")
        # ...Table model with patient
        self.patient_model = QSqlTableModel(self, self.db_connect)
        self.patient_model.setTable("Patients")
        self.patient_model.setFilter("Clinical_ID= '{}'".format(self.patient_data['id']))
        self.patient_model.select()
        #   ...map into form
        self.mapper = QDataWidgetMapper()
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.patient_model)

        self.fill_table()
        self.resize(550, 200)
        # ...delegate for the mapper
        dlg = MyDelegate(self)
        self.mapper.setItemDelegate(dlg)
        # Not map the key to make it work properly
        # self.mapper.addMapping(self.tx?, 0)
        self.mapper.addMapping(self.fr_patient.tx_name, 1)
        self.mapper.addMapping(self.fr_patient.tx_id, 2)
        self.mapper.addMapping(self.fr_patient.dt_birth_date, 3)
        self.mapper.addMapping(self.fr_patient.tx_age, 4)
        self.mapper.addMapping(self.fr_patient.cb_sex, 5, "currentIndex")
        self.mapper.addMapping(self.fr_patient.tx_weight, 6)
        self.mapper.addMapping(self.fr_patient.tx_notes, 7)
        if self.patient_model.rowCount() > 0:
            self.mapper.toFirst()
        else:
            # todo: ask if new patient (may be is the database with other ID)
            self.fill_new_patient_data()
            print "lanzar la cuantificacion, quitar tablas de dosimetria"

    def fill_new_patient_data(self):
        SEX = {'F': 'Female', 'M': 'Male', 'O': 'Other'}
        # add a new record...
        self.patient_model.setFilter("")
        row = self.patient_model.rowCount()
        self.patient_model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        # ...fill data...
        n = self.patient_data['name'].split('^')
        n = n[0] + ", " + n[1]
        self.fr_patient.tx_name.setText(n)
        self.fr_patient.tx_id.setText(self.patient_data['id'])
        y = int(self.patient_data['birth_date'][0:4])
        m = int(self.patient_data['birth_date'][4:6])
        d = int(self.patient_data['birth_date'][6:])
        self.fr_patient.dt_birth_date.setDate(QDate(y, m, d))
        self.fr_patient.tx_age.setText(self.patient_data['age'])
        index = self.fr_patient.cb_sex.findText(SEX[self.patient_data['sex']], Qt.MatchFixedString)
        if index >= 0:
            self.fr_patient.cb_sex.setCurrentIndex(index)
        self.fr_patient.tx_weight.setText(self.patient_data['weight'])
        self.submit_record()

    def submit_record(self):
        # ...update record
        if not self.mapper.submit():
            logging.error("Error adding new patient record..." + self.patient_model.lastError().text())
        else:
            logging.info("record updated")

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
                item = QTableWidgetItem(self.VOI_ROLES[column])
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

    def close_db(self):
        print "close database"
        self.db_connect.close()
        self.reject()


class PatientFrame(ui_patient.Ui_Patient, QFrame):
    # Custom signals
    updated = pyqtSignal()
    def __init__(self, parent=None):
        # Invoke parent's method
        super(PatientFrame, self).__init__(parent)
        self.setupUi(self)
        self.bt_edit.clicked.connect(self.enable_controls)

    def enable_controls(self, checked):
        for c in self.children():
            if not isinstance(c, QPushButton) or c.objectName() != "bt_edit":
                c.setEnabled(checked)
        if checked:
            self.bt_edit.setIcon(QIcon(":/Actions/pictures/unlock.svg"))
        else:
            self.bt_edit.setIcon(QIcon(":/Actions/pictures/lock.svg"))
            # update records
            self.updated.emit()

class MyDelegate(QItemDelegate):
    """
        Clase para procesar los datos en los widget. Implementa los metodos
        basicos setEditorData() y setModelData() para representar los datos del
        modelo en los distintos widgets y viceversa.
        Necesario para hacer bien lo de los comboboxes
    """
    def setEditorData(self, editor, index):
        # if isinstance(editor, QComboBox):
        #     data = index.data()
        #     le = editor.lineEdit()
        #     le.setText()
        #     return
        super(MyDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        # if isinstance(editor, QComboBox):
        #     value = (editor.property("currentIndex")).toLongLong()[0] + 1
        #     model.setData(index, value)
        #     return
        super(MyDelegate, self).setModelData(editor, model, index)