from broker.sapp.drive import sapp_create
from broker.qapp.drive import qapp_run

from multiprocessing import Process, Queue

def init():
    message_queue = dict()
    message_queue['realtime'] = Queue()
    message_queue['code'] = Queue()

    qapp_process = Process(target=qapp_run, args=(message_queue,))
    qapp_process.start()

    sapp = sapp_create(message_queue)
    sapp.run(
        host=sapp.config.HOST,
        port=sapp.config.PORT,
        debug=sapp.config.DEBUG,
    )