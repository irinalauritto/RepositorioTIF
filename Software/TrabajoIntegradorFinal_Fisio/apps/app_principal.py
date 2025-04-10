import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk
import modules.GestorDeArchivos as ga
import modules.GestorDeImagenes as gi
import modules.MarchaDeRayos as mr
import matplotlib.pyplot as plt  # Para generar gráficos
import matplotlib.backends.backend_tkagg as tkagg  # Para integrar gráficos de Matplotlib en Tkinter



gArchivos = ga.gestorDeArchivos("Gestor de Archivos")
gArchivos.extraeListadoDeArchivos("\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas")
directoriosImagenes = gArchivos.getListadoDeArchivos()
gImagen = gi.gestorDeImagenes("Gestor de Imagenes")
mRayos = mr.MarchaDeRayos("Marcha de Rayos", 25, 150, 25, 0)

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
        self.frameGrid = tk.Frame(root)
        self.frameGrid.pack(pady=10, expand=True, fill='both')

        # Configurar la expansión de las filas y columnas
        self.frameGrid.columnconfigure(0, weight=1)
        self.frameGrid.columnconfigure(1, weight=1)
        self.frameGrid.columnconfigure(2, weight=1)
        self.frameGrid.rowconfigure(0, weight=1)

        # Condición
        self.frameCondicion = tk.Frame(self.frameGrid)
        self.frameCondicion.grid(row=0, column=0, padx=10, sticky='nsew')

        condiciones = ["Emétrope", "Miope", "Hipermétrope"]
        condicionSeleccionada = tk.StringVar(root)
        condicionSeleccionada.set("Seleccione Condicion")

        menuBotonCondicion = tk.Menubutton(self.frameCondicion, text="Condición", relief=tk.FLAT, bg="#3b82f6", fg="white")
        menuBotonCondicion.menu = tk.Menu(menuBotonCondicion, tearoff=0)
        menuBotonCondicion["menu"] = menuBotonCondicion.menu

        for condicion in condiciones:
            menuBotonCondicion.menu.add_radiobutton(label=condicion, variable=condicionSeleccionada, value=condicion)

        menuBotonCondicion.pack(pady=5)

        # Cuadro gris debajo de "Condicion"
        self.imagenOriginal = ImageTk.PhotoImage(Image.new("RGB", (200, 200), "gray"))
        self.labelImagenOriginal = tk.Label(self.frameCondicion, image=self.imagenOriginal)
        self.labelImagenOriginal.pack(expand=True, fill='both')

        # Grado
        self.frameGrado = tk.Frame(self.frameGrid)
        self.frameGrado.grid(row=0, column=1, padx=20, sticky='nsew')

        grados = ["Grado 1", "Grado 2", "Grado 3"]
        gradoSeleccionado = tk.StringVar(root)
        gradoSeleccionado.set("Seleccione Grado")

        menuBotonGrado = tk.Menubutton(self.frameGrado, text="Grado", relief=tk.FLAT, bg="#3b82f6", fg="white")
        menuBotonGrado.menu = tk.Menu(menuBotonGrado, tearoff=0)
        menuBotonGrado["menu"] = menuBotonGrado.menu

        for grado in grados:
            menuBotonGrado.menu.add_radiobutton(label=grado, variable=gradoSeleccionado, value=grado)

        menuBotonGrado.pack(pady=1)
        fig, ax = plt.subplots(figsize=(4, 2))  # Ajusta el tamaño del gráfico con figsize
        canvas = tkagg.FigureCanvasTkAgg(fig, master=self.frameGrado)  # Integra el gráfico en Tkinter

        # Usa grid para posicionar el canvas
        canvas.get_tk_widget().pack(pady = 50)  # Posiciona el gráfico en la cuadrícula

        # Configurar el tamaño del frame para que se ajuste al gráfico
        #self.frameGrado.rowconfigure(0, weight=1)
        #self.frameGrado.columnconfigure(0, weight=1)

        # Dibujar la simulación inicial
        mRayos.dibujarSimulacion(25, 150, ax)  # Dibuja la simulación inicial
        #canvas.draw()

        # Distancia
        self.frameDistancia = tk.Frame(self.frameGrid)
        self.frameDistancia.grid(row=0, column=2, padx=10, sticky='nsew')

        distancias = ["Punto lejano", "Punto cercano", "Punto medio"]
        self.distanciaSeleccionada = tk.StringVar(root)
        self.distanciaSeleccionada.set("Seleccione Distancia")

        menuBotonDistancia = tk.Menubutton(self.frameDistancia, text="Distancia", relief=tk.FLAT, bg="#3b82f6", fg="white")
        menuBotonDistancia.menu = tk.Menu(menuBotonDistancia, tearoff=0)
        menuBotonDistancia["menu"] = menuBotonDistancia.menu

        for distancia in distancias:
            menuBotonDistancia.menu.add_radiobutton(label=distancia, variable=self.distanciaSeleccionada, value=distancia)

        menuBotonDistancia.pack(pady=5)

        # Cuadro gris debajo de "Distancia"
        self.imagenEnElCerebro = ImageTk.PhotoImage(Image.new("RGB", (200, 200), "gray"))
        tk.Label(self.frameDistancia, image=self.imagenEnElCerebro).pack(expand=True, fill='both')
        # Información de distancia y botón
        frameInfo = tk.Frame(root, bd=2, relief=tk.SUNKEN, padx=35, pady=15, bg="#e0e0e0")
        frameInfo.pack(padx=10, pady=5, anchor='w')  # Align to the left
        
        
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