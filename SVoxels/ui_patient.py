# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'patient.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Patient(object):
    def setupUi(self, Patient):
        Patient.setObjectName(_fromUtf8("Patient"))
        Patient.resize(611, 233)
        Patient.setFrameShape(QtGui.QFrame.StyledPanel)
        Patient.setFrameShadow(QtGui.QFrame.Raised)
        self.layoutWidget = QtGui.QWidget(Patient)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 50, 551, 136))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.grid_layout = QtGui.QGridLayout(self.layoutWidget)
        self.grid_layout.setObjectName(_fromUtf8("grid_layout"))
        self.tx_name = QtGui.QLineEdit(self.layoutWidget)
        self.tx_name.setObjectName(_fromUtf8("tx_name"))
        self.grid_layout.addWidget(self.tx_name, 0, 6, 1, 2)
        self.tx_age = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_age.sizePolicy().hasHeightForWidth())
        self.tx_age.setSizePolicy(sizePolicy)
        self.tx_age.setMaximumSize(QtCore.QSize(50, 16777215))
        self.tx_age.setObjectName(_fromUtf8("tx_age"))
        self.grid_layout.addWidget(self.tx_age, 1, 6, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.grid_layout.addWidget(self.label_6, 3, 0, 1, 3)
        self.tx_weight = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_weight.sizePolicy().hasHeightForWidth())
        self.tx_weight.setSizePolicy(sizePolicy)
        self.tx_weight.setMaximumSize(QtCore.QSize(50, 16777215))
        self.tx_weight.setObjectName(_fromUtf8("tx_weight"))
        self.grid_layout.addWidget(self.tx_weight, 3, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.grid_layout.addWidget(self.label_4, 1, 5, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.grid_layout.addWidget(self.label_5, 2, 0, 1, 2)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.grid_layout.addWidget(self.label_3, 1, 0, 1, 2)
        self.cb_sex = QtGui.QComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_sex.sizePolicy().hasHeightForWidth())
        self.cb_sex.setSizePolicy(sizePolicy)
        self.cb_sex.setMaximumSize(QtCore.QSize(100, 16777215))
        self.cb_sex.setObjectName(_fromUtf8("cb_sex"))
        self.cb_sex.addItem(_fromUtf8(""))
        self.cb_sex.addItem(_fromUtf8(""))
        self.cb_sex.addItem(_fromUtf8(""))
        self.grid_layout.addWidget(self.cb_sex, 2, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.grid_layout.addItem(spacerItem, 1, 7, 1, 1)
        self.dt_birth_date = QtGui.QDateEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dt_birth_date.sizePolicy().hasHeightForWidth())
        self.dt_birth_date.setSizePolicy(sizePolicy)
        self.dt_birth_date.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dt_birth_date.setObjectName(_fromUtf8("dt_birth_date"))
        self.grid_layout.addWidget(self.dt_birth_date, 1, 2, 1, 2)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.grid_layout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.grid_layout.addWidget(self.label, 0, 5, 1, 1)
        self.tx_id = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_id.sizePolicy().hasHeightForWidth())
        self.tx_id.setSizePolicy(sizePolicy)
        self.tx_id.setMaximumSize(QtCore.QSize(150, 16777215))
        self.tx_id.setObjectName(_fromUtf8("tx_id"))
        self.grid_layout.addWidget(self.tx_id, 0, 1, 1, 4)

        self.retranslateUi(Patient)
        QtCore.QMetaObject.connectSlotsByName(Patient)

    def retranslateUi(self, Patient):
        Patient.setWindowTitle(_translate("Patient", "Frame", None))
        self.label_6.setText(_translate("Patient", "Weight (kg):", None))
        self.label_4.setText(_translate("Patient", "Age:", None))
        self.label_5.setText(_translate("Patient", "sex:", None))
        self.label_3.setText(_translate("Patient", "Birth date:", None))
        self.cb_sex.setItemText(0, _translate("Patient", "Female", None))
        self.cb_sex.setItemText(1, _translate("Patient", "Male", None))
        self.cb_sex.setItemText(2, _translate("Patient", "Other", None))
        self.label_2.setText(_translate("Patient", "ID:", None))
        self.label.setText(_translate("Patient", "Name:", None))

