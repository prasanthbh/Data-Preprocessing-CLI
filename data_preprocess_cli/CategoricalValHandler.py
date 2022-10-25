import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import LabelEncoder

from data_preprocess_cli.common import get_col_index


class CategoricalValHandler:
    dataframe = None

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def get_categorical_cols(self):
        cols = []
        for col_name in self.dataframe.columns:
            if type(self.dataframe[col_name][0]) == type("s"):
                cols.append(col_name)
                print(f"\t{get_col_index(self.dataframe, col_name)}\t{col_name} : "
                    f"contains {len(set(self.dataframe[col_name]))} unique values")
        return cols

    @staticmethod
    def cat_arr_to_num_arr(encoder, cat_col : pd.Series):
        """
        To handle Categorical data\n
        (Note : first label encode the data then use one hot encoing)
        params:
            encoder : string
                To use either label encoder or one hot encoder\n
                possible values: 'label', 'onehot'
            cat_col : series
                column contains categorical field
        return:
            Return encoded numpy array of n cols (n -> no.of distinct categorical values)
        """
        col_name = cat_col.name
        cat_col_unique_vals = sorted(set(cat_col))
        cat_col = np.array(cat_col)
        if encoder == "onehot":
            cat_col = cat_col.reshape(-1, 1)
            ct = ColumnTransformer([('encoder', OneHotEncoder(), [0])], remainder='drop')
            new_cols_arr = ct.fit_transform(cat_col)
            # Assigning names to new columns
            new_cols_names = [f"{col_name}_{i}" for i in cat_col_unique_vals]
            return pd.DataFrame(new_cols_arr, columns=new_cols_names)
        elif encoder == "label":
            new_cols_arr = LabelEncoder().fit_transform(cat_col)
            return pd.Series(new_cols_arr, name=col_name)
