import numpy as np  # Para cálculos matemáticos
import matplotlib.pyplot as plt  # Para generar gráficos
from matplotlib.widgets import Slider  # Para widgets interactivos en gráficos
import tkinter as tk  # Para crear la interfaz gráfica
from tkinter import ttk  # Para widgets avanzados de Tkinter
import matplotlib.backends.backend_tkagg as tkagg  # Para integrar gráficos de Matplotlib en Tkinter
from matplotlib.patches import Ellipse

class MarchaDeRayos:
    """Clase para simular la marcha de rayos en un sistema óptico."""
    def __init__(self, nombre, distanciaFocal, puntoProximo, puntoLejano ):
        self.nombre = nombre
        self.ax = None  # Inicializar el eje como None
        self.alturaObjeto = 170
        self.distanciaFocal = distanciaFocal #mm
        self.distanciaImagen = 250#mm
        self.infinito = self.distanciaFocal*2000
        self.distanciaObjetoMin = puntoProximo #cm
        self.distanciaObjetoMax = puntoLejano #cm  
        self.distanciaObjeto = 0  # Inicializar la distancia del objeto

    def dibujarSimulacion(self,ax):
        self.ax = ax
        self.ax.clear()  # Limpia el gráfico actual
        self.ax.set_xlim(-1500, 500)  # Establece los límites del eje X
        self.ax.set_ylim(-500, 500)  # Establece los límites del eje Y
        self.ax.set_aspect('equal', adjustable='box')  # Asegura que los ejes tengan la misma escala
        self.ax.set_xticks([])  # Elimina las marcas del eje X
        self.ax.set_yticks([])  # Elimina las marcas del eje Y
        self.ax.axvline(x=0, color='blue', linestyle='--', label='Lente')  # Dibuja la lente
        self.ax.axhline(y=0, color='black', linewidth=1)  # Dibuja el eje óptico
        self.ax.axvline(x=self.distanciaImagen, color='black', linewidth=1, linestyle='--', label='Retina')  # Dibuja la retina
        self.ax.add_patch(Ellipse(
            (self.distanciaImagen/2, 0),                # Centro del óvalo
            width=self.distanciaImagen,   # Ancho del óvalo (eje mayor)
            height=self.distanciaImagen,  # Alto del óvalo (eje menor)
            edgecolor='cyan',       # Color del borde
            fill=False,             # Sin relleno
            linestyle='--',         # Estilo de línea
            label='Ojo'
            ))  # Añade el óvalo al gráfico

        self.ax.plot(-self.distanciaObjetoMin, 0, marker='X', markersize=6, label='Punto proximo')
        self.ax.plot(-self.distanciaObjetoMax, 0, marker='X', markersize=6, label='Punto lejano')

         # Dibuja el objeto
        self.ax.plot([-self.distanciaObjeto, -self.distanciaObjeto], [0, self.alturaObjeto], 'k-', linewidth=3, label='Objeto')

         # Dentro de los puntos limite la imagen siempre se formará en la retina la incognita es el punto focal
        # Calculo el punto focal
        if self.distanciaObjetoMin <= self.distanciaObjeto and self.distanciaObjeto <= self.distanciaObjetoMax: # Si se encuentra entre el pto lejano y proximo
            self.distanciaFocal = 1/(1/self.distanciaObjeto+1/self.distanciaImagen)     # El ojo ajusta su potencia para ubicar la imagen en la retina (acomodacion)
        if self.distanciaObjeto < self.distanciaObjetoMin:                      # Si el objeto esta dentro del punto proximo
            self.distanciaFocal = 1/(1/self.distanciaObjetoMin+1/self.distanciaImagen) # La potencia del ojo es la maxima que puede lograr (correspondida a la distancia minima a la que puede ver claramente un objeto)
        if  self.distanciaObjetoMax < self.distanciaObjeto:                     # Si el objeto esta mas alla del punto lejano
            self.distanciaFocal = 1/(1/self.distanciaObjetoMax+1/self.distanciaImagen) # La potencia del ojo es la minima que puede lograr (correspondida a la distancia maxima a la que puede ver claramente un objeto)
        

        # Imagen real
        if self.distanciaFocal < self.distanciaObjeto:  # Calcula y dibuja la imagen si es posible
            self.distanciaImagen = 1 / (1 / self.distanciaFocal - 1 / self.distanciaObjeto)  # Calcula la distancia de la imagen
            self.alturaImagen = -self.alturaObjeto * (self.distanciaImagen / self.distanciaObjeto)  # Calcula la altura de la imagen
            
            # Dibuja la imagen
            self.ax.plot([self.distanciaImagen, self.distanciaImagen], [0, self.alturaImagen], 'r-', linewidth=3, label='Imagen')
        
            # Rayo paralelo al eje óptico
            self.ax.plot(
                [-self.distanciaObjeto, 0,self.distanciaImagen],
                [self.alturaObjeto, self.alturaObjeto, self.alturaImagen],
                'y', linewidth=0.5
            )
            
            # Rayo que cruza el foco
            self.ax.plot(
                [-self.distanciaObjeto, -self.distanciaFocal, self.distanciaImagen],
                [self.alturaObjeto, 0, self.alturaImagen],
                'y', linewidth=0.5
            )
            
            # Rayo que cruza el centro de la lente
            self.ax.plot(
                [-self.distanciaObjeto, 0, self.distanciaImagen],
                [self.alturaObjeto, 0, self.alturaImagen],
                'y', linewidth=0.5
            )
# Actualiza la simulación con los valores de los sliders
    def actualizarSimulacion(self, nuevaDistanciaFocal, nuevaDistanciaObjeto, nuevoPuntoProximo, nuevoPuntolejano):
        self.distanciaFocal= nuevaDistanciaFocal  # Obtiene el valor del slider de longitud focal
        self.distanciaObjeto = nuevaDistanciaObjeto  # Obtiene el valor del slider de distancia del objeto
        self.distanciaObjetoMin = nuevoPuntoProximo
        self.distanciaObjetoMax = nuevoPuntolejano  # Obtiene el valor del slider de distancia del objeto

        self.dibujarSimulacion(self.ax)   


    
    def saludo(self):
        """
        Devuelve un saludo.

        Returns:
            str: El saludo.
        """
        return f"Hola, {self.nombre}!"

