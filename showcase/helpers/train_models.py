import hashlib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
import streamlit as st
from joblib import Parallel, delayed
from concurrent.futures import ThreadPoolExecutor, as_completed

MODELS = [
    {'name': "RandomForest", 'model': RandomForestRegressor(n_estimators=300, random_state=42)},
    {'name': "GradientBoosting", 'model': GradientBoostingRegressor(n_estimators=300, random_state=42)},
    {'name': "LinearRegression", 'model': LinearRegression()},
    {'name': "Ridge", 'model': Ridge()},
    {'name': "Lasso", 'model': Lasso()},
    {'name': "SVR", 'model': SVR()},
    {'name': "KNeighbors", 'model': KNeighborsRegressor()},
    {'name': "DecisionTree", 'model': DecisionTreeRegressor(random_state=42)}
]


def get_features(data, options):
    features = [options['product_id'], 'year', 'month', 'day']
    X = data[features]
    y = data[options['wanted_value']]
    X = pd.get_dummies(X, columns=[options['product_id']], drop_first=True)
    return X, y


def preprocess_and_split(df, options):
    test_split = options['test_split'] / 100
    # test_split = 20 / 100
    X, y = get_features(df, options)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split, random_state=42)
    return X_train, X_test, y_train, y_test


def train_models_st(X_train, y_train, X_test, y_test, model_list):
    results = []
    # training_data = (X_train, y_train, X_test, y_test)
    # st.write("test")
    with st.spinner('Training...'):
        with ThreadPoolExecutor() as executor:
            futures = (executor.submit(_train_and_test, X_train, y_train, X_test, y_test,
                       model_info['model'], model_info['name']) for model_info in model_list)
            for idx, future in enumerate(as_completed(futures), start=1):
                result = future.result()
                results.append(result)

            results_markdown = make_pretty_markdown_from_results(results)
    # st.write(results)
    return results, results_markdown


def make_pretty_markdown_from_results(results: list[tuple]):
    pretty_markdown_header = '|Model Name|MAE|\n|---|---|\n'
    pretty_markdown_list = ["|"+str(name)+'|'+str(round(scores, 2))+"|\n" for scores, name, model in results]
    markdown = "".join([pretty_markdown_header, *pretty_markdown_list])
    return markdown


def train_models_with_parallel(X_train, y_train, X_test, y_test, model_list):
    """unusud but is a possible replacement for train_models_st"""
    results = Parallel(n_jobs=2)(delayed(_train_and_test)(X_train, y_train, X_test,
                                                          y_test, model_info['model']) for model_info in model_list)
    # print(results)
    return results


def _train_and_test(X_train, y_train, X_test, y_test, model, name):
    trained_model = model.fit(X_train.values, y_train.values)
    predicted_y_test = predict(trained_model, X_test.values)
    # report = classification_report(y_test, predicted_y_test)
    mae = mean_absolute_error(y_test.values, predicted_y_test)
    # precision = precision_score(y_test, predicted_y_test)
    # accuracy = accuracy_score(y_test, predicted_y_test)
    # recall = recall_score(y_test, predicted_y_test)
    # f_score = f1_score(y_test, predicted_y_test)
    # scores = {'MAE': mae, 'Precision': precision, 'Accuracy': accuracy, 'Recall': recall, 'F1-Score': f_score}
    return mae, name, trained_model
    # return 0


def select_best_model(results):
    best_result = min(results, key=lambda x: x[1])
    return best_result[0], best_result[1], best_result[2]


def predict(trained_model, X):
    # Use the trained model to make predictions on a new dataframe
    predicted_y = trained_model.predict(X)
    return predicted_y

# Main function that gets options and model names as parameters


def main_st(df, options, model_list):

    if not all([val in df.columns for val in ['year', 'month', 'day']]):
        date_column = options['date_column']
        df[date_column] = pd.to_datetime(df[date_column])
        df['year'] = df[date_column].dt.year
        df['month'] = df[date_column].dt.month
        df['day'] = df[date_column].dt.day

    wanted_model_name = [mn for mn, mb in model_list.items() if mb]
    if not wanted_model_name:
        wanted_model_name = [info['name'] for info in MODELS]
    wanted_models = [model_info for model_info in MODELS if model_info['name'] in wanted_model_name]

    X_train, X_test, Y_train, Y_test = preprocess_and_split(df, options)
    results, results_markdown = train_models_st(X_train, Y_train, X_test, Y_test, wanted_models)
    # results = train_models_with_parallel(X_train, Y_train, X_test, Y_test, wanted_models)
    # st.write(results)
    # print(results)
    return results, results_markdown
