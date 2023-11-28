import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import pickle


class PantallaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.col_x = None
        self.col_y = None
        self.plt = None
        self.grafica = None

        self.configure(background="light blue")
        self.controller = controller
        self.archivos_disponibles = {
            "Archivo 1": self.importar_archivo,
            "Archivo 2": self.importar_archivo,
            "Archivo 3": self.importar_archivo,
        }
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
        boton_analisis.grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Canvas para el gráfico
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack(padx=10, pady=10)

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

    def cambia_columna_y(self, event):
        if self.listbox_y.curselection():
            self.col_y = self.listbox_y.get(self.listbox_y.curselection())

    def actualizar_listas_columnas(self):
        try:
            df = pd.read_csv(self.ruta_archivo)
            columnas = df.columns.tolist()

            self.listbox_x.delete(0, tk.END)
            self.listbox_y.delete(0, tk.END)

            for columna in columnas:
                self.listbox_x.insert(tk.END, columna)
                self.listbox_y.insert(tk.END, columna)
        except pd.errors.EmptyDataError:
            print("El archivo está vacío")
        except pd.errors.ParserError:
            print("Error al analizar el archivo CSV")

    def realizar_analisis(self):
        if self.col_x is not None and self.col_y is not None:
            self.plt = self.test_modelos(self.col_x, self.col_y)

            if self.grafica:
                self.canvas.delete(self.grafica)

            self.grafica = FigureCanvasTkAgg(
                self.plt, master=self.canvas
            )
            self.grafica.draw()
            self.grafica.get_tk_widget().pack()

    def importar_archivo(self):
        # Puedes implementar la lógica para importar un archivo aquí
        pass

    def test_modelos(self, col_x, col_y):
        data = pd.read_csv(self.ruta_archivo)

        datos = data[[col_x, col_y]]

        # Gráfico
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(
            x=data[col_x],
            y=data[col_y],
            c="#FFA500",  # Código hexadecimal para naranja
            label="Datos de dispersión",  # Etiqueta para la leyenda
            marker="o",  # Utiliza círculos como estilo de los puntos
        )
        ax.set_title(f'Distribución de {col_x} y {col_y}')
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        # Añadir leyenda manualmente
        ax.legend(handles=[scatter], loc='upper right')

        return fig


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