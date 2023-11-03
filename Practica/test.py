import unittest
import pandas as pd 
from funciones_auxiliares import importar_archivo_csv, importar_archivo_excel, importar_archivo_db
import tempfile
import os
import tkinter as tk

class TestFuncionesAuxiliares(unittest.TestCase):

    def test_importar_csv(self):
        # Ruta al archivo de prueba
        archivo_prueba = r"f:\Uni_IA\2ºaño\ES\Otros\housing.csv"  

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

    def test_importar_excel(self): 
        # Ruta al archivo de prueba
        archivo_prueba = r"f:\Uni_IA\2ºaño\ES\Otros\housing.xlsx"  

        # Leer el contenido del archivo original
        with open(archivo_prueba, 'r') as archivo_original:
            contenido_original = archivo_original.read()

        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            archtemp = temp_file.name
            temp_file.write(contenido_original)

        try:
            # Prueba para importar un archivo Excel
            resultado = importar_archivo_excel(archtemp)

            # Verifica que el resultado no sea nulo
            self.assertIsNotNone(resultado)

            # Convierte el contenido original en un DataFrame directamente
            df_original = pd.read_csv(archtemp)

            # Compara los DataFrames
            self.assertTrue(df_original.equals(resultado))
        except Exception as e:
                self.fail(f"La prueba falló debido a la excepción: {str(e)}")

        finally: 
            # Borra el archivo temporal
            if os.path.exists(self.archtemp):
                os.remove(self.archtemp)

    def test_interfaz(self):
        ventana_prueba = tk.Tk()
        ventana_prueba.geometry("800x500")
        ventana_prueba.configure(background="light blue")
        tk.Wm.wm_title(ventana_prueba, "Generador de modelos (test) ")

        tk.Button(
            ventana_prueba,
            text= "Generar modelo",
            font = ("Comfortaa", 15),
            bg = "#FFB4CE", #codigo del color en hexadecimal
            fg = "white"
            
        ).pack(
            fill = tk.BOTH, 
            expand = True,
        )

        tk.Label(
            ventana_prueba,
            text = "Pulse arriba para generar modelo",
            font = ("Comfortaa", 15, "bold"),
            fg = "pink",
            bg = "white",
            justify = "center"
        ).pack(
            fill = tk.BOTH, 
            expand = True,
        )
        ventana_prueba.mainloop()

if __name__ == "__main__":
    unittest.main()
