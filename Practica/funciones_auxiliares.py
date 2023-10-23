import pandas as pd

def importar_archivo_csv(ruta_csv):
    #Para llamar a la función, sería importar_archivo_csv(r"C:\Users\lovea\Downloads\housing.csv")"
    path_csv = pd.read_csv(ruta_csv)
    return path_csv
    #print("El archivo csv se ha importado de forma correcta")
    #Para hacer pruebas: 
    #print(path_csv.head())

def importar_archivo_excel(ruta_excel):
    #Para llamar a la función, sería importar_archivo_excel(r"C:\Users\lovea\Downloads\housing.xlsx")
    path_excel = pd.read_excel(ruta_excel)
    return path_excel
    #print("El archivo excel se ha importado de forma correcta")
    #Para hacer pruebas: 
    #print(path_excel.head())


