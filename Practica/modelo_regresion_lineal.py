import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.impute import SimpleImputer


def modelo_regresion(archivo):
    if not isinstance(archivo, pd.DataFrame):
        raise ValueError("El argumento 'archivo' debe ser un DataFrame de pandas.")
    
    X = archivo[['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'ocean_proximity']]
    y = archivo['median_house_value']

    X = pd.get_dummies(X, columns=['ocean_proximity'], drop_first=True)
    
    # Imputar valores nulos
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    model = LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    return r2, mse

