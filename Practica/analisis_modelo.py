import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def ajustar_modelo(ruta_archivo, col_x, col_y):
    data = pd.read_csv(ruta_archivo)

    # Drop rows with any missing values in the specified columns
    data.dropna(subset=[col_x, col_y], inplace=True)

    X = data[col_x]
    X_i = sm.add_constant(X, prepend=True)
    y = data[col_y]

    modelo = sm.OLS(endog=y, exog=X_i).fit()
    return modelo

def actualizar_recta_regresion(modelo, ruta_archivo, col_x, col_y, canvas_regresion):
    data = pd.read_csv(ruta_archivo)

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(
        x=data[col_x],
        y=data[col_y],
        c="#FFA500",
        label="Datos de dispersión",
        marker="o",
    )
    ax.set_title(f'Distribución de {col_x} y {col_y}')
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.legend(handles=[scatter], loc='upper right')
    ax.plot(data[col_x], modelo.predict(exog=sm.add_constant(data[col_x], prepend=True)), linestyle='-', color='blue', label="OLS", linewidth=2)
    ci = modelo.get_prediction(exog=sm.add_constant(data[col_x], prepend=True)).summary_frame(alpha=0.05)
    ax.fill_between(data[col_x], ci["mean_ci_lower"], ci["mean_ci_upper"], color='orange', alpha=0.1, label='95% CI')

    canvas_regresion.delete("all")
    canvas = FigureCanvasTkAgg(fig, master=canvas_regresion)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.NSEW)


def calcular_rmse(modelo, ruta_archivo, col_x, col_y):
    data = pd.read_csv(ruta_archivo)

    X = sm.add_constant(data[col_x], prepend=True)
    y_true = data[col_y]

    y_pred = modelo.predict(exog=X)

    rmse = mean_squared_error(y_true, y_pred, squared=False)
    return rmse