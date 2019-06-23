from environs import Env
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

import backtrader as bt
from bt_haslakrx.comminfokrx import CommInfoKRX


class SmaCrossStrategy(bt.SignalStrategy):

    def __init__(self):
        sma_short, sma_long = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma_short, sma_long)
        self.signal_add(bt.SIGNAL_LONG, crossover)


class SmaCross(bt.SignalStrategy):

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print('{}, {}'.format(dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.data.close
        self.sma = bt.ind.SMA(period=20)

    def next(self):
        self.log('Close, {:.2f}'.format(self.dataclose[0]))
        if self.sma > self.data.close:
            self.buy()

        elif self.sma < self.data.close:
            self.sell()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    url = '/'.join([
        env('DB_SERVER'),
        '005930',
        '20180101',
        '20190601',
    ])

    r = requests.get(url)
    df = pd.DataFrame(r.json())
    df = df.T
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index = pd.to_datetime(df.index)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    cerebro.adddata(
        bt.feeds.PandasData(dataname=df)
    )
    cerebro.broker.addcommissioninfo(CommInfoKRX(commission=0.015))
    cerebro.broker.setcash(1e7)

    print('Starting portfolio value: {:.2f}'.format(cerebro.broker.getvalue()))
    cerebro.run()
    print('Final portfolio value: {:.2f}'.format(cerebro.broker.getvalue()))
    cerebro.plot()
