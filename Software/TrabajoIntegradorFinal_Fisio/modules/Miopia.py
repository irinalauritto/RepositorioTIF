from modules.VicioDeRefraccion import VicioDeRefraccion

class Miopia(VicioDeRefraccion):
    """ 
    This class inheritates all attributes and methods from the VicioDeRefaccion Class
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
        self.radioDifuminacion = self.calcularRadioDeDifuminacion()
        self.DistanciaFocal = self.calcularDistanciaFocal()
    
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
        self.radioDifuminacion = self.calcularRadioDeDifuminacion()
        self.distanciaFocal = self.calcularDistanciaFocal()  

    def getDistanciaFocal(self):    
        """
        Returns the focal distance of the eye.
        """ 
        return self.distanciaFocal
    
    def getDioptriasLenteCorrectora(self):
        return super().getDioptriasLenteCorrectora()
    
    def definirLenteCorrectora(self): #Definimos 1,3, y 6 a los grados leve, moderado y severos, rspectivamente.
        if self.grado == 1:
            self.dioptriasLenteCorrectora = 1.00
        elif self.grado == 3:
            self.dioptriasLenteCorrectora = 3.00
        elif self.grado == 6:
            self.dioptriasLenteCorrectora = 6.00
            
    def calcularPuntoCercano(self): ##Las dioptrias del lente para miopia son negativas, por lo que queda sumando en la formula.
        """
        Calculates the near point.

        Returns:
            float: near point.
        """
        return round(1/((1/0.25)+self.dioptriasLenteCorrectora), 2)
    
    def calcularPuntoLejano(self): ##Las dioptrias del lente para miopia son negativas, por lo que queda sumando en la formula.
        
        return round(1/((1/10)+self.dioptriasLenteCorrectora), 2)
    
    def calcularRadioDeDifuminacion(self):  
        """
        Calculates the radius of the blur circle.

        Returns:
            float: radius of the blur circle.
        """
        if self.grado == 1:
            return 1
        elif self.grado == 3:
            return 3
        elif self.grado == 6:
            return 6
        
    def calcularDistanciaFocal(self):  
        """
        Calculates the focal distance.

        Returns:
            float: focal distance.
        """
        return 1/self.dioptriasLenteCorrectora

