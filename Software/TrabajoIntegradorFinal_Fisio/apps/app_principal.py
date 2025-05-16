import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageFilter
import modules.GestorDeArchivos as ga
import modules.GestorDeImagenes as gi
import modules.MarchaDeRayos as mr
import matplotlib.pyplot as plt  # Para generar gráficos
import matplotlib.backends.backend_tkagg as tkagg  # Para integrar gráficos de Matplotlib en Tkinter
import modules.Hipermetropia as h
import modules.Miopia as m
import modules.Emetropia as e


gArchivos = ga.gestorDeArchivos("Gestor de Archivos")
gArchivos.extraeListadoDeArchivos("\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas")
directoriosImagenes = gArchivos.getListadoDeArchivos()
gImagen = gi.gestorDeImagenes("Gestor de Imagenes")
mRayos = mr.MarchaDeRayos("Marcha de Rayos", 250, 25, 1000)
hipermetropia = h.Hipermetropia("Hipermétrope",1)
miopia = m.Miopia("Miope",1)
emetropia = e.Emetropia("Emétrope")



# Imprimir los archivos cargados para verificar
print("Archivos cargados desde el directorio:")
for archivo in directoriosImagenes:
    print(archivo)

class AplicacionPrincipal:
    """Clase principal de la aplicación."""
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador del ojo humano")
       # self.root.state('zoomed')  # Pantalla completa

        # Variables iniciales
        self.condicion = "Emétrope"  # Inicializa la condición como atributo de la clase
        self.grado = "Grado 1"  # Inicializa el grado como atributo de la clase
        self.distancia = "10 m"  # Inicializa la distancia como atributo de la clase
        self.index = 0
        self.gradoDeDifuminado = 0  # Grado de difuminado inicial

        # Cambiar el color de fondo de la ventana principal
        self.root.configure(bg="#c9c9c9")

        # Crear la barra de tareas con fondo personalizado
        self.frameBarraTareas = tk.Frame(self.root, bg="#c9c9c9")
        self.frameBarraTareas.pack(fill='x')

        # Botón para seleccionar imágenes
        imagenes = ["Arbol", "Vela"]
        self.imagenSeleccionada = tk.StringVar(root)
        self.imagenSeleccionada.set("Seleccionar imagen")

        menu_button_imagen = tk.Menubutton(self.frameBarraTareas, text="Seleccionar Imagen", relief=tk.RAISED, bg="white")
        menu_button_imagen.menu = tk.Menu(menu_button_imagen, tearoff=0)
        menu_button_imagen["menu"] = menu_button_imagen.menu

        for i, imagen in enumerate(imagenes):
            menu_button_imagen.menu.add_radiobutton(label=imagen, variable=self.imagenSeleccionada, value=imagen, command=lambda i=i: self.mostrarImagenes(i, self.gradoDeDifuminado))

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

        # Grid principal con fondo personalizado
        self.frameGrid = tk.Frame(self.root, bg="#c9c9c9")
        self.frameGrid.pack(pady=10, expand=True, fill='both')

        # Configurar la expansión de las filas y columnas
        self.frameGrid.columnconfigure(0, weight=1)
        self.frameGrid.columnconfigure(1, weight=1)
        self.frameGrid.columnconfigure(2, weight=1)
        self.frameGrid.rowconfigure(0, weight=1)

        #Definimos variables iniciales
        
        if(self.condicion == "Emétrope"):
            self.puntoCercano = emetropia.getPuntoCercano()
            self.puntoLejano = emetropia.getPuntoLejano()
            self.lenteCorrectora = 0

        elif(self.condicion == "Miope"):
            miopia.setGrado(self.grado)
            self.puntoCercano = miopia.calcularPuntoCercano()
            self.puntoLejano = miopia.calcularPuntoLejano()
            self.lenteCorrectora = miopia.getDioptriasLenteCorrectora()

        elif(self.condicion == "Hipermétrope"):
            hipermetropia.setGrado(self.grado)
            self.puntoCercano = hipermetropia.calcularPuntoCercano()
            self.puntoLejano = hipermetropia.calcularPuntoLejano()
            self.lenteCorrectora = hipermetropia.getDioptriasLenteCorrectora()

        
        # Condición with customized background
        self.frameCondicion = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameCondicion.grid(row=0, column=0, padx=10, sticky='nsew')

        condiciones = ["Emétrope", "Miope", "Hipermétrope"]
        self.condicionSeleccionada = tk.StringVar(root)
        self.condicionSeleccionada.set("Seleccione Condicion")

        # Ejemplo de fuente grande
        boton_fuente = ("TkDefaultFont", 12)

        # Menubutton Condición
        menuBotonCondicion = tk.Menubutton(
            self.frameCondicion,
            text="Condición",
            relief=tk.FLAT,
            bg="#3b82f6",
            fg="white",
            font=boton_fuente,
            padx=20,
            pady=10,
            width=12
        )
        menuBotonCondicion.menu = tk.Menu(menuBotonCondicion, tearoff=0)
        menuBotonCondicion["menu"] = menuBotonCondicion.menu

        for condicion in condiciones:
            menuBotonCondicion.menu.add_radiobutton(label=condicion, variable=self.condicionSeleccionada, value=condicion)

        menuBotonCondicion.pack(pady=4)

        # Cuadro gris debajo de "Condicion"
        self.imagenOriginal = ImageTk.PhotoImage(Image.new("RGB", (300, 300), "gray"))
        self.labelImagenOriginal = tk.Label(self.frameCondicion, image=self.imagenOriginal, bg="#c9c9c9")
        self.labelImagenOriginal.pack(expand=True, fill='both', padx=10, pady=10)

        # Grado with customized background
        self.frameGrado = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameGrado.grid(row=0, column=1, padx=20, sticky='nsew')

        grados = ["Grado 1", "Grado 2", "Grado 3"]
        self.gradoSeleccionado = tk.StringVar(root)
        self.gradoSeleccionado.set("Seleccione Grado")

        # Menubutton Grado
        menuBotonGrado = tk.Menubutton(
            self.frameGrado,
            text="Grado",
            relief=tk.FLAT,
            bg="#3b82f6",
            fg="white",
            font=boton_fuente,
            padx=20,
            pady=10,
            width=12
        )
        menuBotonGrado.menu = tk.Menu(menuBotonGrado, tearoff=0)
        menuBotonGrado["menu"] = menuBotonGrado.menu

        for grado in grados:
            menuBotonGrado.menu.add_radiobutton(label=grado, variable=self.gradoSeleccionado, value=grado)

        menuBotonGrado.pack(pady=1)
        fig, self.ax = plt.subplots(figsize=(6, 3))  # Ajusta el tamaño del gráfico con figsize
        canvas = tkagg.FigureCanvasTkAgg(fig, master=self.frameGrado)  # Integra el gráfico en Tkinter

        # Usa grid para posicionar el canvas
        canvas.get_tk_widget().pack(pady = 100)  # Posiciona el gráfico en la cuadrícula


        # Dibujar la simulación inicial
        mRayos.setDistanciaObjeto(float(self.distancia.replace(" m", ""))*100)        
        if self.condicion == "Emétrope":
            mRayos.setDistanciaFocal(emetropia.getDistanciaFocal())
        elif self.condicion == "Miope":  
            mRayos.setDistanciaFocal(miopia.getDistanciaFocal())
        elif self.condicion == "Hipermétrope":
            mRayos.setDistanciaFocal(hipermetropia.getDistanciaFocal())
        mRayos.dibujarSimulacion(self.ax)  # Dibuja la simulación inicial
        #canvas.draw()

        # Distancia with customized background
        self.frameDistancia = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameDistancia.grid(row=0, column=2, padx=10, sticky='nsew')

        distancias = ["0.10 m","0.25 m", "0.5 m", "1 m", "2 m", "5 m", "10 m"]
        self.distanciaSeleccionada = tk.StringVar(root)
        self.distanciaSeleccionada.set("0 m")

        # Menubutton Distancia
        menuBotonDistancia = tk.Menubutton(
            self.frameDistancia,
            text="Distancia",
            relief=tk.FLAT,
            bg="#3b82f6",
            fg="white",
            font=boton_fuente,
            padx=20,
            pady=10,
            width=12
        )
        menuBotonDistancia.menu = tk.Menu(menuBotonDistancia, tearoff=0)
        menuBotonDistancia["menu"] = menuBotonDistancia.menu

        for distancia in distancias:
            menuBotonDistancia.menu.add_radiobutton(label=distancia, variable=self.distanciaSeleccionada, value=distancia)

        menuBotonDistancia.pack(pady=5)

        # Cuadro gris debajo de "Distancia"
        self.imagenDifuminada = ImageTk.PhotoImage(Image.new("RGB", (300, 300), "gray"))
        self.labelImagenDifuminada = tk.Label(self.frameDistancia, image=self.imagenDifuminada, bg="#c9c9c9")
        self.labelImagenDifuminada.pack(expand=True, fill='both', padx=10, pady=10)

        # Información de distancia y botón
        frameInfo = tk.Frame(root, bd=2, relief=tk.SUNKEN, padx=35, pady=15, bg="#e0e0e0")
        frameInfo.pack(padx=10, pady=5, anchor='w')  # Align to the left
        
        self.labelCondicion = tk.Label(frameInfo, text="Condición: "+ self.condicion, bg="#e0e0e0")
        self.labelCondicion.pack(anchor='w')
        self.labelGrado = tk.Label(frameInfo, text= self.grado, bg="#e0e0e0")
        self.labelGrado.pack(anchor='w')
        self.labelDistancia = tk.Label(frameInfo, text="Distancia: "+ self.distancia, bg="#e0e0e0")
        self.labelDistancia.pack(anchor='w')
        self.labelPuntoCercano = tk.Label(frameInfo, text="Punto Cercano: "+ str(self.puntoCercano) +"[m]", bg="#e0e0e0")
        self.labelPuntoCercano.pack(anchor='w')
        self.labelPuntoLejano = tk.Label(frameInfo, text="Punto Lejano: "+ str(self.puntoLejano) +"[m]", bg="#e0e0e0")
        self.labelPuntoLejano.pack(anchor='w')
        self.labelLenteCorrectora = tk.Label(frameInfo, text="Lente correctora: "+ str(self.lenteCorrectora) +"[D]", bg="#e0e0e0")
        self.labelLenteCorrectora.pack(anchor='w')
        self.mostrarImagenes(self.index, self.gradoDeDifuminado)  # Muestra la primera imagen al iniciar

        # Botón "Actualizar" en la esquina inferior derecha
        actualizarBoton = tk.Button(
            self.frameDistancia,
            text="Actualizar",
            command=self.actualizarValores,
            relief=tk.RAISED,
            bg="white",
            font=boton_fuente,
            padx=20,
            pady=10,
            width=12
        )
        actualizarBoton.pack(side='bottom', fill='x', padx=10, pady=15)


   

    def mostrarImagen(self, index):
        if index < len(directoriosImagenes):
            print(f"Mostrando imagen {index}")
            imagen_path = "\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas\\" + directoriosImagenes[index]
            print(f"Ruta de la imagen: {imagen_path}")
            imagen = gImagen.mostrar_imagen(imagen_path)
            imagen = imagen.resize((300, 300))
            self.imagenOriginal = ImageTk.PhotoImage(imagen)
            self.labelImagenOriginal.config(image=self.imagenOriginal)
            self.labelImagenOriginal.image = self.imagenOriginal

    def mostrarImagenDifuminada(self, index, grado):
        #if(self.condicion == "Emétrope" and float(self.distancia.replace(" m", ""))<0.25):
        #   self.imagenDifuminada = ImageTk.PhotoImage(Image.new("RGB", (300, 300), "gray"))
        #    self.labelImagenDifuminada = tk.Label(self.frameDistancia, image=self.imagenDifuminada, bg="#c9c9c9")
        #    self.labelImagenDifuminada.pack(expand=True, fill='both', padx=10, pady=10)
            
        if index < len(directoriosImagenes):
                print(f"Mostrando imagen {index}")
                imagen_path = "\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas\\" + directoriosImagenes[index]
                print(f"Ruta de la imagen: {imagen_path}")
                imagen = gImagen.mostrar_imagen(imagen_path)
                imagen = imagen.resize((300, 300))
            
                imagenDifuminada = imagen.filter(ImageFilter.GaussianBlur(radius=grado))
                self.imagenDifuminada = ImageTk.PhotoImage(imagenDifuminada)
                self.labelImagenDifuminada.config(image=self.imagenDifuminada)
                self.labelImagenDifuminada.image = self.imagenDifuminada




    def mostrarImagenes(self, index, grado):
        self.mostrarImagen(index)
        self.index = index
        self.mostrarImagenDifuminada(index, grado)
    
    def actualizarValores(self):
        """Actualiza las variables globales con los valores seleccionados."""
        # Actualizar los atributos de la clase con los valores seleccionados
        self.condicion = self.condicionSeleccionada.get()
        self.grado = self.gradoSeleccionado.get()
        self.distancia = self.distanciaSeleccionada.get()

        print(f"Condición: {self.condicion}, Grado: {self.grado}, Distancia: {self.distancia}")

        # Actualizar la distancia del objeto en mRayos
        mRayos.setDistanciaObjeto(float(self.distancia.replace(" m", "")) * 100)
        if self.grado == "Grado 1":
            grado = 1
        elif self.grado == "Grado 2":   
            grado = 3
        elif self.grado == "Grado 3":
            grado = 6
        # Actualizar la distancia focal y el grado de difuminado según la condición
        if self.condicion == "Emétrope":
            mRayos.setDistanciaFocal(emetropia.getDistanciaFocal())
            mRayos.setPuntoProximo(emetropia.getPuntoCercano())
            mRayos.setPuntoLejano(emetropia.getPuntoLejano())
            self.puntoCercano = emetropia.getPuntoCercano()
            self.puntoLejano = emetropia.getPuntoLejano()
            self.lenteCorrectora = 0
            self.gradoDeDifuminado = 0

        elif self.condicion == "Miope":
            miopia.setGrado(grado)  
            mRayos.setDistanciaFocal(miopia.getDistanciaFocal())
            mRayos.setPuntoProximo(miopia.calcularPuntoCercano())
            mRayos.setPuntoLejano(miopia.calcularPuntoLejano()) 
            self.puntoCercano = miopia.calcularPuntoCercano()
            self.puntoLejano = miopia.calcularPuntoLejano()
            self.lenteCorrectora = miopia.getDioptriasLenteCorrectora()
            self.gradoDeDifuminado = miopia.calcularRadioDeDifuminacion()

        elif self.condicion == "Hipermétrope":
            hipermetropia.setGrado(grado)  
            mRayos.setDistanciaFocal(hipermetropia.getDistanciaFocal())
            mRayos.setPuntoProximo(hipermetropia.calcularPuntoCercano())
            mRayos.setPuntoLejano(hipermetropia.calcularPuntoLejano())
            self.puntoCercano = hipermetropia.calcularPuntoCercano()
            self.puntoLejano = hipermetropia.calcularPuntoLejano()
            self.lenteCorrectora = hipermetropia.getDioptriasLenteCorrectora()
            self.gradoDeDifuminado = hipermetropia.calcularRadioDeDifuminacion()

        # Redibujar la simulación
        self.ax.clear()  # Limpia el gráfico antes de redibujar
        mRayos.setDistanciaObjeto(float(self.distancia.replace(" m", "")) * 100)
        mRayos.dibujarSimulacion(self.ax)  # Dibuja la simulación actualizada
        self.ax.figure.canvas.draw()  # Actualiza el gráfico en la interfaz


        # Actualizar la imagen difuminada
        self.mostrarImagenDifuminada(self.index, self.gradoDeDifuminado)
        

        self.labelCondicion.config(text="Condición: " + self.condicion)
        self.labelGrado.config(text=self.grado)
        self.labelDistancia.config(text="Distancia: " + self.distancia)
        self.labelPuntoCercano.config(text="Punto Cercano: " + str(self.puntoCercano) + "[m]")
        self.labelPuntoLejano.config(text="Punto Lejano: " + str(self.puntoLejano) + "[m]")
        self.labelLenteCorrectora.config(text="Lente correctora: " + str(self.lenteCorrectora) + "[D]")

def ejecutar_gui():
 
    root = tk.Tk()
    app = AplicacionPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_gui()