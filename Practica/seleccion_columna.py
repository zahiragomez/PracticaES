from tkinter import filedialog
import pandas as pd
import numpy as np
import sqlite3
import os
import pickle

def ruta():
    ruta_archivo = filedialog.askopenfilename()
    return ruta_archivo

def cargar_datos(ruta_archivo):
    try:
        # Use os.path.splitext to handle both forward and backward slashes
        _, extension = os.path.splitext(ruta_archivo)
        extension = extension.lower()

        if extension == ".csv":
            df = pd.read_csv(ruta_archivo)
        elif extension == ".xlsx":
            df = pd.read_excel(ruta_archivo, engine='openpyxl')
        elif extension == ".db":
            conn = sqlite3.connect(ruta_archivo)
            df = pd.read_sql_query("SELECT * FROM california_housing_dataset", conn)
            conn.close()
        elif extension == ".pkl":
            # If the extension is pkl, assume it's a Pickle file and load it
            with open(ruta_archivo, 'rb') as f:
                df = pickle.load(f)
        else:
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
