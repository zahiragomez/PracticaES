from tkinter import filedialog
import pandas as pd
import numpy as np
import sqlite3
import os
import pickle

#Abre un cuadro de dialogo de archivo y devuelve la ruta del archivo seleccionado
def ruta():
    ruta_archivo = filedialog.askopenfilename()
    return ruta_archivo

#Carga los datos desde un archivo segun su extension
def cargar_datos(ruta_archivo):
    try:
        #Utiliza os.path.splitext para separar el nombre del archivo y la extension
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
            #Si la extension es pkl, asume que es un archivo Pickle y lo carga
            with open(ruta_archivo, 'rb') as f:
                df = pickle.load(f)
        else:
            print(f"Error: Extensión de archivo no compatible: {extension}")
            return None

        return df

    #Maneja excepciones que pueden ocurrir durante el proceso de carga de datos
    except pd.errors.EmptyDataError:
        print("Error: El archivo está vacío")
        return None
    except pd.errors.ParserError:
        print(f"Error: Error al analizar el archivo {extension}")
        return None
    except Exception as e:
        print(f"Error: No se pudo cargar el archivo. Detalles: {str(e)}")
        return None
    
#Funcion para obtener las columnas con datos numericos de un DataFrame    
def obtener_columnas_numericas(df):
    return df.select_dtypes(include=[np.number]).columns.tolist()