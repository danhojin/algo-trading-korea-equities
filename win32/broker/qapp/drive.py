from PyQt5 import QtWidgets
from PyQt5 import QAxContainer
from PyQt5 import QtCore
from broker.qapp.register_ui import Ui_Form

KW_CONTROL_CLSID = 'A1574A0D-6BFA-4BD7-9020-DED88711818D'


class RegisterForm(QtWidgets.QWidget):

    def __init__(self, q):
        super().__init__()
        self.q = q
        self.th = ListenSapp(self.listening_q)
        self.kiwoom = QAxContainer.QAxWidget(
            KW_CONTROL_CLSID
        )
        self.kiwoom.OnEventConnect.connect(self.on_event_connect)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.kiwoom.dynamicCall('CommConnect()')
        self.th.start()

    def on_event_connect(self, err):
        if err == 0:
            print('Connected')
        else:
            print(err)

    def listening_q(self):
        while True:
            data = self.q.get()
            print(f'q:{data}')
            self.ui.codeLineEdit.setText(data)


class ListenSapp(QtCore.QThread):

    code = QtCore.pyqtSignal(str)

    def __init__(self, func):
        super().__init__()
        self.func = func

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

def qapp_run(q):
    qapp = QtWidgets.QApplication([])
    register_form = RegisterForm(q)
    register_form.show()
    qapp.exec()