"""
import numpy as np
import flet as ft
import matplotlib.pyplot as plt
import tempfile
import os

# Funciones de óptica matricial
def espacio_libre(d):
    return np.array([[1, d], [0, 1]])

def lente_delgada(f):
    return np.array([[1, 0], [-1 / f, 1]])

def sistema_optico(distancia_espacio, distancia_focal, distancia_retina):
    M_espacio = espacio_libre(distancia_espacio)
    M_lente = lente_delgada(distancia_focal)
    M_retina = espacio_libre(distancia_retina)
    return M_retina @ M_lente @ M_espacio

def propagar_rayo(y_inicial, theta_inicial, M_total):
    rayo_inicial = np.array([y_inicial, theta_inicial])
    rayo_final = M_total @ rayo_inicial
    return rayo_inicial, rayo_final

# Generar gráfico y guardarlo como archivo temporal
def generar_grafico(distancia_espacio, distancia_focal, distancia_retina, altura_objeto, angulo_inicial):
    M_total = sistema_optico(distancia_espacio, distancia_focal, distancia_retina)
    
    # Solo dos rayos: el perpendicular y el que pasa por el foco
    y_vals = [0, distancia_focal]
    rayos = [propagar_rayo(y, angulo_inicial, M_total) for y in y_vals]

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axhline(0, color="black", linewidth=0.8)  # Eje óptico
    ax.axvline(distancia_espacio, color="blue", linewidth=1.5, label="Lente")  # Lente
    ax.axvline(distancia_espacio + distancia_retina, color="red", linewidth=1.5, label="Retina")  # Retina

    # Dibujar rayos
    for rayo_inicial, rayo_final in rayos:
        y1, theta1 = rayo_inicial
        y2, _ = rayo_final

        # Primera sección (espacio libre)
        x1, x2 = 0, distancia_espacio
        ax.plot([x1, x2], [y1, y1 + theta1 * distancia_espacio], color="green")

        # Segunda sección (a través de la lente)
        y_lente = y1 + theta1 * distancia_espacio
        theta_lente = theta1 - y_lente / distancia_focal
        x3, x4 = distancia_espacio, distancia_espacio + distancia_retina
        ax.plot([x3, x4], [y_lente, y2], color="green")

    # Etiquetas y configuración del gráfico
    ax.set_title("Simulación de Marcha de Rayos")
    ax.set_xlabel("Distancia (mm)")
    ax.set_ylabel("Altura (mm)")
    ax.legend()
    ax.grid(True)

    # Guardar gráfico temporalmente
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(temp_file.name)
    plt.close(fig)
    return temp_file.name

# Flet: interfaz gráfica
def main(page: ft.Page):
    page.title = "Simulación Óptica - Marcha de Rayos"

    # Parámetros iniciales
    distancia_espacio = 10  # mm
    distancia_focal = 15    # mm
    distancia_retina = 20   # mm
    altura_objeto = 250       # mm
    angulo_inicial = 0    # rad

    # Imagen inicial
    temp_image = generar_grafico(distancia_espacio, distancia_focal, distancia_retina, altura_objeto, angulo_inicial)
    img = ft.Image(
        src=f"/{temp_image}",
        width=600,
        height=300
    )

    # Crear textos para etiquetas
    espacio_label = ft.Text(f"Espacio Libre: {distancia_espacio:.1f} mm")
    focal_label = ft.Text(f"Distancia Focal: {distancia_focal:.1f} mm")
    retina_label = ft.Text(f"Distancia Retina: {distancia_retina:.1f} mm")

    # Función para manejar cambios en sliders
    def on_change(e):
        nonlocal distancia_espacio, distancia_focal, distancia_retina
        if e.control.data == "espacio":
            distancia_espacio = float(e.control.value)
            espacio_label.value = f"Espacio Libre: {distancia_espacio:.1f} mm"
            espacio_label.update()
        elif e.control.data == "focal":
            distancia_focal = float(e.control.value)
            focal_label.value = f"Distancia Focal: {distancia_focal:.1f} mm"
            focal_label.update()
        elif e.control.data == "retina":
            distancia_retina = float(e.control.value)
            retina_label.value = f"Distancia Retina: {distancia_retina:.1f} mm"
            retina_label.update()
        actualizar_imagen()

    # Sliders interactivos
    slider_espacio = ft.Slider(
        min=5, max=30, value=distancia_espacio,
        on_change=on_change, data="espacio", divisions=10
    )

    slider_focal = ft.Slider(
        min=10, max=50, value=distancia_focal,
        on_change=on_change, data="focal", divisions=10
    )

    slider_retina = ft.Slider(
        min=10, max=50, value=distancia_retina,
        on_change=on_change, data="retina", divisions=10
    )

    # Añadir elementos a la página
    page.add(
        espacio_label,
        slider_espacio,
        focal_label,
        slider_focal,
        retina_label,
        slider_retina,
        img
    )

    def actualizar_imagen():
        temp_image = generar_grafico(distancia_espacio, distancia_focal, distancia_retina, altura_objeto, angulo_inicial)
        img.src = f"/{temp_image}"
        img.update()

ft.app(target=main)
"""

