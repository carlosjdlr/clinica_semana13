"""
database.py – Semana 11
Conexión a SQLite y operaciones CRUD para ClínicaSalud.

Tablas:
  - pacientes : información completa de cada paciente.
"""

import sqlite3
import os

# Ruta absoluta de la base de datos (en la raíz del proyecto)
DB_PATH = os.path.join(os.path.dirname(__file__), "clinica_salud.db")

# Campos de la tabla como tupla inmutable (colección)
CAMPOS_PACIENTE: tuple = (
    "id_paciente", "nombre", "apellido", "edad",
    "genero", "telefono", "email", "especialidad", "observaciones"
)


def get_connection():
    """Retorna una conexión SQLite con acceso por nombre de columna."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # Permite acceder como dict
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Crea las tablas si no existen e inserta datos de ejemplo
    solo en la primera ejecución.
    """
    conn = get_connection()
    cur  = conn.cursor()

    # ── Tabla pacientes ──────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id_paciente   INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre        TEXT    NOT NULL,
            apellido      TEXT    NOT NULL,
            edad          INTEGER NOT NULL CHECK(edad BETWEEN 0 AND 120),
            genero        TEXT    NOT NULL,
            telefono      TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            especialidad  TEXT    NOT NULL,
            observaciones TEXT    DEFAULT ''
        )
    """)

    # ── Datos semilla (solo si la tabla está vacía) ───────────────────────────
    cur.execute("SELECT COUNT(*) FROM pacientes")
    if cur.fetchone()[0] == 0:
        pacientes_iniciales = [
            ("Carlos",    "Mendoza",   45, "Masculino", "0991234567", "c.mendoza@email.com",   "Cardiología",   "Hipertensión arterial"),
            ("Ana",       "Torres",    32, "Femenino",  "0987654321", "ana.torres@email.com",  "Neurología",    "Migraña crónica"),
            ("Luis",      "Ramírez",   8,  "Masculino", "0976543210", "l.ramirez@email.com",   "Pediatría",     "Control de crecimiento"),
            ("María",     "González",  29, "Femenino",  "0965432109", "m.gonzalez@email.com",  "Dermatología",  "Acné severo"),
            ("Jorge",     "Castro",    55, "Masculino", "0954321098", "j.castro@email.com",    "Traumatología", "Fractura de muñeca"),
            ("Patricia",  "Rojas",     41, "Femenino",  "0943210987", "p.rojas@email.com",     "Oftalmología",  "Miopía progresiva"),
            ("Roberto",   "Vargas",    67, "Masculino", "0932109876", "r.vargas@email.com",    "Cardiología",   "Arritmia cardíaca"),
            ("Sofía",     "Herrera",   22, "Femenino",  "0921098765", "s.herrera@email.com",   "General",       "Consulta general"),
        ]
        cur.executemany(
            """INSERT INTO pacientes
               (nombre, apellido, edad, genero, telefono, email, especialidad, observaciones)
               VALUES (?,?,?,?,?,?,?,?)""",
            pacientes_iniciales
        )

    conn.commit()
    conn.close()


# ──────────────────────────────────────────────────────────────────────────────
# CRUD PACIENTES
# ──────────────────────────────────────────────────────────────────────────────

def obtener_todos() -> list:
    """Retorna lista de todos los pacientes ordenados por apellido."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM pacientes ORDER BY apellido, nombre")
    filas = cur.fetchall()
    conn.close()
    return filas


def obtener_por_id(id_paciente: int):
    """Retorna el registro del paciente o None."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM pacientes WHERE id_paciente = ?", (id_paciente,))
    fila = cur.fetchone()
    conn.close()
    return fila


def buscar_por_nombre(termino: str) -> list:
    """Búsqueda parcial en nombre o apellido."""
    conn = get_connection()
    cur  = conn.cursor()
    like = f"%{termino}%"
    cur.execute(
        "SELECT * FROM pacientes WHERE nombre LIKE ? OR apellido LIKE ? ORDER BY apellido",
        (like, like)
    )
    filas = cur.fetchall()
    conn.close()
    return filas


def insertar_paciente(datos: dict) -> int:
    """
    Inserta un nuevo paciente. Retorna el id asignado.
    datos: dict con claves nombre, apellido, edad, genero,
           telefono, email, especialidad, observaciones.
    """
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        """INSERT INTO pacientes
           (nombre, apellido, edad, genero, telefono, email, especialidad, observaciones)
           VALUES (:nombre, :apellido, :edad, :genero,
                   :telefono, :email, :especialidad, :observaciones)""",
        datos
    )
    nuevo_id = cur.lastrowid
    conn.commit()
    conn.close()
    return nuevo_id


def actualizar_paciente(id_paciente: int, datos: dict) -> bool:
    """
    Actualiza un paciente existente. Retorna True si se modificó al menos 1 fila.
    """
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        """UPDATE pacientes SET
               nombre        = :nombre,
               apellido      = :apellido,
               edad          = :edad,
               genero        = :genero,
               telefono      = :telefono,
               email         = :email,
               especialidad  = :especialidad,
               observaciones = :observaciones
           WHERE id_paciente = :id_paciente""",
        {**datos, "id_paciente": id_paciente}
    )
    filas_afectadas = cur.rowcount
    conn.commit()
    conn.close()
    return filas_afectadas > 0


def eliminar_paciente(id_paciente: int) -> bool:
    """Elimina un paciente por ID. Retorna True si fue eliminado."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("DELETE FROM pacientes WHERE id_paciente = ?", (id_paciente,))
    filas_afectadas = cur.rowcount
    conn.commit()
    conn.close()
    return filas_afectadas > 0


def estadisticas() -> dict:
    """Retorna estadísticas generales del sistema."""
    conn = get_connection()
    cur  = conn.cursor()

    # Total pacientes
    cur.execute("SELECT COUNT(*) FROM pacientes")
    total = cur.fetchone()[0]

    # Promedio de edad
    cur.execute("SELECT AVG(edad) FROM pacientes")
    prom  = cur.fetchone()[0] or 0

    # Distribución por especialidad
    cur.execute(
        "SELECT especialidad, COUNT(*) as total FROM pacientes GROUP BY especialidad ORDER BY total DESC"
    )
    por_especialidad = [dict(r) for r in cur.fetchall()]

    # Distribución por género
    cur.execute(
        "SELECT genero, COUNT(*) as total FROM pacientes GROUP BY genero"
    )
    por_genero = [dict(r) for r in cur.fetchall()]

    conn.close()
    return {
        "total_pacientes":  total,
        "promedio_edad":    round(prom, 1),
        "por_especialidad": por_especialidad,
        "por_genero":       por_genero,
    }
