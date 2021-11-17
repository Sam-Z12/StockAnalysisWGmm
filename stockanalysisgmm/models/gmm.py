
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import seaborn as sns

from stockanalysisgmm.chart.indicators import RSI_PERIOD, UNBOUND

from ..chart.candle_chart import CandleChart, Candle

NONINIT = 'not instantiated'
SIM_PERIOD = 100


def date_to_mdate(ohlc_df):
    ohlc_df['date'] = pd.to_datetime(ohlc_df['date'])
    ohlc_df['date'] = ohlc_df['date'].apply(mdates.date2num)
    return ohlc_df


def create_training_set(x_train_dict: dict, start_index=None, end_index=None):
    x_train_df = pd.DataFrame(x_train_dict)
    if start_index == None and end_index is not None:
        return np.array(x_train_df[:end_index])
    elif start_index is not None and end_index == None:
        return np.array(x_train_df[start_index:])
    else:
        return np.array(x_train_df[start_index:end_index])


class GmmCandle(Candle):
    def __init__(self, ohlcv_dict):
        super().__init__(ohlcv_dict=ohlcv_dict)
        self.label = UNBOUND


class GmmCandleChart(CandleChart):
    """Have to bind an indicator plugin before instancing a model and calling accosiated class functions"""

    def __init__(self, stock_ticker, candles):
        super().__init__(stock_ticker=stock_ticker, candles=candles)
        self.training_set = NONINIT
        self.model = NONINIT
        self.labels = NONINIT
        self.means = NONINIT
        self.weights = NONINIT
        self.groups = NONINIT

    def model_generator(self, start_index=214, end_index=None, period=SIM_PERIOD,):
        """Returns a generator that contains candles where a new gmm model was run for every candle between 
            the start and end indexs with a training set of size SIM_PERIOD before each candle. 
            Because the training set is based on the SIM_PERIOD periods back from the start_index the 
            start_index must be equal to or greater than the SIM_PERIOD. This function aims to be a better simulation than init_model function 
            at how this stragety would perform in real time trading."""
        if bool(self.indicators) == False:
            raise IndicatorsNotBound
        if start_index < period:
            raise ValueError(
                "Start index must be equal to or greater than the period")
        if end_index == None:
            end_index = (len(self.candles)-1)
        if start_index <= end_index:
            train_set_start_index = start_index - SIM_PERIOD
            training_set = create_training_set(
                x_train_dict=self.indicators, start_index=train_set_start_index, end_index=start_index)
            model = GaussianMixture(n_components=4,
                                    covariance_type='tied',
                                    max_iter=100,
                                    n_init=1,
                                    init_params='kmeans',
                                    verbose=0,
                                    random_state=1,
                                    weights_init=[.25, .25, .25, .25])
            model.fit(training_set)
            labels = model.predict(training_set)
            last_label = labels[-1]

            means = model.means_
            mean_sums = [[i, sum(means[i])] for i in range(len(means))]
            mean_sums.sort(key=lambda row: row[1])
            means_dict = {"low_label": mean_sums[0][0],
                          "low_mid_label": mean_sums[1][0],
                          "high_mid_label": mean_sums[2][0],
                          "high_label": mean_sums[3][0]}

            sim_candle = self.candles[start_index]
            for key in list(means_dict.keys()):
                if last_label == means_dict[key]:
                    sim_candle.label = key
            yield sim_candle
            yield from self.model_generator(start_index=start_index + 1)

    def init_model(self, start_index=None, end_index=None):
        """Fits a gmm model to all candles. When called this function will set the class labels, means, 
            and weights equal to the values calculated in the model"""
        self.training_set = create_training_set(
            x_train_dict=self.indicators, start_index=start_index)

        self.model = GaussianMixture(n_components=4,
                                     covariance_type='tied',
                                     max_iter=100,
                                     n_init=1,
                                     init_params='kmeans',
                                     verbose=0,
                                     random_state=1,
                                     weights_init=[.25, .25, .25, .25])
        self.model.fit(self.training_set)
        self.labels = self.model.predict(self.training_set)
        self.means = self.model.means_
        self.weights = self.model.weights_
        self.remove_candles(start_index=start_index, end_index=end_index)
        self.set_candle_labels()

    def set_candle_labels(self, count=0):
        """Will map each candles lable property to the GmmCandleCharts lables property"""
        candles = self.candles
        if count == len(candles):
            return True
        candles[count].label = self.labels[count]
        self.set_candle_labels(count=(count + 1))
        return True

    def labels_dict(self):
        """Will return a dictionary with what label corresponds which key. Is sorted based on the means from the gmm model"""
        mean_sums = [[i, sum(self.means[i])] for i in range(len(self.means))]
        mean_sums.sort(key=lambda row: row[1])
        return {"low_label": mean_sums[0][0],
                "low_mid_label": mean_sums[1][0],
                "high_mid_label": mean_sums[2][0],
                "high_label": mean_sums[3][0]}

    def label_switchs(self):
        """Finds on what dates the labels switched and what label it switched to"""
        switch_dates = []
        switch_to = []

        label_index = self.labels[0]
        for s in range(len(self.labels)):
            if self.labels[s] != label_index:
                date = self.date()[s]
                label = self.labels[s]
                switch_dates.append(date)
                switch_to.append(label)

                label_index = label
        return{"switch_dates": switch_dates, "switch_to": switch_to}

    def create_label_groups(self):
        """Create list of candles in a group then create a group class object for each list of candles"""
        lab_dict = self.labels_dict()
        groups = []
        for key in list(lab_dict.keys()):
            label = lab_dict[key]
            candle_group = [
                candle for candle in self.candles if candle.label == label]
            groups.append(LabelGroup(key=key, label=label,
                          list_candles=candle_group))
        self.groups = groups
        return self.groups

    def plot(self):
        """plots the ohlc candle chart represented by this class"""
        fig, ax = plt.subplots()
        candles_df = date_to_mdate(self.candles_to_df())
        candles_df = candles_df[['date', 'open', 'high', 'low', 'close']]
        candlestick_ohlc(ax, candles_df.values, width=0.5,
                         colorup='green', colordown='red', alpha=1)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45, fontsize=7)
        plt.title(self.ticker)
        plt.show()

    def cluster_plot(self):

        df = pd.DataFrame(self.training_set)
        df.rename(columns={0: 'rsi', 1: 'macd'}, inplace=True)
        df['labels'] = self.labels
        fig, ax = plt.subplots()
        sns.scatterplot(x=df['rsi'], y=df['macd'], hue=df['labels'],
                        palette=['red', 'green', 'blue', 'purple'])
        plt.title(self.ticker)
        plt.savefig("Indicator_Groups.png",
                    format='png', dpi=150)
        plt.show()

    def optimum_groups(self, min: int = 1, max: int = 10,):
        if min < 1:
            min = 1

        df = pd.DataFrame(columns=['num_groups', 'bic'])
        for i in range(min, max+1):
            m = GaussianMixture(n_components=i,
                                covariance_type='tied',
                                max_iter=100,
                                n_init=1,
                                init_params='kmeans',
                                verbose=0,
                                random_state=1,)
            m.fit(self.training_set)
            bic = m.bic(self.training_set)
            df.loc[len(df.index)] = [i, bic]

            print(bic)
        fig, ax = plt.subplots()
        plt.plot(df['num_groups'], df['bic'])
        plt.savefig("num_groups_vs_bic.png",
                    format='png', dpi=150)
        plt.show()


