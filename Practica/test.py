import unittest
from funciones_auxiliares import importar_archivo
import os
import tkinter as tk
from tkinter import filedialog
import sqlite3
import shutil
import pickle
import matplotlib.pyplot as plt
import statsmodels.api as sm
import  os

#PARA LA CREACIÓN DE MODELOS
# Tratamiento de datos
# ==============================================================================
import pandas as pd
import numpy as np

# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# Preprocesado y modelado
# ==============================================================================
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import statsmodels.formula.api as smf

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

    def test_importar_archivo(self): 
        # Ruta al archivo de prueba 
        archivo_prueba = "/Users/lidiacaneiropardo/Desktop/archivos/housing.xlsx"
        archtemp = "/Users/lidiacaneiropardo/Desktop/archivos/temporal.xlsx"
        extension = archivo_prueba.split(".")[-1].lower()
        
        shutil.copy(archivo_prueba, archtemp)

        try:
            # Prueba para importar un archivo Excel
            resultado = importar_archivo(archtemp)

            # Verifica que el resultado no sea nulo
            self.assertIsNotNone(resultado)

            # Convierte el contenido original en un DataFrame directamente
            if extension == "csv":
                df_original = pd.read_csv(archtemp)
            elif extension == "xlsx" or extension == "xls":
                df_original = pd.read_excel(archtemp)
            elif extension == "db":
                conn = sqlite3.connect(archtemp)
                df_original = pd.read_sql_query("SELECT * FROM california_housing_dataset", conn)
                conn.close()

            # Compara los DataFrames
            self.assertTrue(df_original.equals(resultado))
        except Exception as e:
                self.fail(f"La prueba falló debido a la excepción: {str(e)}")

        finally: 
            # Borra el archivo temporal
            if os.path.exists(archtemp):
                os.remove(archtemp)

    def test_seleccionar_columna(self): 
        df = importar_archivo("/Users/lidiacaneiropardo/Desktop/archivos/housing.xlsx")

        # Escogemos una columna 
        col_original  = df.iloc[:, 0]

        self.assertEqual(len(col_original), 20640)
        self.assertEqual(col_original.min(), -124.35)
        self.assertEqual(col_original.max(), -114.31)

    def test_interfaz(self):
        #crea el objeto ventana
        ventana_prueba = tk.Tk() 

        #dimensiones
        ventana_prueba.geometry("800x500")  

        #color del fondo
        ventana_prueba.configure(background="light blue") 

        #título de la ventana
        tk.Wm.wm_title(ventana_prueba, "Generador de modelos (test) ") 

        #crea un botón
        tk.Button(

            #lo enlaza con la ventana creada
            ventana_prueba,

            #texto dentro del botón
            text= "Generar modelo",

            #fuente del texto
            font = ("Comfortaa", 15),

            #fondo de la ventana (codigo del color en hexadecimal)
            bg = "#FFB4CE", 

            
            fg = "white"
            
        ).pack( #comando necesario para que vaya

            #se amplia al eje X e Y
            fill = tk.BOTH, 

            #se expande al redimensionar la ventana
            expand = True,
        )

        #etiqueta
        tk.Label(

            #llama al objeto ventana
            ventana_prueba,

            #texto de la etiqueta
            text = "Pulse arriba para generar modelo",

            #formato del texto
            font = ("Comfortaa", 15, "bold"),

            fg = "pink",

            bg = "white",

            #que se centre
            justify = "center"

        ).pack(
            fill = tk.BOTH, 
            expand = True,
        )

        #para que salga la ventana
        ventana_prueba.mainloop()
    
    def load_and_check_files(model_file="modelo.pkl", data_file="datos.csv"):
    # Cargar el modelo desde el archivo binario
        with open(model_file, "rb") as f:
            loaded_model = pickle.load(f)

        # Mostrar el resumen del modelo cargado
        print("Resumen del modelo cargado:")
        print(loaded_model.summary())

        # Cargar los datos desde el archivo CSV
        loaded_data = pd.read_csv(data_file)

        # Mostrar las primeras filas de los datos cargados
        print("\nPrimeras filas de los datos cargados:")
        print(loaded_data.head())

        # Eliminar los archivos después de cargarlos y mostrar información
        try:
            os.remove(model_file)
            os.remove(data_file)
            print(f"\nArchivos '{model_file}' y '{data_file}' eliminados correctamente.")
        except FileNotFoundError:
            print("Los archivos no se encontraron. No se eliminaron.")

    def test_modelos(self):
        
        #Datos random para el test
        equipos = ["Texas","Boston","Detroit","Kansas","St.","New_S.","New_Y.",
                   "Milwaukee","Colorado","Houston","Baltimore","Los_An.","Chicago",
                   "Cincinnati","Los_P.","Philadelphia","Chicago","Cleveland","Arizona",
                   "Toronto","Minnesota","Florida","Pittsburgh","Oakland","Tampa",
                   "Atlanta","Washington","San.F","San.I","Seattle"]
        bateos = [5659,  5710, 5563, 5672, 5532, 5600, 5518, 5447, 5544, 5598,
                  5585, 5436, 5549, 5612, 5513, 5579, 5502, 5509, 5421, 5559,
                  5487, 5508, 5421, 5452, 5436, 5528, 5441, 5486, 5417, 5421]

        runs = [855, 875, 787, 730, 762, 718, 867, 721, 735, 615, 708, 644, 654, 735,
                667, 713, 654, 704, 731, 743, 619, 625, 610, 645, 707, 641, 624, 570,
                593, 556]

        datos = pd.DataFrame({'equipos': equipos, 'bateos': bateos, 'runs': runs})


        # Gráfico
        fig, ax = plt.subplots(figsize=(6, 3.84))

        datos.plot(
                    x    = 'bateos',
                    y    = 'runs',
                    c    = 'firebrick',
                    kind = "scatter",
                    ax   = ax
                    )
        ax.set_title('Distribución de bateos y runs');

        # Correlación lineal entre las dos variables
        corr_test = pearsonr(x = datos['bateos'], y =  datos['runs'])
        print("Coeficiente de correlación de Pearson: ", corr_test[0])  
        print("P-value: ", corr_test[1])

        # División de los datos en train y test
        X = datos[['bateos']]
        y = datos['runs']

        X_train, X_test, y_train, y_test = train_test_split(
                                        X.values.reshape(-1,1),
                                        y.values.reshape(-1,1),
                                        train_size   = 0.8,
                                        random_state = 1234,
                                        shuffle      = True
                                    )

        #Creación del modelo utilizando matrices como en scikitlearn

        # A la matriz de predictores se le tiene que añadir una columna de 1s para el intercept del modelo
        X_train = sm.add_constant(X_train, prepend=True)
        modelo = sm.OLS(endog=y_train, exog=X_train,)
        modelo = modelo.fit()
        print(modelo.summary())

        # Intervalos de confianza para los coeficientes del modelo
        modelo.conf_int(alpha=0.05)

        # Predicciones con intervalo de confianza del 95%

        predicciones = modelo.get_prediction(exog = X_train).summary_frame(alpha=0.05)
        predicciones['x'] = X_train[:, 1]
        predicciones['y'] = y_train
        predicciones = predicciones.sort_values('x')

        # Gráfico del modelo
        fig, ax = plt.subplots(figsize=(6, 3.84))

        ax.scatter(predicciones['x'], predicciones['y'], marker='o', color = "gray")
        ax.plot(predicciones['x'], predicciones["mean"], linestyle='-', label="OLS")
        ax.plot(predicciones['x'], predicciones["mean_ci_lower"], linestyle='--', color='red', label="95% CI")
        ax.plot(predicciones['x'], predicciones["mean_ci_upper"], linestyle='--', color='red')
        ax.fill_between(predicciones['x'], predicciones["mean_ci_lower"], predicciones["mean_ci_upper"], alpha=0.1)
        ax.legend();
        plt.show()

        # Error de test del modelo 

        X_test = sm.add_constant(X_test, prepend=True)
        predicciones = modelo.predict(exog = X_test)
        rmse = mean_squared_error(
            y_true  = y_test,
            y_pred  = predicciones,
            squared = False
                    )
        print("")
        print(f"El error (rmse) de test es: {rmse}")

    def test_importar_csv_2_0(self):
        #Comando para que la GUI busque el archivo
        ruta_csv = filedialog.askopenfilename()
        df_csv = pd.read_csv(ruta_csv)
        print("El archivo csv se ha importado de forma correcta")
        return df_csv
    
    def test_importar_excel_2_0(self):
        ruta_excel = filedialog.askopenfilename()
        df = pd.read_excel(ruta_excel)
        print("El archivo excel se ha importado de forma correcta")
        return df
        
    def test_importar_db_2_0(self):
        
        #Comando para que la GUI busque el archivo
        ruta_db = filedialog.askopenfilename() 
    
        # Crear una conexión a la base de datos
        conn = sqlite3.connect(ruta_db)

        # Leer los datos de la base de datos
        df = pd.read_sql_query("SELECT * FROM california_housing_dataset", conn)
        conn.close()

        return df
    
    def test_seleccionar_columna_csv_GUI(self): 
        # Importar los datos
        df = pd.read_csv("/Users/lidiacaneiropardo/Desktop/ES/Practica/archivos/housing.csv")

        # Lista de columnas a seleccionar
        columns = [col for col in df.columns if col != 'ocean_proximity']

        # Llamar a la función select_columns
        selected_df = df[columns]

        # Comprobar que 'ocean_proximity' no está en las columnas seleccionadas
        assert 'ocean_proximity' not in selected_df.columns

        # Comprobar que todas las demás columnas están presentes
        for column in columns:
            assert column in selected_df.columns

        print("Todas las columnas, excepto 'ocean_proximity', están presentes.")

    def test_seleccionar_columna_excel_GUI(self): 
        # Importar los datos
        df = pd.read_excel("/Users/lidiacaneiropardo/Desktop/ES/Practica/archivos/housing.xlsx")

        # Lista de columnas a seleccionar
        columns = [col for col in df.columns if col != 'ocean_proximity']

        # Llamar a la función select_columns
        selected_df = df[columns]

        # Comprobar que 'ocean_proximity' no está en las columnas seleccionadas
        assert 'ocean_proximity' not in selected_df.columns

        # Comprobar que todas las demás columnas están presentes
        for column in columns:
            assert column in selected_df.columns

        print("Todas las columnas, excepto 'ocean_proximity', están presentes.")

    def test_seleccionar_columna_BD_GUI(self): 
        # Importar los datos
        conn = sqlite3.connect("/Users/lidiacaneiropardo/Desktop/ES/Practica/archivos/housing.db")
        df = pd.read_sql_query("SELECT * FROM california_housing_dataset", conn)
        conn.close()

        # Lista de columnas a seleccionar
        columns = [col for col in df.columns if col != 'ocean_proximity']

        # Llamar a la función select_columns
        selected_df = df[columns]

        # Comprobar que 'ocean_proximity' no está en las columnas seleccionadas
        assert 'ocean_proximity' not in selected_df.columns

        # Comprobar que todas las demás columnas están presentes
        for column in columns:
            assert column in selected_df.columns

        print("Todas las columnas, excepto 'ocean_proximity', están presentes.")
    
        
    

if __name__ == "__main__":
    unittest.main()
