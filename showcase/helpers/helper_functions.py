import pandas as pd
import glob
from io import StringIO
from typing import Union
import os
import pickle
import hashlib
import datetime
import numpy as np


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


def only_selected_model_infos(save_model_dict):
    return [info[1] for model_name, info in save_model_dict.items() if info[0]]


def save_model_to_system(model_info, data_filename):
    model_mae, model_name, model, available_products, user_set_model_name = model_info
    model_bytes = pickle.dumps(model)
    hash_model = hashlib.sha256(model_bytes).hexdigest()
    filename = f"{hash_model}"
    meta_info = {'model_name': model_name, 'user_model_name': user_set_model_name,
                 'system_trained': False, 'model_filename': f'{filename}.pkl', 'products': available_products,
                 'train_date': str(datetime.datetime.now().isoformat())}

    current_directory = os.getcwd()
    model_directory = os.path.join(current_directory, f'../tought_models/{filename}')

    with open(model_directory+'.meta', 'wb') as file:
        pickle.dump(meta_info, file)
    file.close()
    with open(model_directory+'.pkl', 'wb') as file:
        pickle.dump(model, file)
    file.close()
    return 0


def save_dataset_to_system(dataset, data_filename, dataset_name, options):
    dataset_bytes = pickle.dumps(dataset)
    hash_dataset = hashlib.sha256(dataset_bytes).hexdigest()
    filename = f"{hash_dataset}"
    meta_info = {'data_name': dataset_name, 'system_trained': False, 'dataset_filename': f'{
        filename}.pkl', 'data_file_name': data_filename, 'rows': len(dataset), 'options': options}
    current_directory = os.getcwd()
    dataset_directory = os.path.join(current_directory, f'../datasets/{filename}')
    with open(dataset_directory+'.meta', 'wb') as file:
        pickle.dump(meta_info, file)
    file.close()
    with open(dataset_directory+'.pkl', 'wb') as file:
        pickle.dump(dataset, file)
    file.close()
    return 0


def pretty_markdown_for_datasets(dataset_dict_list):
    heading = '### Available Datasets \n '
    table_header = '|Dataset Name|Filename|Size/Nr. of Rows|\n|---|---|---|'
    table_rows = ''
    for dataset_info in dataset_dict_list:
        table_rows += f'\n|{dataset_info["data_name"]}|{dataset_info["data_file_name"]}|{dataset_info["rows"]}|'
    markdown = heading + table_header + table_rows
    return markdown


def pretty_markdown_for_models(model_dict_list):
    heading = '### Available Models \n '
    table_header = '|Model Type|Model Name|Model Date|\n|---|---|---|'
    table_rows = ''
    for model_info in model_dict_list:
        if 'user_model_name' not in model_info:
            model_info['user_model_name'] = 'System Trained'
        if 'train_date' not in model_info:
            model_info['train_date'] = datetime.datetime(1970, 1, 1, 0, 0)
        table_rows += f'\n| {model_info["model_name"]} | {model_info["user_model_name"]} | {model_info["train_date"]} |'
    markdown = heading + table_header + table_rows
    return markdown


def get_dataset_from_choice(choice_str, datasets):
    for dataset_info in datasets:
        if dataset_info['data_name']+' - ' + dataset_info['data_file_name'] == choice_str:
            wanted_dataset_info = dataset_info
#            print(wanted_dataset_info)
            break
    df_filename = wanted_dataset_info['dataset_filename']
    current_directory = os.getcwd()
    dataset_file_loc = os.path.join(current_directory, f'../datasets/{df_filename}')
    with open(dataset_file_loc, 'rb') as file:
        df = pickle.load(file)

    options = wanted_dataset_info['options']
    return df, options, wanted_dataset_info['data_file_name']


def get_model_from_choice(choice_str, models):
    for model_info in models:
        if 'user_model_name' not in model_info:
            model_info['user_model_name'] = 'System Trained'
        if model_info['model_name']+' - ' + model_info['user_model_name'] == choice_str:
            wanted_model_info = model_info
            break
    model_filename = wanted_model_info['model_filename']
    current_directory = os.getcwd()
    model_file_loc = os.path.join(current_directory, f'../tought_models/{model_filename}')
    with open(model_file_loc, 'rb') as file:
        model = pickle.load(file)

    available_products = wanted_model_info['products']
    return model, available_products


def make_prediction(model, products, date_range_tuple):

    prediction_collector = {product: 0 for product in products}
    date_range = pd.date_range(date_range_tuple[0], date_range_tuple[1])
    print(prediction_collector)
    for product in products:
        prediction_collector[product] = [model.predict(
            np.array([date.year, date.month, date.day]).reshape(1, -1))[0] for date in date_range]

        #    products_predicted, needed_inventory = [(prod, need_inv) for prod, need_inv in prediction_collector.items()]
    prediction_df = pd.DataFrame.from_dict(prediction_collector, orient='index').sum(axis=1)
    return prediction_df
