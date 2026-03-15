"""
models.py – Semana 11
Programación Orientada a Objetos + Colecciones
Proyecto: ClínicaSalud

Clases principales:
  - Paciente     : modela cada paciente con sus atributos y métodos.
  - GestorPacientes : administra la colección de pacientes en memoria
                      y sirve de capa intermedia con la base de datos.

Colecciones utilizadas:
  - dict   : almacenamiento principal {id: Paciente} → búsqueda O(1).
  - list   : resultados de búsquedas y listados ordenados.
  - set    : control de emails únicos sin duplicados.
  - tuple  : datos inmutables (campos de la tabla, géneros permitidos).
"""

# ──────────────────────────────────────────────────────────────────────────────
# CLASE PACIENTE
# ──────────────────────────────────────────────────────────────────────────────
class Paciente:
    """Representa a un paciente de la clínica."""

    # Tupla inmutable con los géneros válidos
    GENEROS_VALIDOS: tuple = ("Masculino", "Femenino", "Otro")

    # Tupla inmutable con las especialidades disponibles
    ESPECIALIDADES: tuple = (
        "Cardiología", "Neurología", "Pediatría",
        "Traumatología", "Dermatología", "Oftalmología", "General"
    )

    def __init__(
        self,
        id_paciente: int,
        nombre: str,
        apellido: str,
        edad: int,
        genero: str,
        telefono: str,
        email: str,
        especialidad: str,
        observaciones: str = ""
    ):
        # Atributos privados con validación a través de setters
        self.__id_paciente   = id_paciente
        self.__nombre        = nombre
        self.__apellido      = apellido
        self.__edad          = edad
        self.__genero        = genero
        self.__telefono      = telefono
        self.__email         = email
        self.__especialidad  = especialidad
        self.__observaciones = observaciones

    # ── Getters ──────────────────────────────────────────────────────────────
    @property
    def id_paciente(self):   return self.__id_paciente
    @property
    def nombre(self):        return self.__nombre
    @property
    def apellido(self):      return self.__apellido
    @property
    def edad(self):          return self.__edad
    @property
    def genero(self):        return self.__genero
    @property
    def telefono(self):      return self.__telefono
    @property
    def email(self):         return self.__email
    @property
    def especialidad(self):  return self.__especialidad
    @property
    def observaciones(self): return self.__observaciones

    # Nombre completo calculado
    @property
    def nombre_completo(self): return f"{self.__nombre} {self.__apellido}"

    # ── Setters con validación ────────────────────────────────────────────────
    @nombre.setter
    def nombre(self, value: str):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = value.strip().title()

    @apellido.setter
    def apellido(self, value: str):
        if not value.strip():
            raise ValueError("El apellido no puede estar vacío.")
        self.__apellido = value.strip().title()

    @edad.setter
    def edad(self, value: int):
        if not (0 <= value <= 120):
            raise ValueError("La edad debe estar entre 0 y 120.")
        self.__edad = value

    @genero.setter
    def genero(self, value: str):
        if value not in Paciente.GENEROS_VALIDOS:
            raise ValueError(f"Género inválido. Opciones: {Paciente.GENEROS_VALIDOS}")
        self.__genero = value

    @especialidad.setter
    def especialidad(self, value: str):
        if value not in Paciente.ESPECIALIDADES:
            raise ValueError(f"Especialidad inválida. Opciones: {Paciente.ESPECIALIDADES}")
        self.__especialidad = value

    @observaciones.setter
    def observaciones(self, value: str):
        self.__observaciones = value.strip()

    # ── Representación ───────────────────────────────────────────────────────
    def __repr__(self):
        return (
            f"Paciente(id={self.__id_paciente}, "
            f"nombre='{self.nombre_completo}', "
            f"especialidad='{self.__especialidad}')"
        )

    def to_dict(self) -> dict:
        """Serializa el paciente a un diccionario (útil para JSON/plantillas)."""
        return {
            "id_paciente":   self.__id_paciente,
            "nombre":        self.__nombre,
            "apellido":      self.__apellido,
            "edad":          self.__edad,
            "genero":        self.__genero,
            "telefono":      self.__telefono,
            "email":         self.__email,
            "especialidad":  self.__especialidad,
            "observaciones": self.__observaciones,
        }


