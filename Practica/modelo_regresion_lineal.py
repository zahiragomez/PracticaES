import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error


def modelo_csv(archivoCSV):
    if not isinstance(archivoCSV, pd.DataFrame):
        raise ValueError("El argumento 'archivoCSV' debe ser un DataFrame de pandas.")
    
    X = archivoCSV[['VariableIndependiente1', 'VariableIndependiente2']]
    y = archivoCSV['VariableDependiente']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    model = LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    return r2, mse



def modelo_excel(archivoEXCEL):
    if not isinstance(archivoEXCEL, pd.DataFrame):
        raise ValueError("El argumento 'archivoExcel' debe ser un DataFrame de pandas.")
    
    X = archivoEXCEL[['VariableIndependiente1', 'VariableIndependiente2']]
    y = archivoEXCEL['VariableDependiente']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    model = LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    return r2, mse


def modelo_sql(archivoSQL):
    if not isinstance(archivoSQL, pd.DataFrame):
        raise ValueError("El argumento 'archivoSQL' debe ser un DataFrame de pandas.")
    
    X = archivoSQL[['VariableIndependiente1', 'VariableIndependiente2']]
    y = archivoSQL['VariableDependiente']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    model = LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    return r2, mse