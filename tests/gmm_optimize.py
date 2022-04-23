from csv import DictReader

from stockanalysisgmm.models.gmm import GmmCandle, GmmCandleChart
from stockanalysisgmm.chart.indicators import IdicatorsPlugin


def optimize():
    with open("stockanalysisgmm/example_data/AAPL_data.csv", "r") as data:
        csv_reader = DictReader(data)
        price_history_candles = [c for c in csv_reader]

    candle_objs = [GmmCandle(c) for c in price_history_candles]
    gmm_candle_chart = GmmCandleChart(
        stock_ticker='AAPL', candles=candle_objs)
    ip = IdicatorsPlugin(active_indicatos=['rsi', 'macd'])
    gmm_candle_chart.bind_plugin(ip)

    gmm_candle_chart.init_model(start_index=15)

    gmm_candle_chart.optimum_groups(min=1, max=20)
    gmm_candle_chart.cluster_plot()
    print("Charts have been saved in the tests folder.")
