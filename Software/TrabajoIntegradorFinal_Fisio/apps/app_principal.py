import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageFilter
import modules.GestorDeArchivos as ga
import modules.GestorDeImagenes as gi
import modules.MarchaDeRayos as mr
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import modules.Hipermetropia as h
import modules.Miopia as m
import modules.Emetropia as e
from tkinter import ttk

gArchivos = ga.gestorDeArchivos("Gestor de Archivos")
gArchivos.extraeListadoDeArchivos("\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas")
directoriosImagenes = gArchivos.getListadoDeArchivos()
print("Archivos cargados desde el directorio:")
for archivo in directoriosImagenes:
    print(archivo)
gImagen = gi.gestorDeImagenes("Gestor de Imagenes")
mRayos = mr.MarchaDeRayos("Marcha de Rayos") # [mm]
hipermetropia = h.Hipermetropia("Hipermétrope",1)
miopia = m.Miopia("Miope",1)
emetropia = e.Emetropia("Emétrope")
distancias = ["0.10 m","0.25 m", "0.33 m", "0.50 m", "1 m", "2 m", "10 m"]

class AplicacionPrincipal:
    """Clase principal de la aplicación."""
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador del ojo humano")
        self.condicion = "Emétrope"
        self.grado = "Grado 1" # "Grado 1" o simplemente 1
        self.distancia = "10 m"
        self.index = 0
        self.gradoDeDifuminado = 0

        self.root.configure(bg="#c9c9c9")

        # Crea el notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Frame para la simulación
        self.frameSimulacion = tk.Frame(self.notebook, bg="#c9c9c9")
        self.notebook.add(self.frameSimulacion, text="Simulación")

        # Frame para preguntas
        self.framePreguntas = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.framePreguntas, text="Preguntas")

        # Frame para galería de imágenes
        self.frameGaleria = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.frameGaleria, text="Imágenes")

        # Crear la barra de tareas con fondo personalizado
        self.frameBarraTareas = tk.Frame(self.frameSimulacion, bg="#c9c9c9")
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

        # Botón "Ayuda"
        ayudaBoton = tk.Button(self.frameBarraTareas, text="Ayuda", command=lambda: messagebox.showinfo("Ayuda", "Aquí va la ayuda."), relief=tk.RAISED)
        ayudaBoton.pack(side='left', padx=5, pady=5)

        # Grid principal con fondo personalizado
        self.frameGrid = tk.Frame(self.frameSimulacion, bg="#c9c9c9")
        self.frameGrid.pack(expand=True, fill='both')

        # Configura pesos para que las columnas y filas crezcan proporcionalmente
        self.frameGrid.columnconfigure(0, weight=1)
        self.frameGrid.columnconfigure(1, weight=1)
        self.frameGrid.columnconfigure(2, weight=1)
        self.frameGrid.rowconfigure(0, weight=1)

        # Crea los frames hijos ANTES de ubicarlos
        self.frameCondicion = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameGrado = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameDistancia = tk.Frame(self.frameGrid, bg="#c9c9c9")

        # Ahora sí, ubícalos en el grid
        self.frameCondicion.grid(row=0, column=0, padx=10, sticky='nsew')
        self.frameGrado.grid(row=0, column=1, padx=20, sticky='nsew')
        self.frameDistancia.grid(row=0, column=2, padx=10, sticky='nsew')

        # Variables iniciales
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

        # Condición
        self.frameCondicion = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameCondicion.grid(row=0, column=0, padx=10, sticky='nsew')

        condiciones = ["Emétrope", "Miope", "Hipermétrope"]
        self.condicionSeleccionada = tk.StringVar(root)
        self.condicionSeleccionada.set("Seleccione Condicion")

        boton_fuente = ("TkDefaultFont", 12)

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

        self.imagenOriginal = ImageTk.PhotoImage(Image.new("RGB", (300, 300), "gray"))
        self.labelImagenOriginal = tk.Label(self.frameCondicion, image=self.imagenOriginal, bg="#c9c9c9")
        self.labelImagenOriginal.pack(expand=True, fill='both', padx=10, pady=10)

        # Grado
        self.frameGrado = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameGrado.grid(row=0, column=1, padx=20, sticky='nsew')

        grados = ["Grado 1", "Grado 2", "Grado 3"]
        self.gradoSeleccionado = tk.StringVar(root)
        self.gradoSeleccionado.set("Seleccione Grado")

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
        fig, self.ax = plt.subplots(figsize=(6, 3))
        canvas = tkagg.FigureCanvasTkAgg(fig, master=self.frameGrado)
        canvas.get_tk_widget().pack(pady=100)

        # Simulación inicial 
        # Se puede reemplazar esto pasando a mRayos simplemente condición, grado y distancia (o posicion del elemento en vector distancias) como parámetros
        """
        mRayos.setDistanciaObjeto(float(self.distancia.replace(" m", ""))*1000) # Convierte a mm
        if self.condicion == "Emétrope":
            mRayos.setDistanciaFocal(emetropia.getDistanciaFocal())
        elif self.condicion == "Miope":
            mRayos.setDistanciaFocal(miopia.getDistanciaFocal())
        elif self.condicion == "Hipermétrope":
            mRayos.setDistanciaFocal(hipermetropia.getDistanciaFocal())
        mRayos.dibujarSimulacion(self.ax)
"""
        # Distancia
        self.frameDistancia = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameDistancia.grid(row=0, column=2, padx=10, sticky='nsew')

        #distancias = ["0.10 m","0.25 m", "0.33 m", "0.50 m", "1 m", "2 m", "10 m"]
        self.distanciaSeleccionada = tk.StringVar(root)
        self.distanciaSeleccionada.set("0.25 m")

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

        self.imagenDifuminada = ImageTk.PhotoImage(Image.new("RGB", (300, 300), "gray"))
        self.labelImagenDifuminada = tk.Label(self.frameDistancia, image=self.imagenDifuminada, bg="#c9c9c9")
        self.labelImagenDifuminada.pack(expand=True, fill='both', padx=10, pady=10)

        # Información de distancia y botón
        frameInfo = tk.Frame(self.frameSimulacion, bd=2, relief=tk.SUNKEN, padx=35, pady=15, bg="#e0e0e0")
        frameInfo.pack(padx=10, pady=5, anchor='w')

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
        self.mostrarImagenes(self.index, self.gradoDeDifuminado)

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

        # --- PESTAÑA DE PREGUNTAS ---
        pregunta = tk.Label(self.framePreguntas, text="¿Cuál es la distancia focal del ojo humano emétrope?", bg="#f5f5f5", font=("Arial", 12))
        pregunta.pack(pady=20)

        opciones = [
            "A) 250 mm",
            "B) 500 mm",
            "C) 100 mm",
            "D) 10 mm"
        ]
        self.respuesta = tk.StringVar()
        for opcion in opciones:
            tk.Radiobutton(self.framePreguntas, text=opcion, variable=self.respuesta, value=opcion, bg="#f5f5f5").pack(anchor='w', padx=40)

        def verificar():
            if self.respuesta.get().startswith("A"):
                messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            else:
                messagebox.showinfo("Incorrecto", "Respuesta incorrecta.")

        tk.Button(self.framePreguntas, text="Verificar", command=verificar).pack(pady=20)

        # --- PESTAÑA DE IMÁGENES (GALERÍA) ---
        self.imagenes_galeria = [
            {
                "archivo": "manejar_emetrope.jpg",
                "titulo": "Emétrope",
                "descripcion": "Visión de un emétrope al manejar."
            },
            {
                "archivo": "manejar_miope.jpg",
                "titulo": "Miope",
                "descripcion": "Visión de un miope al manejar."
            },
            {
                "archivo": "manejar_hipermetrope.jpg",
                "titulo": "Hipermétrope",
                "descripcion": "Visión de un hipermétrope al manejar."
            },
            # Agrega más imágenes aquí
        ]
        self.galeria_index = 0

        # Imagen
        self.galeria_img_label = tk.Label(self.frameGaleria, bg="#f5f5f5")
        self.galeria_img_label.pack(expand=True, fill='both', pady=20)

        # Título
        self.galeria_titulo_label = tk.Label(self.frameGaleria, font=("Arial", 12, "bold"), bg="#f5f5f5")
        self.galeria_titulo_label.pack()

        # Descripción
        self.galeria_desc_label = tk.Label(self.frameGaleria, font=("Arial", 10), bg="#f5f5f5", wraplength=300, justify="center")
        self.galeria_desc_label.pack(pady=(0, 20))

        # Flechas
        flechas_frame = tk.Frame(self.frameGaleria, bg="#f5f5f5")
        flechas_frame.pack()

        self.boton_izq = tk.Button(flechas_frame, text="⬅", command=self.galeria_anterior, font=("Arial", 16), width=3)
        self.boton_izq.pack(side="left", padx=20, expand=True, fill="both")
        self.boton_der = tk.Button(flechas_frame, text="➡", command=self.galeria_siguiente, font=("Arial", 16), width=3)
        self.boton_der.pack(side="left", padx=20, expand=True, fill="both")

        # Soporte para flechas del teclado
        self.frameGaleria.bind_all("<Left>", lambda e: self.galeria_anterior())
        self.frameGaleria.bind_all("<Right>", lambda e: self.galeria_siguiente())

        # Mostrar la primera imagen al iniciar
        self.mostrar_imagen_galeria()

        # Redimensionar imagen de galería al cambiar tamaño de ventana
        self.frameGaleria.bind("<Configure>", self.redimensionar_imagen_galeria)
        self.galeria_img_label.bind("<Configure>", self.redimensionar_imagen_galeria)

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

    def mostrar_imagen_galeria(self):
        datos = self.imagenes_galeria[self.galeria_index]
        try:
            ruta = f"\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes\\{datos['archivo']}"
            imagen = gImagen.mostrar_imagen(ruta)
            # Obtiene el tamaño actual del label
            w = self.galeria_img_label.winfo_width()
            h = self.galeria_img_label.winfo_height()
            # Si el label aún no tiene tamaño, usa un valor por defecto
            if w < 50 or h < 50:
                w, h = 1600, 1200
          
            img_tk = ImageTk.PhotoImage(imagen)
        except Exception as e:
            print(f"Error cargando imagen de galería: {e}")
            img_tk = None

        if img_tk:
            self.galeria_img_label.config(image=img_tk, text="")
            self.galeria_img_label.image = img_tk
        else:
            self.galeria_img_label.config(image="", text="Imagen no encontrada")
            self.galeria_img_label.image = None

        self.galeria_titulo_label.config(text=datos["titulo"])
        self.galeria_desc_label.config(text=datos["descripcion"])

    def redimensionar_imagen_galeria(self, event):
        self.mostrar_imagen_galeria()

    def galeria_anterior(self):
        if self.galeria_index > 0:
            self.galeria_index -= 1
            self.mostrar_imagen_galeria()

    def galeria_siguiente(self):
        if self.galeria_index < len(self.imagenes_galeria) - 1:
            self.galeria_index += 1
            self.mostrar_imagen_galeria()

    def actualizarValores(self):
        self.condicion = self.condicionSeleccionada.get()
        self.grado = self.gradoSeleccionado.get()
        self.distancia = self.distanciaSeleccionada.get()

        if(self.condicion == "Emétrope"):
            print(f"Condición: {self.condicion}, Grado: {self.grado}, Distancia: {self.distancia}")
        else:
            print(f"Condición: {self.condicion}, Grado: {self.grado}, Distancia: {self.distancia}")

        if self.grado == "Grado 1":
            grado = 1
        elif self.grado == "Grado 2":
            grado = 3
        elif self.grado == "Grado 3":
            grado = 6
        else:
            grado = 1

        if self.condicion == "Emétrope":
            mRayos.setCondicion("Emétrope")
            mRayos.setGrado(1)  # Emétrope no tiene grado, se utiliza grado 1 por defecto
            mRayos.setDistanciaObjeto(distancias.index(self.distancia)) 
            #mRayos.setDistanciaFocal(emetropia.getDistanciaFocal())
            #mRayos.setPuntoProximo(emetropia.getPuntoCercano()*1000)
            #mRayos.setPuntoLejano(emetropia.getPuntoLejano()*1000)
            self.puntoCercano = emetropia.getPuntoCercano()
            self.puntoLejano = emetropia.getPuntoLejano()
            self.lenteCorrectora = 0
            self.gradoDeDifuminado = 0

        elif self.condicion == "Miope": # a mRayos se le pasa en orden condicion -> grado -> distancia
            miopia.setGrado(grado)
            mRayos.setCondicion("Miope")
            mRayos.setGrado(grado)
            mRayos.setDistanciaObjeto(distancias.index(self.distancia))
            #mRayos.setDistanciaFocal(miopia.getDistanciaFocal())
            #mRayos.setPuntoProximo(miopia.calcularPuntoCercano()*1000)
            #mRayos.setPuntoLejano(miopia.calcularPuntoLejano()*1000)
            self.puntoCercano = miopia.calcularPuntoCercano()
            self.puntoLejano = miopia.calcularPuntoLejano()
            self.lenteCorrectora = miopia.getDioptriasLenteCorrectora()
            
            #Difuminado para grado 1
            if grado == 1 and ((self.distancia == "0.25 m" or self.distancia == "0.33 m" or self.distancia == "0.50 m" or 
                                    self.distancia == "1 m" )):
                self.gradoDeDifuminado = 0
            if grado == 1 and ((self.distancia == "0.10 m" or self.distancia == "2 m" or 
                                    self.distancia == "10 m" )):
                self.gradoDeDifuminado = miopia.calcularRadioDeDifuminacion()

            #Difuminado para grado 2
            if grado == 2 and ((self.distancia == "0.25 m" or self.distancia == "0.33 m" or self.distancia == "0.50 m" or 
                                    self.distancia == "1 m" )):
                self.gradoDeDifuminado = 0
            if grado == 1 and ((self.distancia == "0.10 m" or self.distancia == "2 m" or 
                                    self.distancia == "10 m" )):
                self.gradoDeDifuminado = miopia.calcularRadioDeDifuminacion()
            
            #Difuminado para grado 3
            if grado == 1 and ((self.distancia == "0.25 m" or self.distancia == "0.33 m" or self.distancia == "0.50 m" or 
                                    self.distancia == "1 m" )):
                self.gradoDeDifuminado = 0
            if grado == 1 and ((self.distancia == "0.10 m" or self.distancia == "2 m" or 
                                    self.distancia == "10 m" )):
                self.gradoDeDifuminado = miopia.calcularRadioDeDifuminacion()

        elif self.condicion == "Hipermétrope":
            hipermetropia.setGrado(grado)
            mRayos.setCondicion("Hipermétrope") 
            mRayos.setGrado(grado)
            mRayos.setDistanciaObjeto(distancias.index(self.distancia))
            #mRayos.setDistanciaFocal(hipermetropia.getDistanciaFocal())
            #mRayos.setPuntoProximo(hipermetropia.calcularPuntoCercano()*1000)
            #mRayos.setPuntoLejano(hipermetropia.calcularPuntoLejano()*1000)
            self.puntoCercano = hipermetropia.calcularPuntoCercano()
            self.puntoLejano = hipermetropia.calcularPuntoLejano()
            self.lenteCorrectora = hipermetropia.getDioptriasLenteCorrectora()

            #Difuminado para grado 1
            if grado == 1 and (( self.distancia == "0.33 m" or self.distancia == "0.50 m" or 
                                    self.distancia == "1 m" or self.distancia == "2 m" or self.distancia == "10 m" )):
                self.gradoDeDifuminado = 0
            if grado == 1 and ((self.distancia == "0.25 m" or self.distancia == "0.10 m"  )):
                self.gradoDeDifuminado = miopia.calcularRadioDeDifuminacion()

            #Difuminado para grado 2
            if grado == 2 and ((self.distancia == "0.10 m" or self.distancia == "0.25 m" or self.distancia == "0.50 m" or 
                                    self.distancia == "0.33 m" or self.distancia == "0.50 m"  )):
                self.gradoDeDifuminado = hipermetropia.calcularRadioDeDifuminacion()
            if grado == 2 and ((self.distancia == "1 m" or self.distancia == "2 m" or 
                                    self.distancia == "10 m" )):
                self.gradoDeDifuminado = 0

            #Difuminado para grado 3
            if grado == 2 and ((self.distancia == "0.10 m" or self.distancia == "0.25 m" or self.distancia == "0.50 m" or 
                                    self.distancia == "0.33 m" or self.distancia == "0.50 m" or self.distancia == "1 m" )):
                self.gradoDeDifuminado = hipermetropia
            if grado == 3 and ((self.distancia == "2 m" or self.distancia == "10 m" )):
                self.gradoDeDifuminado = 0

        self.ax.clear()
        #mRayos.setDistanciaObjeto(float(self.distancia.replace(" m", "")) * 1000)
        mRayos.dibujarSimulacion(self.ax)

        self.mostrarImagenDifuminada(self.index, self.gradoDeDifuminado)
        if self.condicionSeleccionada.get() == "Emétrope":
            self.puntoCercano = emetropia.getPuntoCercano()
            self.labelCondicion.config(text="Condición: " + self.condicion)
            self.labelGrado.config("Grado: No corresponde")
            self.labelDistancia.config(text="Distancia: " + self.distancia)
            self.labelPuntoCercano.config(text="Punto Cercano: " + str(self.puntoCercano) + "[m]")
            self.labelPuntoLejano.config(text="Punto Lejano: " + str(self.puntoLejano) + "[m]")
            self.labelLenteCorrectora.config(text="Lente correctora: " + str(self.lenteCorrectora) + "[D]")
        else:
            #self.puntoCercano = emetropia.getPuntoCercano()
            self.labelCondicion.config(text="Condición: " + self.condicion)
            self.labelGrado.config(text=self.grado)
            self.labelDistancia.config(text="Distancia: " + self.distancia)
            self.labelPuntoCercano.config(text="Punto Cercano: " + str(self.puntoCercano) + "[m]")
            self.labelPuntoLejano.config(text="Punto Lejano: " + str(self.puntoLejano) + "[m]")
            self.labelLenteCorrectora.config(text="Lente correctora: " + str(self.lenteCorrectora) + "[D]")

    def galeria_anterior(self):
        if self.galeria_index > 0:
            self.galeria_index -= 1
            self.mostrar_imagen_galeria()

    def galeria_siguiente(self):
        if self.galeria_index < len(self.imagenes_galeria) - 1:
            self.galeria_index += 1
            self.mostrar_imagen_galeria()

    
def ejecutar_gui():
    root = tk.Tk()
    app = AplicacionPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_gui()