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
        self.definirLenteCorrectora()
        self.calcularPuntoCercano()
        self.calcularPuntoLejano()
        self.diametroOjo = 0.025  # [m]
    
    # Funciones de la clase
    def setGrado(self, grado):
        """
        Sets the degree of the pathology y define lente correctora, punto cercano y lejano correspondientes.

        Args:
            grado(str): degree of the patology.
        """
        self.grado = grado
        self.definirLenteCorrectora()
        self.calcularPuntoCercano()
        self.calcularPuntoLejano()
    
    def definirLenteCorrectora(self): # Definimos 1,3, y 6 a los grados leve, moderado y severos, respectivamente.
        if self.grado == 1:
            self.dioptriasLenteCorrectora = 1.00
        elif self.grado == 3:
            self.dioptriasLenteCorrectora = 3.00
        elif self.grado == 6:
            self.dioptriasLenteCorrectora = 6.00
            
    def calcularPuntoCercano(self): ##Las dioptrias del lente para miopia son negativas, por lo que queda sumando en la formula.
        """
        Calculates the near point.
        """
        self.puntoCercano = round(1/((1/0.25)+self.dioptriasLenteCorrectora), 2) # [m]
    
    def calcularPuntoLejano(self): # Las dioptrias del lente para miopia son negativas, por lo que queda sumando en la formula.
        self.puntoLejano = round(1/((1/10)+self.dioptriasLenteCorrectora), 2) # [m]
    
    def calcularRadioDeDifuminacion(self, distanciaObjeto):  
        """
        Calculates the radius of the blur circle.
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
    def getDioptriasLenteCorrectora(self):
        """
        Returns the corrective lens of the eye.
        
        Returns:
            float: corrective lens.
        """
        return -self.dioptriasLenteCorrectora
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
