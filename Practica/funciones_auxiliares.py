import pickle
import statsmodels.api as sm
import numpy as np


def guardar(ruta_archivo, col_x, col_y, rmse, modelo):
    try:
        with open(ruta_archivo, 'wb') as f:
            pickle.dump({
                'col_x': col_x,
                'col_y': col_y,
                'rmse': rmse,
                'modelo': {
                    'params': modelo.params.tolist() if modelo.params is not None else None,
                    'rsquared': modelo.rsquared if modelo.rsquared is not None else None,
                },
            }, f)
        print(f"Modelo guardado exitosamente en '{ruta_archivo}'.")
        
    except Exception as e:
        print(f"Error: No se pudo guardar el modelo. Detalles: {str(e)}")


def cargar(ruta_archivo):
    try:
        with open(ruta_archivo, 'rb') as f:
            data = pickle.load(f)

        col_x = data.get('col_x')
        col_y = data.get('col_y')
        rmse = data.get('rmse')
        modelo_data = data.get('modelo')

        if col_x is None or col_y is None or rmse is None or modelo_data is None:
            raise ValueError("El archivo no contiene la información necesaria.")

        modelo_params = modelo_data.get('params')
        modelo_rsquared = modelo_data.get('rsquared')

        if modelo_params is None or modelo_rsquared is None:
            raise ValueError("El archivo no contiene la información necesaria del modelo.")

        modelo = sm.OLS(np.zeros([1]), np.zeros([1]))
        modelo.params = np.array(modelo_params)
        modelo.rsquared = modelo_rsquared

        return col_x, col_y, rmse, modelo

    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no existe.")
        return None

    except Exception as e:
        print(f"Error al cargar el modelo. Detalles: {str(e)}")
        return None
    
def verificar_guardado(ruta_archivo):
    try:
        with open(ruta_archivo, 'rb') as f:
            data = pickle.load(f)

        print("Datos cargados desde el archivo:")
        print(data)

    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no existe.")

    except Exception as e:
        print(f"Error al cargar el modelo. Detalles: {str(e)}")