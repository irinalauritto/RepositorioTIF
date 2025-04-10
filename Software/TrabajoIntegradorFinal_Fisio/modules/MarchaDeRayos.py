import numpy as np  # Para cálculos matemáticos
import matplotlib.pyplot as plt  # Para generar gráficos
from matplotlib.widgets import Slider  # Para widgets interactivos en gráficos
import tkinter as tk  # Para crear la interfaz gráfica
from tkinter import ttk  # Para widgets avanzados de Tkinter
import matplotlib.backends.backend_tkagg as tkagg  # Para integrar gráficos de Matplotlib en Tkinter


class MarchaDeRayos:
    """Clase para simular la marcha de rayos en un sistema óptico."""
    def __init__(self, nombre, dioptriasLente, distanciaObjeto, distanciaFocal, anguloInicial):
        self.nombre = nombre
        self.dioptriasLente = dioptriasLente
        self.ax = None  # Inicializar el eje como None
        self.distanciaObjeto = distanciaObjeto #mm
        self.distanciaFocal = distanciaFocal #mm
        self.distanciaRetina = 25 #mm
        self.anguloInicial = anguloInicial #rad (inicializar en 0)
        self.imagen = None  # Inicializar la imagen como None
    
    def dibujarSimulacion(self, nDistanciaFocal , nDistanciaObjeto ,  ax):
        ax.clear()  # Limpia el gráfico actual
        ax.set_xlim(-200, 200)  # Establece los límites del eje X
        ax.set_ylim(-70, 70)  # Establece los límites del eje Y
        ax.axvline(x=0, color='blue', linestyle='--', label='Lente')  # Dibuja la lente
        ax.axhline(y=0, color='black', linewidth=1)  # Dibuja el eje óptico

        self.distanciaFocal = nDistanciaFocal  # Actualiza la distancia focal
        self.distanciaObjeto = nDistanciaObjeto   # Actualiza la distancia del objeto

        ax.plot([-self.distanciaObjeto, -self.distanciaObjeto], [0, 50], 'k-', linewidth=3, label='Objeto')  # Dibuja el objeto

        if self.distanciaFocal != self.distanciaObjeto:  # Calcula y dibuja la imagen si es posible
            try:
                self.distanciaImagen = 1 / (1 / self.distanciaFocal - 1 / self.distanciaObjeto)  # Calcula la distancia de la imagen
                self.alturaImagen = -50 * (self.distanciaImagen / self.distanciaObjeto)  # Calcula la altura de la imagen
                ax.plot([self.distanciaImagen, self.distanciaImagen], [0, self.alturaImagen], 'r-', linewidth=3, label='Imagen')  # Dibuja la imagen
            except ZeroDivisionError:
                pass  # Maneja el caso en que la distancia del objeto sea igual a la distancia focal

        ax.legend()  # Muestra la leyenda
        ax.figure.canvas.draw()  # Actualiza el gráfico

# Actualiza la simulación con los valores de los sliders
    def actualizarSimulacion(self, nuevaDistanciaFocal, nuevaDistanciaObjeto, ax):
        self.distanciaFocal= nuevaDistanciaFocal  # Obtiene el valor del slider de longitud focal
        self.distanciaObjeto = nuevaDistanciaObjeto  # Obtiene el valor del slider de distancia del objeto
        self.dibujarSimulacion(self.distanciaFocal,self.distanciaObjeto, ax)  # Redibuja la simulación
    
   


    
    def saludo(self):
        """
        Devuelve un saludo.

        Returns:
            str: El saludo.
        """
        return f"Hola, {self.nombre}!"

