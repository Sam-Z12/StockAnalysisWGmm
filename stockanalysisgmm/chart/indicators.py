import pandas as pd
import numpy as np

UNBOUND = 'unbound'
RSI_PERIOD = 14
SHORT_EMA_PERIOD = 12
LONG_EMA_PERIOD = 26 
MACD_PERIOD  = 9

def scale_list(array_vals, upper_bound=100, lower_bound=0):
    return np.interp(array_vals, (np.nanmin(array_vals), np.nanmax(array_vals)), (lower_bound,upper_bound) )

class IdicatorsPlugin:
    def __init__(self, active_indicatos: list,) -> None:
        self.active_indicators = active_indicatos

        self._p_close_prices = UNBOUND
        self._p_open_prices = UNBOUND
        self._p_high_prices = UNBOUND
        self._p_low_prices = UNBOUND

    def rsi(self, period=RSI_PERIOD,):
        close = pd.DataFrame(self._p_close_prices())
        diff = close.diff()
        gains = diff.clip(lower=0)
        losses = diff.clip(upper=0)
        avg_gains = gains.rolling(period).mean()
        avg_losses = losses.rolling(period).mean()
        rs = avg_gains/avg_losses
        rsi = np.array(100 - (100/(1+rs)))
        return scale_list(rsi.flatten())
    
    def macd(self, short_ema_period=SHORT_EMA_PERIOD, long_ema_period=LONG_EMA_PERIOD, macd_period=MACD_PERIOD):
        close = pd.DataFrame(self._p_close_prices())
        short_ema = close.ewm(span=short_ema_period, adjust=False).mean()
        long_ema = close.ewm(span=long_ema_period, adjust=False).mean()
        macd_line = short_ema-long_ema
        signal_line = macd_line.ewm(span=macd_period, adjust=False).mean()
        macd_diff = np.array(macd_line-signal_line)
        return scale_list(macd_diff.flatten())

# ip = indicators_plugin(active_indicatos=['rsi'])
# print([p for p in dir(ip) if not p.startswith("__") ])
# print(ip.__getact__())
# for p in (ip.__getact__()):
#     ip.p()  