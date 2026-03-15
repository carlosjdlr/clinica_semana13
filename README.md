# ClínicaSalud – Semana 13
## Flask + SQLite + SQLAlchemy + MySQL

---

## ⚡ Instalación rápida

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear la BD MySQL en Workbench
#    Abrir clinica_workbench.sql y ejecutar (Ctrl+Shift+Enter)

# 4. Configurar credenciales MySQL
#    Editar Conexion/conexion.py → cambiar user y password

# 5. Ejecutar
python app.py
```

Abrir en el navegador: http://localhost:5000

## 🗄️ Panel MySQL
http://localhost:5000/mysql/estado

---

## 📁 Estructura del proyecto

```
clinica_salud/
├── app.py                  ← aplicación principal
├── models.py               ← clases POO (Paciente, GestorPacientes)
├── database.py             ← CRUD SQLite pacientes
├── database_mysql.py       ← CRUD MySQL (usuarios, pacientes, medicamentos)
├── requirements.txt
├── clinica_workbench.sql   ← script para crear la BD en MySQL
│
├── Conexion/
│   ├── __init__.py
│   └── conexion.py         ← ⭐ configurar credenciales aquí
│
├── inventario/
│   ├── bd.py               ← modelo SQLAlchemy
│   ├── inventario.py       ← TXT, JSON, CSV
│   └── productos.py        ← clase Medicamento
│
├── data/                   ← archivos TXT/JSON/CSV generados en runtime
│
└── templates/
    ├── base.html
    ├── index.html / medicos.html / servicios.html
    ├── horarios.html / contacto.html / acerca.html
    ├── datos.html / inventario_form.html
    ├── pacientes/
    │   ├── lista.html / detalle.html
    │   ├── formulario.html / estadisticas.html
    └── mysql/
        ├── estado.html
        ├── usuarios.html / usuario_form.html
        ├── pacientes.html / paciente_form.html
        ├── medicamentos.html / medicamento_form.html
        └── estadisticas.html
```
