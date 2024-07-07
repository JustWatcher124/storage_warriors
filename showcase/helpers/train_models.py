import hashlib
import pandas as pd
import numpy as np
from pandas._libs.hashtable import mode
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
import streamlit as st
from concurrent.futures import ProcessPoolExecutor, as_completed

MODELS = [
    {'name': "RandomForest", 'model': RandomForestRegressor(n_estimators=100, random_state=42)},
    {'name': "GradientBoosting", 'model': GradientBoostingRegressor(n_estimators=100, random_state=42)},
    {'name': "LinearRegression", 'model': LinearRegression()},
    {'name': "Ridge", 'model': Ridge()},
    {'name': "Lasso", 'model': Lasso()},
    {'name': "SVR", 'model': SVR()},
    {'name': "KNeighbors", 'model': KNeighborsRegressor()},
    {'name': "DecisionTree", 'model': DecisionTreeRegressor(random_state=42)}
]


def get_features(data):
    features = ['product_id', 'year', 'month', 'day']
    X = data[features]
    return X


def preprocess_and_split(df, options):
    X = get_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def train_models_st(X_train, y_train, X_test, y_test, model_list):
    results = []
    training_data = (X_train, y_train, X_test, y_test)
    with st.spinner("Running..."):
        with ProcessPoolExecutor() as executor:
            placeholder = st.empty()
            futures = (executor.submit(_train, *training_data,
                       model_info['model'], model_info['name']) for model_info in model_list)
            results = []
            for idx, future in enumerate(as_completed(futures), start=1):
                count, result = future.result()
                results.append((count, result))
                placeholder.text(str(result))
    return results


def _train(X_train, y_train, X_test, y_test, model, name):
    trained_model = model.fit(model, X_train, y_train)
    predicted_y_test = predict(trained_model, X_test)
    mae = mean_absolute_error(y_test, predicted_y_test)
    return mae, name


def select_best_model(results):
    best_result = min(results, key=lambda x: x[1])
    return best_result[0], best_result[1], best_result[2]


def predict(trained_model, X):
    # Use the trained model to make predictions on a new dataframe
    predicted_y = trained_model.predict(X)
    return predicted_y

# Main function that gets options and model names as parameters


def main_st(df, options, model_list):
    wanted_models = {model_info
                     for model_info in MODELS if model_info['name'] not in model_list}
    X_train, X_test, Y_train, Y_test = preprocess_and_split(df, options)
    results = train_models_st(X_train, Y_train, X_test, Y_test, wanted_models)
    return results
