"""
Este es un módulo de prueba para Doxygen.

Contiene una clase y una función de ejemplo.
"""

class Prueba:
    """
    Clase de ejemplo.

    Attributes:
        nombre (str): Un nombre.
    """

    def __init__(self, nombre):
        """
        Inicializa la clase.

        Args:
            nombre (str): Un nombre para la clase.
        """
        self.nombre = nombre

    def saludo(self):
        """
        Devuelve un saludo.

        Returns:
            str: El saludo.
        """
        return f"Hola, {self.nombre}!"
