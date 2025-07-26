import os
import sys

class gestorDeArchivos:
    """Clase para obtener listado de archivos desde el directorio."""
    def __init__(self, nombre):
        self.listado_de_archivos = []
        self.nombre = nombre
        self.directorio = None

    def resource_path(self, relative_path):
        """Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def extraeListadoDeArchivos(self, p_directorio):
        """Obtiene el listado de archivos en el directorio especificado."""
        aux_listado_de_archivos = []
        # Usa resource_path para obtener la ruta absoluta
        abs_directorio = self.resource_path(p_directorio)
        self.directorio = abs_directorio

        if os.path.isdir(abs_directorio):
            for entry in os.listdir(abs_directorio):
                if entry not in [".", ".."]:
                    aux_listado_de_archivos.append(entry)
            self.listado_de_archivos = aux_listado_de_archivos
        else:
            self.listado_de_archivos = []
            print(f"El directorio {abs_directorio} no existe o no es un directorio válido.")

    def getListadoDeArchivos(self):
        """Devuelve el listado de archivos."""
        return self.listado_de_archivos