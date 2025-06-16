# conversor_archivos.py

# Importamos lo necesario
from abc import ABC, abstractmethod  # Para clases abstractas
import json  # Para manejar archivos JSON
import csv   # Para manejar archivos CSV
import os    # Para trabajar con rutas de archivos
import tkinter as tk  # Para crear la interfaz gráfica
from tkinter import filedialog, messagebox, ttk  # Para cuadros de diálogo y widgets

# Clase abstracta base para representar un archivo genérico
class Archivo(ABC):
    def __init__(self, ruta):
        self.ruta = ruta  # Guarda la ruta del archivo

    @abstractmethod
    def leer(self):
        pass  # Método que las subclases deben implementar

    @abstractmethod
    def convertir_a(self, formato_salida, ruta_destino):
        pass  # Método para convertir el archivo a otro formato

# Clase para archivos CSV
class ArchivoCSV(Archivo):
    def leer(self):
        with open(self.ruta, newline='', encoding='utf-8') as csvfile:
            return list(csv.DictReader(csvfile))  # Lee el archivo CSV como lista de diccionarios

    def convertir_a(self, formato_salida, ruta_destino):
        datos = self.leer()
        if formato_salida == 'json':
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)  # Convierte y guarda como JSON
        else:
            raise ValueError("Formato no soportado desde CSV")

# Clase para archivos JSON
class ArchivoJSON(Archivo):
    def leer(self):
        with open(self.ruta, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)  # Lee el JSON como lista de diccionarios

    def convertir_a(self, formato_salida, ruta_destino):
        datos = self.leer()
        if formato_salida == 'csv':
            with open(ruta_destino, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=datos[0].keys())
                writer.writeheader()  # Escribe los encabezados del CSV
                writer.writerows(datos)  # Escribe los datos
        else:
            raise ValueError("Formato no soportado desde JSON")

# Clase Factory que crea la clase adecuada según la extensión del archivo
class ArchivoFactory:
    @staticmethod
    def crear_archivo(ruta):
        ext = os.path.splitext(ruta)[1].lower()  # Obtiene la extensión del archivo
        if ext == '.csv':
            return ArchivoCSV(ruta)  # Devuelve un objeto CSV
        elif ext == '.json':
            return ArchivoJSON(ruta)  # Devuelve un objeto JSON
        else:
            raise ValueError("Formato de archivo no soportado")

# Interfaz gráfica con Tkinter
class ConversorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Archivos")  # Título de la ventana

        # Variables para guardar los datos del usuario
        self.ruta_entrada = tk.StringVar()
        self.ruta_salida = tk.StringVar()
        self.formato_salida = tk.StringVar(value="json")  # Valor por defecto

        self.crear_widgets()  # Crea los elementos visuales

    def crear_widgets(self):
        # Fila para seleccionar el archivo de entrada
        tk.Label(self.root, text="Archivo de entrada:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.ruta_entrada, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="Buscar", command=self.seleccionar_entrada).grid(row=0, column=2)

        # Fila para seleccionar el formato de salida
        tk.Label(self.root, text="Formato de salida:").grid(row=1, column=0, sticky="e")
        ttk.Combobox(self.root, textvariable=self.formato_salida, values=["json", "csv"]).grid(row=1, column=1)

        # Fila para seleccionar el archivo de salida
        tk.Label(self.root, text="Archivo de salida:").grid(row=2, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.ruta_salida, width=40).grid(row=2, column=1)
        tk.Button(self.root, text="Guardar como", command=self.seleccionar_salida).grid(row=2, column=2)

        # Botón para convertir el archivo
        tk.Button(self.root, text="Convertir", command=self.convertir).grid(row=3, column=1, pady=10)

    def seleccionar_entrada(self):
        # Abre un explorador para elegir el archivo original
        ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV/JSON", "*.csv *.json")])
        if ruta:
            self.ruta_entrada.set(ruta)

    def seleccionar_salida(self):
        # Abre un explorador para elegir dónde guardar el archivo convertido
        ext = self.formato_salida.get()
        ruta = filedialog.asksaveasfilename(defaultextension=f".{ext}", filetypes=[(f"Archivo {ext.upper()}", f"*.{ext}")])
        if ruta:
            self.ruta_salida.set(ruta)

    def convertir(self):
        try:
            archivo = ArchivoFactory.crear_archivo(self.ruta_entrada.get())  # Crea el tipo de archivo correcto
            archivo.convertir_a(self.formato_salida.get(), self.ruta_salida.get())  # Convierte
            messagebox.showinfo("Éxito", "Conversión exitosa.")
        except Exception as e:
            messagebox.showerror("Error", str(e))  # Muestra cualquier error

# Punto de entrada principal
if __name__ == '__main__':
    root = tk.Tk()  # Crea la ventana
    app = ConversorApp(root)  # Instancia la app
    root.mainloop()  # Inicia el loop principal de Tkinter
