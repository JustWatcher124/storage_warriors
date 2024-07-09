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
from joblib import Parallel, delayed
import copy
import pickle

data_file_name = 'single_product_for_showcase.csv'
# Daten laden
data = pd.read_csv(data_file_name)

# Erste Inspektion der Daten
print(data.head())

data['date'] = pd.to_datetime(data['date'])
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data['day'] = data['date'].dt.day

features = ['product_id', 'year', 'month', 'day']
X = data[features]
y = data['sales']

X = pd.get_dummies(X, columns=['product_id'], drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    # "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
    # "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
    # "LinearRegression": LinearRegression(),
    # "Ridge": Ridge(),
    # "Lasso": Lasso(),
    "SVR": SVR(),
    # "KNeighbors": KNeighborsRegressor(),
    # "DecisionTree": DecisionTreeRegressor(random_state=42)
}


def train_and_evaluate(model_info, model, X_train, y_train, X_test, y_test, callback=None):
    # Kopiere die Daten, um den Fehler zu vermeiden
    X_train_copy = copy.deepcopy(X_train)
    y_train_copy = copy.deepcopy(y_train)
    X_test_copy = copy.deepcopy(X_test)
    y_test_copy = copy.deepcopy(y_test)

    model.fit(X_train_copy, y_train_copy)
    y_pred = model.predict(X_test_copy)
    mae = mean_absolute_error(y_test_copy, y_pred)
    result = (model_info, mae, model)

    # Callback aufrufen, falls definiert
    if callback:
        callback(result)

    return result


def print_result(result):
    model_name, mae, model = result
    print(f'Model: {model_name}, MAE: {mae}')


# Modelle parallel trainieren und bewerten
results = Parallel(n_jobs=12)(delayed(train_and_evaluate)(name, model, X_train, y_train,
                                                          X_test, y_test, callback=print_result) for name, model in models.items())

# Beste Modell auswählen
best_model_name, best_mae, best_model = min(results, key=lambda x: x[1])
print(f'Best Model: {best_model_name} with MAE: {best_mae}')

# Beispielvorhersage für neue Daten
new_data = {
    'product_id': '9021',
    'year': 2024,
    'month': 6,
    'day': 15
}

# Konvertierung der neuen Daten in das benötigte Format
new_data_df = pd.DataFrame([new_data])
new_data_df = pd.get_dummies(new_data_df, columns=['product_id'], drop_first=True)
new_data_df = new_data_df.reindex(columns=X.columns, fill_value=0)

# Vorhersage machen
predicted_sales = best_model.predict(new_data_df)
print(f'Predicted Sales: {predicted_sales[0]}')

# with open(f'{hashlib.sha256(df1.to_json().encode()).hexdigest()}.pkl', 'wb') as pickle_file:
#     pickle.dump(best_model, pickle_file)
