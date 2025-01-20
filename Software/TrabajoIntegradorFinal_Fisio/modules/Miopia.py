import VicioDeRefraccion

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
    
    # Funciones de la clase
   
    def calcularLenteCorrectora(self):
        """
        Calculates the corrective lens.

        """
        pass

    def modificarImagen(self, grado):
        """
        Modifies the image according to the degree of the pathology.

        Args:
            grado(str): degree of the patology.
        """
        pass
        
    