import pandas as pd
from funciones_auxiliares import importar_archivo
from funciones_auxiliares import asociar_valores
from modelo_regresion_lineal import test_modelos


    #esto furrula?
    # Rutas archivos: 
    # Samuel: f:\Uni_IA\2ºaño\ES\Otros\housing.xlsx
    # Zahira:
    # Ainhoa: "C:\Users\lovea\Downloads\housing.db"
    # Lidia: "/Users/lidiacaneiropardo/Downloads/housing.db"

def main():
    archivo = importar_archivo("/Users/lidiacaneiropardo/Desktop/archivos/housing.xlsx")

    print(f"archivo csv:\n {archivo}")

    selColumna = asociar_valores("/Users/lidiacaneiropardo/Desktop/archivos/housing.xlsx")

    print(f"archivo csv:\n {selColumna}")

    modelo = test_modelos(archivo)
    
    print(f"R^2, MSE: {modelo}")
    

if __name__ == "__main__":
    main()


    

