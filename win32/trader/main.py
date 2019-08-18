from multiprocessing import Process
from trader.qapp.drive import run as qapp_target


def init():
    qapp_process = Process(target=qapp_target)
    qapp_process.start()