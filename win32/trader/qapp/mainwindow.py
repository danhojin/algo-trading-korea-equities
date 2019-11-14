# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 863)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cbox_autorun = QtWidgets.QCheckBox(self.tab)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cbox_autorun.setFont(font)
        self.cbox_autorun.setObjectName("cbox_autorun")
        self.horizontalLayout.addWidget(self.cbox_autorun)
        self.but_balance = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.but_balance.setFont(font)
        self.but_balance.setObjectName("but_balance")
        self.horizontalLayout.addWidget(self.but_balance)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lcd_clock = QtWidgets.QLCDNumber(self.tab)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lcd_clock.setFont(font)
        self.lcd_clock.setDigitCount(8)
        self.lcd_clock.setObjectName("lcd_clock")
        self.horizontalLayout.addWidget(self.lcd_clock)
        self.but_draw_actions = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.but_draw_actions.setFont(font)
        self.but_draw_actions.setObjectName("but_draw_actions")
        self.horizontalLayout.addWidget(self.but_draw_actions)
        self.but_send_orders = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.but_send_orders.setFont(font)
        self.but_send_orders.setObjectName("but_send_orders")
        self.horizontalLayout.addWidget(self.but_send_orders)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.balance_table = QtWidgets.QTableView(self.groupBox)
        self.balance_table.setObjectName("balance_table")
        self.verticalLayout.addWidget(self.balance_table)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.combo_asset_state = QtWidgets.QComboBox(self.groupBox_2)
        self.combo_asset_state.setEnabled(True)
        self.combo_asset_state.setObjectName("combo_asset_state")
        self.horizontalLayout_2.addWidget(self.combo_asset_state)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.but_add_asset = QtWidgets.QPushButton(self.groupBox_2)
        self.but_add_asset.setEnabled(False)
        self.but_add_asset.setObjectName("but_add_asset")
        self.horizontalLayout_2.addWidget(self.but_add_asset)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.order_table = QtWidgets.QTableView(self.groupBox_2)
        self.order_table.setObjectName("order_table")
        self.verticalLayout_4.addWidget(self.order_table)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cbox_autorun.setText(_translate("MainWindow", "AutoRun"))
        self.but_balance.setText(_translate("MainWindow", "ACCOUNT"))
        self.but_draw_actions.setText(_translate("MainWindow", "Draw Actions"))
        self.but_send_orders.setText(_translate("MainWindow", "Send Orders"))
        self.groupBox.setTitle(_translate("MainWindow", "Balance"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Assets"))
        self.but_add_asset.setText(_translate("MainWindow", "add asset"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Order"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

