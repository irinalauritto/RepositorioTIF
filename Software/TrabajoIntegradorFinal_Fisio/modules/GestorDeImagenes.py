import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np

class gestorDeImagenes:
    """Clase para mostrar imágenes en una nueva ventana."""
    def __init__(self, directorio):
        self.directorio = directorio
        self.imagenes = []
        self.image_array = []
        self.cargar_imagenes()

    def cargar_imagenes(self):
        """Carga las imágenes del directorio especificado."""
        for archivo in os.listdir(self.directorio):
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.imagenes.append(os.path.join(self.directorio, archivo))

    def mostrar_imagenes(self):
        """Muestra las imágenes en una nueva ventana."""
        if not self.imagenes:
            return

        ventana_imagenes = tk.Toplevel()
        ventana_imagenes.title("Imágenes del Directorio")

        for img_path in self.imagenes:
            img = Image.open(img_path)
            img = img.resize((500, 500))
            img_array = np.array(img)  # Convertir la imagen a una matriz de píxeles
            self.image_array.append(img_array)
            img_tk = ImageTk.PhotoImage(Image.fromarray(img_array))

            label = tk.Label(ventana_imagenes, image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.pack()

        ventana_imagenes.mainloop()