import pandas as pd

ruta_del_archivo_csv = r"c:\Users\User\Downloads\housing.csv"
path_csv = pd.read_csv(ruta_del_archivo_csv)
print(path_csv.head())

ruta_del_archivo_excel = r"c:\Users\User\Downloads\housing.xlsx"
path_excel = pd.read_excel(ruta_del_archivo_excel)
print(path_excel.head())