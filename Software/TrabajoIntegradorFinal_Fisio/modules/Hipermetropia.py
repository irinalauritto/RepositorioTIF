from modules.VicioDeRefraccion import VicioDeRefraccion

class Hipermetropia(VicioDeRefraccion):
    """ 
    This class inheritates all attributes and methods from the VicioDeRefraccion Class
    A class used to represent a patology

    """
    def __init__(self, nombre, grado):
        """
        Initializes the class.

        Args:
            grado(str): degree of the patology.
        """
        super().__init__(nombre, grado)
        self.lenteCorrectora = self.definirLenteCorrectora()
        self.puntoCercano = self.calcularPuntoCercano()
        self.puntoLejano = self.calcularPuntoLejano()
        self.diametroOjo = 0.025  # [m]

    # Funciones de la clase
    def setGrado(self, grado):
        """
        Sets the degree of the pathology.

        Args:
            grado(str): degree of the patology.
        """
        self.grado = grado
        self.lenteCorrectora = self.definirLenteCorrectora()
        self.puntoCercano = self.calcularPuntoCercano()
        self.puntoLejano = self.calcularPuntoLejano()    

    def definirLenteCorrectora(self): #Definimos 1,3, y 6 a los grados leve, moderado y severos, rspectivamente. 
        if self.grado == 1:
            self.dioptriasLenteCorrectora = 1.00
        elif self.grado == 3:
            self.dioptriasLenteCorrectora = 3.00
        elif self.grado == 6:
            self.dioptriasLenteCorrectora = 3.50

    def calcularPuntoCercano(self): ##Las dioptrias del lente para hipermetropia son positivas.
        """
        Calculates the near point.

        Returns:
            float: near point.
        """
        return round((((44)-self.dioptriasLenteCorrectora)-(1/0.025))**-1, 2)
    
    def calcularPuntoLejano(self): ##Las dioptrias del lente para hipermetropia son positivas.
   
        if self.grado == 1:
            return 10
        elif self.grado == 3:
            return 20
        elif self.grado == 6:
            return 30  #preguntar si esta bien el punto lejano, ya que no se puede ver de lejos.
    
    
    def calcularRadioDeDifuminacion(self, distanciaObjeto):  
        """
        Calculates the radius of the blur circle.

        Returns:
            float: radius of the blur circle.
        """
        self.DistanciaFocal = self.calcularDistanciaFocal(distanciaObjeto)

        distanciaImagen = 1 / (1 / self.DistanciaFocal - 1 / distanciaObjeto)  # Calcula la distancia de la imagen
        
        if distanciaImagen < self.diametroOjo:  # Si la imagen se forma dentro del ojo
            return self.diametroOjo / distanciaImagen
        if distanciaImagen > self.diametroOjo:  # Si la imagen se forma fuera del ojo
            return distanciaImagen / self.diametroOjo
        if distanciaImagen == self.diametroOjo:  # Si la imagen se forma en la retina
            return 0

    def calcularDistanciaFocal(self, distanciaObjeto):  
        """
        Calculates the focal distance.

        Returns:
            float: focal distance.
        """
        if self.puntoCercano <= distanciaObjeto and distanciaObjeto <= self.puntoLejano: # Si se encuentra entre el pto lejano y proximo
            self.distanciaFocal = 1/(1/distanciaObjeto+1/self.diametroOjo)     # El ojo ajusta su potencia para ubicar la imagen en la retina (acomodacion)
        if distanciaObjeto < self.puntoCercano:                      # Si el objeto esta dentro del punto proximo
            self.distanciaFocal = 1/(1/self.puntoCercano+1/self.diametroOjo) # La potencia del ojo es la maxima que puede lograr (correspondida a la distancia minima a la que puede ver claramente un objeto)
        if  self.puntoLejano < distanciaObjeto:                     # Si el objeto esta mas alla del punto lejano
            self.distanciaFocal = 1/(1/self.puntoLejano+1/self.diametroOjo) # La potencia del ojo es la minima que puede lograr (correspondida a la distancia maxima a la que puede ver claramente un objeto)
        
        return self.distanciaFocal
        
    ### Getters ###
    def getPuntoCercano(self):
        """
        Returns the near point of the eye.
        
        Returns:
            float: near point.
        """
        return self.puntoCercano
    def getPuntoLejano(self):
        """
        Returns the far point of the eye.
        
        Returns:
            float: far point.
        """
        return self.puntoLejano
    def getLenteCorrectora(self):
        """
        Returns the corrective lens of the eye.
        
        Returns:
            float: corrective lens.
        """
        return self.lenteCorrectora
    def getRadioDifuminacion(self):
        """
        Returns the radius of the blur circle.

        Returns:
            float: radius of the blur circle.
        """
        return self.radioDifuminacion
    
    def getDistanciaFocal(self):    
        """
        Returns the focal distance of the eye.
        """ 
        return self.distanciaFocal
    
    #def getDioptriasLenteCorrectora(self):
    #    return super().getDioptriasLenteCorrectora() # Aca no sería return self.dioptriasLenteCorrectora ???

    