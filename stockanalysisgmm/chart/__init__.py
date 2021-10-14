# from td.client import TDClient
# import pandas as pd
# import numpy as np

# from .candle_chart import Candle, CandleChart
# from ..config.config import CONSUMER_KEY, REDIRECT_URI, CREDENTIALS_PATH, ACCOUNT_NUMBER
# from .indicators import IdicatorsPlugin


# STOCK_TICKER = 'AAPL'


# td_session = td_session = TDClient(client_id=CONSUMER_KEY, 
#                             redirect_uri=REDIRECT_URI,
#                             credentials_path=CREDENTIALS_PATH, 
#                             account_number=ACCOUNT_NUMBER)

# td_session.login()

# price_history = td_session.get_price_history(symbol=STOCK_TICKER,
#                                             period_type='year',
#                                             period=3,
#                                             frequency='1',
#                                             frequency_type='daily')
# price_history_candles = price_history['candles']

# candle_objs = [Candle(c) for c in price_history_candles]
# candle_chart = CandleChart(candles=candle_objs)


# ip = IdicatorsPlugin(active_indicatos=['rsi', 'macd'])

# candle_chart.bind_plugin(ip)
# print(candle_chart.indicators)
# print(candle_objs[50].rsi)

#print(f"After: {ip._p_close_prices()}")
#print(ip.rsi())


# rsi = candle_chart.rsi(RSI_PERIOD)

# candle_chart.add_rsi(rsi_array=scale_list(rsi))
# macd = candle_chart.macd(short_ema_period=SHORT_EMA_PERIOD, long_ema_period=LONG_EMA_PERIOD, macd_period=MACD_PERIOD)
# candle_chart.add_macd(macd_array=scale_list(macd))
# print(candle_chart.show_indicators())
# train_data = gmm_train_data(candle_chart.indicators)
# print(train_data.x_train_data(start_index=len(train_data.x_train_df)-10))


