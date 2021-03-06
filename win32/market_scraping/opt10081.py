import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import sqlite3
from dateutil.parser import parse
import datetime
import pandas as pd

TR_REQ_TIME_INTERVAL = 5.0
today = datetime.date.today().strftime('%Y%m%d')
# today = datetime.date(2019, 6, 30)

class Kiwoom(QAxWidget):
    '''
    modified the code from https://wikidocs.net/5756
    '''
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self.conn = sqlite3.connect('krx2.sqlite')
        c = self.conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS prices_daily'
            ' (symbol text, date text, open real, high real,'
            ' low real, close real, volume real)'
        )
        self.conn.commit()
        self.records = []

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)
            if len(self.records) > 2300 or self.remained_data is False:  # 600 * 4
                c = self.conn.cursor()
                c.executemany(
                    'INSERT INTO prices_daily VALUES (?, ?, ?, ?, ?, ?, ?)',
                    self.records
                )
                self.conn.commit()
                print(f'{len(self.records)} records inserted')
                self.records = []
                self.remained_data = False  # break fetch data

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        # data_cnt = 20 if data_cnt > 20 else data_cnt
        symbol = self._comm_get_data(trcode, "", rqname, 0, "종목코드") 
        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
            # print(symbol, date, open, high, low, close, volume)
            self.records.append((
                symbol, parse(date).date().isoformat(), open, high, low, close, volume,
            ))
        print(symbol, data_cnt)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    df_assets = pd.read_csv(
        'market_cap20191114.csv', 
        dtype={'name': str, 'symbol': str, 'cap': int, 'market': str})

    for k, symbol in enumerate(df_assets.iloc[1789:, 1]):  # col 1, symbol
        print(f'{k}: {symbol}')
        # opt10081 TR 요청
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.set_input_value("종목코드", symbol)
        kiwoom.set_input_value("기준일자", today)
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

        while kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            kiwoom.set_input_value("종목코드", symbol)
            kiwoom.set_input_value("기준일자", today)
            kiwoom.set_input_value("수정주가구분", 1)
            kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")