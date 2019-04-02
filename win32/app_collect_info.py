from PyQt5 import QtWidgets
from PyQt5 import QAxContainer
from collect_info_ui import Ui_CollectInfo

import itertools
from functools import partial
import models


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
        self.kiwoom = QAxContainer.QAxWidget(
            '{A1574A0D-6BFA-4BD7-9020-DED88711818D}'
        )
        self.kiwoom.OnEventConnect.connect(
            self.kw_on_event_connect
        )
        self.ui = Ui_CollectInfo()
        self.ui.setupUi(self)
        for symbol in KW_MARKET:
            self.ui.button_get_code_list.clicked.connect(
                partial(
                    self.button_get_code_list_clicked,
                    KW_MARKET,
                    symbol)
            )        

        self.kiwoom.dynamicCall('CommConnect()')

    def kw_on_event_connect(self, err_code):
        if err_code == 0:
            print('Connected')
        else:
            print(err_code)

    def button_get_code_list_clicked(self, market, symbol):
        stocks = self.kiwoom.dynamicCall(
            'GetCodeListByMarket(QString)',
            market[symbol]
        )
        stocks = map(lambda x: x.strip(), stocks.split(';'))
        stocks = filter(len, stocks)
        stocks = [{
            'code': code,
            'name': self.kiwoom.dynamicCall(
                'GetMasterCodeName(QString)', code
            ).strip()} for code in stocks
        ]

        models.insert_into_Stock(stocks)

        market_indices = [{
            'symbol': symbol,
            'stock': code,
        } for (symbol, code) in zip(
            itertools.repeat(symbol),
            [s['code'] for s in stocks]
        )]

        models.insert_into_MarketIndex(market_indices)
        print('db session closed')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    collect_info = AppCollectInfo()
    collect_info.show()
    app.exec()