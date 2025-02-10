import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import modules.GestorDeArchivos as ga
import modules.GestorDeImagenes as gi

gArchivos = ga.gestorDeArchivos("Gestor de Archivos")
#gImagen = gi.gestorDeImagenes("Gestor de Imagenes")

class AplicacionPrincipal:
    """Clase principal de la aplicación."""
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador del ojo humano")
        self.root.geometry("900x500")
        
        #crear la barra de tareas
        self.frameBarraTareas = tk.Frame(self.root)
        self.frameBarraTareas.pack(fill='x')

        #Botón para seleccionar imágenes
        directoriosImagenes = gArchivos.extraeListadoDeArchivos("Imagenes")
        imagenes = ["imagen 1", "imagen 2", "imagen 3", "imagen 4", "imagen 5"]
        imagenSeleccionada = tk.StringVar(root)
        imagenSeleccionada.set("Seleccionar imagen")

        menu_button_imagen = tk.Menubutton(self.frameBarraTareas, text="Seleccionar Imagen", relief=tk.FLAT, bg='gray')
        menu_button_imagen.menu = tk.Menu(menu_button_imagen, tearoff=0)
        menu_button_imagen["menu"] = menu_button_imagen.menu
         

        for imagen in imagenes:
            menu_button_imagen.menu.add_radiobutton(label = imagen, variable = imagenSeleccionada, value = imagen)

        menu_button_imagen.pack(side='left', padx=5, pady=5)
        
        print(imagenSeleccionada)

        # Botón "Preguntas"
        preguntasBoton = tk.Button(self.frameBarraTareas, text="Preguntas", command=lambda: messagebox.showinfo("Preguntas", "Aquí van las preguntas."),relief=tk.FLAT, bg='gray')
        preguntasBoton.pack(side='left', padx=5, pady=5)

        # Botón "Ayuda"
        ayudaBoton = tk.Button(self.frameBarraTareas, text="Ayuda", command=lambda: messagebox.showinfo("Ayuda", "Aquí va la ayuda."), relief=tk.FLAT, bg='gray')
        ayudaBoton.pack(side='left', padx=5, pady=5)

        # Botón "Imágenes de Prueba"
        ImagenesPruebaBoton = tk.Button(self.frameBarraTareas, text="Imágenes de Prueba", command=lambda: messagebox.showinfo("Imágenes de Prueba", "Aquí van las imágenes de prueba."), relief=tk.FLAT, bg='gray')
        ImagenesPruebaBoton.pack(side='left', padx=5, pady=5)

        # Grid principal
        frameGrid = tk.Frame(root)
        frameGrid.pack(pady=10)

       # Condición
        frameCondicion = tk.Frame(frameGrid)
        frameCondicion.grid(row = 0, column = 0, padx = 20)

        condiciones = ["Emétrope", "Miope", "Hipermétrope"]
        condicionSeleccionada = tk.StringVar(root)
        condicionSeleccionada.set("Seleccione Condicion")

        menuBotonCondicion = tk.Menubutton(frameCondicion, text="Condición", relief=tk.FLAT, bg="#3b82f6", fg="white")
        menuBotonCondicion.menu = tk.Menu(menuBotonCondicion, tearoff=0)
        menuBotonCondicion["menu"] = menuBotonCondicion.menu

        for condicion in condiciones:
            menuBotonCondicion.menu.add_radiobutton(label = condicion, variable = condicionSeleccionada, value = condicion)

        menuBotonCondicion.pack(pady=5)

        # Cuadro gris debajo de "Condicion"
        imagenOriginal = ImageTk.PhotoImage(Image.new("RGB", (300, 200), "gray"))
        tk.Label(frameCondicion, image = imagenOriginal).pack()

        # Grado
        frameGrado = tk.Frame(frameGrid)
        frameGrado.grid(row=0, column=1, padx=20)

        grados = ["Grado 1", "Grado 2", "Grado 3"]
        gradoSeleccionado = tk.StringVar(root)
        gradoSeleccionado.set("Seleccione Grado")

        menuBotonGrado = tk.Menubutton(frameGrado, text="Grado", relief=tk.FLAT, bg="#3b82f6", fg="white")
        menuBotonGrado.menu = tk.Menu(menuBotonGrado, tearoff=0)
        menuBotonGrado["menu"] = menuBotonGrado.menu

        for grado in grados:
            menuBotonGrado.menu.add_radiobutton(label = grado, variable = gradoSeleccionado, value = grado)

        menuBotonGrado.pack(pady=5)

        # Cuadro gris debajo de "Grado"
        marchaDeRayos = ImageTk.PhotoImage(Image.new("RGB", (300, 200), "gray"))
        tk.Label(frameGrado, image = marchaDeRayos).pack()

        # Distancia
        frameDistancia = tk.Frame(frameGrid)
        frameDistancia.grid(row=0, column=2, padx=10)
        #tk.Label(frame_distancia, text="Distancia", bg="#3b82f6", fg="white", padx=10, pady=5).pack()

        distancias = ["Punto lejano", "Punto cercano", "Punto medio"]
        distanciaSeleccionada = tk.StringVar(root)
        distanciaSeleccionada.set("Seleccione Distancia")

        menuBotonDistancia = tk.Menubutton(frameDistancia, text="Distancia", relief=tk.FLAT, bg="#3b82f6", fg="white")
        menuBotonDistancia.menu = tk.Menu(menuBotonDistancia, tearoff=0)
        menuBotonDistancia["menu"] = menuBotonDistancia.menu

        for distancia in distancias:
            menuBotonDistancia.menu.add_radiobutton(label = distancia, variable = distanciaSeleccionada, value = distancia)

        menuBotonDistancia.pack(pady=5)

        # Cuadro gris debajo de "Distancia"
        imagenEnElCerebro = ImageTk.PhotoImage(Image.new("RGB", (200, 200), "gray"))
        tk.Label(frameDistancia, image = imagenEnElCerebro).pack()

        # Información de distancia y botón
        frameInfo = tk.Frame(root)
        frameInfo.pack(pady=10, anchor='w')  # Align to the left

        tk.Label(frameInfo, text="Punto Remoto:").pack(anchor='w')
        tk.Label(frameInfo, text="Punto Lejano:").pack(anchor='w')
        tk.Label(frameInfo, text="Lente correctora:").pack(anchor='w')
            
        

def ejecutar_gui():
    root = tk.Tk()
    app = AplicacionPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_gui()