# ──────────────────────────────────────────────────────────────────────────────
# CLASE GESTORPACIENTES  (colección principal en memoria)
# ──────────────────────────────────────────────────────────────────────────────
class GestorPacientes:
    """
    Administra la colección de pacientes usando un diccionario interno
    {id_paciente: Paciente} para búsquedas en O(1).

    También mantiene un set de emails registrados para evitar duplicados
    sin recorrer toda la colección.
    """

    def __init__(self):
        # Colección principal: dict {int → Paciente}
        self.__pacientes: dict[int, Paciente] = {}
        # Conjunto para control de unicidad de emails
        self.__emails_registrados: set = set()

    # ── Añadir ───────────────────────────────────────────────────────────────
    def agregar(self, paciente: Paciente) -> None:
        """Agrega un paciente. Lanza ValueError si el email ya existe."""
        if paciente.email.lower() in self.__emails_registrados:
            raise ValueError(f"El email '{paciente.email}' ya está registrado.")
        self.__pacientes[paciente.id_paciente] = paciente
        self.__emails_registrados.add(paciente.email.lower())

    # ── Eliminar ─────────────────────────────────────────────────────────────
    def eliminar(self, id_paciente: int) -> bool:
        """Elimina por ID. Retorna True si encontrado, False si no."""
        paciente = self.__pacientes.pop(id_paciente, None)
        if paciente:
            self.__emails_registrados.discard(paciente.email.lower())
            return True
        return False

    # ── Actualizar ───────────────────────────────────────────────────────────
    def actualizar(self, id_paciente: int, **kwargs) -> bool:
        """
        Actualiza campos del paciente indicado.
        Acepta: nombre, apellido, edad, genero, telefono,
                email, especialidad, observaciones.
        """
        if id_paciente not in self.__pacientes:
            return False
        p = self.__pacientes[id_paciente]
        # Si se cambia el email, actualizar el set
        nuevo_email = kwargs.get("email")
        if nuevo_email and nuevo_email.lower() != p.email.lower():
            if nuevo_email.lower() in self.__emails_registrados:
                raise ValueError(f"El email '{nuevo_email}' ya pertenece a otro paciente.")
            self.__emails_registrados.discard(p.email.lower())
            self.__emails_registrados.add(nuevo_email.lower())
        # Aplicar cambios usando los setters de la clase
        for campo, valor in kwargs.items():
            setattr(p, campo, valor)
        return True

    # ── Buscar ───────────────────────────────────────────────────────────────
    def buscar_por_nombre(self, termino: str) -> list[Paciente]:
        """Búsqueda parcial e insensible a mayúsculas en nombre o apellido."""
        termino_lower = termino.lower()
        return [
            p for p in self.__pacientes.values()
            if termino_lower in p.nombre.lower()
            or termino_lower in p.apellido.lower()
        ]

    def buscar_por_id(self, id_paciente: int):
        """Retorna el Paciente o None."""
        return self.__pacientes.get(id_paciente)

    def buscar_por_especialidad(self, especialidad: str) -> list[Paciente]:
        """Lista de pacientes filtrados por especialidad."""
        return [
            p for p in self.__pacientes.values()
            if p.especialidad.lower() == especialidad.lower()
        ]

    # ── Listar todos ─────────────────────────────────────────────────────────
    def todos(self) -> list[Paciente]:
        """Retorna lista ordenada por apellido."""
        return sorted(self.__pacientes.values(), key=lambda p: p.apellido)

    # ── Estadísticas ─────────────────────────────────────────────────────────
    def total(self) -> int:
        return len(self.__pacientes)

    def especialidades_activas(self) -> set:
        """Conjunto de especialidades con al menos un paciente."""
        return {p.especialidad for p in self.__pacientes.values()}

    def promedio_edad(self) -> float:
        if not self.__pacientes:
            return 0.0
        edades = [p.edad for p in self.__pacientes.values()]
        return round(sum(edades) / len(edades), 1)

    # ── Cargar desde lista de filas (SQLite) ─────────────────────────────────
    def cargar_desde_db(self, filas: list) -> None:
        """Recibe lista de sqlite3.Row y reconstruye la colección en memoria."""
        self.__pacientes.clear()
        self.__emails_registrados.clear()
        for fila in filas:
            p = Paciente(
                id_paciente   = fila["id_paciente"],
                nombre        = fila["nombre"],
                apellido      = fila["apellido"],
                edad          = fila["edad"],
                genero        = fila["genero"],
                telefono      = fila["telefono"],
                email         = fila["email"],
                especialidad  = fila["especialidad"],
                observaciones = fila["observaciones"],
            )
            self.__pacientes[p.id_paciente] = p
            self.__emails_registrados.add(p.email.lower())
