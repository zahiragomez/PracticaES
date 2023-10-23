import pandas as pd
import unittest
from funciones_auxiliares import importar_archivo_csv
from funciones_auxiliares import importar_archivo_excel
from test import TestFuncionesAuxiliares



def main():
    resultado1 = importar_archivo_csv(r"c:\Users\Usuario\Downloads\housing.csv")
    resultado2 = importar_archivo_excel(r"c:\Users\Usuario\Downloads\housing.xlsx")

    print(f"archivo csv:\n {resultado1}")
    print(f"archivo excel:\n {resultado2}")

def ejecutar_test():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(TestFuncionesAuxiliares)
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    main()
    # Pruebas del test
    ejecutar_test()


    

