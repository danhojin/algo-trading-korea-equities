# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.formLayoutWidget = QtWidgets.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(50, 40, 181, 31))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.codeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.codeLabel.setObjectName("codeLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.codeLabel)
        self.codeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.codeLineEdit.setObjectName("codeLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.codeLineEdit)
        self.button_register = QtWidgets.QPushButton(Form)
        self.button_register.setGeometry(QtCore.QRect(54, 80, 81, 23))
        self.button_register.setObjectName("button_register")
        self.button_unregister = QtWidgets.QPushButton(Form)
        self.button_unregister.setGeometry(QtCore.QRect(150, 80, 75, 23))
        self.button_unregister.setObjectName("button_unregister")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.codeLabel.setText(_translate("Form", "Code"))
        self.codeLineEdit.setText(_translate("Form", "066570"))
        self.button_register.setText(_translate("Form", "Register"))
        self.button_unregister.setText(_translate("Form", "Unregister"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

