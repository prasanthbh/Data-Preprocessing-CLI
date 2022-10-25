import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import Normalizer


class FeatureScaler:
    dataframe: pd.DataFrame
    scaler = None

    def __init__(self, dataframe, scale_type):
        """
        params:
            dataframe : DataFrame
            scale_type : string
                Type of scaling type
                possible values: 'standard', 'minmax', 'robust', 'maxabs', normalizer
        """
        self.dataframe = dataframe

        if scale_type == "standard":
            self.scaler = StandardScaler()
        elif scale_type == "minmax":
            self.scaler = MinMaxScaler()
        elif scale_type == "robust":
            self.scaler = RobustScaler()
        elif scale_type == "maxabs":
            self.scaler = MaxAbsScaler()
        else:
            self.scaler = Normalizer()

    def scale(self) -> pd.DataFrame:
        """
        To scale the data
            np_arr : numpy array
                numpy array to scale the data
        return:
            Return scaled numpy array
        """
        columns = list(self.dataframe.columns)
        np_arr = np.array(self.dataframe)
        np_arr = self.scaler.fit_transform(np_arr)
        return pd.DataFrame(np_arr, columns=columns)

    def __unscale(self, np_arr_scaled):
        """
        To scale the data
        params:
            np_arr_scaled : numpy array
                previously scaled numpy array
        return:
            Return unscaled numpy array
        """
        return self.scaler.inverse_transform(np_arr_scaled)
