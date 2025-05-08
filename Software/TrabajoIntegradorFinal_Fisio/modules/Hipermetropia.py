import VicioDeRefraccion

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
    
    # Funciones de la clase
   
    def definirLenteCorrectora(self): #Definimos 1,3, y 6 a los grados leve, moderado y severos, rspectivamente.
       
        if self.grado == 1:
            self.dioptriasLenteCorrectora = 1.00
        elif self.grado == 3:
            self.dioptriasLenteCorrectora = 3.00
        elif self.grado == 6:
            self.dioptriasLenteCorrectora = 6.00
    
    def calcularPuntoCercano(self): ##Las dioptrias del lente para hipermetropia son positivas.
        """
        Calculates the near point.

        Returns:
            float: near point.
        """
        return 1/((1/0.25)-self.dioptriasLenteCorrectora) #falta el 1/diámetro del ojo
    
    def calcularPuntoLejano(self): ##Las dioptrias del lente para hipermetropia son positivas.
   
        return 1/((1/10)-self.dioptriasLenteCorrectora) #chequear
   
    def modificarImagen(self, grado):
        """
        Modifies the image according to the degree of the pathology.

        Args:
            grado(str): degree of the patology.
        """
        pass
        
    