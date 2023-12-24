"""

1. DESCRIPCION 
La aplicacion es un generador de modelos de progresiones lineales, que permite mostrar sus datos y realizar predicciones, con modelos guardados  anteriormente (en .txt) o con archivos con las extensiones .csv, .xlsx, .db.

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
De ahi, pones en la terminal "pyhton main_GUI.py" y se ejecutará sin problemas el generador de modelos.

3. USO
Nada mas ejecutar el archivo main_GUI.py, aparecerá por pantalla una ventana que da las siguientes opciones:
- Examinar. Si pulsas aquí, te llevará a tus repositorios donde solo podras seleccionar archivos de tipo csv, excel y bases de datos 
            para que todo funcione correctamente. Al darle a aceptar, saldrá la ruta del archivo escogido en el hueco blanco de al lado. 
            Además, se abrirá la selección de columnas con el nombre de cada columna puesto en los archivos, mostrando debajo de cada 
            selección la variable seleccionada. Una vez seleccionadas las columnas, unicamente tenemos la opción de "crear modelo". 
            Seguidamente, aparecera la grafica correspondiente al modelo, su respectivo RMSE y el coeficiente de determinación. 
            En este punto, tenemos la opcion de guardar modelo (en un .txt), cargar modelo (seleccionando un .txt) o volver a crear
            otro modelo con la selecion de archivos y columnas. Tambien aparece una formula para la prediccion, para que cambiando la pendiente 
            y la constante, cambie así de nuevo todo el modelo.

- Cargar. Te llevará a tus repositorios donde tendrás que seleccionar un .txt guardado con anterioridad con los parámetros del modelo. Al seleccionar
          el archivo, te mostrará la gráfica del modelo creado, junto con el RMSE, el coeficiente de determinación, la formula de la prediccion, 
          las opciones de cargar y guardar o volver a crear el modelo de 0.

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

