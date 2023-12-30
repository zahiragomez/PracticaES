import tkinter as tk
from tkinter import filedialog
from seleccion_columna import ruta, cargar_datos, obtener_columnas_numericas
from analisis_modelo import ajustar_modelo, actualizar_recta_regresion, calcular_rmse, calcular_bondad
import funciones_auxiliares
from funciones_auxiliares import guardar
from funciones_auxiliares import cargar


class PantallaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        #Variables de clase para almacenar informacion
        self.col_x = None
        self.col_y = None
        self.modelo= None
        self.fig1 = None
        self.fig2 = None
        self.canvas_regresion = None
        self.rmse = None

        #Configuracion general de la pantalla principal
        self.configure(background="light blue")
        self.controller = controller
        self.ruta_seleccionada = tk.StringVar()

        self.ruta_archivo = ""
        self.variables_seleccionadas_x = []
        self.variables_seleccionadas_y = []

        #Frame para la seleccion de archivo
        self.frame_archivo_seleccionado = tk.Frame(self, bg="light blue")
        self.frame_archivo_seleccionado.pack(side=tk.TOP, padx=10, pady=10)

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

    #Funcion que realiza el analisis de regresion y actualizaa la interfaz grafica
    def realizar_analisis(self):
        if self.col_x is not None and self.col_y is not None:
            modelo = ajustar_modelo(self.ruta_archivo, self.col_x, self.col_y)

            if modelo:
                if self.canvas_regresion:
                    self.canvas_regresion.destroy()

                self.canvas_regresion = tk.Canvas(self.frame_archivo_seleccionado)
                self.canvas_regresion.grid(row=2, column=0, columnspan=3, pady=20, sticky=tk.NSEW)

                #Actualiza el atributo self.modelo con el modelo ajustado
                self.modelo = modelo

                self.boton_guardar.config(state='normal')
                actualizar_recta_regresion(modelo, self.ruta_archivo, self.col_x, self.col_y, self.canvas_regresion)

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

    #Funcion que guarda el modelo en un archivo
    def guardar(self):
        ruta_archivo = filedialog.asksaveasfilename()
        if ruta_archivo and self.modelo is not None:
            funciones_auxiliares.guardar(ruta_archivo, self.col_x, self.col_y, self.rmse, self.modelo)

    #Funcion que carga un modelo desde un archivo
    def cargar(self):
        ruta_archivo = filedialog.askopenfilename()
        print(f"Archivo seleccionado: {ruta_archivo}")  # Add this line
        if ruta_archivo:
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

            else:
                print("Error: No se pudo cargar el modelo.")


class Manager(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Creador de modelos de regresión lineal")

        container = tk.Frame(self)
        container.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True
        )
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
