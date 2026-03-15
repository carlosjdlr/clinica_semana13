"""
database_mysql.py – Semana 13
Proyecto: ClínicaSalud

Crea las tablas en MySQL y provee funciones CRUD para:
  • usuarios      (id_usuario, nombre, mail, password)
  • pacientes_my  (id_paciente, nombre, apellido, edad, genero,
                   telefono, email, especialidad, observaciones)
  • medicamentos_my (id, nombre, precio, cantidad, categoria, descripcion)

Todas las operaciones usan la conexión definida en Conexion/conexion.py.
"""

from Conexion.conexion import get_connection_mysql


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN: crear tablas si no existen
# ─────────────────────────────────────────────────────────────────────────────

def init_mysql():
    """
    Crea las tablas necesarias en MySQL si aún no existen,
    e inserta datos de ejemplo solo en la primera ejecución.
    """
    conn   = get_connection_mysql()
    cursor = conn.cursor()

    # ── Tabla USUARIOS (requerida por la tarea) ───────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT          AUTO_INCREMENT PRIMARY KEY,
            nombre     VARCHAR(100) NOT NULL,
            mail       VARCHAR(150) NOT NULL UNIQUE,
            password   VARCHAR(255) NOT NULL,
            rol        VARCHAR(30)  NOT NULL DEFAULT 'usuario',
            creado_en  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ── Tabla PACIENTES (espejo MySQL de la tabla SQLite) ─────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes_my (
            id_paciente   INT          AUTO_INCREMENT PRIMARY KEY,
            nombre        VARCHAR(80)  NOT NULL,
            apellido      VARCHAR(80)  NOT NULL,
            edad          TINYINT      NOT NULL,
            genero        VARCHAR(20)  NOT NULL,
            telefono      VARCHAR(20)  NOT NULL,
            email         VARCHAR(150) NOT NULL UNIQUE,
            especialidad  VARCHAR(50)  NOT NULL,
            observaciones TEXT,
            registrado_en TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ── Tabla MEDICAMENTOS (espejo MySQL del inventario SQLAlchemy) ───────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos_my (
            id          INT          AUTO_INCREMENT PRIMARY KEY,
            nombre      VARCHAR(100) NOT NULL,
            precio      DECIMAL(8,2) NOT NULL,
            cantidad    INT          NOT NULL DEFAULT 0,
            categoria   VARCHAR(50)  NOT NULL,
            descripcion TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # ── Datos semilla USUARIOS ─────────────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        usuarios_seed = [
            ("Admin Sistema",   "admin@clinica.com",    "admin123",    "admin"),
            ("Recepcionista 1", "recep1@clinica.com",   "recep123",    "recepcionista"),
            ("Dr. Carlos M.",   "c.mendoza@clinica.com","medico123",   "medico"),
            ("Dra. Ana Torres", "a.torres@clinica.com", "medico456",   "medico"),
        ]
        cursor.executemany(
            "INSERT INTO usuarios (nombre, mail, password, rol) VALUES (%s, %s, %s, %s)",
            usuarios_seed
        )

    # ── Datos semilla PACIENTES ────────────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM pacientes_my")
    if cursor.fetchone()[0] == 0:
        pacientes_seed = [
            ("Carlos",   "Mendoza",   45, "Masculino", "0991234567", "c.mendoza@email.com",   "Cardiología",   "Hipertensión arterial"),
            ("Ana",      "Torres",    32, "Femenino",  "0987654321", "ana.torres@email.com",  "Neurología",    "Migraña crónica"),
            ("Luis",     "Ramírez",   8,  "Masculino", "0976543210", "l.ramirez@email.com",   "Pediatría",     "Control de crecimiento"),
            ("María",    "González",  29, "Femenino",  "0965432109", "m.gonzalez@email.com",  "Dermatología",  "Acné severo"),
            ("Jorge",    "Castro",    55, "Masculino", "0954321098", "j.castro@email.com",    "Traumatología", "Fractura de muñeca"),
        ]
        cursor.executemany(
            """INSERT INTO pacientes_my
               (nombre, apellido, edad, genero, telefono, email, especialidad, observaciones)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            pacientes_seed
        )

    # ── Datos semilla MEDICAMENTOS ─────────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM medicamentos_my")
    if cursor.fetchone()[0] == 0:
        meds_seed = [
            ("Ibuprofeno 400mg",  2.50, 150, "Analgésico",      "Analgésico y antiinflamatorio"),
            ("Amoxicilina 500mg", 5.80,  80, "Antibiótico",     "Tratamiento de infecciones bacterianas"),
            ("Loratadina 10mg",   3.20,  60, "Antihistamínico", "Alergia y rinitis alérgica"),
            ("Enalapril 10mg",    4.00, 100, "Antihipertensivo","Control de presión arterial"),
            ("Vitamina C 500mg",  1.90, 200, "Vitaminas",       "Suplemento vitamínico"),
        ]
        cursor.executemany(
            """INSERT INTO medicamentos_my (nombre, precio, cantidad, categoria, descripcion)
               VALUES (%s, %s, %s, %s, %s)""",
            meds_seed
        )

    conn.commit()
    cursor.close()
    conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# CRUD – USUARIOS
# ─────────────────────────────────────────────────────────────────────────────

def usuario_obtener_todos() -> list:
    conn   = get_connection_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre, mail, rol, creado_en FROM usuarios ORDER BY nombre")
    filas  = cursor.fetchall()
    cursor.close(); conn.close()
    return filas


def usuario_obtener_por_id(id_usuario: int) -> dict | None:
    conn   = get_connection_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_usuario, nombre, mail, rol FROM usuarios WHERE id_usuario = %s",
        (id_usuario,)
    )
    fila = cursor.fetchone()
    cursor.close(); conn.close()
    return fila


def usuario_insertar(nombre: str, mail: str, password: str, rol: str = "usuario") -> int:
    conn   = get_connection_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, mail, password, rol) VALUES (%s, %s, %s, %s)",
        (nombre, mail, password, rol)
    )
    nuevo_id = cursor.lastrowid
    conn.commit()
    cursor.close(); conn.close()
    return nuevo_id


def usuario_actualizar(id_usuario: int, nombre: str, mail: str, rol: str) -> bool:
    conn   = get_connection_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET nombre=%s, mail=%s, rol=%s WHERE id_usuario=%s",
        (nombre, mail, rol, id_usuario)
    )
    afectadas = cursor.rowcount
    conn.commit()
    cursor.close(); conn.close()
    return afectadas > 0


def usuario_eliminar(id_usuario: int) -> bool:
    conn   = get_connection_mysql()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    afectadas = cursor.rowcount
    conn.commit()
    cursor.close(); conn.close()
    return afectadas > 0


# ─────────────────────────────────────────────────────────────────────────────
# CRUD – PACIENTES (MySQL)
# ─────────────────────────────────────────────────────────────────────────────

def paciente_my_obtener_todos() -> list:
    conn   = get_connection_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pacientes_my ORDER BY apellido, nombre")
    filas  = cursor.fetchall()
    cursor.close(); conn.close()
    return filas


def paciente_my_obtener_por_id(id_paciente: int) -> dict | None:
    conn   = get_connection_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pacientes_my WHERE id_paciente = %s", (id_paciente,))
    fila = cursor.fetchone()
    cursor.close(); conn.close()
    return fila


def paciente_my_buscar(termino: str) -> list:
    conn   = get_connection_mysql()
    cursor = conn.cursor(dictionary=True)
    like   = f"%{termino}%"
    cursor.execute(
        "SELECT * FROM pacientes_my WHERE nombre LIKE %s OR apellido LIKE %s ORDER BY apellido",
        (like, like)
    )
    filas = cursor.fetchall()
    cursor.close(); conn.close()
    return filas


def paciente_my_insertar(datos: dict) -> int:
    conn   = get_connection_mysql()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO pacientes_my
           (nombre, apellido, edad, genero, telefono, email, especialidad, observaciones)
           VALUES (%(nombre)s, %(apellido)s, %(edad)s, %(genero)s,
                   %(telefono)s, %(email)s, %(especialidad)s, %(observaciones)s)""",
        datos
    )
    nuevo_id = cursor.lastrowid
    conn.commit()
    cursor.close(); conn.close()
    return nuevo_id


def paciente_my_actualizar(id_paciente: int, datos: dict) -> bool:
    conn   = get_connection_mysql()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE pacientes_my SET
               nombre        = %(nombre)s,
               apellido      = %(apellido)s,
               edad          = %(edad)s,
               genero        = %(genero)s,
               telefono      = %(telefono)s,
               email         = %(email)s,
               especialidad  = %(especialidad)s,
               observaciones = %(observaciones)s
           WHERE id_paciente = %(id_paciente)s""",
        {**datos, "id_paciente": id_paciente}
    )
    afectadas = cursor.rowcount
    conn.commit()
    cursor.close(); conn.close()
    return afectadas > 0


def paciente_my_eliminar(id_paciente: int) -> bool:
    conn   = get_connection_mysql()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes_my WHERE id_paciente = %s", (id_paciente,))
    afectadas = cursor.rowcount
    conn.commit()
    cursor.close(); conn.close()
    return afectadas > 0


# ─────────────────────────────────────────────────────────────────────────────
# CRUD – MEDICAMENTOS (MySQL)
# ─────────────────────────────────────────────────────────────────────────────

def medicamento_my_obtener_todos() -> list:
    conn   = get_connection_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicamentos_my ORDER BY nombre")
    filas  = cursor.fetchall()
    cursor.close(); conn.close()
    return filas


def medicamento_my_obtener_por_id(id_med: int) -> dict | None:
    conn   = get_connection_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicamentos_my WHERE id = %s", (id_med,))
    fila = cursor.fetchone()
    cursor.close(); conn.close()
    return fila


def medicamento_my_insertar(datos: dict) -> int:
    conn   = get_connection_mysql()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO medicamentos_my (nombre, precio, cantidad, categoria, descripcion)
           VALUES (%(nombre)s, %(precio)s, %(cantidad)s, %(categoria)s, %(descripcion)s)""",
        datos
    )
    nuevo_id = cursor.lastrowid
    conn.commit()
    cursor.close(); conn.close()
    return nuevo_id