# Ejemplo de simulación de óptica geométrica con Tkinter
import numpy as np  # Para cálculos matemáticos
import matplotlib.pyplot as plt  # Para generar gráficos
from matplotlib.widgets import Slider  # Para widgets interactivos en gráficos
import tkinter as tk  # Para crear la interfaz gráfica
from tkinter import ttk  # Para widgets avanzados de Tkinter
import matplotlib.backends.backend_tkagg as tkagg  # Para integrar gráficos de Matplotlib en Tkinter
from matplotlib.patches import Ellipse

altura_objeto = 50
focal_length_emetrope = 100
infinito = focal_length_emetrope*2000

# Dibuja la simulación óptica en el gráfico
def draw_optical_sim(focal_length, object_distance, ax):

    # Determina la condición del ojo
    if focal_length == focal_length_emetrope:
        condicion = 'Ojo emetrope'
    elif focal_length > focal_length_emetrope:
        condicion = 'Ojo miope'
    else:
        condicion = 'Ojo hipermetrope'

    ax.clear()  # Limpia el gráfico actual
    ax.set_xlim(-400, 400)  # Establece los límites del eje X
    ax.set_ylim(-150, 150)  # Establece los límites del eje Y
    ax.set_aspect('equal', adjustable='box')  # Asegura que los ejes tengan la misma escala
    ax.axvline(x=0, color='blue', linestyle='--', label='Lente')  # Dibuja la lente
    ax.axhline(y=0, color='black', linewidth=1)  # Dibuja el eje óptico
    ax.axvline(x=focal_length, color='black', linewidth=1, linestyle='--',label='Retina')  # Dibuja el eje óptico
    ax.add_patch(Ellipse(
        (focal_length / 2, 0),  # Centro del óvalo
        width=focal_length,     # Ancho del óvalo (eje mayor)
        height=focal_length_emetrope,  # Alto del óvalo (eje menor)
        edgecolor='cyan',       # Color del borde
        fill=False,             # Sin relleno
        linestyle='--',         # Estilo de línea
        label=condicion
        ))  # Añade el óvalo al gráfico

    # Dibuja el objeto
    ax.plot([-object_distance, -object_distance], [0, altura_objeto], 'k-', linewidth=3, label='Objeto')

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
    
    # Imagen virtual
    if focal_length > object_distance:  # Calcula y dibuja la imagen si es posible
            
        image_distance = 1 / (1 / focal_length - 1 / object_distance)  # Calcula la distancia de la imagen
        image_height = -altura_objeto * (image_distance / object_distance)  # Calcula la altura de la imagen
        
        # Dibuja la imagen
        ax.plot([image_distance, image_distance], [0, image_height], 'r-', linewidth=3, label='Imagen')
    
        # Rayo paralelo al eje óptico
        ax.plot(
            [-object_distance, 0, -image_distance],
            [altura_objeto, altura_objeto, -image_height],
            'y', linewidth=0.7
        )

        # Proyección del rayo paralelo al eje óptico
        ax.plot(
            [0, image_distance],
            [altura_objeto, image_height],
            'y--', linewidth=0.9
        )

        # Rayo que cruza el foco
        ax.plot(
            [-object_distance, 0, focal_length],
            [altura_objeto, altura_objeto, 0],
            'y', linewidth=0.7
        )

        # Proyeccion del rayo que cruza el centro de la lente
        ax.plot(
            [-object_distance, image_distance],
            [altura_objeto, image_height],
            'y--', linewidth=0.9
        )
        
        # Rayo que cruza el centro de la lente
        ax.plot(
            [-object_distance, 0, infinito],
            [altura_objeto, image_height, -image_height],
            'y', linewidth=0.7
        )

        # Proyección del rayo que cruza el centro de la lente
        ax.plot(
            [0, image_distance],
            [image_height, image_height],
            'y--', linewidth=0.9
        )

    ax.legend()  # Muestra la leyenda
    ax.figure.canvas.draw()  # Actualiza el gráfico

# Actualiza la simulación con los valores de los sliders
def update_sim(slider_focal, slider_object, ax):
    focal_length = slider_focal.get()  # Obtiene el valor del slider de longitud focal
    object_distance = slider_object.get()  # Obtiene el valor del slider de distancia del objeto
    draw_optical_sim(focal_length, object_distance, ax)  # Redibuja la simulación

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

    # Configura sliders para que se ajusten al tamaño de la ventana
    slider_focal = tk.Scale(frame, from_=50, to=200, resolution=10, orient='horizontal', label='Focal Length')
    slider_focal.set(100)
    slider_focal.grid(row=1, column=0, sticky="ew")  # Expande horizontalmente

    slider_object = tk.Scale(frame, from_=50, to=300, resolution=10, orient='horizontal', label='Object Distance')
    slider_object.set(150)
    slider_object.grid(row=1, column=1, sticky="ew")  # Expande horizontalmente

    update_button = ttk.Button(frame, text="Actualizar", command=lambda: update_sim(slider_focal, slider_object, ax))
    update_button.grid(row=2, column=0, columnspan=2, sticky="ew")  # Expande horizontalmente

    # Configura el gráfico para que se ajuste al tamaño de la ventana
    frame.rowconfigure(0, weight=1)  # Permite que el gráfico se expanda verticalmente
    frame.columnconfigure(0, weight=1)  # Permite que el gráfico se expanda horizontalmente

    draw_optical_sim(100, 150, ax)  # Dibuja la simulación inicial
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica

tkinter_gui()  # Ejecuta la interfaz gráfica
