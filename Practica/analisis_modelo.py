import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from seleccion_columna import cargar_datos
import re

def ajustar_modelo(ruta_archivo, col_x, col_y):
    data = cargar_datos(ruta_archivo)

    if data is None:
        # Manejar el caso en que no se pueda cargar el archivo
        print("Error: No se pudo cargar el archivo.")
        return None

    # Resto del código de ajustar_modelo
    data.dropna(subset=[col_x, col_y], inplace=True)
    X = data[col_x]
    X_i = sm.add_constant(X, prepend=True)
    y = data[col_y]
    modelo = sm.OLS(endog=y, exog=X_i).fit()
    return modelo

def actualizar_recta_regresion(modelo, ruta_archivo, col_x, col_y, canvas_regresion):
    data = cargar_datos(ruta_archivo)

    if data is None:
        # Manejar el caso en que no se pueda cargar el archivo
        print("Error: No se pudo cargar el archivo.")
        return None

    # Resto del código de actualizar_recta_regresion
    fig, ax = plt.subplots(figsize=(6, 4))
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

def actualizar_recta_regresion(modelo, ruta_archivo, col_x, col_y, canvas_regresion):
    # Utilizar la función cargar_datos del módulo seleccion_columna para cargar el archivo
    data = cargar_datos(ruta_archivo)

    fig, ax = plt.subplots(figsize=(6, 4))
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
    # Utilizar la función cargar_datos del módulo seleccion_columna para cargar el archivo
    data = cargar_datos(ruta_archivo)

    X = sm.add_constant(data[col_x], prepend=True)
    y_true = data[col_y]

    y_pred = modelo.predict(exog=X)

    rmse = mean_squared_error(y_true, y_pred, squared=False)
    return rmse

def calcular_bondad(modelo, ruta_archivo, col_x, col_y):
    # Utilizar la función cargar_datos del módulo seleccion_columna para cargar el archivo
    data = cargar_datos(ruta_archivo)

    X = sm.add_constant(data[col_x], prepend=True)
    y_true = data[col_y]

    y_pred = modelo.predict(exog=X)

    ssr = ((y_true - y_pred) ** 2).sum()
    sst = ((y_true - y_true.mean()) ** 2).sum()

    r_cuadrado = 1 - (ssr / sst)
    return r_cuadrado

def obtener_ecuación(modelo): 
    # Obtener los coeficientes del modelo
    coeficientes = modelo.params

    # Crear la ecuación como una cadena de texto
    ecuacion = "y = " + str(coeficientes[0])
    for i in range(1, len(coeficientes)):
        if coeficientes[i] >= 0:
            ecuacion += " + " + str(coeficientes[i]) + "*x"
        else: 
            ecuacion += str(coeficientes[i]) + "*x"

    return ecuacion

def prediccion(ruta_archivo, col_x, col_y, valor_x):
    modelo = ajustar_modelo(ruta_archivo, col_x, col_y)
    ecuacion = obtener_ecuación(modelo)

    # Usamos una expresión regular para extraer los coeficientes de la ecuación
    final_ecu = str(ecuacion)

    match = re.search(r'y = ([-\d.]+)-([\d.]+)\*x', final_ecu)

    if match:
        m = float(match.group(1))  # coeficiente de x
        b = float(match.group(2))  # término independiente
    else:
        raise ValueError(f"No se pudieron extraer los coeficientes de la ecuación '{ecuacion}'")
    
    prediccion = (m * valor_x) + b 

    return prediccion