# Ejemplo de simulación de óptica geométrica con Tkinter
import numpy as np  # Para cálculos matemáticos
import matplotlib.pyplot as plt  # Para generar gráficos
from matplotlib.widgets import Slider  # Para widgets interactivos en gráficos
import tkinter as tk  # Para crear la interfaz gráfica
from tkinter import ttk  # Para widgets avanzados de Tkinter
import matplotlib.backends.backend_tkagg as tkagg  # Para integrar gráficos de Matplotlib en Tkinter
from matplotlib.patches import Ellipse

altura_objeto = 170
focal_length = 100
infinito = focal_length*2000
condicion = ['Emétrope', 'Miope', 'Hipermétrope']
condicion_seleccionada = 0 # 0 emetrope, 1 miope, 2 hipermetrope
distance_values = [5, 10, 15, 20, 25, 30, 100, 300, 500, 700, 1000, 1500] # cm

# Dibuja la simulación óptica en el gráfico
def draw_optical_sim(object_distance, ax):
    
    if condicion_seleccionada == 0: # Si es emetrope
        punto_proximo = 25  # cm
        punto_lejano = 1000 # cm
    elif condicion_seleccionada == 1: # Si es miope
        punto_proximo = 5  # cm
        punto_lejano = 1000 # cm
    elif condicion_seleccionada == 2: # Si es hipermetrope
        punto_proximo = 1000 # cm
        punto_lejano = 1500 # cm
    
    image_distance = 300    # Distancia a la retina, lugar donde siempre se forma la imagen
    min_object_distance = punto_proximo # Distancia de objeto asociada con el punto cercano
    max_object_distance = punto_lejano  # Distancia de objeto asociada con el punto lejano

    ax.clear()  # Limpia el gráfico actual
    ax.set_xlim(-1500, 1500)  # Establece los límites del eje X
    ax.set_ylim(-500, 500)  # Establece los límites del eje Y
    ax.set_aspect('equal', adjustable='box')  # Asegura que los ejes tengan la misma escala
    ax.set_xticks([])  # Elimina las marcas del eje X
    ax.set_yticks([])  # Elimina las marcas del eje Y
    ax.axvline(x=0, color='blue', linestyle='--', label='Lente')  # Dibuja la lente
    ax.axhline(y=0, color='black', linewidth=1)  # Dibuja el eje óptico
    ax.axvline(x=image_distance, color='black', linewidth=1, linestyle='--', label='Retina')  # Dibuja la retina
    ax.add_patch(Ellipse(
        (image_distance/2, 0),                # Centro del óvalo
        width=image_distance,   # Ancho del óvalo (eje mayor)
        height=image_distance,  # Alto del óvalo (eje menor)
        edgecolor='cyan',       # Color del borde
        fill=False,             # Sin relleno
        linestyle='--',         # Estilo de línea
        label='Ojo'
        ))  # Añade el óvalo al gráfico

    ax.plot(-punto_proximo, 0, marker='X', markersize=6, label='Punto proximo')
    ax.plot(-punto_lejano, 0, marker='X', markersize=6, label='Punto lejano')

    # Dibuja el objeto
    ax.plot([-object_distance, -object_distance], [0, altura_objeto], 'k-', linewidth=3, label='Objeto')

    # Dentro de los puntos limite la imagen siempre se formará en la retina la incognita es el punto focal
    # Calculo el punto focal
    if min_object_distance <= object_distance and object_distance <= max_object_distance: # Si se encuentra entre el pto lejano y proximo
        focal_length = 1/(1/object_distance+1/image_distance)     # El ojo ajusta su potencia para ubicar la imagen en la retina (acomodacion)
    if object_distance < min_object_distance:                      # Si el objeto esta dentro del punto proximo
        focal_length = 1/(1/min_object_distance+1/image_distance) # La potencia del ojo es la maxima que puede lograr (correspondida a la distancia minima a la que puede ver claramente un objeto)
    if  max_object_distance < object_distance:                     # Si el objeto esta mas alla del punto lejano
        focal_length = 1/(1/max_object_distance+1/image_distance) # La potencia del ojo es la minima que puede lograr (correspondida a la distancia maxima a la que puede ver claramente un objeto)
    
    # Imagen real
    if focal_length < object_distance:  # Calcula y dibuja la imagen si es posible
        image_distance = 1 / (1 / focal_length - 1 / object_distance)  # Calcula la distancia de la imagen
        image_height = -altura_objeto * (image_distance / object_distance)  # Calcula la altura de la imagen
        
        # Dibuja la imagen
        ax.plot([image_distance, image_distance], [0, image_height], 'r-', linewidth=3, label='Imagen')
    
        # Rayo paralelo al eje óptico
        ax.plot(
            [-object_distance, 0, image_distance],
            [altura_objeto, altura_objeto, image_height],
            'y', linewidth=0.5
        )

        # Rayo que cruza el foco
        ax.plot(
            [-object_distance, -focal_length, image_distance],
            [altura_objeto, 0, image_height],
            'y', linewidth=0.5
        )

        # Rayo que cruza el centro de la lente
        ax.plot(
            [-object_distance, 0, image_distance],
            [altura_objeto, 0, image_height],
            'y', linewidth=0.5
        )
    
    # Imagen virtual e imagen en punto focal no se grafican

    ax.legend()  # Muestra la leyenda
    ax.figure.canvas.draw()  # Actualiza el gráfico

