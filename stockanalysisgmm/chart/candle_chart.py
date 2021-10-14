from datetime import datetime
from numpy.lib.function_base import place
from numpy.ma.core import count
import pandas as pd
import numpy as np
from pandas.core.construction import array
from pandas.core.frame import DataFrame
from td.client import TDClient

from stockanalysisgmm.chart.indicators import RSI_PERIOD


class Candle:
    def __init__(self, ohlcv_dict):
        self.open = float(ohlcv_dict['open'])
        self.high = float(ohlcv_dict['high'])
        self.low = float(ohlcv_dict['low'])
        self.close = float(ohlcv_dict['close'])
        self.volume = float(ohlcv_dict['volume'])
        self.time = float(ohlcv_dict['datetime'])
        self._rsi = None
        self._macd = None

    def open(self):
        return self.open        
    
    def high(self):
        return self.high
    
    def low(self):
        return self.low
    
    def close(self):
        return self.close   

    def volume(self):
        return self.volume
    
    def timestamp(self):
        return self.time/1000
    
    def date(self):
        return str(datetime.fromtimestamp(self.time/1000))
    
    @property
    def rsi(self):
        return self._rsi

    @rsi.setter
    def rsi(self, val):
        self._rsi = val
    
    @property
    def macd(self):
        return self._macd

    @macd.setter
    def macd(self, val):
        self._macd = val



class CandleChart:
    def __init__(self, stock_ticker, candles):
        self.ticker = stock_ticker
        self.candles = candles 
        self.indicators = {}
        self.plugins = []

    def candles(self):
        return self.candles

    def close_prices(self):
        return [c.close for c in self.candles]
    
    def open_prices(self):
        return [c.open for c in self.candles]
    
    def low_prices(self):
        return [c.low for c in self.candles]

    def high_prices(self):
        return [c.high for c in self.candles]
    
    def volume(self):
        return [c.volume for c in self.candles]
    
    def date(self):
        return [c.date() for c in self.candles]

    def show_indicators(self):
        return [self.indicators.keys()]

    def remove_candles(self, start_index, end_index):
        self.candles = self.candles[start_index:end_index]
        return self.candles

    def add_indicator(self, array, indicator, count=0):
        """Used in bind_plugin to recurse through the class candles and for each 
        candle set the corresponding indicator property to the calculated value contain in the array"""
        if count >= len(array):
            self.indicators.update({indicator: array})
            return True
        self.candles[count].__setattr__(indicator, array[count])
        self.add_indicator(array=array, indicator=indicator, count=(count+1))

    def bind_plugin(self, plugin, remove_nan_data=True):
        """Binds the ohlcv properties in the CandleChart to the ohlcv properties in the IndicatorPlugin. 
            After properities are bound the the functions which calculate the indicators specified in the 
            IndicatorPlugin are called. The results are then added to each candle in the CandleChart using 
            the add_indicator function. remove_candles is called because when the RSI is calculated the fist RSI_PERIOD 
            candles will have an rsi value of nan which will cause an error when trying to use the rsi in a training 
            data set so the first RSI_PERIOD candles are removed"""

        # Connect ports between candle chart object and indicator plugin object
        plugin_ports = [port for port in dir(plugin) if port.startswith("_p_")]
        for port in plugin_ports:
            chart_obj = self.__getattribute__(port[3:])
            plugin.__setattr__(port, chart_obj)

        #Run each indicator function and bind the outputs to each candle object
        active_indicators = plugin.active_indicators
        for ind in active_indicators:
            ind_obj = getattr(plugin, ind)
            self.add_indicator(array=ind_obj(),indicator=ind)
            
        if remove_nan_data:
            self.remove_candles(start_index=RSI_PERIOD, end_index=None)

    def candles_to_df(self,):
        """Creates a pandas df from the CandleCharts properties"""
        df = pd.DataFrame({"date": self.date(),
                            "open": self.open_prices(),
                            "high": self.high_prices(),
                            "low": self.low_prices(),
                            "close": self.close_prices(),
                            "volume": self.volume()})
        return df

