import pickle
import statsmodels.api as sm
import numpy as np

def guardar(ruta_archivo, col_x, col_y, rmse, modelo):
    with open(ruta_archivo, 'wb') as f:
        pickle.dump({
            'col_x': col_x,
            'col_y': col_y,
            'rmse': rmse,
            'modelo': {
                'params': modelo.params.tolist(),  # Guardar los coeficientes
                'rsquared': modelo.rsquared,       # Guardar el R^2
            },
        }, f)

def cargar(ruta_archivo):
    try:
        with open(ruta_archivo, 'rb') as f:
            data = pickle.load(f)

        col_x = data['col_x']
        col_y = data['col_y']
        rmse = data['rmse']
        modelo_data = data['modelo']

        # Recuperar el modelo y los coeficientes
        modelo = sm.OLS(np.array([]), np.array([]))  # Crear un modelo vacío
        modelo.params = np.array(modelo_data['params'])
        modelo.rsquared = modelo_data['rsquared']

        return col_x, col_y, rmse, modelo
    except Exception as e:
        print(f"Error: No se pudo cargar el modelo. Detalles: {str(e)}")
        return None