
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error

class PantallaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.col_x = None
        self.col_y = None
        self.fig1 = None
        self.fig2 = None
        self.canvas_regresion = None

        self.configure(background="light blue")
        self.controller = controller
        self.ruta_seleccionada = tk.StringVar()

        self.ruta_archivo = ""
        self.variables_seleccionadas_x = []
        self.variables_seleccionadas_y = []

        # Crear el frame para la selección de archivo
        self.frame_archivo_seleccionado = tk.Frame(self, bg="light blue")
        self.frame_archivo_seleccionado.pack(side=tk.TOP, padx=10, pady=10)

        # Indicaciones
        self.indicaciones_label = tk.Label(
            self.frame_archivo_seleccionado,
            text="(Seleccione el archivo dándole a examinar)",
            justify=tk.LEFT,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        self.indicaciones_label.grid(row=0, columnspan=2, padx=(10, 10), pady=10, sticky=tk.W)

        # Ruta del archivo
        self.ruta_label = tk.Label(
            self.frame_archivo_seleccionado,
            textvariable=self.ruta_seleccionada,
            justify=tk.CENTER,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        self.ruta_label.grid(row=1, columnspan=2, padx=(10, 10), pady=10, sticky=tk.W)

        # Botón Examinar
        self.boton_examinar = tk.Button(
            self.frame_archivo_seleccionado,
            text="Examinar",
            command=self.seleccionar_archivo,
            justify=tk.RIGHT,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        self.boton_examinar.grid(row=1, column=2, padx=(10, 10), pady=10, sticky=tk.W)

        # Listas de selección de columnas (se crean vacías inicialmente)
        self.listbox_x = None
        self.listbox_y = None
        self.etiqueta_x = None
        self.etiqueta_y = None

    def seleccionar_archivo(self):
        self.ruta_archivo = filedialog.askopenfilename()
        if self.ruta_archivo:
            self.ruta_seleccionada.set(
                f"Ruta del archivo seleccionado: {self.ruta_archivo}"
            )
            self.actualizar_listas_columnas()

    def cambia_columna_x(self, event):
        if self.listbox_x.curselection():
            self.col_x = self.listbox_x.get(self.listbox_x.curselection())
            self.etiqueta_x.config(text=f"Variable X seleccionada: {self.col_x}")

    def cambia_columna_y(self, event):
        if self.listbox_y.curselection():
            self.col_y = self.listbox_y.get(self.listbox_y.curselection())
            self.etiqueta_y.config(text=f"Variable Y seleccionada: {self.col_y}")

    def actualizar_listas_columnas(self):
        try:
            df = pd.read_csv(self.ruta_archivo)
            columnas = df.columns.tolist()

            # Crear la lista de columnas X
            self.listbox_x = tk.Listbox(self.frame_archivo_seleccionado)
            self.listbox_x.bind("<<ListboxSelect>>", self.cambia_columna_x)
            self.listbox_x.grid(row=2, column=0, padx=(10, 5), pady=10, sticky=tk.W)

            # Crear la lista de columnas Y
            self.listbox_y = tk.Listbox(self.frame_archivo_seleccionado)
            self.listbox_y.bind("<<ListboxSelect>>", self.cambia_columna_y)
            self.listbox_y.grid(row=2, column=1, padx=(5, 10), pady=10, sticky=tk.W)

            for columna in columnas:
                self.listbox_x.insert(tk.END, columna)
                self.listbox_y.insert(tk.END, columna)

            # Etiqueta para la columna X seleccionada
            self.etiqueta_x = tk.Label(
                self.frame_archivo_seleccionado,
                text=f"Variable X seleccionada: {self.col_x}",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            )
            self.etiqueta_x.grid(row=3, column=0, padx=(10, 10), pady=10, sticky=tk.W)

            # Etiqueta para la columna Y seleccionada
            self.etiqueta_y = tk.Label(
                self.frame_archivo_seleccionado,
                text=f"Variable Y seleccionada: {self.col_y}",
                font=("Comfortaa", 12),
                bg="light blue",
                fg="black",
            )
            self.etiqueta_y.grid(row=3, column=1, padx=(10, 10), pady=10, sticky=tk.E)

            # Botón Crear Modelo
            self.boton_modelo = tk.Button(
                self.frame_archivo_seleccionado,
                text="Crear Modelo",
                command=self.realizar_analisis,
                justify=tk.RIGHT,
                font=("Comfortaa", 12),
                bg="white",
                fg="black",
            )   
            self.boton_modelo.grid(row=4, columnspan=3, pady=10, sticky=tk.NSEW)

        except pd.errors.EmptyDataError:
            print("Error: El archivo está vacío")
        except pd.errors.ParserError:
            print("Error: Error al analizar el archivo CSV")

    def realizar_analisis(self):
        if self.col_x is not None and self.col_y is not None:
            modelo = self.ajustar_modelo(self.col_x, self.col_y)
            if modelo:
                self.actualizar_recta_regresion(modelo)

                # Calcular y mostrar RMSE
                rmse = self.calcular_rmse(self.col_x, self.col_y, modelo)
                #self.etiqueta_rmse.config(text=f'RMSE: {rmse:.4f}')  # Actualiza la etiqueta con el valor del RMSE

    def ajustar_modelo(self, col_x, col_y):
        data = pd.read_csv(self.ruta_archivo)

        # Drop rows with any missing values in the specified columns
        data.dropna(subset=[col_x, col_y], inplace=True)

        X = data[col_x]
        X_i = sm.add_constant(X, prepend=True)
        y = data[col_y]

        modelo = sm.OLS(endog=y, exog=X_i).fit()
        return modelo


    def actualizar_recta_regresion(self, modelo):
        data = pd.read_csv(self.ruta_archivo)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(
            x=data[self.col_x],
            y=data[self.col_y],
            c="#FFA500",
            label="Datos de dispersión",
            marker="o",
        )
        ax.set_title(f'Distribución de {self.col_x} y {self.col_y}')
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.legend(handles=[scatter], loc='upper right')
        ax.plot(data[self.col_x], modelo.predict(exog=sm.add_constant(data[self.col_x], prepend=True)), linestyle='-', color='blue', label="OLS", linewidth=2)
        ci = modelo.get_prediction(exog=sm.add_constant(data[self.col_x], prepend=True)).summary_frame(alpha=0.05)
        ax.fill_between(data[self.col_x], ci["mean_ci_lower"], ci["mean_ci_upper"], color='orange', alpha=0.1, label='95% CI')
        
        self.canvas_regresion = tk.Canvas(self, width=400, height=300, bg="white")
        self.canvas_regresion.pack(padx=10, pady=10)
        
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_regresion)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def calcular_rmse(self, col_x, col_y, modelo):
        data = pd.read_csv(self.ruta_archivo)

        X = sm.add_constant(data[col_x], prepend=True)
        y_true = data[col_y]

        y_pred = modelo.predict(exog=X)

        rmse = mean_squared_error(y_true, y_pred, squared=False)
        return rmse


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

        for F in (PantallaPrincipal,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.show_frame(PantallaPrincipal)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


if __name__ == "__main__":
    app = Manager()
    app.mainloop()
