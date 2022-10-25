import os
import pandas as pd

from data_preprocess_cli.CategoricalValHandler import CategoricalValHandler
from data_preprocess_cli.FeatureScaler import FeatureScaler
from data_preprocess_cli.MissingValHandler import MissingValHandler
from data_preprocess_cli.common import get_col_index, display_columns


class Tool:
    __EXIT_INPUT = "exit()"
    __BACK_INPUT = "back()"
    __BACK_STRING = f'Enter "{__BACK_INPUT}" to go back"'
    __dataset_path = ""

    is_feature_scaled = False

    dataset: pd.DataFrame
    x: pd.DataFrame
    y: pd.Series

    """
        Public Methods
    """

    def import_dataset(self):
        """
        

        Returns
        -------
        None.

        """
        print(f"To exit the tool, Enter {self.__EXIT_INPUT}\n")

        curr_cmd = 0  # Indicates the question
        while True:
            # a) Selecting dataset path
            if curr_cmd == 0:
                while True:
                    print("\nTASK\t: Enter Dataset path:")
                    self.__dataset_path = self.__get_input()
                    if os.path.exists(self.__dataset_path):
                        curr_cmd += 1
                        break
                    else:
                        print("Error\t: The system cannot find the path specified.")
                        continue

            # b) Selecting dataset
            if curr_cmd == 1:
                while True:
                    print("\nTASK\t: Enter Dataset name: ")
                    dataset_name = self.__get_input().split(".")

                    # Check for back command
                    if dataset_name[0] == self.__BACK_INPUT:
                        curr_cmd -= 1
                        break

                    # check if the name is valid or not
                    if len(dataset_name) > 1:
                        # check if data is csv file or not
                        if dataset_name[-1] == "csv":
                            dataset_name = ".".join(dataset_name)
                            dataset_path = os.path.join(self.__dataset_path, dataset_name)

                            # Check if dataset is exists in dataset path
                            if not os.path.exists(dataset_path):
                                print("Error\t: The system cannot find the file specified.")
                                continue
                        else:
                            print("Error\t: Dataset must be a '.csv' file")
                            continue
                    else:
                        print("Error\t: The system cannot find the file specified.")
                        continue

                    # If there are no errors
                    self.__dataset_path = dataset_path
                    # Importing dataset as CSV
                    self.dataset = pd.read_csv(self.__dataset_path)
                    curr_cmd += 1
                    print("Dataset selected.\n")
                    break

            # Selecting target variable
            if curr_cmd == 2:
                display_columns(self.dataset)

                columns = self.dataset.columns
                while True:
                    print("\nTASK\t: Select Target Variable(y):")
                    target_column_num = self.__get_input()

                    # Check for back command
                    if target_column_num == self.__BACK_INPUT:
                        # Changing path i.e., removing selected file from dataset path
                        self.__dataset_path = os.path.dirname(self.__dataset_path)
                        curr_cmd -= 1
                        break
                    try:
                        target_column_num = int(target_column_num)
                        if target_column_num < -len(columns) or target_column_num >= len(columns):
                            print("ERROR\t: Invalid Column number selected")
                            continue
                    except ValueError:
                        print("ERROR\t: Invalid Column number selected")
                        continue

                    # If there is no Error
                    y_column = columns[target_column_num]
                    print(f"Target Variable \"{y_column}\" Selected")

                    # Creating y
                    self.y = self.dataset.iloc[:, target_column_num]

                    # Creating X
                    if target_column_num == len(columns) - 1:
                        self.x = self.dataset.iloc[:, :-1]
                    elif target_column_num == 0:
                        self.x = self.dataset.iloc[:, 1:]
                    else:
                        x_1 = self.dataset.iloc[:, 0: target_column_num]
                        x_2 = self.dataset.iloc[:, target_column_num + 1:]
                        self.x = pd.concat([x_1, x_2], axis=1)

                    curr_cmd += 1
                    print("Dependent and Independent variables selected.\n")
                    break

            if curr_cmd == 3:
                break

    def preprocess(self):
        level = 0
        while True:
            if level == 0:
                print(
                    "\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                print("\nPreprocessing...")
                print("\t1. Show Dataset")
                print("\t2. Show Independent Variables (X)")
                print("\t3. Show Dependent Variable (Y)")
                print("\t4: Describe X")
                print("\t5: Handle Missing Values")
                print("\t6: Encode Categorical Values")
                print("\t7: Delete columns from X")
                print("\t8: Rename columns from X")
                print("\t9: Feature Scale data")
                print("\t10: Download Dataset")
                print(f"\t{self.__EXIT_INPUT}: Exit")
                print("\nTASK\t: Enter Option:")

                level = self.__get_input()

                # Validating input
                try:
                    level = int(level)
                except ValueError:
                    print("ERROR\t: Invalid option selected")
                    continue

            if level in [1, 2, 3]:
                selected_columns = [0]
                if level in [1, 2]:
                    """
                    Selecting Columns
                    """
                    print("\nDisplaying Dataset:")
                    if level == 1:
                        display_columns(self.dataset)
                    else:
                        display_columns(self.x)
                    print(f"\nTASK\t: Select upto 5 columns(numbers) with space separated:")
                    selected_columns = self.__get_input()
                    # validating columns
                    try:
                        selected_columns = list(map(int, selected_columns.split()))
                    except ValueError:
                        print("ERROR\t: Invalid columns selected")

                """
                Selecting Rows
                """
                PRINT_ROW_COUNT = 20
                print(f"\nPrints {PRINT_ROW_COUNT} rows from entered row number")
                print(f"TASK\t: Enter starting row number out of {len(self.dataset) - 1}:")
                row_num = self.__get_input()

                # validating row number
                try:
                    row_num = int(row_num)
                    if row_num >= len(self.dataset) or row_num < 0:
                        # If row number is in negatives or out of index
                        raise ValueError
                    else:
                        if row_num + PRINT_ROW_COUNT > len(self.dataset):
                            # If selected row number in last
                            if level == 1:
                                print(self.dataset.iloc[row_num:, selected_columns])
                            elif level == 2:
                                print(self.x.iloc[row_num:, selected_columns])
                            elif level == 3:
                                print(self.y[row_num:])
                        else:
                            # If selected row number is from first or middle
                            if level == 1:
                                print(self.dataset.iloc[row_num:row_num + PRINT_ROW_COUNT, selected_columns])
                            if level == 2:
                                print(self.x.iloc[row_num:row_num + PRINT_ROW_COUNT, selected_columns])
                            elif level == 3:
                                print(self.y[row_num:row_num + PRINT_ROW_COUNT])

                        # Going back to level 0
                        level = 0
                except ValueError:
                    print("ERROR\t: Invalid row number")
                    pass
                pass

            if level == 4:
                display_columns(self.x)
                print("\nTASK\t: Select column to describe or enter '-1' to describe whole dataset: ")
                option = self.__get_input()

                # Validating Input
                try:
                    option = int(option)
                    if option == -1:
                        print(self.x.describe())
                    else:
                        print(self.x.iloc[:, option].describe())
                    # Going back to level 0
                    level = 0
                except ValueError:
                    print("ERROR\t: Invalid Column number selected")

            if level == 5:
                """
                Handling Missing/Null values
                """
                miss_val_handler = MissingValHandler(self.x)
                missing_val_cols = miss_val_handler.get_missing_columns()  # contains column names
                missing_val_cols = [get_col_index(self.x, col_name) for col_name in
                                    missing_val_cols]  # Contain column indexes
                if len(missing_val_cols) != 0:
                    print()
                    miss_val_handler.analyze()
                    # Going inside categorical level
                    level = 5.1
                else:
                    print("NOTE\t: No columns with missing values")
                    # Going back to starting level
                    level = 0

            if level == 5.1:
                """
                Sub : Handling Missing/Null values
                """
                print(f"\nTASK\t: Enter column number to impute null values or Enter {self.__BACK_INPUT} to go back")
                col_num = self.__get_input()

                # Handling back command
                if col_num == self.__BACK_INPUT:
                    # Going back to level 0
                    level = 0
                    continue

                # Validating Input
                try:
                    col_num = int(col_num)

                    if col_num in missing_val_cols:
                        print("\nTASK\t: Select the Strategy to impute null values")
                        print("\t1: Mean")
                        print("\t2: Median")
                        print("\t3: Mode")

                        strategy = self.__get_input()
                        # Validating Input
                        try:
                            strategy = int(strategy)

                            if strategy > 3:
                                raise ValueError
                            if strategy == 1:
                                strategy = "mean"
                            elif strategy == 2:
                                strategy = "median"
                            else:
                                strategy = "most_frequent"

                            miss_val_handler.impute(col_num, strategy)
                            print(
                                f"Missing values in column with number {col_num} are imputed using strategy {strategy}")
                            print("---------------------------------------------------------------------------------\n")
                            # Going back to level 5
                            level = 5

                        except ValueError:
                            print("ERROR\t: Invalid strategy selected")
                            # Going back to level 5
                            level = 5
                    else:
                        raise ValueError
                except ValueError:
                    print("ERROR\t: Invalid column number selected")
                    # Going back to level 5
                    level = 5

            if level == 6:
                # To check if missing values are handled or not
                miss_val_handler = MissingValHandler(self.x)
                if len(miss_val_handler.get_missing_columns()) > 0:
                    print("NOTE\t: First Handle Missing values before encoding")
                    level = 0
                    continue
                else:
                    # If Missing values are handled
                    categ_handler = CategoricalValHandler(self.x)
                    print()
                    categ_cols = categ_handler.get_categorical_cols()

                    if len(categ_cols) > 0:
                        print(f"\nTASK\t: Enter column number to encode or Enter {self.__BACK_INPUT} to go back")

                        col_num = self.__get_input()

                        # Handling back command
                        if col_num == self.__BACK_INPUT:
                            # Going back to level 0
                            level = 0
                            continue

                        # Validating input
                        try:
                            col_num = int(col_num)
                            print("\t1: Label Encoder")
                            print("\t2: One Hot Encoder")
                            print(f"\nTASK\t: Select encoder type or Enter {self.__BACK_INPUT} to go back")
                            encoder_type = int(self.__get_input())

                            if encoder_type == 1:
                                encoder_type = "label"
                            else:
                                encoder_type = "onehot"

                            # Encoding
                            new_categ_cols = categ_handler.cat_arr_to_num_arr(encoder_type, self.x.iloc[:, col_num])
                            # Removing selected categorical column
                            self.x.drop(self.x.columns[col_num], axis=1, inplace=True)
                            # Appending encoded columns into X dataframe
                            self.x = pd.concat([self.x, new_categ_cols], axis=1)
                        except ValueError:
                            print("ERROR\t: Error in Encoding")
                            level = 6
                    else:
                        print("NOTE\t: No categorical columns")
                        # Going back to starting level
                        level = 0

            if level == 7:
                display_columns(self.x)
                print(f"\nTASK\t: Select column to delete or enter '{self.__BACK_INPUT}' to go back: ")
                option = self.__get_input()

                # Handling going back
                if option == self.__BACK_INPUT:
                    level = 0
                    continue

                # Validating input
                try:
                    option = int(option)
                    # Deleting Column
                    self.x.drop(self.x.columns[option], axis=1, inplace=True)

                    print(f"Column {self.x.columns[option]} deleted from X")
                    print("------------------------------------------------\n")
                except ValueError:
                    print("ERROR\t: Invalid Option selected")
                    # Going back to starting level
                    level = 0

            if level == 8:
                display_columns(self.x)
                print(f"\nTASK\t: Select column to Rename or enter '{self.__BACK_INPUT}' to go back: ")
                option = self.__get_input()

                # Handling going back
                if option == self.__BACK_INPUT:
                    level = 0
                    continue

                # Validating input
                try:
                    print(f"\nTASK\t: Enter new column name:")
                    new_col_name = self.__get_input()

                    option = int(option)
                    # Renaming Column
                    old_col_name = self.x.columns[option]
                    self.x.rename(columns={old_col_name: new_col_name}, inplace=True)
                    print("------------------------------------------------\n")
                except ValueError:
                    print("ERROR\t: Invalid Option selected")
                    # Going back to starting level
                    level = 0

            if level == 9:
                # Check if Categorical columns are encoded or not
                categ_handler = CategoricalValHandler(self.x)
                if len(categ_handler.get_categorical_cols()) > 0:
                    print("NOTE\t: First Encode categorical columns before feature scaling")
                    level = 0
                    continue
                else:
                    print("\n********************  Feature Scaling  ********************\n")
                    print("\t1. Standard Scaling")
                    print("\t2. MinMax Scaling")
                    print("\t3. Robust Scaling")
                    print("\t4. MaxAbs Scaling")
                    print("\t5. Normalizer")
                    print(f"\nTASK\t: Select the type of feature scaling or enter '{self.__BACK_INPUT}' to go back: ")
                    option = self.__get_input()

                    # Handling going back
                    if option == self.__BACK_INPUT:
                        level = 0
                        continue

                    # Validating input
                    try:
                        option = int(option)
                        if option == 1:
                            scaler_type = "scaler"
                        elif option == 2:
                            scaler_type = "minmax"
                        elif option == 2:
                            scaler_type = "robust"
                        elif option == 2:
                            scaler_type = "maxabs"
                        else:
                            scaler_type = "normalizer"

                        self.x = FeatureScaler(self.x, scaler_type).scale()
                        level = 0
                        print("------------------------------------------------\n")
                    except ValueError:
                        print("ERROR\t: Invalid Option selected")
                        # Going back to starting level
                        level = 0

            if level == 10:
                print(f"\nTASK\t: Select path to download datasets or enter '{self.__BACK_INPUT}' to go back: ")
                download_path = self.__get_input()

                # Handling back command
                if download_path == self.__BACK_INPUT:
                    # Going back to level 0
                    level = 0
                    continue

                # Validating Input
                if os.path.exists(self.__dataset_path):
                    print(f"\nTASK\t: Enter file name:")
                    file_name = self.__get_input()

                    if file_name.split(".")[-1] == "csv":
                        final_ds = pd.concat([self.x, self.y], axis=1)
                        final_ds.to_csv(os.path.join(download_path, file_name), index=False)

                        print("Dataset saved successfully")
                        print("Exiting tool.......")
                        exit()
                    else:
                        print("Error\t:Filename must be of .csv format")
                        continue
                else:
                    print("Error\t: The system cannot find the path specified.")
                    continue

    """
        Private Methods
    """

    def __get_input(self) -> str:
        """
        Gets the input from user and checks if user wants to exit

        Parameters
        ----------

        Returns
        -------
        str
            User entered input

        """
        # Getting the input from user
        ip = input("INPUT\t: ")

        # to check if user wants to exit
        if ip == self.__EXIT_INPUT:
            print("Exiting tool.......")
            exit()

        return ip


if __name__ == "__main__":
    print("Hi, Welcome\n")
    print('"Data Preprocess CLI" tool helps you preprocess Data without coding :D')
    print("Let's start ....\n")

    """
    Configs
    """
    pd.set_option('display.max_columns', 5)

    tool = Tool()
    print("Importing dataset")
    # 1) Importing Data
    tool.import_dataset()
    # 2) Starting Preprocessing
    tool.preprocess()
    # print(tool.x)
    # print(type(tool.y))
