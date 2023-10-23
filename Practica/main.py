import pandas as pd
from funciones_auxiliares import importar_archivo_csv
from funciones_auxiliares import importar_archivo_excel



def main():
    resultado1 = importar_archivo_csv(r"c:\Users\Usuario\Downloads\housing.csv")
    resultado2 = importar_archivo_excel(r"c:\Users\Usuario\Downloads\housing.xlsx")

    print(f"archivo csv:\n {resultado1}")
    print(f"archivo excel:\n {resultado2}")


if __name__ == "__main__":
    main()

# Pruebas del test
import unittest
from funciones_auxiliares import importar_archivo_csv, importar_archivo_excel

class TestFuncionesAuxiliares(unittest.TestCase):
# Test para los csv
    def test_importar_csv(self):
        resultado = importar_archivo_csv(r"c:\Users\Usuario\Downloads\housing.csv")
        self.assertIsNotNone(resultado)
# Test para los xlsx
    def test_importar_excel(self):
        resultado = importar_archivo_excel(r"c:\Users\Usuario\Downloads\housing.xlsx")
        self.assertIsNotNone(resultado)

if __name__ == "__main__":
    unittest.main()
