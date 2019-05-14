import sys
from sanic import Sanic
from sanic.response import json
from PyQt5 import (
    QtCore,
    QtWidgets,
)
from form_ui import Ui_Form
from threading import Thread
from multiprocessing import Process


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


def qapp_run():
    qapp = QtWidgets.QApplication([])
    form = MyForm()
    form.ui.label.setText('hi')
    form.show()
    qapp.exec()

app = Sanic()


@app.route('/')
async def test(request):
    return json({'hello': 'world'})


if __name__ == '__main__':
    p = Process(target=qapp_run)
    p.start()
    # p.join()
    app.run(host='0.0.0.0', port=1337, workers=2)