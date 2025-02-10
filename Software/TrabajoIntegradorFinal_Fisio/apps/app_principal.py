import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk
import modules.GestorDeArchivos as ga
import modules.GestorDeImagenes as gi

gArchivos = ga.gestorDeArchivos("Gestor de Archivos")
gArchivos.extraeListadoDeArchivos("\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas")
directoriosImagenes = gArchivos.getListadoDeArchivos()
gImagen = gi.gestorDeImagenes("Gestor de Imagenes")

# Imprimir los archivos cargados para verificar
print("Archivos cargados desde el directorio:")
for archivo in directoriosImagenes:
    print(archivo)

class AplicacionPrincipal:
    """Clase principal de la aplicación."""
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador del ojo humano")
        self.root.geometry("900x500")
        
        # Crear la barra de tareas
        self.frameBarraTareas = tk.Frame(self.root)
        self.frameBarraTareas.pack(fill='x')

        # Botón para seleccionar imágenes
        imagenes = ["Arbol", "Corazón", "Estrella colorida", "Estrella", "Flecha"]
        self.imagenSeleccionada = tk.StringVar(root)
        self.imagenSeleccionada.set("Seleccionar imagen")

        menu_button_imagen = tk.Menubutton(self.frameBarraTareas, text="Seleccionar Imagen", relief=tk.RAISED)
        menu_button_imagen.menu = tk.Menu(menu_button_imagen, tearoff=0)
        menu_button_imagen["menu"] = menu_button_imagen.menu
       
        for i, imagen in enumerate(imagenes):
            menu_button_imagen.menu.add_radiobutton(label=imagen, variable=self.imagenSeleccionada, value=imagen, command=lambda i=i: self.mostrar_imagen(i))

        menu_button_imagen.pack(side='left', padx=5, pady=5)
        
        # Botón "Preguntas"
        preguntasBoton = tk.Button(self.frameBarraTareas, text="Preguntas", command=lambda: messagebox.showinfo("Preguntas", "Aquí van las preguntas."), relief=tk.RAISED)
        preguntasBoton.pack(side='left', padx=5, pady=5)

        # Botón "Ayuda"
        ayudaBoton = tk.Button(self.frameBarraTareas, text="Ayuda", command=lambda: messagebox.showinfo("Ayuda", "Aquí va la ayuda."), relief=tk.RAISED)
        ayudaBoton.pack(side='left', padx=5, pady=5)

        # Botón "Imágenes de Prueba"
        ImagenesPruebaBoton = tk.Button(self.frameBarraTareas, text="Imágenes de Prueba", command=lambda: messagebox.showinfo("Imágenes de Prueba", "Aquí van las imágenes de prueba."), relief=tk.RAISED)
        ImagenesPruebaBoton.pack(side='left', padx=5, pady=5)

        # Grid principal
        frameGrid = tk.Frame(root)
        frameGrid.pack(pady=10, expand=True, fill='both')

        # Configurar la expansión de las filas y columnas
        frameGrid.columnconfigure(0, weight=1)
        frameGrid.columnconfigure(1, weight=1)
        frameGrid.columnconfigure(2, weight=1)
        frameGrid.rowconfigure(0, weight=1)

        # Condición
        frameCondicion = tk.Frame(frameGrid)
        frameCondicion.grid(row=0, column=0, padx=10, sticky='nsew')

        condiciones = ["Emétrope", "Miope", "Hipermétrope"]
        condicionSeleccionada = tk.StringVar(root)
        condicionSeleccionada.set("Seleccione Condicion")

        menuBotonCondicion = tk.Menubutton(frameCondicion, text="Condición", relief=tk.FLAT, bg="#3b82f6", fg="white")
        menuBotonCondicion.menu = tk.Menu(menuBotonCondicion, tearoff=0)
        menuBotonCondicion["menu"] = menuBotonCondicion.menu

        for condicion in condiciones:
            menuBotonCondicion.menu.add_radiobutton(label=condicion, variable=condicionSeleccionada, value=condicion)

        menuBotonCondicion.pack(pady=5)

        # Cuadro gris debajo de "Condicion"
        self.imagenOriginal = ImageTk.PhotoImage(Image.new("RGB", (200, 200), "gray"))
        self.labelImagenOriginal = tk.Label(frameCondicion, image=self.imagenOriginal)
        self.labelImagenOriginal.pack(expand=True, fill='both')

        # Grado
        frameGrado = tk.Frame(frameGrid)
        frameGrado.grid(row=0, column=1, padx=20, sticky='nsew')

        grados = ["Grado 1", "Grado 2", "Grado 3"]
        gradoSeleccionado = tk.StringVar(root)
        gradoSeleccionado.set("Seleccione Grado")

        menuBotonGrado = tk.Menubutton(frameGrado, text="Grado", relief=tk.FLAT, bg="#3b82f6", fg="white")
        menuBotonGrado.menu = tk.Menu(menuBotonGrado, tearoff=0)
        menuBotonGrado["menu"] = menuBotonGrado.menu

        for grado in grados:
            menuBotonGrado.menu.add_radiobutton(label=grado, variable=gradoSeleccionado, value=grado)

        menuBotonGrado.pack(pady=5)

        # Cuadro gris debajo de "Grado"
        self.marchaDeRayos = ImageTk.PhotoImage(Image.new("RGB", (300, 200), "gray"))
        tk.Label(frameGrado, image=self.marchaDeRayos).pack(expand=True, fill='both')

        # Distancia
        frameDistancia = tk.Frame(frameGrid)
        frameDistancia.grid(row=0, column=2, padx=10, sticky='nsew')

        distancias = ["Punto lejano", "Punto cercano", "Punto medio"]
        distanciaSeleccionada = tk.StringVar(root)
        distanciaSeleccionada.set("Seleccione Distancia")

        menuBotonDistancia = tk.Menubutton(frameDistancia, text="Distancia", relief=tk.FLAT, bg="#3b82f6", fg="white")
        menuBotonDistancia.menu = tk.Menu(menuBotonDistancia, tearoff=0)
        menuBotonDistancia["menu"] = menuBotonDistancia.menu

        for distancia in distancias:
            menuBotonDistancia.menu.add_radiobutton(label=distancia, variable=distanciaSeleccionada, value=distancia)

        menuBotonDistancia.pack(pady=5)

        # Cuadro gris debajo de "Distancia"
        self.imagenEnElCerebro = ImageTk.PhotoImage(Image.new("RGB", (200, 200), "gray"))
        tk.Label(frameDistancia, image=self.imagenEnElCerebro).pack(expand=True, fill='both')

        # Información de distancia y botón
        frameInfo = tk.Frame(root, bd=2, relief=tk.SUNKEN, padx=35, pady=15, bg="#e0e0e0")
        frameInfo.pack(padx=10, pady=5, anchor='w')  # Align to the left
        
        # Aumentar el tamaño de la fuente predeterminada
        #default_font = tkFont.nametofont("TkDefaultFont")
        #default_font.configure(size=16)
        
        tk.Label(frameInfo, text="Punto Remoto:", bg="#e0e0e0").pack(anchor='w')
        tk.Label(frameInfo, text="Punto Lejano:", bg="#e0e0e0").pack(anchor='w')
        tk.Label(frameInfo, text="Lente correctora:", bg="#e0e0e0").pack(anchor='w')

    def mostrar_imagen(self, index):
        if index < len(directoriosImagenes):
            print(f"Mostrando imagen {index}")
            imagen_path = "\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas\\" + directoriosImagenes[index]
            print(f"Ruta de la imagen: {imagen_path}")
            imagen = gImagen.mostrar_imagen(imagen_path)
            imagen = imagen.resize((200, 200))
            self.imagenOriginal = ImageTk.PhotoImage(imagen)
            self.labelImagenOriginal.config(image=self.imagenOriginal)
            self.labelImagenOriginal.image = self.imagenOriginal
            
def ejecutar_gui():
    root = tk.Tk()
    app = AplicacionPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_gui()