"""
Trabajo Integrador Final de Fisiología
==============================================

General Description
-------------------
En este proyecto se encuentra el main del TIF de fisiología sobre simulación del ojo humano. 


Changelog
---------
+------------+---------------------------------------------+
| Date       | Description                                 |
+============+=============================================+
| 22/11/2024 | Creación del documento                      |
+------------+---------------------------------------------+

Authors
-------
- Josefina Giorgi (josefina.giorgi@ingenieria.uner.edu.ar)
- Irina Lauritto (irina.lauritto@ingenieria.uner.edu.ar)
- Joaquín Machado (joaquin.machado@ingenieria.uner.edu.ar)
"""
from apps.app_principal import ejecutar_gui

def main():
    """Punto de entrada principal."""
    print("Iniciando la aplicación GUI...")
    ejecutar_gui()

if __name__ == "__main__":
    main()
