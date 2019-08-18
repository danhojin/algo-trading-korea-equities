# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\addassetdialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(238, 145)
        self.formLayout_2 = QtWidgets.QFormLayout(Dialog)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.le_symbol = QtWidgets.QLineEdit(Dialog)
        self.le_symbol.setObjectName("le_symbol")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_symbol)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.sb_max_shares = QtWidgets.QSpinBox(Dialog)
        self.sb_max_shares.setMaximum(1000)
        self.sb_max_shares.setObjectName("sb_max_shares")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sb_max_shares)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.sb_position_size = QtWidgets.QSpinBox(Dialog)
        self.sb_position_size.setMaximum(100)
        self.sb_position_size.setObjectName("sb_position_size")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sb_position_size)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.combo_tactic = QtWidgets.QComboBox(Dialog)
        self.combo_tactic.setObjectName("combo_tactic")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.combo_tactic)
        self.but_ok = QtWidgets.QDialogButtonBox(Dialog)
        self.but_ok.setOrientation(QtCore.Qt.Horizontal)
        self.but_ok.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.but_ok.setObjectName("but_ok")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.but_ok)

        self.retranslateUi(Dialog)
        self.but_ok.accepted.connect(Dialog.accept)
        self.but_ok.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "symbol"))
        self.label_4.setText(_translate("Dialog", "max shares"))
        self.label_2.setText(_translate("Dialog", "position size"))
        self.label_3.setText(_translate("Dialog", "tactic"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

