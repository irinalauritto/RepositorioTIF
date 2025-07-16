
class Emetropia():
    """ 
    This class inheritates all attributes and methods from the VicioDeRefraccion Class
    A class used to represent a patology

    """
    def __init__(self, nombre):
        """
        Initializes the class.
        """
        self.puntoCercano = .25 #[m]
        self.puntoLejano = 10.000  #[m]
        self.dioptriasLenteCorrectora = 0
        self.nombre = nombre
        self.diametroOjo = 0.025  # [m]

    def calcularRadioDeDifuminacion(self, distanciaObjeto):  
        """
        Calculates the radius of the blur circle.

        Returns:
            float: radius of the blur circle.
        """
        self.calcularDistanciaFocal(distanciaObjeto)

        if distanciaObjeto > self.puntoLejano:
            return distanciaObjeto/self.puntoLejano
        if self.puntoLejano >= distanciaObjeto and distanciaObjeto >= self.puntoCercano:
            return 0
        if self.puntoCercano > distanciaObjeto:
            return self.puntoCercano/distanciaObjeto

    def calcularDistanciaFocal(self, distanciaObjeto):  
        """
        Calculates the focal distance.
        """
        if self.puntoCercano <= distanciaObjeto and distanciaObjeto <= self.puntoLejano: # Si se encuentra entre el pto lejano y proximo
            self.distanciaFocal = 1/(1/distanciaObjeto+1/self.diametroOjo)     # El ojo ajusta su potencia para ubicar la imagen en la retina (acomodacion)
        if distanciaObjeto < self.puntoCercano:                      # Si el objeto esta dentro del punto proximo
            self.distanciaFocal = 1/(1/self.puntoCercano+1/self.diametroOjo) # La potencia del ojo es la maxima que puede lograr (correspondida a la distancia minima a la que puede ver claramente un objeto)
        if  self.puntoLejano < distanciaObjeto:                     # Si el objeto esta mas alla del punto lejano
            self.distanciaFocal = 1/(1/self.puntoLejano+1/self.diametroOjo) # La potencia del ojo es la minima que puede lograr (correspondida a la distancia maxima a la que puede ver claramente un objeto)

    ### Getters ###
    def getPuntoCercano(self):
        """
        Returns the near point of the eye.
        """
        return self.puntoCercano
    def getPuntoLejano(self):
        """
        Returns the far point of the eye.
        """
        return self.puntoLejano
    def getRadioDeDifuminacion(self):
        """
        Returns the radius of the blur circle.
        """
        return self.radioDeDifuminacion
    def getDioptriasLenteCorrectora(self):
        """
        Returns the dioptrias of the lens.
        """
        return self.dioptriasLenteCorrectora
    def getDistanciaFocal(self):
        """
        Returns the focal distance of the eye.
        """ 
        return self.distanciaFocal

    
        
    