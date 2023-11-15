import pandas as pd
import pickle
import matplotlib.pyplot as plt
import statsmodels.api as sm
import  os

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

if __name__ == "__main__":
    load_and_check_files()