def medicamento_my_actualizar(id_med: int, datos: dict) -> bool:
    conn   = get_connection_mysql()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE medicamentos_my SET
               nombre      = %(nombre)s,
               precio      = %(precio)s,
               cantidad    = %(cantidad)s,
               categoria   = %(categoria)s,
               descripcion = %(descripcion)s
           WHERE id = %(id)s""",
        {**datos, "id": id_med}
    )
    afectadas = cursor.rowcount
    conn.commit()
    cursor.close(); conn.close()
    return afectadas > 0


def medicamento_my_eliminar(id_med: int) -> bool:
    conn   = get_connection_mysql()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicamentos_my WHERE id = %s", (id_med,))
    afectadas = cursor.rowcount
    conn.commit()
    cursor.close(); conn.close()
    return afectadas > 0


# ─────────────────────────────────────────────────────────────────────────────
# ESTADÍSTICAS MYSQL
# ─────────────────────────────────────────────────────────────────────────────

def estadisticas_mysql() -> dict:
    """Estadísticas generales desde las tablas MySQL."""
    conn   = get_connection_mysql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    total_usuarios = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM pacientes_my")
    total_pacientes = cursor.fetchone()["total"]

    cursor.execute("SELECT AVG(edad) AS promedio FROM pacientes_my")
    row = cursor.fetchone()
    prom_edad = round(float(row["promedio"]), 1) if row["promedio"] else 0.0

    cursor.execute(
        "SELECT especialidad, COUNT(*) AS total FROM pacientes_my "
        "GROUP BY especialidad ORDER BY total DESC"
    )
    por_especialidad = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS total FROM medicamentos_my")
    total_meds = cursor.fetchone()["total"]

    cursor.close(); conn.close()
    return {
        "total_usuarios":    total_usuarios,
        "total_pacientes":   total_pacientes,
        "promedio_edad":     prom_edad,
        "por_especialidad":  por_especialidad,
        "total_medicamentos": total_meds,
    }