import pandas as pd
from funciones_auxiliares import importar_archivo_csv, importar_archivo_excel, importar_archivo_db
from funciones_auxiliares import asociar_valores_csv, asociar_valores_excel, asociar_valores_db
from modelo_regresion_lineal import test_modelos


    #esto furrula?
    # Rutas archivos: 
    # Samuel: f:\Uni_IA\2ºaño\ES\Otros\housing.xlsx
    # Zahira: c:\Users\Usuario\Downloads
    # Ainhoa: "C:\Users\lovea\Downloads\housing.db"
    # Lidia: "/Users/lidiacaneiropardo/Downloads/housing.db"

def main():
    archivoCSV = importar_archivo_csv()
    archivoEXCEL = importar_archivo_excel()
    archivoSQL = importar_archivo_db()


    print(f"archivo csv:\n {archivoCSV}")
    print(f"archivo excel:\n {archivoEXCEL}")
    print(f"archivo sql:\n {archivoSQL}")


    selColumnaCSV = asociar_valores_csv(r"c:\Users\Usuario\Downloads\housing.csv")
    selColumnaEXCEL = asociar_valores_excel(r"c:\Users\Usuario\Downloads\housing.xlsx")
    selColumnaSQL = asociar_valores_db(r"c:\Users\Usuario\Downloads\housing.db")

    print(f"archivo csv:\n {selColumnaCSV}")
    print(f"archivo excel:\n {selColumnaEXCEL}")
    print(f"archivo sql:\n {selColumnaSQL}")


    modeloCSV = test_modelos(archivoCSV)
    

    print(f"R^2, MSE: {modeloCSV}")
    




if __name__ == "__main__":
    main()


    

