import pandas as pd

def asociar_valores_csv(ruta_csv): 
    # Lee el archivo CSV
    df = pd.read_csv(ruta_csv)

    # Añade nombres a las filas
    df.index = [i for i in range(1, len(df) + 1)]

    # Pide al usuario que introduzca el nombre de una fila
    nombre_fila_seleccionada = 20640 

    # Comprueba si el nombre introducido por el usuario es válido
    if nombre_fila_seleccionada in df.index:
        # Si es válido, selecciona la fila
        fila_seleccionada = df.iloc[nombre_fila_seleccionada - 1] # Restamos 1 porque iloc[] es de base 0
        # Imprime la fila seleccionada
        #print(fila_seleccionada)
        return fila_seleccionada
    else:
        #print('El nombre introducido no corresponde a ninguna fila.')
        return None

def asociar_valores_excel(ruta_excel): 
    # Lee el archivo Excel
    df = pd.read_excel(ruta_excel)

    # Añade nombres a las filas
    df.index = [i for i in range(1, len(df) + 1)]

    # Pide al usuario que introduzca el nombre de una fila
    nombre_fila_seleccionada = 20640 

    # Comprueba si el nombre introducido por el usuario es válido
    if nombre_fila_seleccionada in df.index:
        # Si es válido, selecciona la fila
        fila_seleccionada = df.iloc[nombre_fila_seleccionada - 1] # Restamos 1 porque iloc[] es de base 0
        # Imprime la fila seleccionada
        #print(fila_seleccionada)
        return fila_seleccionada
    else:
        #print('El nombre introducido no corresponde a ninguna fila.')
        return None