from PyQt5 import QtWidgets
from PyQt5 import QAxContainer
from PyQt5 import QtCore
from broker.qapp.register_ui import Ui_Form

# KHOPENAPI.KHOpenAPICtrl.1
KW_CONTROL_CLSID = 'A1574A0D-6BFA-4BD7-9020-DED88711818D'


class RegisterForm(QtWidgets.QWidget):

    def __init__(self, q):
        super().__init__()
        self.q = q
        self.th = ListenSappWorker(self.q)
        self.kiwoom = QAxContainer.QAxWidget(
            KW_CONTROL_CLSID
        )
        self.kiwoom.OnEventConnect.connect(self.on_event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.on_receive_tr_data_cb)
        self.kiwoom.OnReceiveRealData.connect(self.on_receive_real_data_cb)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.button_register.clicked.connect(self.button_register_cb)

        self.kiwoom.dynamicCall('CommConnect()')
        self.th.start()
        self.th.code.connect(self.listening_q)

    def on_event_connect(self, err):
        if err == 0:
            print('Connected')
            user = self.kiwoom.dynamicCall('GetLoginInfo(QString)', 'USER_ID')
            accounts = self.kiwoom.dynamicCall('GetLoginInfo(QString)', 'ACCLIST')
            print(user, accounts)
            self.accounts = accounts.split(';')
            self.balance_info()
        else:
            print(err)

    def on_receive_tr_data_cb(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == 'BalanceRq':
            total = self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString', trcode, '', rqname, 0, '총평가금액')
            print(total)

    def on_receive_real_data_cb(self, s_code, s_real_type, s_real_data):
        if s_real_type == '주식체결':
            s_real_data = s_real_data.strip().split()
            print('traded: ', s_real_data)
        elif s_real_type == '주식호가잔량':
            s_real_data = s_real_data.strip().split()
            print('bid/ask: ', s_real_data)
            

    def balance_info(self):
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '계좌번호', self.accounts[0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '비밀번호', '')
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '비밀번호입력매체구분', '00')
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '조회구분', '1')
        self.kiwoom.dynamicCall('CommRqData(QString, QString, QString, QString)', 'BalanceRq', 'opw00018', '0', '8000')
        print('RqCommitted')

    def listening_q(self):
        self.ui.codeLineEdit.setText('1234')
        self.balance_info()

    def button_register_cb(self):
        code = self.ui.codeLineEdit.text()
        self.kiwoom.dynamicCall(
            'SetRealReg(QString, QString, QString, QString)',
            '0150', code, '9001;302;10;13;27;28;41;61', '0'
        )


class ListenSappWorker(QtCore.QThread):

    code = QtCore.pyqtSignal(str)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            data = self.q.get()
            print(f'q:{data}')
            self.code.emit('f{data}')


def qapp_run(q):
    qapp = QtWidgets.QApplication([])
    register_form = RegisterForm(q)
    register_form.show()
    qapp.exec()