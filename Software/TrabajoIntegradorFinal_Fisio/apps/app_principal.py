import tkinter as tk
import modules.GestorDeArchivos as ga

class AplicacionPrincipal:
    def __init__(self, root):

        gArchivos = ga.gestorDeArchivos("Gestor de Archivos")

        self.root = root
        self.root.title("Visor de Archivos de Directorio")
        self.root.geometry("500x400")

        self.label_directorio = tk.Label(self.root, text="Directorio no seleccionado", anchor="w")
        self.label_directorio.pack(fill="x", padx=10, pady=5)

        self.boton_abrir = tk.Button(self.root, text="Seleccionar Directorio", command=self.seleccionar_directorio)
        self.boton_abrir.pack(pady=5)

        self.listbox_archivos = tk.Listbox(self.root, width=60, height=20)
        self.listbox_archivos.pack(padx=10, pady=5)

        self.boton_refrescar = tk.Button(self.root, text="Actualizar", command=self.mostrar_archivos)
        self.boton_refrescar.pack(pady=5)

        self.directorio = None

    def seleccionar_directorio(self):
        from tkinter import filedialog, messagebox
        self.directorio = filedialog.askdirectory(title="Seleccionar Directorio")
        if self.directorio:
            self.label_directorio.config(text=f"Directorio: {self.directorio}")
            self.mostrar_archivos()
        else:
            messagebox.showinfo("Información", "No se seleccionó ningún directorio.")

    def mostrar_archivos(self):
        import os
        if not self.directorio:
            from tkinter import messagebox
            messagebox.showwarning("Advertencia", "Primero selecciona un directorio.")
            return

        self.listbox_archivos.delete(0, tk.END)

        try:
            archivos = os.listdir(self.directorio)
            for archivo in archivos:
                if archivo not in [".", ".."]:
                    self.listbox_archivos.insert(tk.END, archivo)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al leer el directorio: {e}")

def ejecutar_gui():
    root = tk.Tk()
    app = AplicacionPrincipal(root)
    root.mainloop()
