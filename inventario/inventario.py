"""
inventario.py – Semana 12
Funciones de persistencia con archivos TXT, JSON y CSV.
Proyecto: ClínicaSalud
"""

import json
import csv
import os

# Rutas de los archivos de datos
BASE_DIR  = os.path.dirname(__file__)
DATA_DIR  = os.path.join(BASE_DIR, "data")

RUTA_TXT  = os.path.join(DATA_DIR, "datos.txt")
RUTA_JSON = os.path.join(DATA_DIR, "datos.json")
RUTA_CSV  = os.path.join(DATA_DIR, "datos.csv")

# Encabezados del CSV
CABECERAS_CSV = ["nombre", "precio", "cantidad", "categoria", "descripcion"]


# ──────────────────────────────────────────────────────────────────────────────
# PERSISTENCIA TXT  (usando open() en modo escritura y lectura)
# ──────────────────────────────────────────────────────────────────────────────

def guardar_txt(datos: dict) -> None:
    """
    Guarda un registro de medicamento al final del archivo TXT.
    Usa open() en modo 'a' (append) para no sobreescribir registros anteriores.
    """
    linea = (
        f"Nombre: {datos['nombre']} | "
        f"Precio: ${datos['precio']} | "
        f"Cantidad: {datos['cantidad']} | "
        f"Categoría: {datos['categoria']} | "
        f"Descripción: {datos['descripcion']}\n"
    )
    with open(RUTA_TXT, "a", encoding="utf-8") as archivo:
        archivo.write(linea)


def leer_txt() -> list:
    """
    Lee todos los registros del archivo TXT.
    Usa open() en modo 'r' (lectura).
    Retorna una lista de strings (una por línea).
    """
    if not os.path.exists(RUTA_TXT):
        return []
    with open(RUTA_TXT, "r", encoding="utf-8") as archivo:
        lineas = [l.strip() for l in archivo.readlines() if l.strip()]
    return lineas


# ──────────────────────────────────────────────────────────────────────────────
# PERSISTENCIA JSON  (usando la librería json)
# ──────────────────────────────────────────────────────────────────────────────

def guardar_json(datos: dict) -> None:
    """
    Guarda un medicamento en el archivo JSON.
    Lee la lista existente, agrega el nuevo registro y reescribe el archivo.
    """
    registros = leer_json()          # Obtener lista actual
    registros.append(datos)          # Agregar nuevo registro como dict
    with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=4)


def leer_json() -> list:
    """
    Lee todos los registros del archivo JSON.
    Retorna una lista de diccionarios.
    """
    if not os.path.exists(RUTA_JSON):
        return []
    with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
        if not contenido:
            return []
        return json.loads(contenido)


# ──────────────────────────────────────────────────────────────────────────────
# PERSISTENCIA CSV  (usando la librería csv)
# ──────────────────────────────────────────────────────────────────────────────

def guardar_csv(datos: dict) -> None:
    """
    Guarda un medicamento en el archivo CSV.
    Si el archivo no existe crea la fila de cabeceras automáticamente.
    """
    archivo_nuevo = not os.path.exists(RUTA_CSV) or os.path.getsize(RUTA_CSV) == 0

    with open(RUTA_CSV, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CABECERAS_CSV)
        if archivo_nuevo:
            escritor.writeheader()          # Escribir cabeceras solo la primera vez
        escritor.writerow({
            "nombre":      datos["nombre"],
            "precio":      datos["precio"],
            "cantidad":    datos["cantidad"],
            "categoria":   datos["categoria"],
            "descripcion": datos["descripcion"],
        })


def leer_csv() -> list:
    """
    Lee todos los registros del archivo CSV.
    Retorna una lista de diccionarios (uno por fila).
    """
    if not os.path.exists(RUTA_CSV):
        return []
    registros = []
    with open(RUTA_CSV, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            registros.append(dict(fila))
    return registros
