# 🛠️ Documentación de `conversor_archivos.py`

## 📋 Descripción General

`conversor_archivos.py` es una aplicación de escritorio con interfaz gráfica desarrollada en Python que permite convertir archivos entre los formatos **CSV, JSON, YAML y XML**. Utiliza el patrón de diseño **Factory** para crear objetos según el tipo de archivo, y está diseñada con principios de programación orientada a objetos y uso de clases abstractas.

La interfaz gráfica está construida con **Tkinter**.

---

## 🔧 Tecnologías y Librerías Usadas

- `tkinter`: para la interfaz gráfica.
- `csv`, `json`, `yaml`, `xml.etree.ElementTree`: para el manejo de distintos formatos de archivo.
- `abc`: para definir una clase base abstracta.
- `os`: para trabajar con rutas de archivos.

---

## 🧱 Arquitectura del Código

### 1. 📁 Clase Abstracta `Archivo`

Define la interfaz común para todos los tipos de archivo. Contiene dos métodos abstractos:

- `leer()`: lectura del contenido como lista de diccionarios.
- `convertir_a(formato_salida, ruta_destino)`: convierte el archivo al formato solicitado y lo guarda.

### 2. 📂 Subclases de Formato

Cada una implementa `leer()` y `convertir_a()` de acuerdo a su formato.

- **`ArchivoCSV`**: lectura y conversión desde archivos CSV.
- **`ArchivoJSON`**: maneja archivos `.json`.
- **`ArchivoYAML`**: para archivos `.yaml` o `.yml`.
- **`ArchivoXML`**: extrae datos de archivos `.xml` estructurados como `<item>`s.

### 3. 🏭 `ArchivoFactory`

Clase encargada de identificar el tipo de archivo según su extensión y retornar la clase correspondiente:

```python
ArchivoFactory.crear_archivo("ruta/al/archivo.csv")
```

Devuelve un objeto `ArchivoCSV`, `ArchivoJSON`, etc., según el caso.

### 4. 🖼️ `ConversorApp` (Interfaz gráfica)

Clase que crea la ventana principal de la aplicación. Sus funciones clave:

- `crear_widgets()`: construye la UI (campos de entrada, botones, combo de formatos).
- `seleccionar_entrada()`: abre un diálogo para elegir el archivo de entrada.
- `seleccionar_salida()`: diálogo para elegir el archivo de salida.
- `convertir()`: ejecuta la conversión usando `ArchivoFactory` y muestra mensajes de éxito o error.

---

## 🎛️ Flujo de la Aplicación

1. El usuario selecciona un archivo (CSV, JSON, YAML, XML).
2. Elige un formato de salida desde una lista desplegable.
3. Selecciona dónde guardar el archivo convertido.
4. La conversión se ejecuta y se informa el resultado.

---

## 📁 Ejemplo de Uso

1. Ejecutar el archivo:

```bash
python conversor_archivos.py
```

2. Se abrirá una ventana:

- Elegí un archivo (ej. `data.csv`)
- Seleccioná el formato de salida (`JSON`, `XML`, etc.)
- Elegí una ruta para guardarlo (`data_convertido.json`)
- Clic en **Convertir**

---

## ⚠️ Validaciones y Errores

- Si el formato de salida no es compatible, lanza un `ValueError`.
- El botón **Convertir** está protegido con un `try/except` que muestra mensajes amigables en caso de error.

---

## ✅ Requisitos

- Python 3.7+
- Módulo externo requerido:
  ```bash
  pip install pyyaml
  ```

---

## 💡 Mejora Sugerida (opcional)

- Agregar validación de estructura (ej. que todos los items tengan las mismas claves).
- Permitir importar múltiples archivos en lote.
- Añadir soporte para otros formatos (TOML, XLSX, etc).
