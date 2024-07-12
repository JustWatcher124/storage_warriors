import pandas as pd
import glob
from io import StringIO
from typing import Union
import os
import pickle
import hashlib
import datetime
import numpy as np
from math import ceil as ceiling


def load_data_stringio(stringio_list) -> pd.DataFrame:
    """
    Loads one or more data files (CSV, Parquet, Excel/xlsx/xls, ODS) into a Pandas DataFrame.

    The function now handles StringIO objects. 
    It ensures that the columns' names are converted to lowercase before concatenating the individual DataFrames.

    Args:
        stringio_list: list[tuple], tuple containing (StringIO, filename: str)

    Returns:
        pd.DataFrame: A concatenated DataFrame containing the data from all loaded files.
    """

    def load_single_file(stringio, filename):
        ext = filename.split(".")[-1]

        if ext == "csv":  # csv file
            return pd.read_csv(stringio)
        elif ext == "parquet":
            return pd.read_parquet(stringio, engine="pyarrow")
        elif ext in ("xlsx", "xls"):
            return pd.read_excel(stringio)
        elif ext == "ods":
            return pd.read_excel(stringio, engine="odf")

    # list to hold dataframe unconcatenated
    list_df = list()

    # all columns in all files get converted to lowercase to make concatenation less error prone

    for stringio, filename in stringio_list:
        # load a single stringio object
        df = load_single_file(stringio, filename)
        # make all column names lower case -- helps with mis input in the original data files
        df.columns = map(lambda x: x.lower().strip(), df.columns)
        list_df.append(df)

    # concatenate the dataframes into one
    data_raw = pd.concat(list(list_df))
    return data_raw


def get_files(directory='.', extension='.meta'):
    '''
        Searches for all files in a directory / path with the extension specified
        Returns:
            list[str]: containing full paths to the files
    '''
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(extension)]


def only_selected_models(model_dict):
    '''
        Used to only get models that the user wants to train
        Returns:
            list[str]: Names of the modes
    '''
    return [model_name for model_name, boolean in model_dict.items() if boolean]


def only_selected_model_infos(save_model_dict):
    '''
        Used to get the meta information for models in train_or_save.py
    '''
    return [info[1] for model_name, info in save_model_dict.items() if info[0]]


def save_model_to_system(model_info, data_filename):
    '''
        Saves the model to the system model folders the systems file format 
        Saves model and metainformation seperately
    '''
    # unpack the model_info list
    _, model_name, model, available_products, user_set_model_name = model_info
    # generate a unique file name per model
    model_bytes = pickle.dumps(model)
    hash_model = hashlib.sha256(model_bytes).hexdigest()
    filename = f"{hash_model}"
    # format the meta information
    meta_info = {'model_name': model_name, 'user_model_name': user_set_model_name,
                 'system_trained': False, 'model_filename': f'{filename}.pkl', 'products': available_products,
                 'train_date': str(datetime.datetime.now().isoformat()), 'data_file_name': data_filename}

    # get path to directory for saving the models
    current_directory = os.getcwd()
    model_directory = os.path.join(current_directory, f'../tought_models/{filename}')

    # write the meta information to a .meta file
    with open(model_directory+'.meta', 'wb') as file:
        pickle.dump(meta_info, file)
    file.close()
    # write the trained model to a pkl file
    with open(model_directory+'.pkl', 'wb') as file:
        pickle.dump(model, file)
    file.close()
    return


def save_dataset_to_system(dataset, data_filename, dataset_name, options):
    # generate a unique name per dataset
    dataset_bytes = pickle.dumps(dataset)
    hash_dataset = hashlib.sha256(dataset_bytes).hexdigest()
    filename = f"{hash_dataset}"

    # format the meta information
    meta_info = {'data_name': dataset_name, 'system_trained': False, 'dataset_filename': f'{
        filename}.pkl', 'data_file_name': data_filename, 'rows': len(dataset), 'options': options}
    # get directory to save the datasets there
    current_directory = os.getcwd()
    dataset_directory = os.path.join(current_directory, f'../datasets/{filename}')

    # save the meta information to a .meta file
    with open(dataset_directory+'.meta', 'wb') as file:
        pickle.dump(meta_info, file)
    file.close()
    # save the dataset to a .pkl file
    with open(dataset_directory+'.pkl', 'wb') as file:
        pickle.dump(dataset, file)
    file.close()
    return


