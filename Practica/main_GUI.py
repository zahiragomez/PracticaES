from funciones_auxiliares import *
import tkinter as tk
from tkinter import filedialog
from modelo_regresion_lineal import test_modelos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Manager(tk.Tk):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.title("Creador de modelos de regresión lineal")

        #Va a contener el resto de ventanas

        container = tk.Frame(self)
        container.pack(
            side = tk.TOP,
            fill = tk.BOTH, #se expanda la ventana hacia todos lados
            expand = True
        )
        container.configure(background ="light blue")
        container.grid_columnconfigure(0, weight=1) #índice y peso
        container.grid_rowconfigure(0, weight = 1)

        self.frames = {}

        for F in (PantallaPrincipal,):  # Añade una coma para crear una tupla con un solo elemento
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)


            #Hemos guardado todos los frame en un diccionario en Manager para tenerlos todos a mano7
        self.show_frame(PantallaPrincipal)


    def show_frame(self, container):

        frame = self.frames[container]
        #frame.tkraise() #se pone delante
        frame.pack()



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
            "Archivo 1": importar_archivo,
            "Archivo 2": importar_archivo,
            "Archivo 3": importar_archivo
        }
        self.ruta_seleccionada = tk.StringVar() 
        self.columna_seleccionada = tk.StringVar()
        self.ruta_archivo = ""  # Nuevo atributo para almacenar la ruta del archivo seleccionado
        self.variables_seleccionadas_x = []  # Inicializa la lista de variables seleccionadas para X
        self.variables_seleccionadas_y = []


        self.iniciar_widgets()


    def seleccionar_archivo(self):
            
        self.ruta_archivo = filedialog.askopenfilename()
        if self.ruta_archivo:
            self.ruta_seleccionada.set(f"Ruta del archivo seleccionado: {self.ruta_archivo}")

    def cambia_columna_x(self, event):
        if self.listbox_x.curselection():
            self.col_x = self.listbox_x.curselection()[0]
            self.columna_x.config(text='Columna X: ' + str(self.col_x))

            if self.col_y is not None:
                if self.plt is not None:
                    self.plt.close()

                fig, plt = test_modelos(self.col_x, self.col_y)
                self.plt = plt
                
                if self.grafica:
                    self.grafica.pop()
                    self.grafica.destroy()
                
                self.grafica = FigureCanvasTkAgg(fig, master=self).get_tk_widget()
                self.grafica.pack()

    def cambia_columna_y(self, event):
        if self.listbox_y.curselection():
            self.col_y = self.listbox_y.curselection()[0]
            self.columna_y.config(text='Columna Y: ' + str(self.col_y))

            if self.col_x is not None:
                if self.plt is not None:
                    self.plt.close()

                fig, plt = test_modelos(self.col_x, self.col_y)
                self.plt = plt
                
                if self.grafica:
                    self.grafica.pop()
                    self.grafica.destroy()
                
                self.grafica = FigureCanvasTkAgg(fig, master=self).get_tk_widget()
                self.grafica.pack()

    #Ahora crearemos los atributos que tiene la pantalla principal

    def iniciar_widgets(self):

        #Primero creamos una etiqueta para la función que realiza el programa
        archivo_seleccionado_button = tk.Button(self, 
            text="Pulse para seleccionar el tipo de archivo para la creación del modelo",
            command=self.seleccionar_archivo,
            justify=tk.CENTER,
            font=("Comfortaa", 14),
            bg="white",
            fg="light blue"
        )
        archivo_seleccionado_button.pack(side=tk.TOP, padx=160, pady=160)
        
        ruta_label = tk.Label(
            self,
            textvariable=self.ruta_seleccionada,
            font=("Comfortaa", 14),
            bg="white",
            fg="light blue"
        )
        ruta_label.pack(side=tk.TOP, fill=tk.BOTH, padx=30, pady=30)

        frame_horizontal = tk.Frame(self)
        frame_horizontal.pack()
        
        self.listbox_x = tk.Listbox(frame_horizontal)
        self.listbox_x.bind('<<ListboxSelect>>', self.cambia_columna_x)
        self.listbox_x.pack(side=tk.LEFT)
        self.listbox_x.insert(tk.END, 'longitude')
        self.listbox_x.insert(tk.END, 'latitude')
        self.listbox_x.insert(tk.END, 'housing_median_age')
        self.listbox_x.insert(tk.END, 'total_rooms')
        self.listbox_x.insert(tk.END, 'total_bedrooms')
        self.listbox_x.insert(tk.END, 'population')
        self.listbox_x.insert(tk.END, 'households')
        self.listbox_x.insert(tk.END, 'median_income')
        self.listbox_x.insert(tk.END, 'median_house_value')
        self.listbox_x.insert(tk.END, 'ocean_proximity')
        self.listbox_x.pack()
        
        self.listbox_y = tk.Listbox(frame_horizontal)
        self.listbox_y.bind('<<ListboxSelect>>', self.cambia_columna_y)
        self.listbox_y.pack(side=tk.LEFT)
        self.listbox_y.insert(tk.END, 'longitude')
        self.listbox_y.insert(tk.END, 'latitude')
        self.listbox_y.insert(tk.END, 'housing_median_age')
        self.listbox_y.insert(tk.END, 'total_rooms')
        self.listbox_y.insert(tk.END, 'total_bedrooms')
        self.listbox_y.insert(tk.END, 'population')
        self.listbox_y.insert(tk.END, 'households')
        self.listbox_y.insert(tk.END, 'median_income')
        self.listbox_y.insert(tk.END, 'median_house_value')
        self.listbox_y.insert(tk.END, 'ocean_proximity')
        self.listbox_y.pack()
        
        self.columna_x = tk.Label(self)
        self.columna_x.pack()
        
        self.columna_y = tk.Label(self)
        self.columna_y.pack()
    
if __name__ == "__main__":
    app = Manager()
    app.mainloop()
