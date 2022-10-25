import pandas as pd


def __get_bolded_string(string: str) -> str:
    """
    Formates the string into bold string to print in console

    Parameters
    ----------
    string : str
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    """

    return "\033[1m" + string + "\033[0m"


def get_col_index(dataframe, col_name):
    """
    Returns the column index of column in dataset
    """
    return list(dataframe.columns).index(col_name)


def display_columns(dataframe: pd.DataFrame):
    columns = dataframe.columns
    print("Total Columns:", len(columns))
    print("\tNo.\tColumn Name")
    for column_ind in range(len(columns)):
        print(f"\t{column_ind}\t{columns[column_ind]}")
