"""
Proyecto Final Integrador - Oximetría de Pulso
==============================================

General Description
-------------------
En este proyecto se encuentra una parte del proyecto final presentado en la cátedra de Electrónica Programable por las alumnas Josefina Giorgi e Irina Lauritto.
Este código adquiere datos de la oximetría de pulso y envía parámetros como la frecuencia cardíaca y la saturación de oxígeno en sangre, a través de BLE para su visualización en una aplicación móvil.

Hardware Connection
-------------------
+-----------------+---------------+
| ODP Módulo      | EDU-ESP       |
+=================+===============+
| SCL             | SCL           |
+-----------------+---------------+
| SDA             | SDA           |
+-----------------+---------------+
| GND             | GND           |
+-----------------+---------------+
| +3V             | +3V           |
+-----------------+---------------+
| EN              | +3V           |
+-----------------+---------------+
| INT             | GPIO_1        |
+-----------------+---------------+

Changelog
---------
+------------+---------------------------------------------+
| Date       | Description                                 |
+============+=============================================+
| 11/11/2024 | Entrega del proyecto Final Integrador.      |
+------------+---------------------------------------------+

Authors
-------
- Josefina Giorgi (josefina.giorgi@ingenieria.uner.edu.ar)
- Irina Lauritto (irina.lauritto@ingenieria.uner.edu.ar)
"""
from apps.app_principal import ejecutar_gui

def main():
    """Punto de entrada principal."""
    print("Iniciando la aplicación GUI...")
    ejecutar_gui()

if __name__ == "__main__":
    main()
