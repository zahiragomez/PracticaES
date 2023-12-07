import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename()
    return ruta_archivo

def cargar_datos(ruta_archivo):
    try:
        df = pd.read_csv(ruta_archivo)
        return df
    except pd.errors.EmptyDataError:
        print("Error: El archivo está vacío")
        return None
    except pd.errors.ParserError:
        print("Error: Error al analizar el archivo CSV")
        return None

def obtener_columnas_numericas(df):
    return df.select_dtypes(include=[np.number]).columns.tolist()