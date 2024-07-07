import pandas as pd
import glob
from io import StringIO
import tempfile
from typing import Union
import os


def load_data_path_or_stringio(file_path: Union[str, StringIO], worksheet=0) -> pd.DataFrame:
    """
    Loads one or more data files (CSV, Parquet, Excel/xlsx/xls, ODS) into a Pandas DataFrame.

    The function now handles StringIO objects as well. It searches for all files matching the provided file path and loads them one by one using an inner helper function.
    It ensures that the columns' names are converted to lowercase before concatenating the individual DataFrames.

    Args:
        file_path (Union[str, StringIO]): The path of the file(s) or a StringIO object containing data to load.
        worksheet (int, string or list[str, int], optional): The worksheet(s) (by zero-index or name(s)) to load from Excel files. Default is 0.

    Returns:
        pd.DataFrame: A concatenated DataFrame containing the data from all loaded files.
    """

    def load_single_file(data):
        # Check if the input is a StringIO object
        if isinstance(data, StringIO):
            return pd.read_csv(data)

        ext = path_filename.split(".")[-1]
        if ext == "csv":  # csv file
            return pd.read_csv(path_filename)
        elif ext == "parquet":
            return pd.read_parquet(path_filename, engine="pyarrow")
        elif ext in ("xlsx", "xls"):
            return pd.read_excel(StringIO(data.getvalue().decode("utf-8")), sheet_name=worksheet)
        elif ext == "ods":
            return pd.read_excel(StringIO(data.getvalue().decode("utf-8")), engine="odf")

    if isinstance(file_path, str):
        all_files = glob.glob(file_path)
    else:  # Handling StringIO object
        all_files = file_path

#    print('This file or these files will be loaded:\n', ''.join([f.name for f in all_files]))

    # all columns in all files get converted to lowercase to make concatenation less error prone
    list_df = list()
    for filename in all_files:
        df = load_single_file(filename)
        df.columns = map(lambda x: x.lower().strip(), df.columns)
        list_df.append(df)

    data_raw = pd.concat(list(list_df))
    return data_raw


def load_data_from_path(file_path: str, worksheet=0) -> pd.DataFrame:
    """
    Loads one or more data files (CSV, Parquet, Excel/xlsx/xls, ODS) into a Pandas DataFrame.

    The function searches for all files matching the provided file path and loads them one by one using an inner helper function.
    It ensures that the columns' names are converted to lowercase before concatenating the individual DataFrames.

    Args:
        file_path (str): The path of the file(s) to load, or a pattern for multiple files.
        worksheet (int, string or list[str, int], optional): The worksheet(s) (by zero-index or name(s)) to load from Excel files. Default is 0. 

    Returns:
        pd.DataFrame: A concatenated DataFrame containing the data from all loaded files.
    """
    # inner function to facilitate the loading of one file
    def load_single_file(path_filename):
        ext = path_filename.split(".")[-1]
        if ext == "csv":  # csv file
            return pd.read_csv(path_filename)
        elif ext == "parquet":
            return pd.read_parquet(path_filename, engine="pyarrow")
        elif ext in ("xlsx", "xls"):
            return pd.read_excel(path_filename, sheet_name=worksheet)
        elif ext == "ods":
            return pd.read_excel(path_filename, engine="odf")

    all_files = glob.glob(file_path)
    print('This file or these files will be loaded:\n', ''.join(all_files))

    # all columns in all files get converted to lowercase to make concatenation less error prone
    list_df = list()
    for filename in all_files:
        df = load_single_file(filename)
        df.columns = map(lambda x: x.lower().strip(), df.columns)
        list_df.append(df)

    data_raw = pd.concat(list(list_df))
    return data_raw


def get_files(directory='.', extension='.meta'):
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(extension)]


def only_selected_models(model_dict):
    return [model_name for model_name, boolean in model_dict.items() if boolean]
