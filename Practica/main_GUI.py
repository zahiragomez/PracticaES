import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

class PantallaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.col_x = None
        self.col_y = None
        self.fig1 = None
        self.fig2 = None

        self.configure(background="light blue")
        self.controller = controller
        self.ruta_seleccionada = tk.StringVar()

        self.ruta_archivo = ""
        self.variables_seleccionadas_x = []
        self.variables_seleccionadas_y = []

        # Crear el frame para la ruta del archivo y botón de examinar
        frame_archivo_seleccionado = tk.Frame(self, bg="light blue")
        frame_archivo_seleccionado.pack(side=tk.TOP, padx=10, pady=10)

        # Indicaciones
        indicaciones_label = tk.Label(
            frame_archivo_seleccionado,
            text="(Seleccione el archivo dándole a examinar)",
            justify=tk.LEFT,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        indicaciones_label.grid(
            row=0, column=0, padx=(10, 10), pady=10, sticky=tk.W
        )

        # Ruta del archivo
        ruta_label = tk.Label(
            frame_archivo_seleccionado,
            textvariable=self.ruta_seleccionada,
            justify=tk.CENTER,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        ruta_label.grid(
            row=1, column=0, padx=(10, 10), pady=10, sticky=tk.W
        )

        # Botón Examinar
        boton_examinar = tk.Button(
            frame_archivo_seleccionado,
            text="Examinar",
            command=self.seleccionar_archivo,
            justify=tk.RIGHT,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )
        boton_examinar.grid(
            row=1, column=1, padx=(10, 10), pady=10, sticky=tk.W
        )

        # Crear la lista de columnas X
        self.listbox_x = tk.Listbox(frame_archivo_seleccionado)
        self.listbox_x.bind("<<ListboxSelect>>", self.cambia_columna_x)
        self.listbox_x.grid(
            row=2, column=0, padx=(10, 5), pady=10, sticky=tk.W
        )

        # Crear la lista de columnas Y
        self.listbox_y = tk.Listbox(frame_archivo_seleccionado)
        self.listbox_y.bind("<<ListboxSelect>>", self.cambia_columna_y)
        self.listbox_y.grid(
            row=2, column=1, padx=(5, 10), pady=10, sticky=tk.W
        )

        
        # Etiqueta para la columna X seleccionada
        self.etiqueta_x = tk.Label(
            frame_archivo_seleccionado,  # Usa frame_archivo_seleccionado como el contenedor
            text=f"Variable X seleccionada: {self.col_x}",
            font=("Comfortaa", 12),
            bg="light blue",
            fg="black",
        )
        self.etiqueta_x.grid(row=3, column=0, padx=(10, 10), pady=10, sticky=tk.W)
        # Etiqueta para la columna Y seleccionada
        self.etiqueta_y = tk.Label(
            frame_archivo_seleccionado,  # Usa frame_archivo_seleccionado como el contenedor
            text=f"Variable Y seleccionada: {self.col_y}",
            font=("Comfortaa", 12),
            bg="light blue",
            fg="black",
        )
        self.etiqueta_y.grid(row=3, column=1, padx=(10, 10), pady=10, sticky=tk.E)

        # Botón Realizar Análisis
        boton_analisis = tk.Button(
            frame_archivo_seleccionado,
            text="Realizar Análisis",
            command=self.realizar_analisis,
            justify=tk.RIGHT,
            font=("Comfortaa", 12),
            bg="white",
            fg="black",
        )   
        boton_analisis.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.NSEW)

        # Canvas para el gráfico 1
        self.canvas1 = tk.Canvas(self, width=400, height=300, bg="white")
        self.canvas1.pack(padx=10, pady=10, side=tk.LEFT)

        # Canvas para el gráfico 2
        self.canvas2 = tk.Canvas(self, width=400, height=300, bg="white")
        self.canvas2.pack(padx=10, pady=10, side=tk.LEFT)

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

            self.listbox_x.delete(0, tk.END)
            self.listbox_y.delete(0, tk.END)

            for columna in columnas:
                self.listbox_x.insert(tk.END, columna)
                self.listbox_y.insert(tk.END, columna)

            # Etiqueta para la columna X seleccionada
            etiqueta_x_text = f"Variable X seleccionada: {self.col_x}"
            self.etiqueta_x.config(text=etiqueta_x_text)

            # Etiqueta para la columna Y seleccionada
            etiqueta_y_text = f"Variable Y seleccionada: {self.col_y}"
            self.etiqueta_y.config(text=etiqueta_y_text)

        except pd.errors.EmptyDataError:
            print("Error: El archivo está vacío")
        except pd.errors.ParserError:
            print("Error: Error al analizar el archivo CSV")

    def realizar_analisis(self):
        if self.col_x is not None and self.col_y is not None:
            modelo = self.ajustar_modelo(self.col_x, self.col_y)
            if modelo:
                self.fig1, self.fig2 = self.test_modelos(self.col_x, self.col_y, modelo)
                if self.fig1:
                    self.actualizar_grafica(self.fig1, self.canvas1)
                if self.fig2:
                    self.actualizar_grafica(self.fig2, self.canvas2)


    def ajustar_modelo(self, col_x, col_y):
        data = pd.read_csv(self.ruta_archivo)

        X = data[col_x]
        X = sm.add_constant(X, prepend=True)
        y = data[col_y]

        modelo = sm.OLS(endog=y, exog=X).fit()
        return modelo

    def test_modelos(self, col_x, col_y, modelo):
        data = pd.read_csv(self.ruta_archivo)

        # Análisis y gráfico 1
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        scatter1 = ax1.scatter(
            x=data[col_x],
            y=data[col_y],
            c="#FFA500",
            label="Datos de dispersión",
            marker="o",
        )
        ax1.set_title(f'Distribución de {col_x} y {col_y}')
        ax1.set_xlabel('Eje X')
        ax1.set_ylabel('Eje Y')
        ax1.legend(handles=[scatter1], loc='upper right')

        # Otro análisis y gráfico 2
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        scatter2 = ax2.scatter(
            x=data[col_x],
            y=data[col_y],
            c="gray",
            label="Datos Observados",
            marker="o",
            alpha=0.8,
        )
        ax2.plot(data[col_x], modelo.predict(exog=sm.add_constant(data[col_x], prepend=True)), linestyle='-', color='blue', label="OLS", linewidth=2)
        ci = modelo.get_prediction(exog=sm.add_constant(data[col_x], prepend=True)).summary_frame(alpha=0.05)
        ax2.fill_between(data[col_x], ci["mean_ci_lower"], ci["mean_ci_upper"], color='orange', alpha=0.1, label='95% CI')
        ax2.set_xlabel('Variable Independiente')
        ax2.set_ylabel('Variable Dependiente')
        ax2.set_title('Gráfico del Modelo con Predicciones')
        ax2.grid(True, linestyle='--', alpha=0.5)
        ax2.set_facecolor('#F9F9F9')
        ax2.legend()

        return fig1, fig2

    def actualizar_grafica(self, fig, canvas):
        # Crear una nueva instancia de FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


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

