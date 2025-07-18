import os

class gestorDeArchivos:
    """Clase para obtener listado de archivos desde el directorio."""
    def __init__(self, nombre):
        self.listado_de_archivos = []
        self.nombre = nombre
        self.directorio = None

    def extraeListadoDeArchivos(self, p_directorio):
        """Obtiene el listado de archivos en el directorio especificado."""
        aux_listado_de_archivos = []
        self.directorio = p_directorio
        
        #print("Ruta absoluta:", os.path.abspath(p_directorio)) # Para depuración, mostrar la ruta absoluta del directorio

        if os.path.isdir(p_directorio):
            # Listar todos los elementos del directorio
            for entry in os.listdir(p_directorio):
                # Ignorar "." y ".."
                if entry not in [".", ".."]:
                    aux_listado_de_archivos.append(entry)
            
            self.listado_de_archivos = aux_listado_de_archivos
        else:
            # Si el directorio no existe, limpiar la lista
            self.listado_de_archivos = []
            print(f"El directorio {p_directorio} no existe o no es un directorio válido.")

    def getListadoDeArchivos(self):
        """Devuelve el listado de archivos."""
        return self.listado_de_archivos