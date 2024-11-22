import tkinter as tk
from tkinter import messagebox
from modules.clase1 import Procesador

def ejecutar_gui():
    """Lanza una aplicación GUI simple."""
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Simulación del Ojo Humano")
    ventana.geometry("400x200")  # Tamaño de la ventana (ancho x alto)

    # Crear instancia de la clase Procesador
    procesador = Procesador()

    # Función para manejar el evento de botón
    def procesar_texto():
        texto_entrada = entrada.get()  # Obtiene el texto de la entrada
        procesador.dato = texto_entrada
        resultado = procesador.procesar_dato()  # Procesa el dato
        salida.config(text=f"Resultado: {resultado}")  # Muestra el resultado
        messagebox.showinfo("Procesado", "El dato fue procesado con éxito.")

    # Etiqueta de descripción
    etiqueta = tk.Label(ventana, text="Ingresa un texto para procesar:")
    etiqueta.pack(pady=10)  # Margen vertical

    # Entrada de texto
    entrada = tk.Entry(ventana, width=30)
    entrada.pack(pady=5)

    # Botón para procesar
    boton_procesar = tk.Button(ventana, text="Procesar", command=procesar_texto)
    boton_procesar.pack(pady=10)

    # Etiqueta para mostrar el resultado
    salida = tk.Label(ventana, text="Resultado: ")
    salida.pack(pady=10)

    # Inicia el bucle de la aplicación
    ventana.mainloop()

if __name__ == "__main__":
    ejecutar_gui()
