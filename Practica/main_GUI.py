
from funciones_auxiliares import *
import tkinter as tk
from funciones_auxiliares import *
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

        self.iniciar_widgets()


    def seleccionar_archivo(self):
            
            ruta_archivo = filedialog.askopenfilename()
        
            file_data = importar_archivo(ruta_archivo)
            # Haz algo con el archivo importado, por ejemplo:
            
            self.ruta_seleccionada.set(f"Ruta del archivo seleccionado: {ruta_archivo}")
           
    def seleccionar_columnas(self):
        print("Seleccionar Columnas")

        # Solicitar al usuario que seleccione un archivo
        archivo_seleccionado = filedialog.askopenfilename()

        # Verificar si se seleccionó un archivo
        if not archivo_seleccionado:
            print("No se seleccionó ningún archivo.")
            return

        # Obtener la extensión del archivo
        extension = archivo_seleccionado.split(".")[-1].lower()

        # Utilizar la función correspondiente según la extensión del archivo
        if extension == "csv":
            # Importar el archivo CSV
            df = importar_archivo(archivo_seleccionado)

            # Crear una nueva ventana para mostrar las variables en un Listbox
            ventana_variables = tk.Toplevel(self)
            ventana_variables.title("Seleccionar Variables")

            # Crear un Listbox con scroll Y
            listbox_variables = tk.Listbox(ventana_variables, selectmode=tk.MULTIPLE, exportselection=0)
            scrollbar_y = tk.Scrollbar(ventana_variables, orient=tk.VERTICAL, command=listbox_variables.yview)
            listbox_variables.config(yscrollcommand=scrollbar_y.set)

            # Insertar las variables en el Listbox
            for variable in df.columns:
                listbox_variables.insert(tk.END, variable)

            listbox_variables.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

            # Función para manejar la selección en el Listbox
            def on_variable_selected(event):
                selected_variables = listbox_variables.curselection()
                selected_columns = [listbox_variables.get(idx) for idx in selected_variables]
                self.columna_seleccionada.set(f"Columnas seleccionadas: {', '.join(selected_columns)}")

            # Asociar la función al evento <<ListboxSelect>>
            listbox_variables.bind("<<ListboxSelect>>", on_variable_selected)
        

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


         # Botón para seleccionar el archivo y mostrar variables disponibles
        seleccionar_archivo_button = tk.Button(
            self,
            text="Seleccionar Archivo y Mostrar Variables",
            command=self.seleccionar_columnas,
            justify=tk.CENTER,
            font=("Comfortaa", 14),
            bg="white",
            fg="light blue"
        )
        seleccionar_archivo_button.pack(side=tk.TOP, padx=160, pady=10)

        # Etiqueta para mostrar la columna seleccionada
        columna_label = tk.Label(
            self,
            textvariable=self.columna_seleccionada,
            font=("Comfortaa", 14),
            bg="white",
            fg="light blue"
        )
        columna_label.pack(side=tk.TOP, fill=tk.BOTH, padx=30, pady=10)
        
        

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
