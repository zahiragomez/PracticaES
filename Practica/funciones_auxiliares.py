import pandas as pd

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
        print(columna_seleccionada)
    else:
        print('El índice introducido no corresponde a ninguna columna.')

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
        print(columna_seleccionada)
    else:
        print('El índice introducido no corresponde a ninguna columna.')
