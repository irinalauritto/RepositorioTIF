import tkinter as tk
import modules.GestorDeArchivos as ga
import modules.GestorDeImagenes as gi

gArchivos = ga.gestorDeArchivos("Gestor de Archivos")

class AplicacionPrincipal:
    """Clase principal de la aplicación."""
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador del ojo humano")
        self.root.geometry("500x400")

        self.label_directorio = tk.Label(self.root, text="Directorio no seleccionado", anchor="w")
        self.label_directorio.pack(fill="x", padx=10, pady=5)

        self.directorios_preestablecidos = ["C:\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes", "C:\\RepositorioTIF\\Software\\TrabajoIntegradorFinal_Fisio\\imagenes_guardadas"]
        self.directorio_seleccionado = tk.StringVar(self.root)
        self.directorio_seleccionado.set(self.directorios_preestablecidos[0])  # Set default value

        self.menu_directorios = tk.OptionMenu(self.root, self.directorio_seleccionado, *self.directorios_preestablecidos)
        self.menu_directorios.pack(pady=5)

        self.boton_seleccionar = tk.Button(self.root, text="Seleccionar Directorio", command=self.seleccionar_directorio)
        self.boton_seleccionar.pack(pady=5)

        self.listbox_archivos = tk.Listbox(self.root, width=60, height=20)
        self.listbox_archivos.pack(padx=10, pady=5)

        self.listbox_archivos.delete(0, tk.END)

        try:
            for archivo in gArchivos.listado_de_archivos:
                if archivo not in [".", ".."]:
                    self.listbox_archivos.insert(tk.END, archivo)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al leer el directorio: {e}")

        self.boton_refrescar = tk.Button(self.root, text="Actualizar", command=self.actualizar_listado)
        self.boton_refrescar.pack(pady=5)

        self.boton_mostrar_imagenes = tk.Button(self.root, text="Mostrar Imágenes", command=self.mostrar_imagenes)
        self.boton_mostrar_imagenes.pack(pady=5)

        self.directorio = None

    def seleccionar_directorio(self):
        from tkinter import messagebox
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
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al leer el directorio: {e}")

    def mostrar_imagenes(self):
        gestor_imagenes = gi.GestorDeImagenes(self.directorio)
        gestor_imagenes.mostrar_imagenes()

def ejecutar_gui():
    root = tk.Tk()
    app = AplicacionPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_gui()