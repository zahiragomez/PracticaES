import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import os

def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename()
    return ruta_archivo

def cargar_datos(ruta_archivo):
    try:
        # Obtener la extensión del archivo
        extension = os.path.splitext(ruta_archivo)[1].lower()

        if extension == ".csv":
            # Si la extensión es CSV, intenta cargar como CSV
            df = pd.read_csv(ruta_archivo)
        elif extension == ".xlsx":
            # Si la extensión es XLSX, intenta cargar como Excel con el motor openpyxl
            df = pd.read_excel(ruta_archivo, engine='openpyxl')
        else:
            # Si la extensión no es reconocida, muestra un mensaje de error
            print(f"Error: Extensión de archivo no compatible: {extension}")
            return None

        return df
    except pd.errors.EmptyDataError:
        print("Error: El archivo está vacío")
        return None
    except pd.errors.ParserError:
        print(f"Error: Error al analizar el archivo {extension}")
        return None
    except Exception as e:
        print(f"Error: No se pudo cargar el archivo. Detalles: {str(e)}")
        return None
    
def obtener_columnas_numericas(df):
    return df.select_dtypes(include=[np.number]).columns.tolist()