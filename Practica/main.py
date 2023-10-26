import pandas as pd
import unittest
from funciones_auxiliares import importar_archivo_csv
from funciones_auxiliares import importar_archivo_excel
from test import TestFuncionesAuxiliares
from valores_filas import asociar_valores_csv
from valores_filas import asociar_valores_excel

    # Rutas archivos: 
    # Samuel: f:\Uni_IA\2ºaño\ES\Otros\housing.xlsx
    # Zahira:
    # Ainhoa:
    # Lidia: 

def main():
    resultado1 = importar_archivo_csv(r"f:\Uni_IA\2ºaño\ES\Otros\housing.csv")
    resultado2 = importar_archivo_excel(r"f:\Uni_IA\2ºaño\ES\Otros\housing.xlsx")

    print(f"archivo csv:\n {resultado1}")
    print(f"archivo excel:\n {resultado2}")


    selFila1 = asociar_valores_csv(r"f:\Uni_IA\2ºaño\ES\Otros\housing.csv")
    selFila2 = asociar_valores_excel(r"f:\Uni_IA\2ºaño\ES\Otros\housing.xlsx")

    print(f"archivo csv:\n {selFila1}")
    print(f"archivo excel:\n {selFila2}")


# def ejecutar_test():
#     loader = unittest.TestLoader()
#     suite = loader.loadTestsFromModule(TestFuncionesAuxiliares)
#     runner = unittest.TextTestRunner()
#     runner.run(suite)


if __name__ == "__main__":
    main()
    # Pruebas del test
    #ejecutar_test()


    

