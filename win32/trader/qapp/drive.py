from collections import namedtuple, OrderedDict, defaultdict
from functools import partial
from itertools import product
from environs import Env
import datetime
import requests
import json
import time

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QAxContainer

from pony import orm
import trader.qapp.db.model as db
from trader.qapp.mainwindow import Ui_MainWindow
from trader.qapp.addassetdialog import Ui_Dialog

# KW_CONTROL_CLSID = 'A1574A0D-6BFA-4BD7-9020-DED88711818D'
KW_CONTROL_CLSID = 'KHOPENAPI.KHOpenAPICtrl.1'
TR_RQ_SLEEP = 300
TODAY = datetime.date.today()

def on_receive_tr(rq_name):
    def _deco(func):
        def wrapper(*args, **kwargs):
            if rq_name == args[2]:
                func(*args, **kwargs)
            return
        return wrapper
    return _deco


def on_receive_real(real_type):
    def _deco(func):
        def wrapper(*args, **kwargs):
            if real_type == args[2]:
                func(*args, **kwargs)
            return
        return wrapper
    return _deco


class ProxyModel(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_active_assets = False

    def headerData(self, section, orientation, role):
        return self.sourceModel().headerData(section, orientation, role)

    @QtCore.pyqtSlot(str)
    def asset_state(self, asset_state):
        if asset_state == 'all':
            self.view_active_assets = False
        else:  # active assets only
            self.view_active_assets = True
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        index_symbol = model.index(source_row, 0, source_parent)
        if self.view_active_assets:
            if model.item(source_row, 0).checkState():
                return True
            return False
        return True


class MainWindow(QtWidgets.QMainWindow):
    balance_signal = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Supress the following warning on close
        # QBasicTimer::start: QBasicTimer can only be used with
        # threads started with QThread
        self.env = Env()
        self.env.read_env()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.balance_signal.connect(self.update_balance)

        self.balance_columns = OrderedDict({
            'capital': 'capital',
            'security': 'security',
            'cash': 'cash',
            'buy': 'buy',
            'sell': 'sell',
        })
        self.balance_rows = OrderedDict({
            'day2': 'D+2',
            'increment_e': 'cash increment(E)',
            'increment_r': 'cash increment(R)',
            'close2': 'D+2 close',
        })
        self.order_columns = OrderedDict({
            'symbol': 'symbol',
            'sell_buy': 'sell-buy',
            'security': 'security',
            'profit': 'profit\n(sell-buy)+security',
            'latest_entry': 'latest\nentry',
            'num_shares': 'num\nshares',
            'max_shares': 'max\nshares',
            'tactic': 'tactic',
            'quote': 'quote',
            'daily_return': 'daily\nreturn',
            'position_size': 'position\nsize',
            'action': 'action',
            'action_remained': 'action\nremained',
        })
        self.order_col = {k: v for (v, k)
                          in enumerate(self.order_columns.keys())}
        self.col = {
            'balance': {
                k: v for (v, k) in enumerate(self.balance_columns.keys())},
            'order': {
                k: v for (v, k) in enumerate(self.order_columns.keys())},
        }
        self.row = {
            'balance': {
                k: v for (v, k) in enumerate(self.balance_rows.keys())},
        }
        self.model = {
            'balance': self.create_balance_model(),
            'order': self.create_order_model(),
        }

        self.init_model_items()

        # self.assets, self.tactics = self.get_assets_tactics()
        self.row['order'], self.tactics = self.get_assets_tactics()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # basic setup for ui components
        self.ui.combo_asset_state.addItems(['all', 'active'])
        self.ui.cbox_autorun.stateChanged.connect(
            self.cbox_autorun_state_changed)
        self.autorun_timer = None
        self.ui.but_balance.clicked.connect(self.on_but_balance)
        self.ui.but_add_asset.clicked.connect(self.on_but_add_asset)
        self.ui.but_draw_actions.clicked.connect(self.on_but_draw_actions)
        self.ui.but_send_orders.clicked.connect(self.on_but_send_orders)

        self.view = {
            'balance': self.ui.balance_table,
            'order': self.ui.order_table,
        }
        self.view['balance'].setModel(self.model['balance'])
        self.proxy_model = ProxyModel()
        self.proxy_model.setSourceModel(self.model['order'])
        self.ui.combo_asset_state.currentTextChanged.connect(
            self.proxy_model.asset_state)
        self.view['order'].setModel(self.proxy_model)
        self.view['order'].horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.view['order'].sortByColumn(0, Qt.AscendingOrder)
        self.view['order'].setSortingEnabled(True)

        # lcd_clock
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.lcd_clock_update)
        self.timer.start(1000)
        self._lcd_clock_blink = 0
        self.lcd_clock_update()

        self.asset_symbols = set()
        for symbol in self.row['order'].keys():
            self.asset_symbols.add(symbol)

        # kiwoom
        self.candle_data = dict()
        self.kiwoom = QAxContainer.QAxWidget(KW_CONTROL_CLSID)
        self.kiwoom.OnEventConnect.connect(self.on_event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.balance_day2)
        self.kiwoom.OnReceiveTrData.connect(self.balance_close2)
        self.kiwoom.OnReceiveTrData.connect(self.ohlcv_draw_actions)
        self.kiwoom.OnReceiveTrData.connect(self.send_order)
        self.kiwoom.OnReceiveMsg.connect(self.send_order_msg)
        self.kiwoom.OnReceiveChejanData.connect(self.send_order_chejan_data)
        self.kiwoom.OnReceiveRealData.connect(self.quote_stream)
        self.kiwoom.dynamicCall('CommConnect()')

    def cbox_autorun_state_changed(self):
        if self.ui.cbox_autorun.isChecked():
            print('autorun checked')
            self.ui.but_draw_actions.setEnabled(False)
            self.ui.but_send_orders.setEnabled(False)
            t_run = QtCore.QTime(15, 22, 0)
            t_now = QtCore.QTime.currentTime()
            t_sec = (t_run.hour() - t_now.hour()) * 3600
            t_sec += (t_run.minute() - t_now.minute()) * 60
            t_sec += (t_run.second() - t_now.second())
            t_sec = max(t_sec, 10)
            print(t_sec)
            if self.autorun_timer:
                self.autorun_timer.stop()
                self.autorun_timer.deleteLater()
            self.autorun_timer = QtCore.QTimer()
            self.autorun_timer.timeout.connect(self.autorun_process)
            self.autorun_timer.setSingleShot(True)
            self.autorun_timer.start(t_sec * 1000)
        else:
            print('autorun unchecked')
            self.ui.but_draw_actions.setEnabled(True)
            self.ui.but_send_orders.setEnabled(True)
            if self.autorun_timer:
                self.autorun_timer.stop()
                self.autorun_timer.deleteLater()
            self.autorun_timer = None

    def autorun_process(self):
        # self.on_but_balance()
        self.on_but_draw_actions()
        self.on_but_send_orders()

    def get_assets_tactics(self):
        tactics = {
            tactic.name: tactic.id for tactic in db.Tactic.select()}
        col = self.col['order']
        assets = []
        for asset in db.Asset.select():
            assets.insert(0, {'symbol': asset.symbol})
            self.model['order'].insertRow(0)
            for j in range(len(self.col['order'])):
                item = QtGui.QStandardItem()
                item.setData('0', Qt.DisplayRole)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                self.model['order'].setItem(0, j, item)

            item = self.model['order'].item(0, col['symbol'])
            item.setData(asset.symbol, Qt.DisplayRole)
            item.setCheckable(True)
            if asset.is_active == True:
                item.setCheckState(Qt.Checked)
            query = db.Entry.select(lambda x: x.asset == asset) \
                .order_by(orm.desc(db.Entry.date))
            query = list(query)
            if query:
                latest_entry = query[0].date
                sell_buy = sum([-entry.price * entry.order for
                                entry in query])
            else:
                latest_entry = datetime.date(1900, 1, 1)
                sell_buy = 0
            self.set_model_data(
                'order', 0, col['sell_buy'], int(sell_buy))
            item = self.model['order'].item(0, col['latest_entry'])
            item.setData(latest_entry.isoformat(), Qt.DisplayRole)
            item = self.model['order'].item(0, col['tactic'])
            item.setData(asset.tactic.name, Qt.DisplayRole)
            self.set_model_data('order', 0, col['num_shares'],
                                asset.num_shares)
            self.set_model_data('order', 0, col['max_shares'],
                                asset.max_shares)
            self.set_model_data('order', 0, col['position_size'],
                                asset.position_size)

        for row, asset in enumerate(assets):
            asset['row'] = row

        order_row = {
            asset['symbol']: row for row, asset in enumerate(assets)}

        return order_row, tactics

    def create_balance_model(self):
        model = QtGui.QStandardItemModel(
            len(self.balance_rows),
            len(self.balance_columns))
        model.setHorizontalHeaderLabels(self.balance_columns.values())
        model.setVerticalHeaderLabels(self.balance_rows.values())
        return model

    def create_order_model(self):
        model = QtGui.QStandardItemModel(
            0,
            len(self.order_columns))
        model.setHorizontalHeaderLabels(self.order_columns.values())
        return model

    def init_model_items(self):
        indexes = list((r, c) for r, c in product(
            ['day2', 'close2'], ['capital', 'security', 'cash']))
        indexes += list((r, c) for r, c in product(
            ['increment_e', 'increment_r'], ['cash', 'buy', 'sell']))
        row, col = self.row['balance'], self.col['balance']
        for (r, c) in indexes:
            item = QtGui.QStandardItem()
            item.setData('0', Qt.DisplayRole)
            item.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
            self.model['balance'].setItem(
                row[r], col[c], item)

    def get_model_data(self, model, row, col):
        item = self.model[model].item(row, col)
        return int(float(item.data(Qt.DisplayRole).replace(',', '')))

    def set_model_data(self, model, row, col, value):
        item = self.model[model].item(row, col)
        item.setData('{:,}'.format(value), Qt.DisplayRole)

    def kiwoom_set_input_values(self, kvs):
        for k, v in kvs.items():
            self.kiwoom.dynamicCall(
                'SetInputValue(QString, QString)',
                k, v)

    def kiwoom_comm_rq_data(self, s_rq_name, s_tr_code,
                            n_prev_next, s_screen_no):
        QtCore.QThread.msleep(TR_RQ_SLEEP)
        status = self.kiwoom.dynamicCall(
            'CommRqData(QString, QString, int, QString)',
            s_rq_name, s_tr_code, n_prev_next, s_screen_no)

        if status:  # check error
            print('[Error] CommRqData', status)
        self.kiwoom_tr_event_loop = QtCore.QEventLoop()
        self.kiwoom_tr_event_loop.exec()
        return status

    def kiwoom_get_comm_data(self, s_tr_code, s_record_name,
                             n_index, s_item_name):
        value = self.kiwoom.dynamicCall(
            'GetCommData(QString, QString, int, QString)',
            s_tr_code, s_record_name, n_index, s_item_name)
        return value.strip()

    def kiwoom_get_chejan_data(self, n_fids):
        values = []
        for n_fid in n_fids:
            value = self.kiwoom.dynamicCall(
                'GetChejanData(int)', n_fid)
            values.append(value.strip())
        return values

    def kiwoom_send_order(self, s_rq_name, s_screen_no, s_acc_no,
                          n_order_type, s_code, n_qty,
                          n_price, s_hoga, s_org_no):
        QtCore.QThread.msleep(TR_RQ_SLEEP)
        kiwoom_cmd = ('SendOrder(QString, QString, QString,'
                      ' int, QString, int,'
                      ' int, QString, QString)')
        status = self.kiwoom.dynamicCall(
            kiwoom_cmd, [s_rq_name, s_screen_no, s_acc_no,
                         n_order_type, s_code, n_qty,
                         n_price, s_hoga, s_org_no])

        print('[status] send order',
              s_rq_name, s_screen_no, s_acc_no,
              n_order_type, s_code, n_qty,
              n_price, s_hoga, s_org_no,
              'status', status)

        if status:  # check error
            print('[Error] SendOrder', status)
        self.kiwoom_order_event_loop = QtCore.QEventLoop()
        self.kiwoom_order_event_loop.exec()
        return status

    def on_but_balance(self):
        self.kiwoom_set_input_values({
            '계좌번호': self.account,
            '비밀번호': '0000',
            '상장폐지조회구분': '0',
            '비밀번호입력매체구분': '00',
        })
        self.kiwoom_comm_rq_data(
            'balance_day2', 'opw00004', 0, '0200')

        if self.asset_symbols:
            self.set_real_reg()

    def on_but_draw_actions(self):
        self.candle_data = dict()  # ohlcv_draw_orders fills the datas
        # today = datetime.date.today().strftime('%Y%m%d')
        today = TODAY.strftime('%Y%m%d')
        for symbol in self.asset_symbols:
            # print('symbol', symbol)
            # time.sleep(0.2)
            self.kiwoom_set_input_values({
                '종목코드': symbol,
                '기준일자': today,
                '수정주가구분': '1',
            })
            self.kiwoom_comm_rq_data(
                'ohlcv_draw_actions', 'opt10081', 0, '0400')

        net_buy = 0
        net_sell = 0
        for symbol, row in self.row['order'].items():
            item = self.model['order'].item(
                row, self.col['order']['symbol'])
            if item.checkState() != Qt.Checked:
                print(f'{symbol} is not checked. Do nothing.')
                continue
            print('draw', symbol, row)
            with orm.db_session:
                asset = db.Asset.get(symbol=symbol)
                tactic_endpoint = asset.tactic.endpoint
            headers = {'Content-type': 'application/json'}
            data = self.candle_data[symbol]
            buy = 0
            for _ in range(self.get_model_data(
                'order', row, self.col['order']['position_size'])):
                r = requests.post(url=tactic_endpoint,
                                  headers=headers,
                                  data=json.dumps(data))
                if int(r.json()['action']) == 0:  # BUY
                    buy += 1
                elif int(r.json()['action']) == 2:  # SELL
                    buy -= 1
            close_ = int(r.json()['close'])
            print('rl', symbol, buy, close_)

            item = self.model['order'].item(
                row, self.col['order']['action'])
            item.setData('{:+}'.format(buy), Qt.DisplayRole)
            item = self.model['order'].item(
                row, self.col['order']['action_remained'])
            item.setData('{:+}'.format(buy), Qt.DisplayRole)

            if buy > 0:
                net_buy -= buy*close_
            else:
                net_sell -= buy*close_

        print('net_buy', type(net_buy), net_buy, net_sell)
        row = self.row['balance']['increment_e']
        col = self.col['balance']
        self.set_model_data(
            'balance', row, col['cash'], int(net_sell + net_buy))
        self.set_model_data(
            'balance', row, col['buy'], int(net_buy))
        self.set_model_data(
            'balance', row, col['sell'], int(net_sell))

    def on_but_send_orders(self):
        col = self.col['order']
        for symbol, row in self.row['order'].items():
            item = self.model['order'].item(
                row, col['symbol'])
            if item.checkState() != Qt.Checked:
                print(f'{symbol} is not checked. Do nothing.')
                continue
            buy = self.get_model_data(
                'order', row, col['action'])
            print('but_send_orders', buy, symbol)
            if buy == 0:
                continue
            elif buy < 0:  # sell
                buy = max(
                    -self.get_model_data(
                        'order',
                        row, self.col['order']['num_shares']),
                    buy)
                if buy == 0:  # no shares to sell
                    continue
            close_price = self.get_model_data(
                'order',
                row, self.col['order']['quote'])
            close_price = int(close_price)
            print('send order, account', self.account, close_price)
            err = self.kiwoom_send_order(
                'send_order', '0700', self.account,
                1 if buy > 0 else 2,  # init submit, 1 for buy, 2 for sell
                symbol, abs(buy),
                0, # abs(close_price),
                '03',  # bid market price
                ''  # new order
            )
            if err == 0:
                print('submitted:', symbol, buy)
            else:
                print('submit error')
            QtCore.QThread.msleep(TR_RQ_SLEEP)

    def lcd_clock_update(self):
        def change_palette():
            self._lcd_clock_blink += 1
            if self._lcd_clock_blink % 2 == 0:
                self.ui.lcd_clock.setStyleSheet(
                    'QLCDNumber {background-color: blue;}')
            else:
                self.ui.lcd_clock.setStyleSheet(
                    'QLCDNumber {background-color: red;}')

        time = QtCore.QTime.currentTime()
        alert_time = QtCore.QTime(15, 21, 0)
        close_time = QtCore.QTime(15, 30, 0)
        if time > alert_time and time < close_time:
            if not self.ui.cbox_autorun.isChecked():
                self.ui.cbox_autorun.setChecked(True)
            change_palette()
        self.ui.lcd_clock.display(time.toString('hh:mm:ss'))

    def on_but_add_asset(self):
        @orm.db_session
        def on_accepted():
            print(ui.le_symbol.text(), ui.sb_max_shares.text(),
                  ui.sb_position_size.text(), ui.combo_tactic.currentText())
            asset = db.Asset(
                symbol=ui.le_symbol.text(),
                num_shares=0,
                max_shares=int(ui.sb_max_shares.text()),
                position_size=int(ui.sb_position_size.text()),
                is_active=False,
                tactic=db.Tactic[self.tactics[ui.combo_tactic.currentText()]]
            )
            # reset attributes
            row_count = self.model['order'].rowCount()
            for _ in range(row_count):
                self.model['order'].removeRow(0)
            self.assets, self.tactics = self.get_assets_tactics()
            self.set_real_reg()
            self.asset_symbols = set()
            for symbol in self.row['order'].keys():
                self.asset_symbols.add(symbol)

        dialog = QtWidgets.QDialog()
        dialog.setModal(True)
        ui = Ui_Dialog()
        ui.setupUi(dialog)
        ui.combo_tactic.addItems(
            self.tactics.keys())
        ui.but_ok.accepted.connect(on_accepted)
        dialog.exec()

    def on_event_connect(self, err):
        if err == 0:
            self.ui.statusbar.showMessage('connected')
            print('Connected')
            accounts = self.kiwoom.dynamicCall(
                'GetLoginInfo(QString)', 'ACCLIST')
            accounts = accounts.split(';')
            self.account = accounts[0].strip()  # guess only one account
            self.ui.but_balance.setText(self.account)
            if self.account == self.env.str('REAL_ACCOUNT'):
                self.ui.but_balance.setStyleSheet('background-color: green')
            else:
                self.ui.but_balance.setStyleSheet('background-color: gray')
            self.on_but_balance()
        else:
            print('Error:', err)

    @on_receive_tr('send_order')
    def send_order(self, s_screen_no, s_rq_name, s_tr_code,
                    s_record_name, s_prev_next, *_):
        self.order_no = self.kiwoom_get_comm_data(
            s_tr_code, s_record_name, 0, '주문번호'
        )
        if self.order_no == '':
            print('tr order failed')
        else:
            print('tr order no:', self.order_no)

        self.kiwoom_order_event_loop.exit()

    @on_receive_tr('send_order')
    def send_order_msg(self, s_screen_no, s_rq_name, s_tr_code, s_msg):
        print(f'msg send order {s_rq_name}: {s_msg}')

    def send_order_chejan_data(self, s_gubun, n_item_cnt, s_fid_list):
        order_status = {'accepted': '접수', 'completed': '체결'}
        if s_gubun == '0':  # accepted/completed
            symbol, status = self.kiwoom_get_chejan_data(
                [9001, 913])
            symbol = symbol.lstrip('A')
            if symbol not in self.row['order']:
                print(f'unknown transaction, {symbol}')
                return
            order_id, order_type = self.kiwoom_get_chejan_data(
                [9203, 905])
            order_type = 1 if '+' in order_type else -1
            if status == order_status['accepted']:
                print(f'chejan, accepted id {order_id}, o {order_type}')
            elif status == order_status['completed']:
                print(f'chejan, completed id {order_id}, o {order_type}')
                price, qty, qty_remained, net_value, unit_qty = \
                    self.kiwoom_get_chejan_data([910, 915, 902, 903, 915])
                price, qty = int(price), int(qty)
                qty_remained, net_value = int(qty_remained), int(net_value)
                qty_remained *= order_type
                print('chejan 0: ', symbol, status, price, qty, unit_qty)
                print('chejan 0-1:', qty_remained, net_value)

                if qty_remained == 0:
                    sell, buy = (0, -1) if order_type == 1 else (1, 0)
                    sell *= net_value
                    buy *= net_value
                    sell += self.get_model_data(
                        'balance',
                        self.row['balance']['increment_r'],
                        self.col['balance']['sell'])
                    buy += self.get_model_data(
                        'balance',
                        self.row['balance']['increment_r'],
                        self.col['balance']['buy'])
                    self.set_model_data(
                        'balance',
                        self.row['balance']['increment_r'],
                        self.col['balance']['sell'],
                        sell)
                    self.set_model_data(
                        'balance',
                        self.row['balance']['increment_r'],
                        self.col['balance']['buy'],
                        buy)
                    self.set_model_data(
                        'balance',
                        self.row['balance']['increment_r'],
                        self.col['balance']['cash'],
                        sell + buy)

                item = self.model['order'].item(
                    self.row['order'][symbol],
                    self.col['order']['action_remained'])
                item.setData('{:+}'.format(qty_remained), Qt.DisplayRole)

                with orm.db_session:
                    asset = db.Asset.get(symbol=symbol)
                    print('ass1: ', asset.symbol)
                    db.Entry(asset=asset, date=TODAY.isoformat(),
                             price=price, order=qty*order_type)

                # self.kiwoom_comm_rq_data(
                #     'balance_close2', 'opw00004', 0, '0200')

        elif s_gubun == '1':  # executed result
            print('balance')
            symbol, num_shares = self.kiwoom_get_chejan_data(
                [9001, 930])
            symbol = symbol.lstrip('A')
            if symbol not in self.row['order']:
                print(f'unknown transaction, {symbol}')
                return
            num_shares = int(num_shares)
            print('chejan 1: ', symbol, num_shares)

            self.set_model_data(
                'order',
                self.row['order'][symbol],
                self.col['order']['num_shares'],
                num_shares)
            with orm.db_session:
                asset = db.Asset.get(symbol=symbol)
                print('ass2: ', asset.symbol)
                asset.num_shares = num_shares

        else:
            print('err,,, check,,, else data: ', s_gubun)

    @QtCore.pyqtSlot(object)
    def update_balance(self, balance):
        capital = balance['capital']
        security = balance['security']
        day2 = balance['day2']

        if balance['view'] == 'day2':
            row = self.row['balance']['day2']
        else:
            row = self.row['balance']['close2']

        col = self.col['balance']
        self.set_model_data(
            'balance', row, col['capital'], capital)
        self.set_model_data(
            'balance', row, col['security'], security)
        self.set_model_data(
            'balance', row, col['cash'], day2)

        self.kiwoom_tr_event_loop.exit()

    @on_receive_tr('balance_day2')
    def balance_day2(self, s_screen_no, s_rq_name, s_tr_code,
                     s_record_name, s_prev_next, *_):
        n_index = 0
        s_item_name = 'D+2추정예수금'
        day2 = self.kiwoom_get_comm_data(
            s_tr_code, s_record_name, n_index, s_item_name)
        s_item_name = '유가잔고평가액'
        security = self.kiwoom_get_comm_data(
            s_tr_code, s_record_name, n_index, s_item_name)
        s_item_name = '추정예탁자산'
        capital = self.kiwoom_get_comm_data(
            s_tr_code, s_record_name, n_index, s_item_name)

        self.balance_signal.emit({
            'view': 'day2', 'capital': int(capital),
            'security': int(security), 'day2': int(day2)})
    
    @on_receive_tr('balance_close2')
    def balance_close2(self, s_screen_no, s_rq_name, s_tr_code,
                    s_record_name, s_prev_next, *_):
        n_index = 0
        s_item_name = 'D+2추정예수금'
        day2 = self.kiwoom_get_comm_data(
            s_tr_code, s_record_name, n_index, s_item_name)
        s_item_name = '유가잔고평가액'
        security = self.kiwoom_get_comm_data(
            s_tr_code, s_record_name, n_index, s_item_name)
        s_item_name = '추정예탁자산'
        capital = self.kiwoom_get_comm_data(
            s_tr_code, s_record_name, n_index, s_item_name)

        self.balance_signal.emit({
            'view': 'close2', 'capital': int(capital),
            'security': int(security), 'day2': int(day2)})
    
    @on_receive_tr('ohlcv_draw_actions')
    def ohlcv_draw_actions(self, s_screen_no, s_rq_name, s_tr_code,
                           s_record_name, s_prev_next, *_):
        # num_records = self.kiwoom.dynamicCall(
        #     'GetRepeatCnt(QString, QString)',
        #     s_tr_code, s_rq_name)
        data = defaultdict(list)
        symbol = self.kiwoom_get_comm_data(
            s_tr_code, s_record_name, 0, '종목코드')
        print('tr:symbol', symbol)
        t_open = QtCore.QTime(9, 0, 0)
        t_now = QtCore.QTime.currentTime()
        if t_now > QtCore.QTime(15, 20, 0):
            t_frac = 390.0 / 380.0
        else:
            t_frac = (t_now.hour() - t_open.hour()) * 60
            t_frac += (t_now.minute() - t_open.minute())
            t_frac = 390.0 / t_frac

        for n_index in range(30):  # num_records
            date_ = self.kiwoom_get_comm_data(
                s_tr_code, s_record_name, n_index, '일자')
            data['date'].append(date_)
            open_ = self.kiwoom_get_comm_data(
                s_tr_code, s_record_name, n_index, '시가')
            data['open'].append(float(open_))
            high_ = self.kiwoom_get_comm_data(
                s_tr_code, s_record_name, n_index, '고가')
            data['high'].append(float(high_))
            low_ = self.kiwoom_get_comm_data(
                s_tr_code, s_record_name, n_index, '저가')
            data['low'].append(float(low_))
            close_ = self.kiwoom_get_comm_data(
                s_tr_code, s_record_name, n_index, '현재가')
            data['close'].append(float(close_))
            volume_ = self.kiwoom_get_comm_data(
                s_tr_code, s_record_name, n_index, '거래량')
            if n_index == 0:
                print('daily:', symbol, date_, volume_, t_frac)
                volume_ = float(volume_) * t_frac
                # print(date_, t_frac, volume_)
            data['volume'].append(float(volume_))
            # print(date_, open_, high_, low_, close_, volume_)

        self.candle_data[symbol] = data
        self.kiwoom_tr_event_loop.exit()

    def set_real_reg(self):
        s_screen_no = '0150'
        s_code_list = ';'.join(self.asset_symbols)
        s_fid_list = ';'.join(['10', '12'])
        s_opt_type = '0'  # clear and set the new register
        self.kiwoom.dynamicCall(
            'SetRealReg(QString, QString, QString, QString)',
            s_screen_no, s_code_list, s_fid_list, s_opt_type)

    @on_receive_real('주식체결')
    def quote_stream(self, s_symbol, s_real_type, s_real_data):
        quote = self.kiwoom.dynamicCall(
            'GetCommRealData(QString, int)',
            s_symbol, 10)
        quote = int(quote)
        daily_return = self.kiwoom.dynamicCall(
            'GetCommRealData(QString, int)',
            s_symbol, 12)
        daily_return = float(daily_return)
        for symbol, row in self.row['order'].items():
            if s_symbol == symbol:
                # quote
                item = self.model['order'].item(
                    row, self.col['order']['quote'])
                item.setData('{:+,}'.format(quote), Qt.DisplayRole)
                # daily_return
                item = self.model['order'].item(
                    row, self.col['order']['daily_return'])
                item.setData('{:+,.2f}'.format(daily_return), Qt.DisplayRole)
                # security
                security = abs(quote) * self.get_model_data(
                    'order', row, self.col['order']['num_shares'])
                self.set_model_data(
                    'order', row, self.col['order']['security'],
                    security)
                # profit
                sell_buy = self.get_model_data(
                    'order', row, self.col['order']['sell_buy'])
                self.set_model_data(
                    'order', row, self.col['order']['profit'],
                    sell_buy + security)


def run():
    qapp = QtWidgets.QApplication([])
    
    mainwindow = MainWindow()
    mainwindow.show()

    qapp.exec()
