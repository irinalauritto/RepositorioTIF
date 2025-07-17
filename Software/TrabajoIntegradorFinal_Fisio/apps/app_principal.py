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
import random

# Creacion de objetos
gArchivos = ga.gestorDeArchivos("Gestor de Archivos")
gImagen = gi.gestorDeImagenes("Gestor de Imagenes")
mRayos = mr.MarchaDeRayos("Marcha de Rayos") 
hipermetropia = h.Hipermetropia("Hipermétrope",1)
miopia = m.Miopia("Miope",1)
emetropia = e.Emetropia("Emétrope")

# Carga de archivos
gArchivos.extraeListadoDeArchivos("\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas")
directoriosImagenes = gArchivos.getListadoDeArchivos()
print("Archivos cargados desde el directorio:")
for archivo in directoriosImagenes:
    print(archivo)

# Creación de vector distancias
distancias = ["0.10 m","0.25 m", "0.33 m", "0.50 m", "1 m", "2 m", "10 m", "15 m"]

# Variable auxiliar de limite de difuminación en las imagenes arbol y vela
limiteDifuminacion = 10

class AplicacionPrincipal:
    """Clase principal de la aplicación."""
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador del ojo humano")
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

        # --- PESTAÑA DE SIMULACION ---
        self.configuracionDeSimulacion()

        # --- PESTAÑA DE PREGUNTAS ---
        self.configuracionDePreguntas()

        # --- PESTAÑA DE IMÁGENES (GALERÍA) ---
        self.configuracionDeGaleria()

    def configuracionDeSimulacion(self):
        # Botón para seleccionar imágenes
        imagenes = ["Árbol", "Vela"]
        self.imagenSeleccionada = tk.StringVar(self.root)
        self.imagenSeleccionada.set("Seleccionar imagen")

        menu_button_imagen = tk.Menubutton(self.frameBarraTareas, text="Seleccionar Imagen", relief=tk.RAISED, bg="white")
        menu_button_imagen.menu = tk.Menu(menu_button_imagen, tearoff=0)
        menu_button_imagen["menu"] = menu_button_imagen.menu

        for i, imagen in enumerate(imagenes):
            menu_button_imagen.menu.add_radiobutton(label=imagen, variable=self.imagenSeleccionada, value=imagen, command=lambda i=i: self.mostrarImagenes(i, self.gradoDeDifuminado))

        menu_button_imagen.pack(side='left', padx=5, pady=5)

        # Botón "Ayuda"
        ayudaBoton = tk.Button(
            self.frameBarraTareas,
            text="Ayuda",
            command=self.mostrar_ayuda,  # Cambia el comando aquí
            relief=tk.RAISED
        )
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

        # Se ubican los frames en el grid
        self.frameCondicion.grid(row=0, column=0, padx=10, sticky='nsew')
        self.frameGrado.grid(row=0, column=1, padx=10, sticky='nsew')
        self.frameDistancia.grid(row=0, column=2, padx=10, sticky='nsew')
        self.frameDistancia.rowconfigure(0, weight=1)  # <-- Agrega esto
        
        # Botón de condición
        self.frameCondicion = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameCondicion.grid(row=0, column=0, padx=10, sticky='nsew')

        condiciones = ["Emétrope", "Miope", "Hipermétrope"]
        self.condicionSeleccionada = tk.StringVar(self.root)
        self.condicionSeleccionada.set("Seleccione condición")

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

        # Botón de grado
        self.frameGrado = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameGrado.grid(row=0, column=1, padx=20, sticky='nsew')

        grados = ["Grado 1", "Grado 2", "Grado 3"]
        self.gradoSeleccionado = tk.StringVar(self.root)
        #self.gradoSeleccionado.set("Seleccione Grado")

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

        # Botón de distancia
        self.frameDistancia = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameDistancia.grid(row=0, column=2, padx=10, sticky='nsew')
        self.frameDistancia.rowconfigure(0, weight=1)  # <-- Agrega esto
        self.distanciaSeleccionada = tk.StringVar(self.root)
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

        # Se crea el gráfico donde irá la marcha de rayos (simulación inicial en blanco)
        fig, self.ax = plt.subplots(figsize=(7, 5))
        self.ax.set_xticks([])  # Elimina las marcas del eje X
        self.ax.set_yticks([])  # Elimina las marcas del eje Y
        canvas = tkagg.FigureCanvasTkAgg(fig, master=self.frameGrado)
        canvas.get_tk_widget().pack(pady=100)

        # Configura una nueva fila para info
        self.frameGrid.rowconfigure(1, weight=0)  # Fila para info, no se expande tanto como la de imágenes

        # Crea frameInfo y ubícalo en el grid, columna central (debajo de frameGrado)
        self.frameInfo = tk.Frame(self.frameGrid, bd=2, relief=tk.SUNKEN, padx=25, pady=10, bg="#e0e0e0")
        self.frameInfo.grid(row=3, column=0, padx=20, pady=(10, 20), sticky='ew')

        # Labels dentro de frameInfo
        self.labelCondicion = tk.Label(self.frameInfo, text="Seleccione condición", bg="#e0e0e0")
        self.labelCondicion.pack(anchor='w')
        self.labelGrado = tk.Label(self.frameInfo, text= "", bg="#e0e0e0")
        self.labelGrado.pack(anchor='w')
        self.labelDistancia = tk.Label(self.frameInfo, text="Distancia: ", bg="#e0e0e0")
        self.labelDistancia.pack(anchor='w')
        self.labelPuntoCercano = tk.Label(self.frameInfo, text="Punto cercano: ", bg="#e0e0e0")
        self.labelPuntoCercano.pack(anchor='w')
        self.labelPuntoLejano = tk.Label(self.frameInfo, text="Punto lejano: ", bg="#e0e0e0")
        self.labelPuntoLejano.pack(anchor='w')
        self.labelLenteCorrectora = tk.Label(self.frameInfo, text="Lente correctora: ", bg="#e0e0e0")
        self.labelLenteCorrectora.pack(anchor='w')

       
        # Se ubica la imagen original
        self.imagenOriginal = ImageTk.PhotoImage(Image.new("RGB", (400, 500), "gray"))
        self.labelImagenOriginal = tk.Label(self.frameCondicion, image=self.imagenOriginal, bg="#c9c9c9")
        self.labelImagenOriginal.pack(expand=True, fill='both', padx=10, pady=10)

        # Se ubica la imagen difuminada
        self.imagenDifuminada = ImageTk.PhotoImage(Image.new("RGB", (400, 500), "gray"))
        self.labelImagenDifuminada = tk.Label(self.frameDistancia, image=self.imagenDifuminada, bg="#c9c9c9")
        self.labelImagenDifuminada.pack(expand=True, fill='both', padx=10, pady=10)

        # Se muestran las imagenes
        self.mostrarImagenes(self.index, self.gradoDeDifuminado)

        # Nuevo frame para el botón debajo de la imagen difuminada
        self.frameActualizar = tk.Frame(self.frameGrid, bg="#c9c9c9")
        self.frameActualizar.grid(row=3, column=2, padx=10, pady=(0,20), sticky='nsew')

        actualizarBoton = tk.Button(
            self.frameActualizar,
            text="Actualizar",
            command=self.actualizarValores,
            relief=tk.RAISED,
            bg="white",
            font=boton_fuente,
            padx=20,
            pady=10,
            width=10
        )
        actualizarBoton.pack(expand=True, pady=10)

    def mostrarImagen(self, index):
        if index < len(directoriosImagenes):
            print(f"Mostrando imagen {index}")
            imagen_path = "\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas\\" + directoriosImagenes[index]
            print(f"Ruta de la imagen: {imagen_path}")
            imagen = gImagen.mostrar_imagen(imagen_path)
            imagen = imagen.resize((400, 500))
            self.imagenOriginal = ImageTk.PhotoImage(imagen)
            self.labelImagenOriginal.config(image=self.imagenOriginal)
            self.labelImagenOriginal.image = self.imagenOriginal

    def mostrarImagenDifuminada(self, index, gradoDifuminacion):
        if gradoDifuminacion > limiteDifuminacion:
            gradoDifuminacion = limiteDifuminacion
        if index < len(directoriosImagenes):
            print(f"Mostrando imagen {index}")
            imagen_path = "\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_nuevas\\" + directoriosImagenes[index]
            print(f"Ruta de la imagen: {imagen_path}")
            imagen = gImagen.mostrar_imagen(imagen_path)
            imagen = imagen.resize((400, 500))
            imagenDifuminada = imagen.filter(ImageFilter.GaussianBlur(radius=gradoDifuminacion))
            self.imagenDifuminada = ImageTk.PhotoImage(imagenDifuminada)
            self.labelImagenDifuminada.config(image=self.imagenDifuminada)
            self.labelImagenDifuminada.image = self.imagenDifuminada

    def mostrarImagenes(self, index, gradoDifuminacion):
        self.mostrarImagen(index)
        self.index = index
        self.mostrarImagenDifuminada(index, gradoDifuminacion)

    def mostrar_imagen_galeria(self):
        datos = self.imagenes_galeria[self.galeria_index]
        try:
            ruta = f"\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes\\{datos['archivo']}"
            imagen = gImagen.mostrar_imagen(ruta)
            # Redimensiona la imagen al tamaño fijo 528x397
            imagen = imagen.resize((900,700), Image.LANCZOS) # Tamaño con el que quiero que se muestren las imagenes
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

    def configuracionDePreguntas(self):
        import tkinter.font as tkFont
        # Banco de preguntas (puedes agregar más)
        banco_preguntas = [
            {
                "pregunta": "¿Qué lente corrige la miopía?",
                "opciones": [
                    "A) Lente convergente",
                    "B) Lente divergente",
                    "C) Lente bifocal",
                    "D) Lente cilíndrica"
                ],
                "respuesta": "B"
            },
            {
                "pregunta": "¿Cuál es el punto lejano de un ojo miope sin corregir?",
                "opciones": [
                    "A) Infinito",
                    "B) 50 m",
                    "C) Menor que infinito",
                    "D) Mayor que infinito"
                ],
                "respuesta": "C"
            },
            {
                "pregunta": "¿Qué es la hipermetropía?",
                "opciones": [
                    "A) Dificultad para ver de lejos",
                    "B) Dificultad para ver de cerca",
                    "C) Visión doble",
                    "D) Visión borrosa solo de noche"
                ],
                "respuesta": "B"
            },
            {
                "pregunta": "¿Qué lente corrige la hipermetropía?",
                "opciones": [
                    "A) Lente divergente",
                    "B) Lente convergente",
                    "C) Lente bifocal",
                    "D) Lente cilíndrica"
                ],
                "respuesta": "B"
            },
            {
                "pregunta": "¿Qué significa emetropía?",
                "opciones": [
                    "A) Condición oftalmológica ideal",
                    "B) Dificultad para ver de lejos",
                    "C) Dificultad para ver de cerca",
                    "D) Visión borrosa"
                ],
                "respuesta": "A"
            },
            {
                "pregunta": "¿Cuál es el punto cercano típico de un ojo sano?",
                "opciones": [
                    "A) 10 cm",
                    "B) 25 cm",
                    "C) 50 cm",
                    "D) 1 m"
                ],
                "respuesta": "B"
            },
            {
                "pregunta": "¿Qué unidad se usa para medir la potencia de una lente?",
                "opciones": [
                    "A) Metro",
                    "B) Dioptría",
                    "C) Milímetro",
                    "D) Grado"
                ],
                "respuesta": "B"
            }
        ]

        # Selecciona 3 preguntas al azar y en orden aleatorio
        self.preguntas = random.sample(banco_preguntas, 4)

        # Limpia el frame antes de agregar widgets
        for widget in self.framePreguntas.winfo_children():
            widget.destroy()

        self.respuestas_usuario = [tk.StringVar(value="") for _ in self.preguntas]
        self.resultados = [None for _ in self.preguntas]
        self.marcadores = []  # Para los labels de tick/cruz

        pregunta_frames = []

        def verificar_individual(idx):
            correcta = self.preguntas[idx]["respuesta"]
            seleccion = self.respuestas_usuario[idx].get()
            # Limpia todos los marcadores antes de marcar
            for lbl in self.marcadores[idx]:
                lbl.config(text="")
            if seleccion == "":
                return  # No marcar nada si no eligió
            for i, opcion in enumerate(self.preguntas[idx]["opciones"]):
                letra = opcion[0]
                if seleccion == letra:
                    if seleccion == correcta:
                        self.marcadores[idx][i].config(text="✔️", fg="green")
                        self.resultados[idx] = True
                    else:
                        self.marcadores[idx][i].config(text="❌", fg="red")
                        self.resultados[idx] = False
                elif letra == correcta and seleccion != correcta:
                    self.marcadores[idx][i].config(text="✔️", fg="green")

        # Mostrar todas las preguntas
        for idx, pregunta in enumerate(self.preguntas):
            frame_preg = tk.Frame(self.framePreguntas, bg="#f5f5f5", bd=2, relief=tk.GROOVE)
            frame_preg.pack(padx=10, pady=10, fill="x")
            pregunta_frames.append(frame_preg)

            tk.Label(frame_preg, text=f"{idx+1}. {pregunta['pregunta']}", bg="#f5f5f5", font=("Arial", 12)).pack(anchor="w", pady=(5, 2))

            marcadores_opciones = []
            opciones_frame = tk.Frame(frame_preg, bg="#f5f5f5")
            opciones_frame.pack(anchor="w")
            for i, opcion in enumerate(pregunta["opciones"]):
                subframe = tk.Frame(opciones_frame, bg="#f5f5f5")
                subframe.pack(anchor="w")
                rb = tk.Radiobutton(
                    subframe,
                    text=opcion,
                    variable=self.respuestas_usuario[idx],
                    value=opcion[0],  # "A", "B", etc.
                    bg="#f5f5f5"
                )
                rb.pack(side="left")
                lbl = tk.Label(subframe, text="", bg="#f5f5f5", font=("Arial", 14, "bold"))
                lbl.pack(side="left", padx=10)
                marcadores_opciones.append(lbl)
            self.marcadores.append(marcadores_opciones)

            tk.Button(
                frame_preg,
                text="Verificar",
                command=lambda i=idx: verificar_individual(i)
            ).pack(anchor="e", pady=5)

        # Calificación
        self.calificacion_label = tk.Label(self.framePreguntas, text="", bg="#f5f5f5", font=("Arial", 14, "bold"))
        self.calificacion_label.pack(pady=10)

        def calificar():
            correctas = 0
            total = len(self.preguntas)
            for idx, pregunta in enumerate(self.preguntas):
                if self.respuestas_usuario[idx].get() == pregunta["respuesta"]:
                    correctas += 1
            nota = round(correctas / total * 10, 2)
            self.calificacion_label.config(text=f"Respuestas correctas: {correctas} de {total}   Nota: {nota}/10")

        tk.Button(self.framePreguntas, text="Calificar", command=calificar, bg="#3b82f6", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

    def configuracionDeGaleria(self):
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
            {
                "archivo": "aula_emetrope.jpg",
                "titulo": "Emétrope",
                "descripcion": "Visión de un emétrope en un aula."
            },
            {
                "archivo": "aula_miope.jpg",
                "titulo": "Miope",
                "descripcion": "Visión de un miope en un aula."
            },
            {
                "archivo": "aula_hipermetrope.jpg",
                "titulo": "Hipermétrope",
                "descripcion": "Visión de un hipermétrope en un aula."
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

    def mostrar_ayuda(self):
        ayuda_win = tk.Toplevel(self.root)
        ayuda_win.title("Ayuda")
        ayuda_win.configure(bg="white")

        # Frame para imagen y texto
        frame = tk.Frame(ayuda_win, bg="white")
        frame.pack(padx=20, pady=20)

        # Cuadro de texto antes de la imagen
        texto_ayuda = (
            "En esta ventana encontrarás ayuda sobre el uso del simulador.\n"
            "Selecciona una condición para el ojo, el grado de patología y la distancia a la que se ubicará el objeto.\n"
            "Luego haz clic en el botón Actualizar para ver los resultados.\n"
            "En la esquina inferior izquierda tendrás información sobre la situación elegida.\n\n"
            "Referencias de la marcha de rayos:\n"
        )
        label_texto_superior = tk.Label(
            frame,
            text=texto_ayuda,
            bg="white",
            font=("Arial", 12),
            wraplength=380,
            justify="left"  
        )
        label_texto_superior.pack(pady=(0, 15), anchor="w")  # Opcional: anchor="w" para alinear aún más a la izquierda

        # Cargar imagen de ayuda
        try:
            img_path = "\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\ayuda\\legends.png"
            imagen = Image.open(img_path)
            imagen = imagen.resize((200, 200))  # Ajusta el tamaño según lo necesario
            img_tk = ImageTk.PhotoImage(imagen)
        except Exception as e:
            img_tk = None

        # Mostrar imagen
        if img_tk:
            label_img = tk.Label(frame, image=img_tk, bg="white")
            label_img.image = img_tk  # Mantener referencia
            label_img.pack()
        else:
            label_img = tk.Label(frame, text="No se pudo cargar la imagen.", bg="white")
            label_img.pack()

    def actualizarValores(self):
        self.condicion = self.condicionSeleccionada.get()
        self.grado = self.gradoSeleccionado.get()
        self.distancia = self.distanciaSeleccionada.get()

        print(f"Condición: {self.condicion}, Grado: {self.grado}, Distancia: {self.distancia}")
        
        if self.grado == "Grado 1":
            grado = 1
            seleccionaGrado = True
        elif self.grado == "Grado 2":
            grado = 3
            seleccionaGrado = True
        elif self.grado == "Grado 3":
            grado = 6
            seleccionaGrado = True
        else: 
            grado = 1
            seleccionaGrado = False # Variable auxiliar de seleccion de grado inicial

        if seleccionaGrado == False:
            if self.condicion == "Emétrope":
                self.labelGrado.config(text="")
            else:
                self.labelGrado.config(text="Seleccione grado")

        if seleccionaGrado == True or self.condicion == "Emétrope":
            if self.condicion == "Emétrope":
                mRayos.setCondicion("Emétrope")
                mRayos.setGrado(1)  # Emétrope no tiene grado, se utiliza grado 1 por defecto
                mRayos.setDistanciaObjeto(distancias.index(self.distancia)) 

                self.puntoCercano = emetropia.getPuntoCercano()
                self.puntoLejano = emetropia.getPuntoLejano()
                self.lenteCorrectora = 0
                self.gradoDeDifuminado = emetropia.calcularRadioDeDifuminacion(float(self.distancia.replace(" m", "")))

            elif self.condicion == "Miope": # a mRayos se le pasa en orden condicion -> grado -> distancia
                miopia.setGrado(grado)
                self.puntoCercano = miopia.getPuntoCercano()
                self.puntoLejano = miopia.getPuntoLejano()
                self.lenteCorrectora = miopia.getDioptriasLenteCorrectora()

                mRayos.setCondicion("Miope")
                mRayos.setGrado(grado)
                mRayos.setDistanciaObjeto(distancias.index(self.distancia))

                self.gradoDeDifuminado = miopia.calcularRadioDeDifuminacion(float(self.distancia.replace(" m", "")))
                
            elif self.condicion == "Hipermétrope":
                hipermetropia.setGrado(grado)
                self.puntoCercano = hipermetropia.getPuntoCercano()
                self.puntoLejano = hipermetropia.getPuntoLejano()
                self.lenteCorrectora = hipermetropia.getDioptriasLenteCorrectora()

                mRayos.setCondicion("Hipermétrope") 
                mRayos.setGrado(grado)
                mRayos.setDistanciaObjeto(distancias.index(self.distancia))

                self.gradoDeDifuminado = hipermetropia.calcularRadioDeDifuminacion(float(self.distancia.replace(" m", "")))

            self.ax.clear()
            mRayos.dibujarSimulacion(self.ax)

            self.mostrarImagenDifuminada(self.index, self.gradoDeDifuminado)
            
            self.labelCondicion.config(text="Condición: " + self.condicion)
            if self.condicion == "Emétrope":
                self.labelGrado.config(text="")
            else:
                self.labelGrado.config(text=self.grado)
            self.labelDistancia.config(text="Distancia: " + self.distancia)
            self.labelPuntoCercano.config(text="Punto cercano: " + str(self.puntoCercano) + "[m]")
            self.labelPuntoLejano.config(text="Punto lejano: " + str(self.puntoLejano) + "[m]")
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
    root.state('zoomed')  # Maximiza la ventana al iniciar (Windows)
    app = AplicacionPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_gui()