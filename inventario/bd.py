"""
bd.py – Semana 12
Configuración de SQLAlchemy y modelo ORM para inventario de medicamentos.
Proyecto: ClínicaSalud
"""

from flask_sqlalchemy import SQLAlchemy

# Instancia de SQLAlchemy (se inicializa con la app en app.py)
db = SQLAlchemy()


class MedicamentoDB(db.Model):
    """
    Modelo ORM que representa la tabla 'medicamentos' en SQLite.
    SQLAlchemy mapea automáticamente esta clase a la tabla de la BD.
    """

    __tablename__ = "medicamentos"

    # Campos / columnas
    id          = db.Column(db.Integer,       primary_key=True, autoincrement=True)
    nombre      = db.Column(db.String(100),   nullable=False)
    precio      = db.Column(db.Float,         nullable=False)
    cantidad    = db.Column(db.Integer,       nullable=False, default=0)
    categoria   = db.Column(db.String(50),    nullable=False)
    descripcion = db.Column(db.Text,          default="")

    def __repr__(self):
        return f"<MedicamentoDB {self.nombre} | stock:{self.cantidad}>"

    def to_dict(self) -> dict:
        """Convierte el objeto ORM a diccionario."""
        return {
            "id":          self.id,
            "nombre":      self.nombre,
            "precio":      self.precio,
            "cantidad":    self.cantidad,
            "categoria":   self.categoria,
            "descripcion": self.descripcion,
        }
