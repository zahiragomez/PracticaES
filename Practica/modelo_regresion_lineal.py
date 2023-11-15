import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
#Para persistir datos
import pickle
import  matplotlib.pyplot as plt

def test_modelos():
    # Read the CSV file into a DataFrame
    data = pd.read_csv(r"c:\Users\Usuario\Downloads\housing.csv")

    # Display the first few rows of the DataFrame
    print("CSV Data:")
    print(data.head())

    # Allow the user to input multiple column names for X
    x_columns = input("Introduce las columnas para las X (separa con comas): ").split(',')
    y_column = input("Introduce la columnas para Y: ")

    # Verificar que las columnas ingresadas por el usuario son numéricas
    numeric_columns = data.select_dtypes(include='number').columns.tolist()
    
    for col in x_columns + [y_column]:
        if col not in numeric_columns:
            print(f"La columna {col} no es numérica. Por favor, elige columnas numéricas.")
            return  # Salir de la función si se encuentra una columna no numérica

   # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Correlación lineal entre las dos variables
    corr_test = pearsonr(x=data[x_columns[0]], y=data[y_column])
    print("Coeficiente de correlación de Pearson: ", corr_test[0])
    print("P-value: ", corr_test[1])

    for x_column in x_columns:
        ax.scatter(data[x_column], data[y_column], label=x_column)

    ax.set_title(f'Distribución de {", ".join(x_columns)} y {y_column}')
    ax.legend()
    plt.show()

    # División de los datos en train y test
    X = data[x_columns]
    y = data[y_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        train_size=0.8,
        random_state=1234,
        shuffle=True
    )

    # Creación del modelo utilizando matrices como en scikit-learn
    X_train = sm.add_constant(X_train, prepend=True)
    modelo = sm.OLS(endog=y_train, exog=X_train)
    modelo = modelo.fit()
    print(modelo.summary())

    # Intervalos de confianza para los coeficientes del modelo
    print("Intervalos de confianza para los coeficientes del modelo:")
    print(modelo.conf_int(alpha=0.05))

    # Predicciones con intervalo de confianza del 95%
    predicciones = modelo.get_prediction(exog=X_train).summary_frame(alpha=0.05)
    predicciones['x'] = X_train[X_train.columns[1]]
    predicciones['y'] = y_train
    predicciones = predicciones.sort_values('x')

    # Gráfico del modelo
    fig, ax = plt.subplots(figsize=(6, 3.84))
    for column in X_train.columns[1:]:
        ax.scatter(X_train[column], y_train, label=column)

    ax.set_title('Distribución de las columnas de X y Y')
    ax.legend()
    plt.show()

    # Error de test del modelo
    X_test = sm.add_constant(X_test, prepend=True)
    predicciones = modelo.predict(exog=X_test)
    rmse = mean_squared_error(
        y_true=y_test,
        y_pred=predicciones,
        squared=False
    )
    print("")
    print(f"El error (rmse) de test es: {rmse}")

    #Guarda los datos en un archivo csv
    data.to_csv("datos.csv",index=False)
    #Guarda el modelo en un archivo binario usando pickle
    with open("modelo.pkl", "wb") as f:
        pickle.dump(modelo, f)

if __name__ == "__main__":
    test_modelos()
