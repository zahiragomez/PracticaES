import pandas as pd
import sqlite3

def importar_archivo(ruta_archivo):
    # Obtener la extensión del archivo
    extension = ruta_archivo.split(".")[-1].lower()
    
    if extension == "csv":
        df = pd.read_csv(ruta_archivo)
        print("El archivo CSV se ha importado correctamente.")
    elif extension == "xlsx" or extension == "xls":
        df = pd.read_excel(ruta_archivo)
        print("El archivo Excel se ha importado correctamente.")
    elif extension == "db":
        conn = sqlite3.connect(ruta_archivo)
        df = pd.read_sql_query("SELECT * FROM california_housing_dataset", conn)
        conn.close()
        print("La base de datos se ha importado correctamente.")
    else:
        print("Extensión de archivo no compatible.")
        return None
    
    return df



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