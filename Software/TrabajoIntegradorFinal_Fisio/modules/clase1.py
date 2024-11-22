class Procesador:
    """Clase para procesar datos en la aplicación."""
    def __init__(self, dato_inicial=""):
        self.dato = dato_inicial

    def procesar_dato(self):
        """Ejemplo de procesamiento: transforma el dato en mayúsculas."""
        return self.dato.upper()