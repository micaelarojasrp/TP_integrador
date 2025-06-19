# conversor_archivos.py

# Importamos las librerías necesarias para manejar distintos formatos y la GUI
from abc import ABC, abstractmethod
import json
import csv
import os
import yaml
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Clase abstracta base que representa un archivo
class Archivo(ABC):
    def __init__(self, ruta):
        self.ruta = ruta  # Ruta del archivo original

    @abstractmethod
    def leer(self):
        # Método abstracto para leer un archivo
        pass

    @abstractmethod
    def convertir_a(self, formato_salida, ruta_destino):
        # Método abstracto para convertir el archivo a otro formato
        pass

# Clase para archivos CSV
class ArchivoCSV(Archivo):
    def leer(self):
        # Abrimos el CSV y lo leemos como lista de diccionarios
        with open(self.ruta, newline='', encoding='utf-8') as csvfile:
            return list(csv.DictReader(csvfile))

    def convertir_a(self, formato_salida, ruta_destino):
        datos = self.leer()
        if formato_salida == 'json':
            # Convertimos a JSON
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
        elif formato_salida == 'yaml':
            # Convertimos a YAML
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                yaml.dump(datos, f)
        elif formato_salida == 'xml':
            # Convertimos a XML creando elementos
            root = ET.Element("root")
            for fila in datos:
                item = ET.SubElement(root, "item")
                for clave, valor in fila.items():
                    ET.SubElement(item, clave).text = str(valor)
            tree = ET.ElementTree(root)
            tree.write(ruta_destino, encoding='utf-8', xml_declaration=True)
        else:
            raise ValueError("Formato no soportado desde CSV")

# Clase para archivos JSON
class ArchivoJSON(Archivo):
    def leer(self):
        # Leemos el JSON y devolvemos la estructura como lista de diccionarios
        with open(self.ruta, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)

    def convertir_a(self, formato_salida, ruta_destino):
        datos = self.leer()
        if formato_salida == 'csv':
            # Convertimos a CSV
            with open(ruta_destino, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=datos[0].keys())
                writer.writeheader()
                writer.writerows(datos)
        elif formato_salida == 'yaml':
            # Convertimos a YAML
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                yaml.dump(datos, f)
        elif formato_salida == 'xml':
            # Convertimos a XML
            root = ET.Element("root")
            for fila in datos:
                item = ET.SubElement(root, "item")
                for clave, valor in fila.items():
                    ET.SubElement(item, clave).text = str(valor)
            tree = ET.ElementTree(root)
            tree.write(ruta_destino, encoding='utf-8', xml_declaration=True)
        else:
            raise ValueError("Formato no soportado desde JSON")

# Clase para archivos YAML
class ArchivoYAML(Archivo):
    def leer(self):
        # Leemos el YAML como lista de diccionarios
        with open(self.ruta, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def convertir_a(self, formato_salida, ruta_destino):
        datos = self.leer()
        if formato_salida == 'json':
            # Convertimos a JSON
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
        elif formato_salida == 'csv':
            # Convertimos a CSV
            with open(ruta_destino, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=datos[0].keys())
                writer.writeheader()
                writer.writerows(datos)
        elif formato_salida == 'xml':
            # Convertimos a XML
            root = ET.Element("root")
            for fila in datos:
                item = ET.SubElement(root, "item")
                for clave, valor in fila.items():
                    ET.SubElement(item, clave).text = str(valor)
            tree = ET.ElementTree(root)
            tree.write(ruta_destino, encoding='utf-8', xml_declaration=True)
        else:
            raise ValueError("Formato no soportado desde YAML")

# Clase para archivos XML
class ArchivoXML(Archivo):
    def leer(self):
        # Leemos el XML y convertimos cada <item> en un diccionario
        tree = ET.parse(self.ruta)
        root = tree.getroot()
        datos = []
        for item in root.findall("item"):
            fila = {child.tag: child.text for child in item}
            datos.append(fila)
        return datos

    def convertir_a(self, formato_salida, ruta_destino):
        datos = self.leer()
        if formato_salida == 'json':
            # Convertimos a JSON
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
        elif formato_salida == 'csv':
            # Convertimos a CSV
            with open(ruta_destino, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=datos[0].keys())
                writer.writeheader()
                writer.writerows(datos)
        elif formato_salida == 'yaml':
            # Convertimos a YAML
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                yaml.dump(datos, f)
        else:
            raise ValueError("Formato no soportado desde XML")

# Fábrica que devuelve la clase correspondiente según el tipo de archivo
class ArchivoFactory:
    @staticmethod
    def crear_archivo(ruta):
        ext = os.path.splitext(ruta)[1].lower()
        if ext == '.csv':
            return ArchivoCSV(ruta)
        elif ext == '.json':
            return ArchivoJSON(ruta)
        elif ext == '.yaml' or ext == '.yml':
            return ArchivoYAML(ruta)
        elif ext == '.xml':
            return ArchivoXML(ruta)
        else:
            raise ValueError("Formato de archivo no soportado")

# Clase que representa la aplicación con interfaz gráfica
class ConversorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Archivos Avanzado")

        # Variables para guardar rutas y formato seleccionado
        self.ruta_entrada = tk.StringVar()
        self.ruta_salida = tk.StringVar()
        self.formato_salida = tk.StringVar(value="json")

        self.crear_widgets()

    def crear_widgets(self):
        # Etiquetas, campos y botones para la interfaz
        tk.Label(self.root, text="Archivo de entrada:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.ruta_entrada, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="Buscar", command=self.seleccionar_entrada).grid(row=0, column=2)

        tk.Label(self.root, text="Formato de salida:").grid(row=1, column=0, sticky="e")
        formatos = ["json", "csv", "yaml", "xml"]
        ttk.Combobox(self.root, textvariable=self.formato_salida, values=formatos).grid(row=1, column=1)

        tk.Label(self.root, text="Archivo de salida:").grid(row=2, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.ruta_salida, width=40).grid(row=2, column=1)
        tk.Button(self.root, text="Guardar como", command=self.seleccionar_salida).grid(row=2, column=2)

        tk.Button(self.root, text="Convertir", command=self.convertir).grid(row=3, column=1, pady=10)

    def seleccionar_entrada(self):
        # Abrimos un diálogo para seleccionar archivo
        ruta = filedialog.askopenfilename(filetypes=[("Archivos", "*.csv *.json *.yaml *.yml *.xml")])
        if ruta:
            self.ruta_entrada.set(ruta)

    def seleccionar_salida(self):
        # Elegimos dónde guardar el archivo convertido
        ext = self.formato_salida.get()
        ruta = filedialog.asksaveasfilename(defaultextension=f".{ext}", filetypes=[(f"Archivo {ext.upper()}", f"*.{ext}")])
        if ruta:
            self.ruta_salida.set(ruta)

    def convertir(self):
        try:
            # Usamos la fábrica para crear el tipo correcto de archivo
            archivo = ArchivoFactory.crear_archivo(self.ruta_entrada.get())
            archivo.convertir_a(self.formato_salida.get(), self.ruta_salida.get())
            messagebox.showinfo("Éxito", "Conversión exitosa.")
        except Exception as e:
            # Mostramos errores si ocurren
            messagebox.showerror("Error", str(e))

# Punto de entrada del programa
if __name__ == '__main__':
    root = tk.Tk()
    app = ConversorApp(root)
    root.mainloop()
