import pandas as pd
import numpy as np

class GmmTrainingData:
    def __init__(self, indicator_dict):
        self.x_train_df = pd.DataFrame(indicator_dict)

    def x_train_data(self, start_index=None, end_index=None):
        if start_index == None and end_index is not None:
            return np.array(self.x_train_df[:end_index])
        elif start_index is not None and end_index == None:
            return np.array(self.x_train_df[start_index:])
        else:
            return np.array(self.x_train_df[start_index:end_index])