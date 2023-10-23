import unittest
import pandas as pd 
from funciones_auxiliares import importar_archivo_csv
import tempfile

class TestFuncionesAuxiliares(unittest.TestCase):

    def test_importar_csv(self):
        # Ruta al archivo de prueba
        archivo_prueba = r"c:\Users\Usuario\Downloads\housing.csv"  

        # Leer el contenido del archivo original
        with open(archivo_prueba, 'r') as archivo_original:
            contenido_original = archivo_original.read()

        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            archtemp = temp_file.name
            temp_file.write(contenido_original)

        try:
            # Prueba para importar un archivo CSV
            resultado = importar_archivo_csv(archtemp)

            # Verifica que el resultado no sea nulo
            self.assertIsNotNone(resultado)

            # Convierte el contenido original en un DataFrame directamente
            df_original = pd.read_csv(archtemp)

            # Compara los DataFrames
            self.assertTrue(df_original.equals(resultado))
        finally:
            # Borra el archivo temporal
            import os
            os.remove(archtemp)
if __name__ == "__main__":
    unittest.main()
