import numpy as np  # Para cálculos matemáticos
import matplotlib.pyplot as plt  # Para generar gráficos
from matplotlib.widgets import Slider  # Para widgets interactivos en gráficos
import tkinter as tk  # Para crear la interfaz gráfica
from tkinter import ttk  # Para widgets avanzados de Tkinter
import matplotlib.backends.backend_tkagg as tkagg  # Para integrar gráficos de Matplotlib en Tkinter
from matplotlib.patches import Ellipse

tamanoLegends = 5  # Tamaño de las leyendas en el gráfico

class MarchaDeRayos:
    """Clase para simular la marcha de rayos en un sistema óptico."""
    def __init__(self, nombre, distanciaFocal, puntoProximo, puntoLejano):
        self.nombre = nombre
        self.ax = None  # Inicializar el eje como None
        self.alturaObjeto = 170 #mm


        # Esto quizas podria comentarse e inicializar la graficacion en condicion emetrope
        self.distanciaFocal = distanciaFocal #mm
        self.distanciaImagen = 250 #mm
        self.infinito = self.distanciaFocal*2000
        self.distanciaObjetoMin = puntoProximo #mm
        self.distanciaObjetoMax = puntoLejano #mm  
        self.distanciaObjeto = 0  # Inicializar la distancia del objeto

    def setPuntoProximo(self, puntoProximo):
        """
        Establece el punto proximo.

        Args:
            puntoProximo (float): Punto proximo.
        """
        self.distanciaObjetoMin = puntoProximo
    def setPuntoLejano(self, puntoLejano):
        """
        Establece el punto lejano.

        Args:
            puntoLejano (float): Punto lejano.
        """
        self.distanciaObjetoMax = puntoLejano

    def setDistanciaObjeto(self, distanciaObjeto):
        """
        Establece la distancia del objeto.

        Args:
            distanciaObjeto (float): Distancia del objeto.
        """
        self.distanciaObjeto = distanciaObjeto
    
    def setDistanciaFocal(self, distanciaFocal):
        """
        Establece la distancia focal.

        Args:
            distanciaFocal (float): Distancia focal.
        """
        self.distanciaFocal = distanciaFocal
    
    def dibujarSimulacion(self,ax):
        """
        No se puede aplicar escala logaritmica solo a la mitad del eje x. 
        Probe ajustar y achicar el eje x, en funcion de la distancia del objeto, pero no es del todo conveniente.
        Estoy trabajando con el punto lejano para eso. 
        Creo que deberiamos trabajar con ifs. 
        Si la distancia focal es tanto, entonces el eje va de tanto a tanto. y asi sucesivamente.
        """
        self.ax = ax
        self.ax.clear()  # Limpia el gráfico actual
        self.ax.set_xlim(-self.distanciaObjetoMax*1.05, self.distanciaImagen*2)  # Establece los límites del eje X
        self.ax.set_ylim(-200, 200)  # Establece los límites del eje Y
        #self.ax.set_aspect('equal', adjustable='box')  # Asegura que los ejes tengan la misma escala
        #self.ax.set_xticks([])  # Elimina las marcas del eje X
        #self.ax.set_yticks([])  # Elimina las marcas del eje Y
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

        self.ax.plot(-self.distanciaObjetoMin, 0, marker='X', markersize=6, label='Punto proximo')  # Dibuja el punto proximo
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
        
        ax.legend(fontsize=tamanoLegends)  # Muestra la leyenda
        ax.figure.canvas.draw()  # Actualiza el gráfico
    
    def saludo(self):
        """
        Devuelve un saludo.

        Returns:
            str: El saludo.
        """
        return f"Hola, {self.nombre}!"

