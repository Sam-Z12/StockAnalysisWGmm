from td.client import TDClient

from stockanalysisgmm.chart import Candle, CandleChart
from stockanalysisgmm.config.config import CONSUMER_KEY, REDIRECT_URI, CREDENTIALS_PATH, ACCOUNT_NUMBER
from stockanalysisgmm.chart.indicators import IdicatorsPlugin


STOCK_TICKER = 'AAPL'

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



candle_objs = [Candle(c) for c in price_history_candles]
candle_chart = CandleChart(candles=candle_objs)
ip = IdicatorsPlugin(active_indicatos=['rsi', 'macd'])
candle_chart.bind_plugin(ip)

candle_chart_indicators = list(candle_chart.indicators.keys())
indicators_plugin_active = ip.active_indicators

candle_rsi = [c.rsi for c in candle_objs]
chart_rsi = candle_chart.indicators['rsi'].tolist()
def is_equal(list1, list2):
    if list1 == list2:
        return True
    else:
        return False


if is_equal(candle_chart_indicators, indicators_plugin_active) and is_equal(candle_rsi[15:], chart_rsi[15:]):
    print("Test Passed")
else:
    print("Test Failed")

