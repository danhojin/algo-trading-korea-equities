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
        CollectInfo.resize(400, 300)
        self.button_get_code_list = QtWidgets.QPushButton(CollectInfo)
        self.button_get_code_list.setGeometry(QtCore.QRect(20, 20, 121, 23))
        self.button_get_code_list.setObjectName("button_get_code_list")

        self.retranslateUi(CollectInfo)
        QtCore.QMetaObject.connectSlotsByName(CollectInfo)

    def retranslateUi(self, CollectInfo):
        _translate = QtCore.QCoreApplication.translate
        CollectInfo.setWindowTitle(_translate("CollectInfo", "Collect Info"))
        self.button_get_code_list.setText(_translate("CollectInfo", "GetCodeListByMarket"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CollectInfo = QtWidgets.QWidget()
    ui = Ui_CollectInfo()
    ui.setupUi(CollectInfo)
    CollectInfo.show()
    sys.exit(app.exec_())

