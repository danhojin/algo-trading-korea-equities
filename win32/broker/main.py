from broker.sapp.drive import sapp_create
from broker.qapp.drive import qapp_run

from multiprocessing import Process, Queue

def init():
    q = Queue()

    p = Process(target=qapp_run, args=(q,))
    p.start()

    sapp = sapp_create(q)
    sapp.run(
        host=sapp.config.HOST,
        port=sapp.config.PORT,
        debug=sapp.config.DEBUG,
    )