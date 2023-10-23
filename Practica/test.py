import unittest
from funciones_auxiliares import importar_archivo_csv, importar_archivo_excel

class TestFuncionesAuxiliares(unittest.TestCase):

    def test_importar_csv(self):
        # Prueba para importar un archivo CSV
        resultado = importar_archivo_csv(r"c:\Users\Usuario\Downloads\housing.csv")
        self.assertIsNotNone(resultado)
        
    def test_importar_excel(self):
        # Prueba para importar un archivo Excel
        resultado = importar_archivo_excel(r"c:\Users\Usuario\Downloads\housing.xlsx")
        self.assertIsNotNone(resultado)
        
if __name__ == "__main__":
    unittest.main()