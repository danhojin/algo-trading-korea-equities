from PyQt5 import QtWidgets
from PyQt5 import QAxContainer
from PyQt5 import QtCore
from broker.qapp.register_ui import Ui_Form

import datetime

# KHOPENAPI.KHOpenAPICtrl.1
# KW_CONTROL_CLSID = 'A1574A0D-6BFA-4BD7-9020-DED88711818D'
KW_CONTROL_CLSID = 'KHOPENAPI.KHOpenAPICtrl.1'


def on_receive_real(real_type):
    def _deco(func):
        def wrapper(*args, **kwargs):
            if real_type == args[2]:
                func(*args, **kwargs)
            return
        return wrapper
    return _deco


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
        self.kiwoom.OnReceiveRealData.connect(self.on_real_traded)
        # self.kiwoom.OnReceiveRealData.connect(self.on_real_bidask)

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

    def on_receive_tr_data_cb(self, s_screen_number, s_rq_name,
                              s_tr_code, s_record_name, s_prev_next, *_):
        if s_rq_name == 'BalanceRq':
            total = self.kiwoom.dynamicCall(
                'CommGetData(QString, QString, QString, int, QString',
                s_tr_code, '', s_rq_name, 0, '총평가금액')
            print(total)

    @on_receive_real('주식체결')
    def on_real_traded(self, s_code, s_real_type, s_real_data):
        s_real_data = s_real_data.strip().split()
        deal = dict()
        deal['time'] = (s_real_data[0][:2], s_real_data[0][2:4], s_real_data[0][4:])
        deal['time'] = datetime.time(*map(lambda x: int(x), deal['time']))
        deal['quote'] = float(s_real_data[1])
        deal['cum_volume'] = float(s_real_data[7])

    @on_receive_real('주식호가잔량')
    def on_real_bidask(self, s_code, s_real_type, s_real_data):
        s_real_data = s_real_data.strip().split()
        print('bida', '-'*10, s_real_data[:3])

    def balance_info(self):
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '계좌번호', self.accounts[0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '비밀번호', '')
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '비밀번호입력매체구분', '00')
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)',
                                '조회구분', '1')
        self.kiwoom.dynamicCall('CommRqData(QString, QString, QString, QString)',
                                'BalanceRq', 'opw00018', '0', '8000')
        print('RqCommitted')

    def listening_q(self):
        self.ui.codeLineEdit.setText('1234')
        self.balance_info()

    def button_register_cb(self):
        code = self.ui.codeLineEdit.text()
        # s_screen_no
        # s_code_list
        # s_fid_list
        # s_opt_type 0 for initial reg, 1 for add list
        self.kiwoom.dynamicCall(
            'SetRealReg(QString, QString, QString, QString)',
            # '0150', code, '9001;302;10;13;27;28;41;61', '0'
            '0150', code, '10;13;61', '0'
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