class LabelGroup:
    def __init__(self, key, label, list_candles: list):
        self.key = key
        self.label = label
        self.candles = list_candles


class IndicatorsNotBound(Exception):
    """Must bind indicators before calling this function"""
    pass


class GmmSimulation:
    def __init__(self, model_generator):
        self.simulation_generator = model_generator
        self.sim_storage = {}

    def sim_label_switchs(self, candle):
        label = candle.label
        if "sim_label_switchs" not in self.sim_storage:
            new_dict = {"sim_label_switchs": {"prev_label": label,
                                              "switchs": {'switch_to': [],
                                                          'switch_date': []}}}

            self.sim_storage.update(new_dict)

        else:
            prev_label = self.sim_storage['sim_label_switchs']['prev_label']
            if label != prev_label:
                self.sim_storage['sim_label_switchs']['switchs']['switch_to'].append(
                    label)
                self.sim_storage['sim_label_switchs']['switchs']['switch_date'].append(
                    candle.date())
                print(f"Label Switch: {prev_label} -> {label}")

            self.sim_storage['sim_label_switchs']['prev_label'] = label

    def sim_label_groups(self, candle):
        """Create list of candles in a group then create a group class object for each list of candles"""
        label = candle.label
        if "sim_label_groups" not in self.sim_storage:
            new_dict = {"sim_label_groups": {label: [candle]}}
            self.sim_storage.update(new_dict)
            print(f"New Group: {label}")

        else:
            if label not in list(self.sim_storage["sim_label_groups"].keys()):
                new_label_dict = {label: [candle]}
                self.sim_storage["sim_label_groups"].update(new_label_dict)
                print(f"New Group: {label}")
            else:
                self.sim_storage['sim_label_groups'][label].append(candle)

    def run(self):
        for c in self.simulation_generator:
            self.sim_label_switchs(candle=c)
            self.sim_label_groups(candle=c)
        # Run simulation
        return self.sim_storage
