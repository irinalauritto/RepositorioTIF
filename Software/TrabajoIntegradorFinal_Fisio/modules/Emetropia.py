
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
        self.distanciaFocal = .025 #[m]
        self.dioptriasLenteCorrectora = 0
        self.radioDeDifuminacion = 0
        self.nombre = nombre
    
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

    
        
    