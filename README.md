"""

1. DESCRIPCION 
La aplicacion es un generador de modelos de progresiones lineales, que permite mostrar sus datos y realizar predicciones, con modelos guardados  anteriormente (en .pkl) o con archivos con las extensiones .csv, .xlsx, .db.

Ademas, es posible crear modelos desde 0 a partir de la propia interfaz, cargar los que se hayan hecho anteriormente y guardar todos los posibles cambios efectuados.

2. INSTALACION
Para ejecutar la aplicación, necesitaras tener instalados los siguientes paquetes de Python:
- statsmodels
- scikit-learn
- matplotlib
- pandas
- numpy

Para instalar todos estos paquetes, puedes poner en la terminal "pip install statsmodels scikit-learn matplotlib pandas numpy"
para poder trabajar con ellos.

Primero, debes descargarte el archivo .zip y descomprimirlo en descargas.
Para poder abrir la aplicación, debes entrar en la terminal y desplazarte a descargas, y seguidamente, a la carpeta interna llamada "Practica".
De ahi, pones en la terminal "python main_GUI.py" y se ejecutará sin problemas el generador de modelos.

3. USO
Nada mas ejecutar el archivo main_GUI.py, aparecerá por pantalla una ventana con la opción de examinar, que te  llevará a la gestión de tus directorios para elegir un archivo (.csv, .xlsx, .db).
Al escogerlo, saldrá a la izquierda una etiqueta con la ruta del archivo y debajo la selección de columnas con dos etiquetas que muestran cuáles están marcadas. Seguidamente, tienes la opción de cargar
un modelo de un archivo .pkl hecho con la misma aplicación y mismo archivo.

Al darle a crear modelo, aparecerá a la derecha de todo la gráfica del modelo. Debajo de la selección de columnas, aparecerán los datos del RMSE, el coeficiente de determinación y la ecuación de la grafica.
Ahí se te abrirá la opción de guardar el modelo en un archivo .pkl.
Debajo, aparece la opción para introducir un valor numérico de x, que nos dará la predicción al pulsar el botón "Predicción".
A continuación se muestran dos recuadros para añadir la pendiente y la constante, y crear un nuevo modelo al pulsar "Actualizar Gráfica".

4. ESTRUCTURA DEL PROYECTO
Al entrar en la carpeta Practica, encontraremos dos archivos ejecutables:
- test.py. Se encarga de las pruebas unitarias que comprueban que las funciones principales funcionan correctamente.
- main_GUI.py. Ejecuta la aplicación.
El resto de ficheros contienen las funciones en si a las que se llaman en los archivos ejecutables.

5. DESARROLLADORES.
- Lidia Caneiro. lidia.caneiro@udc.es
- Ainhoa de Diego. ainhoa.dediego.silva@udc.es
- Zahira Gomez. zahira.gomez@udc.es
- Samuel Fernandez. samuel.frey@udc.es

"""

