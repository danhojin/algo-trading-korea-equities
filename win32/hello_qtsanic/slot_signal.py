from PyQt5 import (
    QtWidgets,
    QtCore,
)

from slot_signal_ui import Ui_Form


QtCore.pyqtSlot(str)
def emit_but_slot(name):
    print(f'emitted: {name}')


class MyForm(QtWidgets.QWidget):
    my_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.emit_but.clicked.connect(self.emit_but_cb)
        self.th = MyThread()
        self.my_signal.connect(self.th.emit_but_slot)

    def emit_but_cb(self):
        self.my_signal.emit('abc')

class MyThread(QtCore.QThread):

    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot(str)
    def emit_but_slot(self, name):
        print(f'another thread: {name}')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    form = MyForm()
    form.my_signal.connect(emit_but_slot)
    form.show()
    app.exec()