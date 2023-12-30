import unittest
import tkinter as tk
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import style
import  os
from funciones_auxiliares import guardar, cargar
from seleccion_columna import ruta, cargar_datos
from analisis_modelo import ajustar_modelo, calcular_rmse, prediccion


# Configuración matplotlib
# ==============================================================================
plt.rcParams['image.cmap'] = "bwr"
#plt.rcParams['figure.dpi'] = "100"
plt.rcParams['savefig.bbox'] = "tight"
style.use('ggplot') or plt.style.use('ggplot')

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')

class TestFuncionesAuxiliares(unittest.TestCase):

    def test_interfaz(self):

        print ("Test GUI")
        ruta_archivo = ruta()
        df = cargar_datos(ruta_archivo)

        #Muestra la primera columna del archivo
        primera_columna= df.columns[0]

        #Crea el objeto ventana
        ventana_prueba = tk.Tk() 

        #Dimensiones
        ventana_prueba.geometry("800x500")  

        #Color del fondo
        ventana_prueba.configure(background="light blue") 

        #Titulo de la ventana
        tk.Wm.wm_title(ventana_prueba, "Generador de modelos (test) ") 

        #Crea un boton
        tk.Button(

            #Lo enlaza con la ventana creada
            ventana_prueba,

            #Texto dentro del botón
            text= primera_columna,

            #Fuente del texto
            font = ("Comfortaa", 15),

            #Fondo de la ventana (codigo del color en hexadecimal)
            bg = "#FFB4CE", 

            
            fg = "white"
            
        ).pack( #comando necesario para que vaya

            #Se amplia al eje X e Y
            fill = tk.BOTH, 

            #Se expande al redimensionar la ventana
            expand = True,
        )

        #Etiqueta
        tk.Label(

            #Llama al objeto ventana
            ventana_prueba,

            #Texto de la etiqueta
            text = "Pulse arriba para generar modelo",

            #Formato del texto
            font = ("Comfortaa", 15, "bold"),

            fg = "pink",

            bg = "white",

            #Que se centre
            justify = "center"

        ).pack(
            fill = tk.BOTH, 
            expand = True,
        )

        #para que salga la ventana
        ventana_prueba.mainloop()
    

    def test_modelos(self):
        print("Test modelos")

        #Simula la ruta del archivo (reemplaza con tu ruta real)
        ruta_archivo = ruta()

        #Intenta cargar los datos y verifica si se ha cargado correctamente
        data = cargar_datos(ruta_archivo)

        if data is None:
            raise ValueError("No se pudieron cargar los datos desde el archivo. Verifica la ruta del archivo y el método cargar_datos.")

        #Verifica que hay al menos dos columnas en el conjunto de datos
        if len(data.columns) < 2:
            raise ValueError("El conjunto de datos debe contener al menos dos columnas para el análisis")

        #Selecciona las dos primeras columnas automaticamente
        col_x = data.columns[0]  #Simplemente usa las dos primeras columnas del DataFrame
        col_y = data.columns[1]

        modelo = ajustar_modelo(ruta_archivo, col_x, col_y)

        if modelo:
            print(f"El modelo ha sido ajustado correctamente.")

        else:
            print("No se ha podido generar el modelo.")
       
        
    def test_cargar_datos(self): 

        print("Test cargar datos del modelo")


        ruta_archivo = ruta()
        df = cargar_datos(ruta_archivo)
        extension = os.path.splitext(ruta_archivo)[1].lower()

        #Prueba diferentes extensiones y compara resultados
        if extension == ".csv":
            df_csv = pd.read_csv(ruta_archivo)
            assert df.equals(df_csv)
            print("El archivo csv se ha importado corectamente:", ruta_archivo)

        elif extension == ".xlsx":
            df_xlsx = pd.read_excel(ruta_archivo, engine='openpyxl')
            assert df.equals(df_xlsx)
            print("El archivo xlsx se ha importado corectamente:", ruta_archivo)

        elif extension == ".db":
           conn = sqlite3.connect(ruta_archivo)
           df_db = pd.read_sql_query("SELECT * FROM california_housing_dataset", conn)
           conn.close
           assert df.equals(df_db)
           print("El archivo db se ha importado corectamente:", ruta_archivo)

        else:
            print("El archivo no tiene la extensión necesaria o no ha sido seleccionado")


    def test_calcular_rmse(self):

        print("Test para RMSE")


        ruta_archivo = ruta()
      
        #Solicita al usuario los nombres de las columnas
        col_x = input("Nombre de la columna x seleccionada:")
        col_y = input("Nombre de la columna y seleccionada:")

        modelo = ajustar_modelo(ruta_archivo, col_x, col_y)

        rmse = calcular_rmse(modelo, ruta_archivo, col_x, col_y)

        # Comprueba que el RMSE es un número flotante 
        self.assertIsInstance(rmse, float)

        # Comprueba que el RMSE es mayor o igual a cero
        self.assertGreaterEqual(rmse, 0.0)

        print("El RMSE se ha calculado de forma correcta", rmse)


    def test_guardar_cargar(self):

        print("Test guardar y cargar")
        ruta_archivo = ruta()
    
        #Abre el archivo y lee lineas
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            if len(lineas) != 3:
                raise ValueError("El archivo debe contener tres líneas con los datos")

        col_x = lineas[0].strip()  #Se lee la primera linea como col_x
        col_y = lineas[1].strip()  #La segunda linea como col_y
        rmse = float(lineas[2].strip())  #La tercera linea como rmse (convertida a float)

        guardar("modelo_guardado.txt", col_x, col_y, rmse)
    
        #Cargar datos desde el archivo
        datos = cargar("modelo_guardado.txt")
    
        #Verificar los datos cargados
        assert datos[0] == col_x
        assert datos[1] == col_y
        assert datos[2] == rmse

        print("Se ha cargado el modelo con los datos del archivo correctamente.")

    def test_prediccion(self):

        print("Test predicción")
        ruta_archivo = ruta()
    
        col_x = input("Nombre de la columna x seleccionada:")
        col_y = input("Nombre de la columna y seleccionada:")

        valor_x = float(input("Valor de x para hacer la predicción:"))

        resultado = prediccion(ruta_archivo, col_x, col_y, valor_x)
    
        # Comprueba que el RMSE es un número flotante 
        self.assertIsInstance(resultado, float)

        print("La predicción se ha calculado de forma correcta", resultado)

if __name__ == "__main__":
    unittest.main()
