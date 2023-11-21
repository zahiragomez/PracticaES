
from funciones_auxiliares import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog



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
        self.variables_seleccionadas_x = []
        self.variables_seleccionadas_y = []


        self.iniciar_widgets()

        



    def seleccionar_archivo(self):
            
        self.ruta_archivo = filedialog.askopenfilename()
        if self.ruta_archivo:
            self.ruta_seleccionada.set(f"Ruta del archivo seleccionado: {self.ruta_archivo}")



    def seleccionar_variable_x(self):
        self.ruta_archivo = filedialog.askopenfilename()
        if self.ruta_archivo:
            self.ruta_seleccionada.set(f"Ruta del archivo seleccionado: {self.ruta_archivo}")
            self.columna_seleccionada.set("")
           


    def seleccionar_variable_y(self):
        if not self.ruta_archivo:
            print("Primero selecciona un archivo.")
            return

        df = importar_archivo(self.ruta_archivo)

        ventana_variables_y = tk.Toplevel(self)
        ventana_variables_y.title("Seleccionar Variable Y")

        listbox_variables_y = tk.Listbox(ventana_variables_y, selectmode=tk.SINGLE, exportselection=0)
        scrollbar_y = tk.Scrollbar(ventana_variables_y, orient=tk.VERTICAL, command=listbox_variables_y.yview)
        listbox_variables_y.config(yscrollcommand=scrollbar_y.set)

        for variable in df.columns:
            listbox_variables_y.insert(tk.END, variable)

        listbox_variables_y.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        def on_variable_selected_y(event):
            selected_variable_y = listbox_variables_y.get(listbox_variables_y.curselection())
            self.variables_seleccionadas_y = [selected_variable_y]
            self.columna_seleccionada.set(f"Variable Y seleccionada: {selected_variable_y}")
            print(f"Variable Y seleccionada: {selected_variable_y}")

        listbox_variables_y.bind("<<ListboxSelect>>", on_variable_selected_y)


    def seleccionar_columnas(self):
        if not self.ruta_archivo:
            print("Primero selecciona un archivo.")
            return

        df = importar_archivo(self.ruta_archivo)

        ventana_variables_x = tk.Toplevel(self)
        ventana_variables_x.title("Seleccionar Variables X")

        listbox_variables_x = tk.Listbox(ventana_variables_x, selectmode=tk.MULTIPLE, exportselection=0)
        scrollbar_y = tk.Scrollbar(ventana_variables_x, orient=tk.VERTICAL, command=listbox_variables_x.yview)
        listbox_variables_x.config(yscrollcommand=scrollbar_y.set)

        for variable in df.columns:
            listbox_variables_x.insert(tk.END, variable)

        listbox_variables_x.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        def on_variable_selected_x(event):
            selected_variables_x = listbox_variables_x.curselection()
            self.variables_seleccionadas_x = [listbox_variables_x.get(idx) for idx in selected_variables_x]

            # Abrir ventana para seleccionar las variables Y
            self.seleccionar_variables_y()

        listbox_variables_x.bind("<<ListboxSelect>>", on_variable_selected_x)



    def seleccionar_variables_y(self):
        if not self.variables_seleccionadas_x:
            print("Primero selecciona las variables X.")
            return

        df = importar_archivo(self.ruta_archivo)

        ventana_variables_y = tk.Toplevel(self)
        ventana_variables_y.title("Seleccionar Variable Y")

        listbox_variables_y = tk.Listbox(ventana_variables_y, selectmode=tk.SINGLE, exportselection=0)
        scrollbar_y = tk.Scrollbar(ventana_variables_y, orient=tk.VERTICAL, command=listbox_variables_y.yview)
        listbox_variables_y.config(yscrollcommand=scrollbar_y.set)

        for variable in df.columns:
            if variable not in self.variables_seleccionadas_x:
                listbox_variables_y.insert(tk.END, variable)

        listbox_variables_y.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        def on_variable_selected_y(event):
            selected_variable_y = listbox_variables_y.get(listbox_variables_y.curselection())
            self.variables_seleccionadas_y = [selected_variable_y]
            print(f"Variable Y seleccionada: {selected_variable_y}")

        listbox_variables_y.bind("<<ListboxSelect>>", on_variable_selected_y)
        

    def guardar_variables_modelo(self):
        # Verificar si se han seleccionado variables
        if not self.variables_seleccionadas:
            print("No se han seleccionado variables para el modelo de regresión.")
            return

        # Aquí puedes hacer lo que necesites con las variables seleccionadas.
        # Por ejemplo, podrías asignarlas a una variable X para el modelo de regresión.
        variable_X = self.variables_seleccionadas

        # Imprimir o hacer algo con la variable X
        print(f"Variables seleccionadas para el modelo de regresión (variable X): {', '.join(variable_X)}")

        # Agrega una etiqueta para mostrar las variables seleccionadas para X
        etiqueta_variables_x = tk.Label(
            self,
            text=f"Variables seleccionadas para X: {', '.join(variable_X)}",
            font=("Comfortaa", 14),
            bg="white",
            fg="light blue"
        )
        etiqueta_variables_x.pack(side=tk.TOP, fill=tk.BOTH, padx=30, pady=10)

    #Ahora crearemos los atributos que tiene la pantalla principal

    def iniciar_widgets(self):

        #Primero creamos una etiqueta para la función que realiza el programa

        archivo_seleccionado = tk.Button(self, 
                 text = "Pulse para seleccionar el tipo de archivo para la creación del modelo",
                 command = self.seleccionar_archivo,
                 justify = tk.CENTER,
                 font = ("Comfortaa", 14),
                 bg = "white", 
                 fg = "light blue"

                 ).pack(side = tk.TOP,
                     padx = 160, #distancia de la etiqueta al margen por el eje x
                     pady = 160)
        
        ruta_label = tk.Label(
            self,
            textvariable=self.ruta_seleccionada,
            font=("Comfortaa", 14),
            bg="white",
            fg="light blue"
        )
        ruta_label.pack(side=tk.TOP, fill=tk.BOTH, padx=30, pady=30)

        seleccionar_columna = tk.Button(self, 
                 text = "Pulse para seleccionar la columna para la creación del modelo",
                 command = self.seleccionar_columnas,
                 justify = tk.CENTER,
                 font = ("Comfortaa", 14),
                 bg = "white", 
                 fg = "light blue"

                 ).pack(side = tk.TOP,
                     padx = 160, #distancia de la etiqueta al margen por el eje x
                     pady = 160)
        
        columna_label = tk.Label(
            self,
            textvariable=self.columna_seleccionada,
            font=("Comfortaa", 14),
            bg="white",
            fg="light blue"
        )
        columna_label.pack(side=tk.TOP, fill=tk.BOTH, padx=30, pady=30)
            
        
        

        # for (key, value) in self.archivos_disponibles.items():
        #     tk.Radiobutton(optionsFrame,
        #                    text = key,
        #                    command = self.move_to_crear_modelos ,
        #                    variable = self.archivos_disponibles,
        #                    value = value,
        #                    font = ("Comfortaa", 14),
        #                     bg = "white", 
        #                     fg = "light blue"
        #                    ).pack(
        #                        side = tk.LEFT, 
        #                        fill = tk.BOTH,
        #                        expand = True, 
        #                        padx = 5,
        #                        pady  = 5
        #                    )
    






if __name__ == "__main__":
    app = Manager()
    app.mainloop()

    #  frame = tk.Frame()
    #  boton = tk.Button(frame, text="Botón")
    #  etiqueta = tk.Label(frame, text="Etiqueta")

    #  boton.pack()
    #  etiqueta.pack()

    #  frame.pack()

    #  app = frame
    #  app.mainloop()
