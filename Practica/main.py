import pandas as pd
from funciones_auxiliares import importar_archivo_csv, importar_archivo_excel, importar_archivo_db
from funciones_auxiliares import asociar_valores_csv, asociar_valores_excel, asociar_valores_db
from modelo_regresion_lineal import modelo_regresion


    #esto furrula?
    # Rutas archivos: 
    # Samuel: f:\Uni_IA\2ºaño\ES\Otros\housing.xlsx
    # Zahira:
    # Ainhoa: "C:\Users\lovea\Downloads\housing.db"
    # Lidia: "/Users/lidiacaneiropardo/Downloads/housing.db"

def main():
    archivoCSV = importar_archivo_csv(r"f:\Uni_IA\2ºaño\ES\Otros\housing.csv")
    archivoEXCEL = importar_archivo_excel(r"f:\Uni_IA\2ºaño\ES\Otros\housing.xlsx")
    archivoSQL = importar_archivo_db(r"f:\Uni_IA\2ºaño\ES\Otros\housing.db")


    print(f"archivo csv:\n {archivoCSV}")
    print(f"archivo excel:\n {archivoEXCEL}")
    print(f"archivo sql:\n {archivoSQL}")


    selColumnaCSV = asociar_valores_csv(r"f:\Uni_IA\2ºaño\ES\Otros\housing.csv")
    selColumnaEXCEL = asociar_valores_excel(r"f:\Uni_IA\2ºaño\ES\Otros\housing.xlsx")
    selColumnaSQL = asociar_valores_db(r"f:\Uni_IA\2ºaño\ES\Otros\housing.db")

    print(f"archivo csv:\n {selColumnaCSV}")
    print(f"archivo excel:\n {selColumnaEXCEL}")
    print(f"archivo sql:\n {selColumnaSQL}")


    modeloCSV = modelo_regresion(archivoCSV)
    

    print(f"R^2, MSE: {modeloCSV}")
    




if __name__ == "__main__":
    main()


    