# Actualiza la simulación con los valores de los sliders
def update_sim(slider_object, slider_value, ax):
    index = slider_object.get()  # Obtiene el índice del slider
    object_distance = distance_values[index]  # Obtiene el valor real de distance_values
    slider_value.set(f"Distancia objeto: {object_distance} cm")  # Actualiza la etiqueta del slider
    draw_optical_sim(object_distance, ax)  # Redibuja la simulación

# Crea la interfaz gráfica con Tkinter
def tkinter_gui():
    root = tk.Tk()  # Crea la ventana principal
    root.title("Simulación de Óptica Geométrica")  # Establece el título de la ventana

    # Configura la ventana para que se pueda redimensionar
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    frame = ttk.Frame(root, padding=10)  # Crea un marco para organizar los widgets
    frame.grid(row=0, column=0, sticky="nsew")  # Permite que el marco se expanda
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    fig, ax = plt.subplots()  # Crea un gráfico de Matplotlib
    canvas = tkagg.FigureCanvasTkAgg(fig, master=frame)  # Integra el gráfico en Tkinter
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew")  # Permite que el gráfico se expanda

    # Variable para mostrar el valor actual del slider
    slider_value = tk.StringVar()
    slider_value.set(f"{distance_values[8]} cm")  # Valor inicial
    # Etiqueta para mostrar el valor actual del slider
    label = ttk.Label(frame, textvariable=slider_value)
    label.grid(row=2, column=0, columnspan=2, sticky="ew")

    # Configura sliders para que se ajusten al tamaño de la ventana
    slider_object = tk.Scale(
        frame, from_=0, to=len(distance_values)-1, 
        orient='horizontal', label='Distancia del objeto: ', 
        showvalue=False
    )
    slider_object.set(8)  # Establece el valor inicial del slider
    slider_object.grid(row=1, column=0, sticky="ew")  # Expande horizontalmente

    update_button = ttk.Button(frame, text="Actualizar", command=lambda: update_sim(slider_object, slider_value, ax))
    update_button.grid(row=3, column=0, columnspan=2, sticky="ew")  # Expande horizontalmente

    # Configura el gráfico para que se ajuste al tamaño de la ventana
    frame.rowconfigure(0, weight=1)  # Permite que el gráfico se expanda verticalmente
    frame.columnconfigure(0, weight=1)  # Permite que el gráfico se expanda horizontalmente

    draw_optical_sim(distance_values[8], ax)  # Dibuja la simulación inicial
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica

tkinter_gui()  # Ejecuta la interfaz gráfica