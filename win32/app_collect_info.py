from PyQt5 import QtWidgets
from PyQt5 import QAxContainer
from PyQt5 import QtCore
from collect_info_ui import Ui_CollectInfo

from collections import deque
from collections import OrderedDict
from collections import defaultdict
import itertools
from datetime import datetime
from functools import partial

import json
from kafka import KafkaProducer
import db
from settings import KW_CONTROL_CLSID, KAFKA_BOOTSTRAP_SERVER

import pandas as pd


KW_MARKET = {
    'FLOOR': '0',  # 장내
    'KOSDAQ': '10',
    'ELW': '3',
    'ETF': '8',
    'KONEX': '50',
    'MUTUAL_FUNDS': '4',
    'WARRANTY': '5',  # 신주인수권
    'REITS': '6',  # 리츠
    'HAIER': '9',  # 하이얼펀드
    'K-OTC': '30',
}

class AppCollectInfo(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.code_funcs = defaultdict(list)
        self.kiwoom = QAxContainer.QAxWidget(
            KW_CONTROL_CLSID
        )
        self.kiwoom.OnEventConnect.connect(self.on_event_connect)
        self.kiwoom.OnReceiveRealData.connect(self.on_receive_real_data)

        self.ui = Ui_CollectInfo()
        self.ui.setupUi(self)
        for symbol in KW_MARKET:
            self.ui.get1_but_codes.clicked.connect(
                partial(
                    self.get1_but_codes_clicked_cb,
                    KW_MARKET,
                    symbol)
            )
        self.ui.obs1_but_watching.clicked.connect(
            self.obs1_but_watching_clicked_cb
        )
        self.ui.obs1_but_stop.clicked.connect(
            self.obs1_but_stop_clicked_cb
        )
        self.ui.obs2_but_set_codes.clicked.connect(
            self.obs2_but_set_codes_cb
        )
        self.ui.obs2_but_watching.clicked.connect(
            self.obs2_but_watching_clicked_cb
        )

        self.obs1_cells = deque(maxlen=10)
        self.obs2_cells = deque(maxlen=100)
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.kiwoom.dynamicCall('CommConnect()')

    def on_receive_real_data(self, s_code, s_real_type, s_real_data):
        if s_real_type == '주식체결':
            '''
            now = datetime.now().strftime('%H:%M:%S')
            price = self.kiwoom.dynamicCall(
                'GetCommRealData(QString, int)',
                s_code,
                10
            )
            cum_volume = self.kiwoom.dynamicCall(
                'GetCommRealData(QString, int)',
                s_code,
                13
            )
            '''
            s_real_data = s_real_data.strip().split()
            data = OrderedDict()
            data['event'] = s_real_data[0]
            data['price'] = s_real_data[1]
            data['cum_volume'] = s_real_data[7]
            for func in self.code_funcs[s_code]:
                func(**data)

    def obs1_but_watching_clicked_cb(self):
        code = self.ui.obs1_line_code.text()
        if code not in self.code_funcs:
            self.kiwoom.dynamicCall(
                "SetRealReg(QString, QString, QString, QString)",
                "0150", code, "9001;10;13;20", "1")
        self.code_funcs[code].append(self.obs1_code_func)

    def obs1_code_func(self, **data):
        self.obs1_cells.append([v for v in data.values()])
        
        for i, d in enumerate(self.obs1_cells):
            for j, v in enumerate(d):
                self.ui.obs1_table.setItem(i, j, QtWidgets.QTableWidgetItem(v))

        self.kafka_producer.send('StockTradingPrice', data)

    def obs1_but_stop_clicked_cb(self):
        self.kiwoom.dynamicCall(
            'SetRealRemove(QString, QString)',
            'All', 'All'
        )

    def obs2_but_set_codes_cb(self):
        df = pd.read_csv(
            '../scraps_markets/list_kospi200.csv',
            dtype={'code': str},
        )
        df_obs2 = df.sample(n=100)
        # iteration over rows
        # see. https://medium.com/@rtjeannier/pandas-101-cont-9d061cb73bfc
        for i, (_, row) in enumerate(df_obs2.iterrows()):
            # print(i, row['code'], row['name'])
            self.code_funcs[row['code']].append(partial(self.obs2_code_func, i_table=i))
            self.ui.obs2_table.setItem(i, 0, QtWidgets.QTableWidgetItem(row['code']))
            self.ui.obs2_table.setItem(i, 1, QtWidgets.QTableWidgetItem(row['name']))

    def obs2_code_func(self, **data):
        self.ui.obs2_table.setItem(data['i_table'], 2, QtWidgets.QTableWidgetItem(data['event']))
        self.ui.obs2_table.setItem(data['i_table'], 3, QtWidgets.QTableWidgetItem(data['price']))
        self.kafka_producer.send('StockTradingPrice', data)

    def obs2_but_watching_clicked_cb(self):
        n_rows = self.ui.obs2_table.rowCount()
        codes = []
        for i in range(n_rows):
            try:
                codes.append(self.ui.obs2_table.item(i, 0).text())
            except AttributeError:
                break
        for code in codes:
            self.kiwoom.dynamicCall(
                'SetRealReg(QString, QString, QString, QString)',
                '0160', code, '9001;20;10;13', '1'
            )

    def on_event_connect(self, err_code):
        if err_code == 0:
            print('Connected')
        else:
            print(err_code)

    def get1_but_codes_clicked_cb(self, market, symbol):
        assets = self.kiwoom.dynamicCall(
            'GetCodeListByMarket(QString)',
            market[symbol]
        )
        assets = map(lambda x: x.strip(), assets.split(';'))
        assets = filter(len, assets)
        assets = [{
            'code': code,
            'name': self.kiwoom.dynamicCall(
                'GetMasterCodeName(QString)', code
            ).strip()} for code in assets
        ]

        db.insert_into_Asset(assets)

        market_indices = [{
            'symbol': symbol,
            'asset': code,
        } for (symbol, code) in zip(
            itertools.repeat(symbol),
            [s['code'] for s in assets]
        )]

        db.insert_into_MarketIndex(market_indices)
        print('db session closed')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    collect_info = AppCollectInfo()
    collect_info.show()
    app.exec()