def pretty_markdown_for_datasets(dataset_dict_list):
    """
        Formats meta information of datasets into a markdown table to show to the user
    """
    heading = '### Available Datasets \n '
    table_header = '|Dataset Name|Filename|Size/Nr. of Rows|\n|---|---|---|'
    table_rows = ''
    for dataset_info in dataset_dict_list:
        table_rows += f'\n|{dataset_info["data_name"]}|{dataset_info["data_file_name"]}|{dataset_info["rows"]}|'
    markdown = heading + table_header + table_rows
    return markdown


def pretty_markdown_for_models(model_dict_list):
    """
        Formats meta information of models into a markdown table to show to the user
    """
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
    """
        Get the correct dataset that the user chose to load from a string identifier

        Returns:
            pd.DataFrame: First dataset file that fits the search algorithm gets returned
    """
    for dataset_info in datasets:
        if dataset_info['data_name']+' - ' + dataset_info['data_file_name'] == choice_str:
            wanted_dataset_info = dataset_info
            break
    df_filename = wanted_dataset_info['dataset_filename']
    current_directory = os.getcwd()
    dataset_file_loc = os.path.join(current_directory, f'../datasets/{df_filename}')
    with open(dataset_file_loc, 'rb') as file:
        df = pickle.load(file)

    options = wanted_dataset_info['options']
    return df, options, wanted_dataset_info['data_file_name']


def get_model_from_choice(choice_str, models):
    """
        Get the correct model that the user chose to load from a string identifier

        Returns:
            sklearn regression models: First model that fits the search algorithm gets returned
    """
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
    """
        Ask a model to predict the needed inventory for a given product, in a given time range

        Returns:
            pd.DataFrame: index = list of products, first and only column is the predicted value for the time range
    """

    # collect predictions for products in a single place to later make dataframe from
    prediction_collector = {product: 0 for product in products}
    # date_range is a list of dates to predict the models with
    date_range = pd.date_range(date_range_tuple[0], date_range_tuple[1])

    # needed to make concatenation work (and I like easter eggs)
    pred_features = pd.DataFrame(
        {'product_id': ['Never Gonna Give You Up'],
         'year': [2003],
         'month': [3],
         'day': [15]})

    # make a prediction feature dataframe to ask for multiple products
    for product in products:
        for date in date_range:
            # temp_df is used for one row, then overwritten with new, same structure as pred_features
            temp_df = pd.DataFrame([[product, date.year, date.month, date.day]], columns=pred_features.columns)
            pred_features.index = pred_features.index + 1
            pred_features = pd.concat([pred_features, temp_df])

    # delete the easter egg (which actually makes this thing work lol)
    pred_features = pred_features[~pred_features['product_id'].eq('Never Gonna Give You Up')]
    # produce dummy values for product id's as the models can't handel string inputs
    pred_features = pd.get_dummies(pred_features, columns=['product_id'])

    # go through the list of products again
    for product in products:
        # collector for all predictions
        needed = 0
        # iterates through the pred_features dataframe, while only taking products that we want to predict for in this product iteration
        for _, row in pred_features[pred_features['product_id_'+product]].iterrows():
            needed += model.predict(np.array(row.values).reshape(1, -1))
        # collect the needed inventory prediction into the designated place
        prediction_collector[product] = ceiling(needed)

    # reformat the prediction collector for display into a dataframe
    prediction_df = pd.DataFrame.from_dict(prediction_collector, orient='index').sum(axis=1)
    return prediction_df
