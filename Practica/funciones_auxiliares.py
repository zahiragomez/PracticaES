import pandas as pd
import sqlite3

def importar_archivo_csv(ruta_csv):
    # Lee el archivo CSV y devuelve un DataFrame
    df = pd.read_csv(ruta_csv)
    print("El archivo csv se ha importado de forma correcta")
    return df

def importar_archivo_excel(ruta_excel):
    # Lee el archivo Excel y devuelve un DataFrame
    df = pd.read_excel(ruta_excel)
    print("El archivo excel se ha importado de forma correcta")
    return df

def importar_archivo_db(ruta_db):
    # Crear una conexión a la base de datos
    conn = sqlite3.connect(ruta_db)

    #### Conocer el nombre de la tabla 
    # Consulta para obtener los nombres de todas las tablas en la base de datos
    #query = "SELECT name FROM sqlite_master WHERE type='table';"

    # Ejecutar la consulta y obtener los resultados
    #tablas = pd.read_sql_query(query, conn)

    # Leer los datos de la base de datos
    df = pd.read_sql_query("SELECT * FROM california_housing_dataset", conn)
    
    return df



def asociar_valores_csv(ruta_csv):
    # Lee el archivo CSV
    df = importar_archivo_csv(ruta_csv)

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

def asociar_valores_excel(ruta_excel):
    # Lee el archivo Excel
    df = importar_archivo_excel(ruta_excel)

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

def asociar_valores_db(ruta_db):
    # Lee el archivo SQL
    df = importar_archivo_db(ruta_db)

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
