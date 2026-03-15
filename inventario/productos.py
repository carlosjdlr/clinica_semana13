"""
productos.py – Semana 12
Clase Medicamento usando Programación Orientada a Objetos.
Proyecto: ClínicaSalud
"""


class Medicamento:
    """
    Representa un medicamento del inventario de la clínica.

    Atributos:
        id          : identificador único (int)
        nombre      : nombre del medicamento (str)
        precio      : precio unitario en USD (float)
        cantidad    : unidades disponibles en stock (int)
        categoria   : tipo de medicamento (str)
        descripcion : descripción o indicación (str)
    """

    # Categorías válidas de medicamentos (tupla inmutable)
    CATEGORIAS: tuple = (
        "Analgésico", "Antibiótico", "Antiinflamatorio",
        "Vitaminas", "Antihipertensivo", "Antihistamínico", "Otro"
    )

    def __init__(
        self,
        id_medicamento: int,
        nombre: str,
        precio: float,
        cantidad: int,
        categoria: str,
        descripcion: str = ""
    ):
        self.__id_medicamento = id_medicamento
        self.__nombre         = nombre
        self.__precio         = precio
        self.__cantidad       = cantidad
        self.__categoria      = categoria
        self.__descripcion    = descripcion

    # ── Getters ──────────────────────────────────────────────────────────────
    @property
    def id_medicamento(self):  return self.__id_medicamento

    @property
    def nombre(self):          return self.__nombre

    @property
    def precio(self):          return self.__precio

    @property
    def cantidad(self):        return self.__cantidad

    @property
    def categoria(self):       return self.__categoria

    @property
    def descripcion(self):     return self.__descripcion

    # ── Setters con validación ────────────────────────────────────────────────
    @nombre.setter
    def nombre(self, value: str):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = value.strip().title()

    @precio.setter
    def precio(self, value: float):
        if value < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = round(float(value), 2)

    @cantidad.setter
    def cantidad(self, value: int):
        if value < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = int(value)

    @categoria.setter
    def categoria(self, value: str):
        if value not in Medicamento.CATEGORIAS:
            raise ValueError(f"Categoría inválida. Opciones: {Medicamento.CATEGORIAS}")
        self.__categoria = value

    @descripcion.setter
    def descripcion(self, value: str):
        self.__descripcion = value.strip()

    # ── Representación ───────────────────────────────────────────────────────
    def __repr__(self):
        return (
            f"Medicamento(id={self.__id_medicamento}, "
            f"nombre='{self.__nombre}', precio={self.__precio}, "
            f"stock={self.__cantidad})"
        )

    def to_dict(self) -> dict:
        """Serializa el medicamento a diccionario (útil para JSON/CSV/TXT)."""
        return {
            "id_medicamento": self.__id_medicamento,
            "nombre":         self.__nombre,
            "precio":         self.__precio,
            "cantidad":       self.__cantidad,
            "categoria":      self.__categoria,
            "descripcion":    self.__descripcion,
        }
