import unittest
import tkinter as tk
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import style
import statsmodels.api as sm
import  os
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
from funciones_auxiliares import guardar, cargar
from seleccion_columna import ruta, cargar_datos
from analisis_modelo import ajustar_modelo, calcular_rmse


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

        #va a mostrar la primera columna del archivo
        primera_columna= df.columns[0]

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
            text= primera_columna,

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
    

    def test_modelos(self):
        print("Test modelos")

        ruta_archivo = ruta()
        df = cargar_datos(ruta_archivo)

        # Verificar que hay al menos dos columnas en el conjunto de datos
        if len(df.columns) < 2:
            raise ValueError("El conjunto de datos debe contener al menos dos columnas para el análisis")

        # Seleccionar las dos primeras columnas automáticamente
        col_x, col_y = df.columns[:2]

        datos = pd.DataFrame({col_x: df[col_x], col_y: df[col_y]})

        # Gráfico
        fig, ax = plt.subplots(figsize=(6, 3.84))
        datos.plot(x=col_x, y=col_y, c='firebrick', kind="scatter", ax=ax)
        ax.set_title(f'Distribución de {col_x} y {col_y}')

        # Correlación lineal entre las dos variables
        corr_test = pearsonr(x=datos[col_x], y=datos[col_y])
        print(f"Coeficiente de correlación de Pearson entre {col_x} y {col_y}: ", corr_test[0])
        print("P-value: ", corr_test[1])

        # División de los datos en train y test
        X = datos[[col_x]]
        y = datos[col_y]

        X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.8, random_state=1234, shuffle=True
         )

        # Ajuste del modelo utilizando matrices como en scikitlearn
        X_train = sm.add_constant(X_train, prepend=True)
        modelo = sm.OLS(endog=y_train, exog=X_train)
        modelo = modelo.fit()

        # Intervalos de confianza para los coeficientes del modelo
        conf_int = modelo.conf_int(alpha=0.05)

        # Predicciones con intervalo de confianza del 95%
        X_test = sm.add_constant(X_test, prepend=True)
        predicciones = modelo.get_prediction(exog=X_test).summary_frame(alpha=0.05)
    
        # Gráfico del modelo y sus intervalos de confianza
        fig, ax = plt.subplots(figsize=(6, 3.84))
        ax.scatter(X_test[col_x], y_test, marker='o', color="gray")
        ax.plot(X_test[col_x], predicciones["mean"], linestyle='-', label="OLS")
        ax.plot(X_test[col_x], predicciones["mean_ci_lower"], linestyle='--', color='red', label="95% CI")
        ax.plot(X_test[col_x], predicciones["mean_ci_upper"], linestyle='--', color='red')
        ax.fill_between(X_test[col_x], predicciones["mean_ci_lower"], predicciones["mean_ci_upper"], alpha=0.1)
        ax.legend()
        plt.show()

         # Error de test del modelo
        errores_test = y_test - modelo.predict(X_test)
        print("Errores de test del modelo:", errores_test)


    def test_cargar_datos(self): 



        print("Test cargar datos del modelo")
        ruta_archivo = ruta()
        df = cargar_datos(ruta_archivo)
        extension = os.path.splitext(ruta_archivo)[1].lower()

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
    
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            if len(lineas) != 3:
                raise ValueError("El archivo debe contener tres líneas con los datos")

        col_x = lineas[0].strip()  # Se lee la primera línea como col_x
        col_y = lineas[1].strip()  # La segunda línea como col_y
        rmse = float(lineas[2].strip())  # La tercera línea como rmse (convertida a float)

        guardar("modelo_guardado.txt", col_x, col_y, rmse)
    
        # Cargar datos desde el archivo
        datos = cargar("modelo_guardado.txt")
    
        # Verificar los datos cargados
        assert datos[0] == col_x
        assert datos[1] == col_y
        assert datos[2] == rmse

        print("Se ha cargado el modelo con los datos del archivo correctamente.")



if __name__ == "__main__":
    unittest.main()
