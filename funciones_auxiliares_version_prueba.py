import pandas as pd

def importar_archivo_csv(ruta_csv):
    #Para llamar a la función, sería importar_archivo_csv(r"c:\Users\Usuario\Downloads\housing.csv")"
    path_csv = pd.read_csv(ruta_csv)
    print("El archivo csv se ha importado de forma correcta")
    #Para hacer pruebas: 
    #print(path_csv.head())

def importar_archivo_excel(ruta_excel):
    #Para llamar a la función, sería importar_archivo_excel(r"c:\Users\Usuario\Downloads\housing.xlsx")
    path_excel = pd.read_excel(ruta_excel)
    print("El archivo excel se ha importado de forma correcta")
    #Para hacer pruebas: 
    #print(path_excel.head())


def asociar_valores_csv(ruta_csv): 
    # Lee el archivo CSV
    ruta_csv = input("Introduzca la ruta del archivo .csv: ")
    df = importar_archivo_csv(ruta_csv)

    # Añade nombres a las filas

    df.row = [i for i in range(1, len(df) + 1)]
    df.column = [i for i in range(1, len(df) + 1)]

    # Pide al usuario que introduzca el nombre de una fila

    nombre_fila_seleccionada = int(input("Introduzca el índice de la fila a seleccionar: "))
    nombre_columna_seleccionada = int(input("Introduzca el índice de la columna a seleccionar: "))

    # Comprueba si el nombre introducido por el usuario es válido

    if nombre_fila_seleccionada in df.row:
        # Si es válido, selecciona la fila
        fila_seleccionada = df.iloc[nombre_fila_seleccionada - 1] # Restamos 1 porque iloc[] es de base 0
        # Imprime la fila seleccionada
        print(fila_seleccionada)
    else:
        print('El nombre introducido no corresponde a ninguna fila.')

    if nombre_columna_seleccionada in df.column:
        # Si es válido, selecciona la fila
        columna_seleccionada = df.iloc[nombre_columna_seleccionada - 1] # Restamos 1 porque iloc[] es de base 0
        # Imprime la fila seleccionada
        print(columna_seleccionada)
    else:
        print('El nombre introducido no corresponde a ninguna columna.')

def asociar_valores_excel(ruta_excel): 
    # Lee el archivo CSV
    ruta_excel = input("Introduzca la ruta del archivo .xslx: ")
    df = importar_archivo_excel(ruta_excel)

    # Añade nombres a las filas

    df.row = [i for i in range(1, len(df) + 1)]
    df.column = [i for i in range(1, len(df) + 1)]

    # Pide al usuario que introduzca el nombre de una fila

    nombre_fila_seleccionada = int(input("Introduzca el índice de la fila a seleccionar: "))
    nombre_columna_seleccionada = int(input("Introduzca el índice de la columna a seleccionar: "))

    # Comprueba si el nombre introducido por el usuario es válido

    if nombre_fila_seleccionada in df.row:
        # Si es válido, selecciona la fila
        fila_seleccionada = df.iloc[nombre_fila_seleccionada - 1] # Restamos 1 porque iloc[] es de base 0
        # Imprime la fila seleccionada
        print(fila_seleccionada)
    else:
        print('El nombre introducido no corresponde a ninguna fila.')

    if nombre_columna_seleccionada in df.column:
        # Si es válido, selecciona la fila
        columna_seleccionada = df.iloc[nombre_columna_seleccionada - 1] # Restamos 1 porque iloc[] es de base 0
        # Imprime la fila seleccionada
        print(columna_seleccionada)
    else:
        print('El nombre introducido no corresponde a ninguna columna.')

