import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import modules.GestorDeArchivos as ga
import modules.GestorDeImagenes as gi

gArchivos = ga.gestorDeArchivos("Gestor de Archivos")
#gImagen = gi.gestorDeImagenes("Gestor de Imagenes")

class AplicacionPrincipal:
    """Clase principal de la aplicación."""
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador del ojo humano")
        self.root.geometry("600x600")
        self.root.configure(bg='lightblue')  # Set background color to light blue

        self.label_directorio = tk.Label(self.root, text="Directorio no seleccionado", anchor="w", highlightbackground="gray", highlightthickness=1, bg='lightblue')
        self.label_directorio.pack(fill="x", padx=10, pady=5)

        self.directorios_preestablecidos = ["\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes", "\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_guardadas"]
        self.directorio_seleccionado = tk.StringVar(self.root)
        self.directorio_seleccionado.set(self.directorios_preestablecidos[0])  # Set default value

        self.menu_directorios = tk.OptionMenu(self.root, self.directorio_seleccionado, *self.directorios_preestablecidos)
        self.menu_directorios.config(bg='lightblue')
        self.menu_directorios.pack(pady=5)

        self.boton_seleccionar = tk.Button(self.root, text="Seleccionar Directorio", command=self.seleccionar_directorio, bg='lightblue')
        self.boton_seleccionar.pack(pady=5)

        self.listbox_archivos = tk.Listbox(self.root, width=60, height=20)
        self.listbox_archivos.pack(padx=10, pady=5)

        self.boton_refrescar = tk.Button(self.root, text="Actualizar", command=self.actualizar_listado, bg='lightblue')
        self.boton_refrescar.pack(pady=5)

        self.boton_mostrar_imagenes = tk.Button(self.root, text="Mostrar Imágenes", command=self.mostrar_imagenes, bg='lightblue')
        self.boton_mostrar_imagenes.pack(pady=5)

        self.boton_mostrar_imagen = tk.Button(self.root, text="Mostrar Imagen Seleccionada", command=self.mostrar_imagen_seleccionada, bg='lightblue')
        self.boton_mostrar_imagen.pack(pady=5)

        self.directorio = None

    def seleccionar_directorio(self):
        self.directorio = self.directorio_seleccionado.get()
        print(self.directorio)
        if self.directorio:
            self.label_directorio.config(text=f"Directorio: {self.directorio}")
            gArchivos.extraeListadoDeArchivos(self.directorio)
            self.actualizar_listado()
        else:
            messagebox.showinfo("Información", "No se seleccionó ningún directorio.")

    def actualizar_listado(self):
        self.listbox_archivos.delete(0, tk.END)
        try:
            for archivo in gArchivos.listado_de_archivos:
                if archivo not in [".", ".."]:
                    self.listbox_archivos.insert(tk.END, archivo)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el directorio: {e}")

    def mostrar_imagenes(self):
        if self.directorio:
            gestor_imagenes = gi.GestorDeImagenes(self.directorio)
            gestor_imagenes.mostrar_imagenes()
        else:
            messagebox.showinfo("Información", "No se ha seleccionado ningún directorio.")

    def mostrar_imagen_seleccionada(self):
        seleccion = self.listbox_archivos.curselection()
        if seleccion:
            archivo_seleccionado = self.listbox_archivos.get(seleccion)
            ruta_imagen = f"{self.directorio}/{archivo_seleccionado}"
            self.mostrar_imagen(ruta_imagen)
        else:
            messagebox.showinfo("Información", "No se ha seleccionado ningún archivo.")

    def mostrar_imagen(self, ruta_imagen):
        ventana_imagen = tk.Toplevel(self.root)
        ventana_imagen.title("Imagen Seleccionada")

        img = Image.open(ruta_imagen)
        img = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(ventana_imagen, image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection
        label.pack()

def ejecutar_gui():
    root = tk.Tk()
    app = AplicacionPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_gui()