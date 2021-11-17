import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from td.client import TDClient
from csv import DictReader

from stockanalysisgmm.models.gmm import GmmCandle, GmmCandleChart
from stockanalysisgmm.chart.indicators import IdicatorsPlugin
from stockanalysisgmm.config.config import CONSUMER_KEY, REDIRECT_URI, CREDENTIALS_PATH, ACCOUNT_NUMBER


STOCK_TICKER = 'AAPL'


def gen(n, start_num=0):
    if start_num <= n:
        yield start_num
        yield from gen(n=n, start_num=start_num + 1)


class Iter(QThread):

    # Dont __init__ or the pyqtSignal doesnt work
    sig = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.c = []
        self.can_list = [[20.00, 33.22, 15.33, 30.24],
                         [25.55, 36.44, 22.23, 22.78],
                         [26.02, 30.44, 21.95, 28.78],
                         [28.80, 34.44, 18.10, 21.78],
                         [21.75, 23.44, 20.10, 22.78]]

    def run(self):
        g = gen(4)
        for i in g:
            self.c.append(self.can_list[i])
            self.sig.emit()
            self.sleep(2)


class GmmSim(QThread):

    sig = pyqtSignal()

    def __init__(self, live=False):
        super().__init__()
        self.cans = []
        self.live = live

    def init_model(self):

        td_session = td_session = TDClient(client_id=CONSUMER_KEY,
                                           redirect_uri=REDIRECT_URI,
                                           credentials_path=CREDENTIALS_PATH,
                                           account_number=ACCOUNT_NUMBER)
        td_session.login()
        price_history = td_session.get_price_history(symbol=STOCK_TICKER,
                                                     period_type='year',
                                                     period=3,
                                                     frequency='1',
                                                     frequency_type='daily')
        price_history_candles = price_history['candles']

        candle_objs = [GmmCandle(c) for c in price_history_candles]
        gmm_candle_chart = GmmCandleChart(
            stock_ticker=STOCK_TICKER, candles=candle_objs)
        ip = IdicatorsPlugin(active_indicatos=['rsi', 'macd'])
        gmm_candle_chart.bind_plugin(ip)
        return gmm_candle_chart.model_generator()

    def run(self):
        self.sim_generator = self.init_model()
        for candle in self.sim_generator:

            ohlc_tup = (candle.open, candle.high, candle.low,
                        candle.close, candle.label, candle.timestamp())
            self.cans.append(ohlc_tup)

            # print("running_sim.....")
            if self.live == True:
                self.sleep(1)
                self.sig.emit()
        self.sig.emit()


class ExampleSim(QThread):

    sig = pyqtSignal()

    def __init__(self, live=False):
        super().__init__()
        self.cans = []
        self.live = live

    def init_model(self):

        with open("stockanalysisgmm/example_data/AAPL_data.csv", "r") as data:
            csv_reader = DictReader(data)
            price_history_candles = [c for c in csv_reader]

        candle_objs = [GmmCandle(c) for c in price_history_candles]
        gmm_candle_chart = GmmCandleChart(
            stock_ticker=STOCK_TICKER, candles=candle_objs)
        ip = IdicatorsPlugin(active_indicatos=['rsi', 'macd'])
        gmm_candle_chart.bind_plugin(ip)
        return gmm_candle_chart.model_generator()

    def run(self):
        self.sim_generator = self.init_model()
        for candle in self.sim_generator:

            ohlc_tup = (candle.open, candle.high, candle.low,
                        candle.close, candle.label, candle.timestamp())
            self.cans.append(ohlc_tup)

            # print("running_sim.....")
            if self.live == True:
                time.sleep(0.25)
                self.sig.emit()
        self.sig.emit()
