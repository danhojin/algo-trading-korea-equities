from PyQt5 import QtWidgets
from PyQt5 import QAxContainer
from PyQt5 import QtCore
from hello_expert_ui import Ui_Form
import time


class AppHelloExpert(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.expert = QAxContainer.QAxWidget(
            'ITGExpertCtl.ITGExpertCtlCtrl.1'
            # '{08E39D09-206D-43D1-AC78-D1AE3635A4E9}'
        )
        self.expert.ReceiveData.connect(self.receive_data_cb)
        self.expert_account = QAxContainer.QAxWidget(
            'ITGExpertCtl.ITGExpertCtlCtrl.1'
        )

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.account_but_get.clicked.connect(
            self.account_but_get_cb
        )

    def account_but_get_cb(self):
        self.expert.dynamicCall('SetSingleData(int, QString)', 0, 'J')
        self.expert.dynamicCall('SetSingleData(int, QString)', 1, '005930')
        self.expert.dynamicCall('RequestData(QString)', 'SCP')
        n_accounts = self.expert_account.dynamicCall('GetAccountCount()')
        print(f'no. accounts: {n_accounts}')

    def receive_data_cb(self, *args):
        v = self.expert.dynamicCall('GetSingleData(int, int)', 11, 0)
        print(v)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    hello_expert = AppHelloExpert()
    hello_expert.show()
    app.exec()