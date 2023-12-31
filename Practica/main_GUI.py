import tkinter as tk
from tkinter import filedialog
from seleccion_columna import ruta, cargar_datos, obtener_columnas_numericas
from analisis_modelo import ajustar_modelo, actualizar_recta_regresion, calcular_rmse, calcular_bondad, obtener_ecuación, prediccion
import funciones_auxiliares


class PantallaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.contenedor_principal = tk.Frame(self, bg="light blue")
        self.contenedor_principal.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.frame_archivo_seleccionado = tk.Frame(self.contenedor_principal, bg="light blue")
        self.frame_archivo_seleccionado.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)


        # Contenedor para selección de columnas
        self.frame_seleccion_columnas = tk.Frame(self.contenedor_principal, bg="light blue")
        self.frame_seleccion_columnas.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

        # Contenedor para la gráfica y resultados
        self.frame_grafica_resultados = tk.Frame(self.contenedor_principal, bg="light blue")
        self.frame_grafica_resultados.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH)  # Eliminamos expand=True

        #Variables de clase para almacenar informacion
        self.col_x = None
        self.col_y = None
        self.modelo= None
        self.fig1 = None
        self.fig2 = None
        self.canvas_regresion = None
        self.rmse = None
        self.valor_x = None
        self.coeficiente_pendiente = None
        

        #Configuracion general de la pantalla principal
        self.configure(background="light blue")
        self.controller = controller
        self.ruta_seleccionada = tk.StringVar()

        self.ruta_archivo = ""
        self.variables_seleccionadas_x = []
        self.variables_seleccionadas_y = []

    

        #Indicaciones
        self.indicaciones_label = tk.Label(
            self.frame_archivo_seleccionado,
            text="(Seleccione el archivo dándole a examinar)",
            justify=tk.LEFT,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        self.indicaciones_label.grid(row=0, columnspan=3, padx=(10, 10), pady=10, sticky=tk.W)

        #Ruta del archivo
        self.ruta_label = tk.Label(
            self.frame_archivo_seleccionado,
            textvariable=self.ruta_seleccionada,
            justify=tk.CENTER,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        self.ruta_label.grid(row=1, columnspan=3, padx=(10, 10), pady=10, sticky=tk.W)

        #Boton Examinar
        self.boton_examinar = tk.Button(
            self.frame_archivo_seleccionado,
            text="Examinar",
            command=self.seleccionar_archivo,
            justify=tk.RIGHT,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        self.boton_examinar.grid(row=1, column=3, padx=(10, 10), pady=10, sticky=tk.W)

        #Boton Cargar
        self.boton_cargar = tk.Button(
            self.frame_archivo_seleccionado,
            text="Cargar",
            command=self.cargar,
            justify=tk.RIGHT,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        self.boton_cargar.grid(row=1, column=4, padx=(10, 10), pady=10, sticky=tk.W)


        #Listas de seleccion de columnas (se crean vacias inicialmente)
        self.listbox_x = None
        self.listbox_y = None
        self.etiqueta_x = None
        self.etiqueta_y = None

    #Funcion que selecciona un archivo y actualiza la interfaz grafica
    def seleccionar_archivo(self):
        self.ruta_archivo = ruta()
        if self.ruta_archivo:
            self.ruta_seleccionada.set(
                f"Ruta del archivo seleccionado: {self.ruta_archivo}"
            )
            self.actualizar_listas_columnas()

    #Funcion que maneja el cambio de columna X seleccionada
    def cambia_columna_x(self, event):
        if self.listbox_x.curselection():
            self.col_x = self.listbox_x.get(self.listbox_x.curselection())
            self.etiqueta_x.config(text=f"Variable X seleccionada: {self.col_x}")

    #Funcion que maneja el cambio de columna Y seleccionada
    def cambia_columna_y(self, event):
        if self.listbox_y.curselection():
            self.col_y = self.listbox_y.get(self.listbox_y.curselection())
            self.etiqueta_y.config(text=f"Variable Y seleccionada: {self.col_y}")

    #Funcion que actualiza las listas de seleccion de columnas
    def actualizar_listas_columnas(self):
        df = cargar_datos(self.ruta_archivo)
        if df is not None:
            columnas_numericas = obtener_columnas_numericas(df)

            #Limpia listas de seleccion
            if self.listbox_x is not None:
                self.listbox_x.destroy()
            if self.listbox_y is not None:
                self.listbox_y.destroy()

            #Crea la lista de columnas X
            self.listbox_x = tk.Listbox(self.frame_archivo_seleccionado)
            self.listbox_x.bind("<<ListboxSelect>>", self.cambia_columna_x)
            self.listbox_x.grid(row=2, column=0, padx=(10, 5), pady=10, sticky=tk.W)

            #Crea la lista de columnas Y
            self.listbox_y = tk.Listbox(self.frame_archivo_seleccionado)
            self.listbox_y.bind("<<ListboxSelect>>", self.cambia_columna_y)
            self.listbox_y.grid(row=2, column=1, padx=(5, 10), pady=10, sticky=tk.W)

            for columna in columnas_numericas:
                self.listbox_x.insert(tk.END, columna)
                self.listbox_y.insert(tk.END, columna)

            #Etiqueta para la columna X seleccionada
            self.etiqueta_x = tk.Label(
                self.frame_archivo_seleccionado,
                text=f"Variable X seleccionada: {self.col_x}",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            )
            self.etiqueta_x.grid(row=3, column=0, padx=(10, 10), pady=10, sticky=tk.W)

            #Etiqueta para la columna Y seleccionada
            self.etiqueta_y = tk.Label(
                self.frame_archivo_seleccionado,
                text=f"Variable Y seleccionada: {self.col_y}",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            )
            self.etiqueta_y.grid(row=3, column=1, padx=(10, 10), pady=10, sticky=tk.E)

            # #Nueva etiqueta para mostrar el coeficiente de la pendiente
            # self.etiqueta_coeficiente = tk.Label(
            #     self.frame_archivo_seleccionado,
            #     text="Coeficiente de Pendiente: ",
            #     font=("Comfortaa", 12),
            #     bg="light blue",
            #     fg="black",
            # )
            # self.etiqueta_coeficiente.grid(row=4, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

            # # Nueva etiqueta para mostrar la constante de la pendiente
            # self.etiqueta_constante = tk.Label(
            #     self.frame_archivo_seleccionado,
            #     text="Constante de Pendiente: ",
            #     font=("Comfortaa", 12),
            #     bg="light blue",
            #     fg="black",
            # )
            # self.etiqueta_constante.grid(row=4, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

            #Boton Crear Modelo
            self.boton_modelo = tk.Button(
                self.frame_archivo_seleccionado,
                text="Crear Modelo",
                command=self.realizar_analisis,
                justify=tk.RIGHT,
                font=("Comfortaa", 12),
                bg="white",
                fg="black",
            )
            self.boton_modelo.grid(row=4, column=1, pady=(0, 10), padx=5, sticky=tk.E)

            #Boton Guardar Modelo
            self.boton_guardar = tk.Button(
                self.frame_archivo_seleccionado,
                text="Guardar",
                command=self.guardar,
                justify=tk.RIGHT,
                font=("Comfortaa", 12),
                bg="white",
                fg="black",
            )
            self.boton_guardar.config(state='disabled')
            self.boton_guardar.grid(row=4, column=2, pady=(0, 10), padx=5, sticky=tk.W)
            
            
            #Etiqueta para mostrar el RMSE
            self.etiqueta_rmse = tk.Label(
                self.frame_archivo_seleccionado,
                text="RMSE: ",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            )
            self.etiqueta_rmse.grid(row=5, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

            #Etiqueta para mostrar el R^2
            self.etiqueta_r2 = tk.Label(
                self.frame_archivo_seleccionado,
                text="Coeficiente de determinación (R^2): ",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            )
            self.etiqueta_r2.grid(row=6, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

            # Etiqueta para mostrar la ecuación
            self.etiqueta_ecuacion = tk.Label(
                self.frame_archivo_seleccionado,
                text="Ecuación: ",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            )
            self.etiqueta_ecuacion.grid(row=7, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

            # Etiqueta para mostrar la prediccion
            self.etiqueta_prediccion = tk.Label(
                self.frame_archivo_seleccionado,
                text=f"Predicción: ",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            )
            self.etiqueta_prediccion.grid(row=8, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

            # Botón Predicción
            self.boton_prediccion = tk.Button(
                self.frame_archivo_seleccionado,
                text="Predicción",
                command=self.prediccion,
                justify=tk.RIGHT,
                font=("Comfortaa", 12),
                bg="white",
                fg="black",
            )
            self.boton_prediccion.config(state='disabled')
            self.boton_prediccion.grid(row=8, column=2, pady=(0, 10), padx=5, sticky=tk.W)

            # Crear un widget de entrada de texto para el coeficiente de pendiente
            self.entry_coeficiente = tk.Entry(self.frame_archivo_seleccionado)
            self.entry_coeficiente.grid(row=10, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)
            tk.Label(
                self.frame_archivo_seleccionado,
                text="Nuevo Coeficiente de Pendiente: ",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            ).grid(row=9, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

            # Crear un widget de entrada de texto para la constante de pendiente
            self.entry_constante = tk.Entry(self.frame_archivo_seleccionado)
            self.entry_constante.grid(row=10, column=2, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)
            tk.Label(
                self.frame_archivo_seleccionado,
                text="Nueva Constante de Pendiente: ",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            ).grid(row=9, column=2, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

            # Botón Actualizar Gráfica con Nuevos Coeficientes
            self.boton_actualizar_grafica = tk.Button(
                self.frame_archivo_seleccionado,
                text="Actualizar Gráfica",
                command=self.actualizar_grafica,
                justify=tk.RIGHT,
                font=("Comfortaa", 12),
                bg="white",
                fg="black",
            )
            self.boton_actualizar_grafica.grid(row=10, column=4, pady=(0, 10), padx=5, sticky=tk.W)


            # Crear un widget de entrada de texto
            self.etiqueta_valor_x = tk.Label(
                self.frame_archivo_seleccionado,
                text=f"Introduzca un valor para x: ",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            )
            self.etiqueta_valor_x.grid(row=9, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)
            self.entry = tk.Entry(self.frame_archivo_seleccionado)
            self.entry.grid(row=9, column=2, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)


    def realizar_analisis(self):
        if self.col_x is not None and self.col_y is not None:
            modelo = ajustar_modelo(self.ruta_archivo, self.col_x, self.col_y)

            if modelo:
                # Elimina elementos anteriores en el frame de gráfica y resultados
                for widget in self.frame_grafica_resultados.winfo_children():
                    widget.destroy()

                # Actualiza la gráfica y resultados en el frame correspondiente
                # En la sección donde se actualiza el Canvas con la gráfica:

                self.canvas_regresion = tk.Canvas(self.frame_grafica_resultados, bg="light blue", highlightthickness=0)  # Cambiamos el fondo a "light blue"
                self.canvas_regresion.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH)  # Eliminamos expand=True

                #Actualiza el atributo self.modelo con el modelo ajustado
                self.modelo = modelo

                
                

                self.boton_guardar.config(state='normal')
                self.boton_prediccion.config(state='normal')

                # Actualizamos la gráfica dentro del canvas
                actualizar_recta_regresion(modelo, self.ruta_archivo, self.col_x, self.col_y, self.canvas_regresion)

                # Y dentro del método para centrar la gráfica:

                self.rmse = calcular_rmse(modelo, self.ruta_archivo, self.col_x, self.col_y)

                

                #Etiqueta para mostrar el RMSE
                self.etiqueta_rmse = tk.Label(
                    self.frame_archivo_seleccionado,
                    text=f"RMSE: {self.rmse:.4f}",
                    font=("Comfortaa", 12),
                    bg="light blue",
                    fg="black",
                )
                self.etiqueta_rmse.grid(row=5, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

                self.bondad = calcular_bondad(modelo, self.ruta_archivo, self.col_x, self.col_y)

                #Etiqueta para mostrar el R^2
                self.etiqueta_r2 = tk.Label(
                    self.frame_archivo_seleccionado,
                    text=f"Coeficiente de determinación (R^2): {self.bondad:.4f}",
                    font=("Comfortaa", 12),
                    bg="light blue",
                    fg="black",
                )
                self.etiqueta_r2.grid(row=6, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

                self.ecuacion = obtener_ecuación(modelo)

                # Etiqueta para mostrar la ecuación
                self.etiqueta_ecuacion = tk.Label(
                    self.frame_archivo_seleccionado,
                    text=f"Ecuación: {self.ecuacion}",
                    font=("Comfortaa", 12),
                    bg="light blue",
                    fg="black",
                )
                self.etiqueta_ecuacion.grid(row=7, column=0, columnspan=2, pady=(0, 10), padx=5, sticky=tk.W)

    def guardar(self):
        ruta_archivo = filedialog.asksaveasfilename()
        if ruta_archivo and self.modelo is not None:
            try:
                funciones_auxiliares.guardar(
                    ruta_archivo,
                    self.col_x,
                    self.col_y,
                    self.rmse,
                    self.modelo
                )

                # Llamar a la función de verificación después de guardar
                funciones_auxiliares.verificar_guardado(ruta_archivo)

            except Exception as e:
                print(f"Error: No se pudo guardar el modelo. Detalles: {str(e)}")

    def cargar(self):
        ruta_archivo = filedialog.askopenfilename()
        print(f"Archivo seleccionado: {ruta_archivo}")
        if ruta_archivo:
            try:
                col_x, col_y, rmse, modelo = funciones_auxiliares.cargar(ruta_archivo)

                if col_x is not None and col_y is not None and modelo is not None:
                    self.col_x = col_x
                    self.col_y = col_y
                    self.rmse = rmse
                    self.modelo = modelo

                    print("Coeficientes del modelo:")
                    print(self.modelo.params)

                    self.actualizar_listas_columnas()

                    self.realizar_analisis()

            except Exception as e:
                print(f"Error: No se pudo cargar el modelo. Detalles: {str(e)}")

                
    def prediccion(self):
        if self.ruta_archivo and self.col_x and self.col_y is not None: 
                valor_x_str = self.entry.get()

                if valor_x_str.strip():  # Verificar si la cadena no está vacía después de eliminar espacios en blanco
                    try:
                        valor_x = float(valor_x_str)
                        resultado_prediccion = prediccion(self.ruta_archivo, self.col_x, self.col_y, valor_x)

                        # Etiqueta para mostrar la predicción
                        self.etiqueta_prediccion.config(
                            text=f"Predicción: {resultado_prediccion}",
                            font=("Comfortaa", 12),
                            bg="light blue",
                            fg="black",
                        )
                    except ValueError:
                        # Manejar el caso en el que la cadena no se puede convertir a un número
                        self.etiqueta_prediccion.config(
                            text="Error: Ingrese un valor numérico para x",
                            font=("Comfortaa", 12),
                            bg="light blue",
                            fg="black",
                        )
                else:
                    # Manejar el caso en el que la cadena está vacía
                    self.etiqueta_prediccion.config(
                        text="Error: El campo de entrada está vacío",
                        font=("Comfortaa", 12),
                        bg="light blue",
                        fg="black",
                    )

    # Función para actualizar la gráfica con los nuevos coeficientes
    def actualizar_grafica(self):
        if self.modelo and self.col_x and self.col_y:
            try:
                # Obtener los nuevos valores de coeficiente y constante de pendiente
                nuevo_coeficiente = float(self.entry_coeficiente.get())
                nueva_constante = float(self.entry_constante.get())

                # Actualizar los coeficientes del modelo
                self.modelo.params[self.col_x] = nuevo_coeficiente
                self.modelo.params['const'] = nueva_constante

                # Actualizar la gráfica
                self.canvas_regresion.delete("all")
                actualizar_recta_regresion(self.modelo, self.ruta_archivo, self.col_x, self.col_y, self.canvas_regresion)

                # Actualizar el RMSE
                self.rmse = calcular_rmse(self.modelo, self.ruta_archivo, self.col_x, self.col_y)
                self.etiqueta_rmse.config(text=f"RMSE: {self.rmse:.4f}")

                # Actualizar el coeficiente de determinación (R^2)
                self.bondad = calcular_bondad(self.modelo, self.ruta_archivo, self.col_x, self.col_y)
                self.etiqueta_r2.config(text=f"Coeficiente de determinación (R^2): {self.bondad:.4f}")

                # Actualizar la ecuación
                self.ecuacion_actual = obtener_ecuación(self.modelo)
                self.etiqueta_ecuacion.config(text=f"Ecuación: {self.ecuacion_actual}")

            except ValueError:
                print("Error: Ingrese valores numéricos para el coeficiente y la constante de pendiente.")                

class Manager(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Creador de modelos de regresión lineal")

        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.configure(background="light blue")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}

        #Crea instancias de las pantallas (frames) y las almacena en un diccionario
        for F in (PantallaPrincipal,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        #Muestra la primera pantalla
        self.show_frame(PantallaPrincipal)

    #Funcion que cambia entre las pantallas
    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


if __name__ == "__main__":
    app = Manager()
    app.mainloop()