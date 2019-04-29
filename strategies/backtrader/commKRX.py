from datetime import datetime
import backtrader as bt


class CommInfoKRX(bt.CommInfoBase):
    params = (
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_PERC),
        ('percabs', False),  # 0.xx%
    )

    def __init__(self):
        super().__init__()

    def _getcommission(self, size, price, pseudoexec):
        tax = 0.3 * 0.01  # 0.3%
        return (abs(size) * self.p.commission * price if size > 0
                else abs(size) * (tax + self.p.commission) * price)


class DummyOrder(bt.SignalStrategy):
    params = (('pfast', 10), ('pslow', 30),)

    def __init__(self):
        super().__init__()

    def next(self):
        if not self.position:
            self.order = self.buy()
        else:
            self.order = self.sell()


cerebro = bt.Cerebro()
comminfo = CommInfoKRX(commission=0.015)  # Kiwoom HTS, 0.xx%
cerebro.broker.addcommissioninfo(comminfo)

data = bt.feeds.YahooFinanceCSVData(dataname='datas/commKRXdummy.txt',
                                    fromdate=datetime(1995, 1, 3),
                                    todate=datetime(1995, 1, 10))

cerebro.adddata(data)
cerebro.addstrategy(DummyOrder)
cerebro.run()
cerebro.plot()
