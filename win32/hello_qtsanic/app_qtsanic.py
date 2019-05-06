from PyQt5 import (
    QtCore,
    QtWidgets,
)
from sanic import Sanic
from sanic.response import json

from form_ui import Ui_Form


class MyForm(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.nclicked = 0
        self.ui.button.clicked.connect(self.button_clicked_cb)

    def button_clicked_cb(self):
        self.nclicked += 1
        self.ui.label.setText(str(self.nclicked))


sapp = Sanic()

@sapp.route('/')
async def test(request):
    return json({'hello': 'world'})


class SanicThread(QtCore.QThread):

    def __init__(self, sapp):
        super().__init__()
        self.sapp = sapp

    def run(self):
        self.sapp.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = MyForm()
    Form.ui.label.setText('hi')
    Form.show()
    sanic_thread = SanicThread(sapp)
    sanic_thread.start()
    app.exec()