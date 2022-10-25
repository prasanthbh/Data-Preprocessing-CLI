import numpy as np

from sklearn.impute import SimpleImputer


class MissingValHandler:
    dataframe = None

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def get_missing_columns(self):
        """
        Returns columns names of columns which contains Nan or missing values\n
        params:
            None
        returns:
            list : list contains numbers of columns
        """

        missing_cols = [col for col in self.dataframe.columns if self.dataframe[col].isnull().any()]
        return missing_cols

    def get_missing_columns_nums1(self):
        """
        Returns columns numbers of columns which contains Nan or missing values\n
        params:
            None
        returns:
            list : list contains numbers of columns
        """

        missing_cols = [self.dataframe.columns.get_loc(col) for col in self.dataframe.columns if self.dataframe[col].isnull().any()]
        return missing_cols

    def analyze(self):
        """
        Prints analysis on Missing data i.e., percentage of missing data on eac column
        """
        for col in self.get_missing_columns():
            col_series = self.dataframe[col]
            total_val = len(col_series)  # total values in column
            total_nulls = total_val - col_series.count()  # total null values in column
            nulls_perc = (total_nulls / total_val) * 100
            print(f"\t{self.dataframe.columns.get_loc(col)}:\t{col} of type {self.dataframe.dtypes[col]} "
                  f"contains {nulls_perc:.2f} % of null values")

    def impute(self, col_range, strategy, missing_vals=np.NaN):
        """
        Returns dataset with removed missing values in the given columns
        params:
            col_range:
                Tuple containing index of columns range
                Ex: only one column    --->    3
                    3rd to 6th columns --->    (3, 6)
            strategy:
                How to handle missing values in column
                    possible values: mean (defaul), median, most_frequent
            missing_vals:
                what values to be changed. by default "NaN"
        returns:
            dataframe
        """
        imputer = SimpleImputer(missing_values=missing_vals, strategy=strategy)
        if type(col_range) == type(1):
            # df[["B"]] = imputer.fit_transform(df[[]"B"]])
            self.dataframe[[self.dataframe.columns[col_range]]] = imputer.fit_transform(
                self.dataframe[[self.dataframe.columns[col_range]]])
        else:
            # df.iloc[:, 1: 3 ] = imputer.fit_transform(df.iloc[:, 1: 3 ])
            self.dataframe.iloc[:, col_range[0]: col_range[1] + 1] = imputer.fit_transform(
                self.dataframe.iloc[:, col_range[0]: col_range[1] + 1])

        return self.dataframe
