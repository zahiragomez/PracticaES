import pandas as pd

ruta_del_archivo_csv = r"C:\Users\lovea\Downloads\housing.csv"
path_csv = pd.read_csv(ruta_del_archivo_csv)
print(path_csv.head())

ruta_del_archivo_excel = r"C:\Users\lovea\Downloads\housing.xlsx"
path_excel = pd.read_excel(ruta_del_archivo_excel)
(path_excel.head())


