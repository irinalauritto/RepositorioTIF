class VicioDeRefraccion:
    """
    Clase que representa un vicio de refracción.

    """

    def __init__(self, nombre, grado = 0):
        """
        Inicializa la clase.

        Args:
            grado(str): grado de la patología .
        """
        self.nombre = nombre
        self.grado = grado
        self.dioptriasLenteCorrectora = 0

    # GETTERS AND SETTERS
    def setGrado(self, grado):
        self.grado = grado

    def getGrado(self):
        return self.grado
    
    def getDioptriasLenteCorrectora(self):
        return self.dioptriasLenteCorrectora
    
    def calcularLenteCorrectora():
        """
        Calcula la lente correctora.

        """
        pass
    
    def modificarImagen(grado):
        """
        Modifica la imagen según el grado de la patología.

        Args:
            grado(str): grado de la patología.
        """
        pass
