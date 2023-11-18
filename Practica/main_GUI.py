
from funciones_auxiliares import *
import tkinter as tk
from funciones_auxiliares import *



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

        self.iniciar_widgets()


    def seleccionar_archivos(self):
            
            ruta_archivo = filedialog.askopenfilename()
        
            file_data = importar_archivo(ruta_archivo)
            # Haz algo con el archivo importado, por ejemplo:
            
            self.ruta_seleccionada.set(f"Ruta del archivo seleccionado: {ruta_archivo}")
           
    

        

    #Ahora crearemos los atributos que tiene la pantalla principal

    def iniciar_widgets(self):

        #Primero creamos una etiqueta para la función que realiza el programa

        archivo_seleccionado = tk.Button(self, 
                 text = "Pulse para seleccionar el tipo de archivo para la creación del modelo",
                 command = self.seleccionar_archivos,
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
