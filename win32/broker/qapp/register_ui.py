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
        Form.resize(614, 554)
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
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(280, 40, 181, 241))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 1, 1, 1)
        self.totalPurchaseLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.totalPurchaseLabel.setObjectName("totalPurchaseLabel")
        self.gridLayout.addWidget(self.totalPurchaseLabel, 2, 1, 1, 1)
        self.accountComboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.accountComboBox.setObjectName("accountComboBox")
        self.gridLayout.addWidget(self.accountComboBox, 0, 1, 1, 1)
        self.passwordLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.gridLayout.addWidget(self.passwordLineEdit, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(480, 40, 91, 23))
        self.pushButton.setObjectName("pushButton")
        self.loginInfoTextEdit = QtWidgets.QTextEdit(Form)
        self.loginInfoTextEdit.setGeometry(QtCore.QRect(280, 290, 291, 241))
        self.loginInfoTextEdit.setObjectName("loginInfoTextEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.codeLabel.setText(_translate("Form", "Code"))
        self.codeLineEdit.setText(_translate("Form", "066570"))
        self.button_register.setText(_translate("Form", "Register"))
        self.button_unregister.setText(_translate("Form", "Unregister"))
        self.label.setText(_translate("Form", "계좌번호"))
        self.label_2.setText(_translate("Form", "비밀번호"))
        self.label_3.setText(_translate("Form", "전체 매입금액"))
        self.label_4.setText(_translate("Form", "전체 평가금액"))
        self.label_6.setText(_translate("Form", "전체 수익률"))
        self.label_5.setText(_translate("Form", "전체 손익금액"))
        self.label_7.setText(_translate("Form", "TextLabel"))
        self.label_8.setText(_translate("Form", "TextLabel"))
        self.label_9.setText(_translate("Form", "TextLabel"))
        self.totalPurchaseLabel.setText(_translate("Form", "TextLabel"))
        self.pushButton.setText(_translate("Form", "계좌 잔고 요청"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

