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
