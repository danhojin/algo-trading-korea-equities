# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'collect_info_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CollectInfo(object):
    def setupUi(self, CollectInfo):
        CollectInfo.setObjectName("CollectInfo")
        CollectInfo.resize(638, 466)
        self.button_get_code_list = QtWidgets.QPushButton(CollectInfo)
        self.button_get_code_list.setGeometry(QtCore.QRect(420, 20, 191, 23))
        self.button_get_code_list.setObjectName("button_get_code_list")
        self.obs_table = QtWidgets.QTableWidget(CollectInfo)
        self.obs_table.setGeometry(QtCore.QRect(20, 70, 371, 370))
        self.obs_table.setRowCount(10)
        self.obs_table.setObjectName("obs_table")
        self.obs_table.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.obs_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.obs_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.obs_table.setHorizontalHeaderItem(2, item)
        self.verticalLayoutWidget = QtWidgets.QWidget(CollectInfo)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(420, 70, 191, 370))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.obs_line_code = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.obs_line_code.setObjectName("obs_line_code")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.obs_line_code)
        self.verticalLayout.addLayout(self.formLayout)
        self.obs_btn_set_real_reg = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.obs_btn_set_real_reg.setObjectName("obs_btn_set_real_reg")
        self.verticalLayout.addWidget(self.obs_btn_set_real_reg)
        self.obs_btn_set_real_remove = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.obs_btn_set_real_remove.setObjectName("obs_btn_set_real_remove")
        self.verticalLayout.addWidget(self.obs_btn_set_real_remove)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(CollectInfo)
        QtCore.QMetaObject.connectSlotsByName(CollectInfo)

    def retranslateUi(self, CollectInfo):
        _translate = QtCore.QCoreApplication.translate
        CollectInfo.setWindowTitle(_translate("CollectInfo", "Collect Info"))
        self.button_get_code_list.setText(_translate("CollectInfo", "GetCodeListByMarket"))
        item = self.obs_table.horizontalHeaderItem(0)
        item.setText(_translate("CollectInfo", "이벤트시간"))
        item = self.obs_table.horizontalHeaderItem(1)
        item.setText(_translate("CollectInfo", "체결가"))
        item = self.obs_table.horizontalHeaderItem(2)
        item.setText(_translate("CollectInfo", "누적거래량"))
        self.label.setText(_translate("CollectInfo", "Code"))
        self.obs_btn_set_real_reg.setText(_translate("CollectInfo", "SetRealReg"))
        self.obs_btn_set_real_remove.setText(_translate("CollectInfo", "SetRealRemove"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CollectInfo = QtWidgets.QWidget()
    ui = Ui_CollectInfo()
    ui.setupUi(CollectInfo)
    CollectInfo.show()
    sys.exit(app.exec_())

