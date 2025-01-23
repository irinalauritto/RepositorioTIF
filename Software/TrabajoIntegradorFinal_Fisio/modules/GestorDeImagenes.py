import tkinter as tk
from PIL import Image, ImageTk
import os

class GestorDeImagenes:
    """Clase para mostrar imágenes en una nueva ventana."""
    def __init__(self, directorio):
        self.directorio = directorio
        self.imagenes = []
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
            img = img.resize((200, 200), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(ventana_imagenes, image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.pack()

        ventana_imagenes.mainloop()