from datetime import datetime
import backtrader as bt


class CommInfoKRX(bt.CommInfoBase):
    params = (
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_PERC),
        ('percabs', False),  # take percentage
    )

    def __init__(self):
        super().__init__()

    def _getcommission(self, size, price, pseudoexec):
        tax = 0.3 * 0.01  # 0.3%
        tax += 0.2 * 0.01 # additional noise penalty
        return (abs(size) * self.p.commission * price if size > 0
                else abs(size) * (tax + self.p.commission) * price)


if __name__ == '__main__':
    class DummyOrder(bt.SignalStrategy):

        def next(self):
            if not self.position:
                self.order = self.buy()
            else:
                self.order = self.sell()

    cerebro = bt.Cerebro()
    comminfo = CommInfoKRX(commission=0.015)  # Kiwoom HTS, 0.015%
    cerebro.broker.addcommissioninfo(comminfo)

    data = bt.feeds.YahooFinanceCSVData(dataname='datas/commKRXdummy.txt',
                                        fromdate=datetime(1995, 1, 3),
                                        todate=datetime(1995, 1, 10))

    cerebro.adddata(data)
    cerebro.addstrategy(DummyOrder)
    cerebro.run()
    cerebro.plot()
