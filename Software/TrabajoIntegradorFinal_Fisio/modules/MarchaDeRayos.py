import numpy as np
import flet as ft
import matplotlib.pyplot as plt
import tempfile
import os

class MarchaDeRayos:
    """Clase para simular la marcha de rayos en un sistema óptico."""
    def __init__(self, nombre, dioptriasLente, distanciaEspacio, distanciaFocal, distanciaRetina, alturaObjeto, anguloInicial):
        self.nombre = nombre
        self.dioptriasLente = dioptriasLente
        self.distanciaEspacio = distanciaEspacio #mm
        self.distanciaFocal = distanciaFocal #mm
        self.distanciaRetina = distanciaRetina #mm
        self.alturaObjeto = alturaObjeto #mm
        self.anguloInicial = anguloInicial #rad (inicializar en 0)
        self.imagen = None  # Inicializar la imagen como None
    
    def espacioLibre(self, d):
        return np.array([[1, d], [0, 1]])

    def lenteDelgada(self, f):
        return np.array([[1, 0], [-1 / f, 1]])
    
    def sistemaOptico(self):
        M_espacio = self.espacioLibre(self.distanciaEspacio)
        M_lente = self.lenteDelgada(self.distanciaFocal)
        M_retina = self.espacioLibre(self.distanciaRetina)
        return M_retina @ M_lente @ M_espacio

    def propagarRayo(self, yInicial, thetaInicial, M_total):
        rayoInicial = np.array([yInicial, thetaInicial])
        rayoFinal = M_total @ rayoInicial
        return rayoInicial, rayoFinal
    
    def generarGrafico(self ):
        M_total = self.sistemaOptico()
        
        # Solo dos rayos: el perpendicular y el que pasa por el foco
        y_vals = [0, self.distanciaFocal]
        rayos = [self.propagarRayo(y, self.anguloInicial, M_total) for y in y_vals]

        # Crear gráfico
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axhline(0, color="black", linewidth=0.8)  # Eje óptico
        ax.axvline(self.distanciaEspacio, color="blue", linewidth=1.5, label="Lente")  # Lente
        ax.axvline(self.distanciaEspacio + self.distanciaRetina, color="red", linewidth=1.5, label="Retina")  # Retina

        # Dibujar rayos
        for rayoInicial, rayoFinal in rayos:
            y1, theta1 = rayoInicial
            y2, _ = rayoFinal

            # Primera sección (espacio libre)
            x1, x2 = 0, self.distanciaEspacio
            ax.plot([x1, x2], [y1, y1 + theta1 * self.distanciaEspacio], color="green")

            # Segunda sección (a través de la lente)
            y_lente = y1 + theta1 * self.distanciaEspacio
            theta_lente = theta1 - y_lente / self.distanciaFocal
            x3, x4 = self.distanciaEspacio, self.distanciaEspacio + self.distanciaRetina
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

       
    def mostrarImagen(self, tempImage):
         self.imagen = ft.Image(
            src=f"/{tempImage}",
            width=600,
            height=300
        )
         
   # def actualizarImagen():
    #    temp_image = generarGrafico()
     #   img.src = f"/{temp_image}"
      
      #  img.update()
    
    def saludo(self):
        """
        Devuelve un saludo.

        Returns:
            str: El saludo.
        """
        return f"Hola, {self.nombre}!"

