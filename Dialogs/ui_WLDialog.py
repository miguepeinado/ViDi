# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WLDialog.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 266)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 381, 240))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sld_center = QtGui.QSlider(self.layoutWidget)
        self.sld_center.setOrientation(QtCore.Qt.Horizontal)
        self.sld_center.setObjectName(_fromUtf8("sld_center"))
        self.gridLayout.addWidget(self.sld_center, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.sld_min_value = QtGui.QSlider(self.layoutWidget)
        self.sld_min_value.setEnabled(False)
        self.sld_min_value.setOrientation(QtCore.Qt.Horizontal)
        self.sld_min_value.setObjectName(_fromUtf8("sld_min_value"))
        self.gridLayout.addWidget(self.sld_min_value, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spb_center = QtGui.QSpinBox(self.layoutWidget)
        self.spb_center.setMinimumSize(QtCore.QSize(80, 0))
        self.spb_center.setObjectName(_fromUtf8("spb_center"))
        self.gridLayout.addWidget(self.spb_center, 0, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.sld_alpha = QtGui.QSlider(self.layoutWidget)
        self.sld_alpha.setEnabled(False)
        self.sld_alpha.setMaximum(255)
        self.sld_alpha.setOrientation(QtCore.Qt.Horizontal)
        self.sld_alpha.setObjectName(_fromUtf8("sld_alpha"))
        self.gridLayout.addWidget(self.sld_alpha, 7, 1, 1, 1)
        self.sld_window = QtGui.QSlider(self.layoutWidget)
        self.sld_window.setOrientation(QtCore.Qt.Horizontal)
        self.sld_window.setObjectName(_fromUtf8("sld_window"))
        self.gridLayout.addWidget(self.sld_window, 1, 1, 1, 1)
        self.spb_window = QtGui.QSpinBox(self.layoutWidget)
        self.spb_window.setMinimumSize(QtCore.QSize(80, 0))
        self.spb_window.setObjectName(_fromUtf8("spb_window"))
        self.gridLayout.addWidget(self.spb_window, 1, 2, 1, 1)
        self.sld_max_value = QtGui.QSlider(self.layoutWidget)
        self.sld_max_value.setEnabled(False)
        self.sld_max_value.setOrientation(QtCore.Qt.Horizontal)
        self.sld_max_value.setObjectName(_fromUtf8("sld_max_value"))
        self.gridLayout.addWidget(self.sld_max_value, 6, 1, 1, 1)
        self.spb_min_value = QtGui.QSpinBox(self.layoutWidget)
        self.spb_min_value.setEnabled(False)
        self.spb_min_value.setMinimumSize(QtCore.QSize(80, 0))
        self.spb_min_value.setObjectName(_fromUtf8("spb_min_value"))
        self.gridLayout.addWidget(self.spb_min_value, 4, 2, 1, 1)
        self.spb_max_value = QtGui.QSpinBox(self.layoutWidget)
        self.spb_max_value.setEnabled(False)
        self.spb_max_value.setMinimumSize(QtCore.QSize(80, 0))
        self.spb_max_value.setObjectName(_fromUtf8("spb_max_value"))
        self.gridLayout.addWidget(self.spb_max_value, 6, 2, 1, 1)
        self.spb_alpha = QtGui.QSpinBox(self.layoutWidget)
        self.spb_alpha.setEnabled(False)
        self.spb_alpha.setMinimumSize(QtCore.QSize(80, 0))
        self.spb_alpha.setMaximum(255)
        self.spb_alpha.setObjectName(_fromUtf8("spb_alpha"))
        self.gridLayout.addWidget(self.spb_alpha, 7, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.lb_overlay = QtGui.QLabel(self.layoutWidget)
        self.lb_overlay.setEnabled(False)
        self.lb_overlay.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_overlay.setObjectName(_fromUtf8("lb_overlay"))
        self.gridLayout.addWidget(self.lb_overlay, 2, 0, 1, 3)
        self.line = QtGui.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 3, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.label_4.setBuddy(self.sld_min_value)
        self.label.setBuddy(self.sld_center)
        self.label_2.setBuddy(self.sld_window)
        self.label_5.setBuddy(self.sld_alpha)
        self.label_3.setBuddy(self.sld_max_value)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("close_db()")), Dialog.reject)
        QtCore.QObject.connect(self.sld_center, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spb_center.setValue)
        QtCore.QObject.connect(self.spb_center, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sld_center.setValue)
        QtCore.QObject.connect(self.sld_window, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spb_window.setValue)
        QtCore.QObject.connect(self.spb_window, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sld_window.setValue)
        QtCore.QObject.connect(self.sld_min_value, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spb_min_value.setValue)
        QtCore.QObject.connect(self.spb_min_value, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sld_min_value.setValue)
        QtCore.QObject.connect(self.sld_max_value, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spb_max_value.setValue)
        QtCore.QObject.connect(self.spb_max_value, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sld_max_value.setValue)
        QtCore.QObject.connect(self.sld_alpha, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spb_alpha.setValue)
        QtCore.QObject.connect(self.spb_alpha, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sld_alpha.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_4.setText(_translate("Dialog", "min. value", None))
        self.label.setText(_translate("Dialog", "Center", None))
        self.label_2.setText(_translate("Dialog", "Window", None))
        self.label_5.setText(_translate("Dialog", "alpha", None))
        self.label_3.setText(_translate("Dialog", "max. value", None))
        self.lb_overlay.setText(_translate("Dialog", "Overlay", None))

