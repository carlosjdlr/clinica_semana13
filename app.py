"""
app.py – ClínicaSalud · Semana 13
Flask + POO + SQLite + SQLAlchemy + Archivos TXT/JSON/CSV + MySQL
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash

# ── Semanas anteriores ────────────────────────────────────────────────────────
from models   import Paciente, GestorPacientes
from database import (
    init_db, obtener_todos, obtener_por_id,
    buscar_por_nombre, insertar_paciente,
    actualizar_paciente, eliminar_paciente, estadisticas,
    get_connection
)
from inventario.bd         import db, MedicamentoDB
from inventario.inventario import (
    guardar_txt, leer_txt,
    guardar_json, leer_json,
    guardar_csv, leer_csv,
)
from inventario.productos  import Medicamento

# ── Semana 13: MySQL ──────────────────────────────────────────────────────────
from Conexion.conexion import probar_conexion
from database_mysql import (
    init_mysql,
    usuario_obtener_todos, usuario_obtener_por_id,
    usuario_insertar, usuario_actualizar, usuario_eliminar,
    paciente_my_obtener_todos, paciente_my_obtener_por_id,
    paciente_my_buscar, paciente_my_insertar,
    paciente_my_actualizar, paciente_my_eliminar,
    medicamento_my_obtener_todos, medicamento_my_obtener_por_id,
    medicamento_my_insertar, medicamento_my_actualizar,
    medicamento_my_eliminar,
    estadisticas_mysql,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "clinica_salud_2025_key"

app.config["SQLALCHEMY_DATABASE_URI"]        = "sqlite:///inventario.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    if MedicamentoDB.query.count() == 0:
        semilla = [
            MedicamentoDB(nombre="Ibuprofeno 400mg",    precio=2.50,  cantidad=150, categoria="Analgésico",       descripcion="Analgésico y antiinflamatorio"),
            MedicamentoDB(nombre="Amoxicilina 500mg",   precio=5.80,  cantidad=80,  categoria="Antibiótico",      descripcion="Tratamiento de infecciones bacterianas"),
            MedicamentoDB(nombre="Loratadina 10mg",     precio=3.20,  cantidad=60,  categoria="Antihistamínico",  descripcion="Alergia y rinitis alérgica"),
            MedicamentoDB(nombre="Enalapril 10mg",      precio=4.00,  cantidad=100, categoria="Antihipertensivo", descripcion="Control de presión arterial"),
            MedicamentoDB(nombre="Vitamina C 500mg",    precio=1.90,  cantidad=200, categoria="Vitaminas",        descripcion="Suplemento vitamínico"),
        ]
        db.session.add_all(semilla)
        db.session.commit()

init_db()

try:
    init_mysql()
    print("✅ MySQL conectado correctamente.")
except Exception as e:
    print(f"⚠️  MySQL no disponible al iniciar: {e}")

gestor = GestorPacientes()

ESPECIALIDADES = Paciente.ESPECIALIDADES
GENEROS        = Paciente.GENEROS_VALIDOS
CATEGORIAS_MED = Medicamento.CATEGORIAS


# ─────────────────────────────────────────────────────────────────────────────
# RUTAS PRINCIPALES (Semanas 9 y 10)
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    especialidades = [
        {"nombre": "Cardiología",   "icono": "❤️",  "descripcion": "Diagnóstico y tratamiento del corazón."},
        {"nombre": "Neurología",    "icono": "🧠",  "descripcion": "Trastornos del sistema nervioso."},
        {"nombre": "Pediatría",     "icono": "👶",  "descripcion": "Atención médica para niños y adolescentes."},
        {"nombre": "Traumatología", "icono": "🦴",  "descripcion": "Lesiones y enfermedades del sistema óseo."},
        {"nombre": "Dermatología",  "icono": "🩺",  "descripcion": "Diagnóstico de enfermedades de la piel."},
        {"nombre": "Oftalmología",  "icono": "👁️",  "descripcion": "Salud visual y enfermedades del ojo."},
    ]
    stats = estadisticas()
    return render_template('index.html', especialidades=especialidades, stats=stats)


@app.route('/cita/<paciente>')
def cita(paciente):
    return render_template('cita.html', paciente=paciente.capitalize())


@app.route('/especialidad/<nombre>')
def especialidad(nombre):
    info = {
        "cardiologia":   {"titulo": "Cardiología",   "icono": "❤️",  "descripcion": "Especialidad médica que se ocupa de las afecciones del corazón.", "horario": "Lunes a Viernes 8:00 – 18:00"},
        "neurologia":    {"titulo": "Neurología",    "icono": "🧠",  "descripcion": "Rama de la medicina que estudia los trastornos del sistema nervioso.", "horario": "Lunes a Jueves 9:00 – 17:00"},
        "pediatria":     {"titulo": "Pediatría",     "icono": "👶",  "descripcion": "Especialidad médica dedicada a la atención de la salud de niños.", "horario": "Lunes a Sábado 8:00 – 14:00"},
        "traumatologia": {"titulo": "Traumatología", "icono": "🦴",  "descripcion": "Especialidad que trata lesiones del sistema músculo-esquelético.", "horario": "Martes a Viernes 8:00 – 16:00"},
        "dermatologia":  {"titulo": "Dermatología",  "icono": "🩺",  "descripcion": "Especialidad médica enfocada en enfermedades de la piel.", "horario": "Lunes, Miércoles y Viernes 10:00 – 18:00"},
        "oftalmologia":  {"titulo": "Oftalmología",  "icono": "👁️",  "descripcion": "Especialidad médica que trata las enfermedades del ojo.", "horario": "Martes a Sábado 9:00 – 15:00"},
    }
    key   = nombre.lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    datos = info.get(key, {"titulo": nombre.capitalize(), "icono": "🏥", "descripcion": "Especialidad disponible.", "horario": "Consultar en recepción"})
    return render_template('especialidad.html', datos=datos)


@app.route('/acerca')
def acerca():
    return render_template('acerca.html')


@app.route('/medicos')
def medicos():
    doctores = [
        {"nombre": "Dr. Carlos Mendoza",  "especialidad": "Cardiología",   "experiencia": "15 años", "educacion": "Universidad Nacional · Maestría en Cardiología Clínica",  "icono": "❤️"},
        {"nombre": "Dra. Ana Torres",     "especialidad": "Neurología",    "experiencia": "12 años", "educacion": "Universidad de los Andes · Especialización en Neurología", "icono": "🧠"},
        {"nombre": "Dr. Luis Ramírez",    "especialidad": "Pediatría",     "experiencia": "10 años", "educacion": "Universidad Central · Postgrado en Pediatría Integral",    "icono": "👶"},
        {"nombre": "Dra. María González", "especialidad": "Dermatología",  "experiencia": "8 años",  "educacion": "Universidad Javeriana · Dermatología Cosmética",           "icono": "🩺"},
        {"nombre": "Dr. Jorge Castro",    "especialidad": "Traumatología", "experiencia": "18 años", "educacion": "Universidad del Rosario · Cirugía Ortopédica",            "icono": "🦴"},
        {"nombre": "Dra. Patricia Rojas", "especialidad": "Oftalmología",  "experiencia": "14 años", "educacion": "Universidad Nacional · Cirugía Láser Ocular",             "icono": "👁️"},
    ]
    return render_template('medicos.html', doctores=doctores)


@app.route('/horarios')
def horarios():
    horarios_data = {
        "clinica": {"lunes_viernes": "7:00 AM - 8:00 PM", "sabados": "8:00 AM - 2:00 PM", "domingos": "Cerrado", "urgencias": "24/7"},
        "especialidades": [
            {"nombre": "Cardiología",   "horario": "Lunes a Viernes 8:00 – 18:00"},
            {"nombre": "Neurología",    "horario": "Lunes a Jueves 9:00 – 17:00"},
            {"nombre": "Pediatría",     "horario": "Lunes a Sábado 8:00 – 14:00"},
            {"nombre": "Traumatología", "horario": "Martes a Viernes 8:00 – 16:00"},
            {"nombre": "Dermatología",  "horario": "Lunes, Miércoles y Viernes 10:00 – 18:00"},
            {"nombre": "Oftalmología",  "horario": "Martes a Sábado 9:00 – 15:00"},
        ]
    }
    return render_template('horarios.html', horarios=horarios_data)


@app.route('/servicios')
def servicios():
    servicios_list = [
        {"titulo": "Laboratorio Clínico",   "icono": "🔬", "descripcion": "Análisis de sangre, orina y estudios especializados.", "incluye": ["Hemograma completo", "Perfil lipídico", "Glucosa", "Análisis de orina"]},
        {"titulo": "Radiología e Imágenes", "icono": "📷", "descripcion": "Rayos X, ecografías y resonancias magnéticas.",         "incluye": ["Rayos X digital", "Ecografía 4D", "Tomografía", "Resonancia magnética"]},
        {"titulo": "Farmacia 24 Horas",     "icono": "💊", "descripcion": "Medicamentos genéricos y de marca las 24 horas.",       "incluye": ["Entrega inmediata", "Medicamentos recetados", "Genéricos", "Cuidado personal"]},
        {"titulo": "Servicio de Urgencias", "icono": "🚑", "descripcion": "Atención médica de emergencia todos los días.",         "incluye": ["Atención inmediata", "Ambulancia", "Sala de observación", "Médicos especializados"]},
        {"titulo": "Vacunación",            "icono": "💉", "descripcion": "Esquemas de vacunación para niños y adultos.",          "incluye": ["Vacunas infantiles", "Vacunas adultos", "Certificados internacionales", "Asesoría médica"]},
        {"titulo": "Telemedicina",          "icono": "💻", "descripcion": "Consultas médicas virtuales desde tu hogar.",           "incluye": ["Consulta en línea", "Recetas digitales", "Seguimiento", "Historial digital"]},
    ]
    return render_template('servicios.html', servicios=servicios_list)


@app.route('/contacto')
def contacto():
    datos_contacto = {
        "direccion": "Calle Principal #45-67, Sector Centro",
        "telefono":  "+593 (02) 234-5678",
        "whatsapp":  "+593 98 765 4321",
        "email":     "contacto@clinicasalud.com",
        "horario_atencion": "Lunes a Viernes: 7:00 AM - 8:00 PM | Sábados: 8:00 AM - 2:00 PM"
    }
    return render_template('contacto.html', contacto=datos_contacto)


# ─────────────────────────────────────────────────────────────────────────────
# RUTAS SEMANA 11 – GESTIÓN DE PACIENTES (CRUD con SQLite)
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/pacientes')
def pacientes_lista():
    termino    = request.args.get('q', '').strip()
    filtro_esp = request.args.get('especialidad', '').strip()

    if termino:
        filas = buscar_por_nombre(termino)
    elif filtro_esp:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM pacientes WHERE especialidad = ? ORDER BY apellido", (filtro_esp,))
        filas = cur.fetchall()
        conn.close()
    else:
        filas = obtener_todos()

    gestor.cargar_desde_db(obtener_todos())
    stats = {
        "total":          gestor.total(),
        "promedio_edad":  gestor.promedio_edad(),
        "especialidades": sorted(gestor.especialidades_activas()),
    }

    return render_template(
        'pacientes/lista.html',
        pacientes      = [dict(f) for f in filas],
        stats          = stats,
        termino        = termino,
        especialidades = ESPECIALIDADES,
        filtro_esp     = filtro_esp,
    )


@app.route('/pacientes/<int:id_paciente>')
def paciente_detalle(id_paciente):
    fila = obtener_por_id(id_paciente)
    if not fila:
        flash("Paciente no encontrado.", "error")
        return redirect(url_for('pacientes_lista'))
    return render_template('pacientes/detalle.html', paciente=dict(fila))


@app.route('/pacientes/nuevo', methods=['GET', 'POST'])
def paciente_nuevo():
    if request.method == 'POST':
        datos = {
            "nombre":        request.form['nombre'].strip().title(),
            "apellido":      request.form['apellido'].strip().title(),
            "edad":          int(request.form['edad']),
            "genero":        request.form['genero'],
            "telefono":      request.form['telefono'].strip(),
            "email":         request.form['email'].strip().lower(),
            "especialidad":  request.form['especialidad'],
            "observaciones": request.form.get('observaciones', '').strip(),
        }
        try:
            nuevo_id = insertar_paciente(datos)
            flash(f"✅ Paciente registrado correctamente (ID #{nuevo_id}).", "success")
            return redirect(url_for('pacientes_lista'))
        except Exception as e:
            flash(f"❌ Error al guardar: {e}", "error")
    return render_template(
        'pacientes/formulario.html',
        paciente=None, especialidades=ESPECIALIDADES, generos=GENEROS, accion="Registrar",
    )


@app.route('/pacientes/<int:id_paciente>/editar', methods=['GET', 'POST'])
def paciente_editar(id_paciente):
    fila = obtener_por_id(id_paciente)
    if not fila:
        flash("Paciente no encontrado.", "error")
        return redirect(url_for('pacientes_lista'))

    if request.method == 'POST':
        datos = {
            "nombre":        request.form['nombre'].strip().title(),
            "apellido":      request.form['apellido'].strip().title(),
            "edad":          int(request.form['edad']),
            "genero":        request.form['genero'],
            "telefono":      request.form['telefono'].strip(),
            "email":         request.form['email'].strip().lower(),
            "especialidad":  request.form['especialidad'],
            "observaciones": request.form.get('observaciones', '').strip(),
        }
        try:
            actualizar_paciente(id_paciente, datos)
            flash("✅ Paciente actualizado correctamente.", "success")
            return redirect(url_for('paciente_detalle', id_paciente=id_paciente))
        except Exception as e:
            flash(f"❌ Error al actualizar: {e}", "error")

    return render_template(
        'pacientes/formulario.html',
        paciente=dict(fila), especialidades=ESPECIALIDADES, generos=GENEROS, accion="Actualizar",
    )


@app.route('/pacientes/<int:id_paciente>/eliminar', methods=['POST'])
def paciente_eliminar(id_paciente):
    ok = eliminar_paciente(id_paciente)
    flash("🗑️ Paciente eliminado correctamente." if ok else "❌ No se encontró el paciente.",
          "success" if ok else "error")
    return redirect(url_for('pacientes_lista'))


@app.route('/pacientes/estadisticas')
def pacientes_estadisticas():
    return render_template('pacientes/estadisticas.html', stats=estadisticas())


# ─────────────────────────────────────────────────────────────────────────────
# RUTAS SEMANA 12 – INVENTARIO (TXT · JSON · CSV · SQLAlchemy)
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/datos')
def datos():
    datos_txt  = leer_txt()
    datos_json = leer_json()
    datos_csv  = leer_csv()
    datos_sql  = [m.to_dict() for m in MedicamentoDB.query.order_by(MedicamentoDB.nombre).all()]
    return render_template(
        'datos.html',
        datos_txt  = datos_txt,
        datos_json = datos_json,
        datos_csv  = datos_csv,
        datos_sql  = datos_sql,
        categorias = CATEGORIAS_MED,
    )


@app.route('/datos/guardar', methods=['POST'])
def datos_guardar():
    try:
        registro = {
            "nombre":      request.form['nombre'].strip().title(),
            "precio":      float(request.form['precio']),
            "cantidad":    int(request.form['cantidad']),
            "categoria":   request.form['categoria'],
            "descripcion": request.form.get('descripcion', '').strip(),
        }
        guardar_txt(registro)
        guardar_json(registro)
        guardar_csv(registro)
        flash("✅ Medicamento guardado en TXT, JSON y CSV.", "success")
    except Exception as e:
        flash(f"❌ Error al guardar archivos: {e}", "error")
    return redirect(url_for('datos'))


@app.route('/inventario/nuevo', methods=['GET', 'POST'])
def inventario_nuevo():
    if request.method == 'POST':
        try:
            med = MedicamentoDB(
                nombre      = request.form['nombre'].strip().title(),
                precio      = float(request.form['precio']),
                cantidad    = int(request.form['cantidad']),
                categoria   = request.form['categoria'],
                descripcion = request.form.get('descripcion', '').strip(),
            )
            db.session.add(med)
            db.session.commit()
            flash(f"✅ Medicamento '{med.nombre}' agregado (ID #{med.id}).", "success")
            return redirect(url_for('datos'))
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error: {e}", "error")
    return render_template('inventario_form.html', categorias=CATEGORIAS_MED, medicamento=None, accion="Agregar")


@app.route('/inventario/<int:id_med>/editar', methods=['GET', 'POST'])
def inventario_editar(id_med):
    med = MedicamentoDB.query.get_or_404(id_med)
    if request.method == 'POST':
        try:
            med.nombre      = request.form['nombre'].strip().title()
            med.precio      = float(request.form['precio'])
            med.cantidad    = int(request.form['cantidad'])
            med.categoria   = request.form['categoria']
            med.descripcion = request.form.get('descripcion', '').strip()
            db.session.commit()
            flash(f"✅ Medicamento '{med.nombre}' actualizado.", "success")
            return redirect(url_for('datos'))
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error: {e}", "error")
    return render_template('inventario_form.html', categorias=CATEGORIAS_MED, medicamento=med, accion="Actualizar")


@app.route('/inventario/<int:id_med>/eliminar', methods=['POST'])
def inventario_eliminar(id_med):
    med = MedicamentoDB.query.get_or_404(id_med)
    nombre = med.nombre
    try:
        db.session.delete(med)
        db.session.commit()
        flash(f"🗑️ Medicamento '{nombre}' eliminado.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error: {e}", "error")
    return redirect(url_for('datos'))


# ─────────────────────────────────────────────────────────────────────────────
# RUTAS SEMANA 13 – MySQL
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/mysql/estado')
def mysql_estado():
    resultado = probar_conexion()
    return render_template('mysql/estado.html', resultado=resultado)


# ── CRUD USUARIOS ─────────────────────────────────────────────────────────────

@app.route('/mysql/usuarios')
def mysql_usuarios():
    usuarios = usuario_obtener_todos()
    return render_template('mysql/usuarios.html', usuarios=usuarios)


@app.route('/mysql/usuarios/nuevo', methods=['GET', 'POST'])
def mysql_usuario_nuevo():
    if request.method == 'POST':
        try:
            usuario_insertar(
                nombre   = request.form['nombre'].strip().title(),
                mail     = request.form['mail'].strip().lower(),
                password = request.form['password'].strip(),
                rol      = request.form.get('rol', 'usuario'),
            )
            flash("✅ Usuario registrado en MySQL.", "success")
            return redirect(url_for('mysql_usuarios'))
        except Exception as e:
            flash(f"❌ Error: {e}", "error")
    return render_template('mysql/usuario_form.html', usuario=None, accion="Registrar")


@app.route('/mysql/usuarios/<int:id_usuario>/editar', methods=['GET', 'POST'])
def mysql_usuario_editar(id_usuario):
    usuario = usuario_obtener_por_id(id_usuario)
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for('mysql_usuarios'))
    if request.method == 'POST':
        try:
            usuario_actualizar(
                id_usuario = id_usuario,
                nombre     = request.form['nombre'].strip().title(),
                mail       = request.form['mail'].strip().lower(),
                rol        = request.form.get('rol', 'usuario'),
            )
            flash("✅ Usuario actualizado.", "success")
            return redirect(url_for('mysql_usuarios'))
        except Exception as e:
            flash(f"❌ Error: {e}", "error")
    return render_template('mysql/usuario_form.html', usuario=usuario, accion="Actualizar")


@app.route('/mysql/usuarios/<int:id_usuario>/eliminar', methods=['POST'])
def mysql_usuario_eliminar(id_usuario):
    ok = usuario_eliminar(id_usuario)
    flash("🗑️ Usuario eliminado." if ok else "❌ No encontrado.",
          "success" if ok else "error")
    return redirect(url_for('mysql_usuarios'))


# ── CRUD PACIENTES MySQL ──────────────────────────────────────────────────────

@app.route('/mysql/pacientes')
def mysql_pacientes():
    termino   = request.args.get('q', '').strip()
    pacientes = paciente_my_buscar(termino) if termino else paciente_my_obtener_todos()
    return render_template('mysql/pacientes.html', pacientes=pacientes, termino=termino,
                           especialidades=ESPECIALIDADES, generos=GENEROS)


@app.route('/mysql/pacientes/nuevo', methods=['GET', 'POST'])
def mysql_paciente_nuevo():
    if request.method == 'POST':
        try:
            datos = {
                "nombre":        request.form['nombre'].strip().title(),
                "apellido":      request.form['apellido'].strip().title(),
                "edad":          int(request.form['edad']),
                "genero":        request.form['genero'],
                "telefono":      request.form['telefono'].strip(),
                "email":         request.form['email'].strip().lower(),
                "especialidad":  request.form['especialidad'],
                "observaciones": request.form.get('observaciones', '').strip(),
            }
            paciente_my_insertar(datos)
            flash("✅ Paciente registrado en MySQL.", "success")
            return redirect(url_for('mysql_pacientes'))
        except Exception as e:
            flash(f"❌ Error: {e}", "error")
    return render_template('mysql/paciente_form.html', paciente=None,
                           especialidades=ESPECIALIDADES, generos=GENEROS, accion="Registrar")


@app.route('/mysql/pacientes/<int:id_paciente>/editar', methods=['GET', 'POST'])
def mysql_paciente_editar(id_paciente):
    paciente = paciente_my_obtener_por_id(id_paciente)
    if not paciente:
        flash("Paciente no encontrado.", "error")
        return redirect(url_for('mysql_pacientes'))
    if request.method == 'POST':
        try:
            datos = {
                "nombre":        request.form['nombre'].strip().title(),
                "apellido":      request.form['apellido'].strip().title(),
                "edad":          int(request.form['edad']),
                "genero":        request.form['genero'],
                "telefono":      request.form['telefono'].strip(),
                "email":         request.form['email'].strip().lower(),
                "especialidad":  request.form['especialidad'],
                "observaciones": request.form.get('observaciones', '').strip(),
            }
            paciente_my_actualizar(id_paciente, datos)
            flash("✅ Paciente actualizado en MySQL.", "success")
            return redirect(url_for('mysql_pacientes'))
        except Exception as e:
            flash(f"❌ Error: {e}", "error")
    return render_template('mysql/paciente_form.html', paciente=paciente,
                           especialidades=ESPECIALIDADES, generos=GENEROS, accion="Actualizar")


@app.route('/mysql/pacientes/<int:id_paciente>/eliminar', methods=['POST'])
def mysql_paciente_eliminar(id_paciente):
    ok = paciente_my_eliminar(id_paciente)
    flash("🗑️ Paciente eliminado de MySQL." if ok else "❌ No encontrado.",
          "success" if ok else "error")
    return redirect(url_for('mysql_pacientes'))


# ── CRUD MEDICAMENTOS MySQL ───────────────────────────────────────────────────

@app.route('/mysql/medicamentos')
def mysql_medicamentos():
    medicamentos = medicamento_my_obtener_todos()
    return render_template('mysql/medicamentos.html',
                           medicamentos=medicamentos, categorias=CATEGORIAS_MED)


@app.route('/mysql/medicamentos/nuevo', methods=['GET', 'POST'])
def mysql_medicamento_nuevo():
    if request.method == 'POST':
        try:
            datos = {
                "nombre":      request.form['nombre'].strip().title(),
                "precio":      float(request.form['precio']),
                "cantidad":    int(request.form['cantidad']),
                "categoria":   request.form['categoria'],
                "descripcion": request.form.get('descripcion', '').strip(),
            }
            medicamento_my_insertar(datos)
            flash("✅ Medicamento agregado a MySQL.", "success")
            return redirect(url_for('mysql_medicamentos'))
        except Exception as e:
            flash(f"❌ Error: {e}", "error")
    return render_template('mysql/medicamento_form.html',
                           medicamento=None, categorias=CATEGORIAS_MED, accion="Agregar")


@app.route('/mysql/medicamentos/<int:id_med>/editar', methods=['GET', 'POST'])
def mysql_medicamento_editar(id_med):
    med = medicamento_my_obtener_por_id(id_med)
    if not med:
        flash("Medicamento no encontrado.", "error")
        return redirect(url_for('mysql_medicamentos'))
    if request.method == 'POST':
        try:
            datos = {
                "nombre":      request.form['nombre'].strip().title(),
                "precio":      float(request.form['precio']),
                "cantidad":    int(request.form['cantidad']),
                "categoria":   request.form['categoria'],
                "descripcion": request.form.get('descripcion', '').strip(),
            }
            medicamento_my_actualizar(id_med, datos)
            flash("✅ Medicamento actualizado en MySQL.", "success")
            return redirect(url_for('mysql_medicamentos'))
        except Exception as e:
            flash(f"❌ Error: {e}", "error")
    return render_template('mysql/medicamento_form.html',
                           medicamento=med, categorias=CATEGORIAS_MED, accion="Actualizar")


@app.route('/mysql/medicamentos/<int:id_med>/eliminar', methods=['POST'])
def mysql_medicamento_eliminar(id_med):
    ok = medicamento_my_eliminar(id_med)
    flash("🗑️ Medicamento eliminado de MySQL." if ok else "❌ No encontrado.",
          "success" if ok else "error")
    return redirect(url_for('mysql_medicamentos'))


@app.route('/mysql/estadisticas')
def mysql_estadisticas():
    stats = estadisticas_mysql()
    return render_template('mysql/estadisticas.html', stats=stats)


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=False)
