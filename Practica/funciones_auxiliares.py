import pandas as pd
import sqlite3

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

def importar_archivo():
    ruta_archivo = filedialog.askopenfilename()
    return ruta_archivo

def cargar_datos(ruta_archivo):
    try:
        # Intenta cargar como CSV
        df = pd.read_csv(ruta_archivo)
        return df
    except pd.errors.EmptyDataError:
        print("Error: El archivo está vacío")
        return None
    except pd.errors.ParserError:
        print("Error: Error al analizar el archivo CSV")
        return None
    except Exception as e:
        # Si no es un archivo CSV, intenta cargar como Excel
        try:
            df = pd.read_excel(ruta_archivo)
            return df
        except pd.errors.EmptyDataError:
            print("Error: El archivo está vacío")
            return None
        except pd.errors.ParserError:
            print("Error: Error al analizar el archivo Excel")
            return None
        except Exception as e:
            print(f"Error: No se pudo cargar el archivo. Detalles: {str(e)}")
            return None

def obtener_columnas_numericas(df):
    return df.select_dtypes(include=[np.number]).columns.tolist()

def asociar_valores(ruta_archivo):
    # Lee el archivo dependiendo de la extensión
    df = importar_archivo(ruta_archivo)

    # Añade nombres a las columnas
    df['column'] = [i for i in range(1, len(df) + 1)]

    # Pide al usuario que introduzca el índice de una columna
    nombre_columna_seleccionada = int(input("Introduzca el índice de la columna a seleccionar: "))

    # Comprueba si el índice introducido por el usuario es válido
    if nombre_columna_seleccionada in df['column']:
        # Si es válido, selecciona la columna
        columna_seleccionada = df.iloc[:, nombre_columna_seleccionada - 1]  # Restamos 1 porque iloc[] es de base 0
        # Imprime la columna seleccionada
        return columna_seleccionada
    else:
        #print('El índice introducido no corresponde a ninguna columna.')
        return None
    
def guardar(ruta_archivo, col_x, col_y, rmse):
    with open(ruta_archivo, 'wt') as f:
        f.write(f'{col_x}\n')
        f.write(f'{col_y}\n')
        f.write(f'{rmse}\n')

def cargar(ruta_archivo):
    with open(ruta_archivo, 'rt') as f:
        lines = f.readlines()

    return (lines[0].strip(), lines[1].strip(), float(lines[2].strip()))