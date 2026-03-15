"""
Conexion/conexion.py – Semana 13
Proyecto: ClínicaSalud

Configuración de la conexión entre Flask y MySQL.
Proporciona una función get_connection_mysql() que retorna
una conexión activa lista para ejecutar consultas.

Requisitos previos:
  pip install mysql-connector-python

Base de datos MySQL requerida:
  CREATE DATABASE clinica_salud_mysql CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

import mysql.connector
from mysql.connector import Error

# ─────────────────────────────────────────────────────────────────────────────
# PARÁMETROS DE CONEXIÓN
# Modifica estos valores según tu entorno local de MySQL.
# ─────────────────────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",      # Servidor MySQL (127.0.0.1 también válido)
    "port":     3307,             # Puerto por defecto de MySQL
    "user":     "root",           # Usuario MySQL
    "password": "12345",           # Contraseña del usuario
    "database": "clinica_salud_mysql",  # Base de datos del proyecto
    "charset":  "utf8mb4",        # Soporte para caracteres especiales (tildes, ñ)
    "collation": "utf8mb4_unicode_ci",
    "autocommit": False,          # Control manual de transacciones
}


def get_connection_mysql():
    """
    Crea y retorna una conexión activa a MySQL.

    Returns:
        mysql.connector.connection.MySQLConnection : conexión lista para usar.

    Raises:
        mysql.connector.Error : si no se puede establecer la conexión.

    Ejemplo de uso:
        conn = get_connection_mysql()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        filas = cursor.fetchall()
        conn.close()
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        raise ConnectionError(
            f"❌ No se pudo conectar a MySQL.\n"
            f"Verifica host, usuario y contraseña en Conexion/conexion.py\n"
            f"Detalle del error: {e}"
        )


def probar_conexion() -> dict:
    """
    Prueba la conexión y retorna un diccionario con el resultado.
    Útil para la ruta /mysql/estado en app.py.

    Returns:
        dict con claves: ok (bool), mensaje (str), version (str|None)
    """
    try:
        conn = get_connection_mysql()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {
            "ok":      True,
            "mensaje": "Conexión exitosa a MySQL ✅",
            "version": version,
            "host":    DB_CONFIG["host"],
            "base":    DB_CONFIG["database"],
        }
    except Exception as e:
        return {
            "ok":      False,
            "mensaje": f"Error de conexión: {e}",
            "version": None,
            "host":    DB_CONFIG["host"],
            "base":    DB_CONFIG["database"],
        }
