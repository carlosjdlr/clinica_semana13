-- ============================================================
-- ClínicaSalud - Base de datos MySQL
-- Semana 13
-- ============================================================
-- INSTRUCCIONES:
-- 1. Copia todo este contenido
-- 2. En MySQL Workbench abre una nueva pestaña (Ctrl+T)
-- 3. Pega el contenido
-- 4. Presiona el rayo (Execute All) o Ctrl+Shift+Enter
-- ============================================================

CREATE DATABASE IF NOT EXISTS clinica_salud_mysql;

USE clinica_salud_mysql;

-- ── Tabla USUARIOS ────────────────────────────────────────────
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    mail       VARCHAR(150) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,
    rol        VARCHAR(30) NOT NULL DEFAULT 'usuario',
    creado_en  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Tabla PACIENTES ───────────────────────────────────────────
DROP TABLE IF EXISTS pacientes_my;
CREATE TABLE pacientes_my (
    id_paciente   INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(80) NOT NULL,
    apellido      VARCHAR(80) NOT NULL,
    edad          INT NOT NULL,
    genero        VARCHAR(20) NOT NULL,
    telefono      VARCHAR(20) NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    especialidad  VARCHAR(50) NOT NULL,
    observaciones TEXT,
    registrado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Tabla MEDICAMENTOS ────────────────────────────────────────
DROP TABLE IF EXISTS medicamentos_my;
CREATE TABLE medicamentos_my (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    precio      DECIMAL(8,2) NOT NULL,
    cantidad    INT NOT NULL DEFAULT 0,
    categoria   VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- ── Datos de prueba: USUARIOS ─────────────────────────────────
INSERT INTO usuarios (nombre, mail, password, rol) VALUES
('Admin Sistema',   'admin@clinica.com',     'admin123',  'admin'),
('Recepcionista 1', 'recep1@clinica.com',    'recep123',  'recepcionista'),
('Dr. Carlos M.',   'c.mendoza@clinica.com', 'medico123', 'medico'),
('Dra. Ana Torres', 'a.torres@clinica.com',  'medico456', 'medico');

-- ── Datos de prueba: PACIENTES ────────────────────────────────
INSERT INTO pacientes_my (nombre, apellido, edad, genero, telefono, email, especialidad, observaciones) VALUES
('Carlos',  'Mendoza',  45, 'Masculino', '0991234567', 'c.mendoza@email.com',  'Cardiologia',   'Hipertension arterial'),
('Ana',     'Torres',   32, 'Femenino',  '0987654321', 'ana.torres@email.com', 'Neurologia',    'Migrana cronica'),
('Luis',    'Ramirez',  8,  'Masculino', '0976543210', 'l.ramirez@email.com',  'Pediatria',     'Control de crecimiento'),
('Maria',   'Gonzalez', 29, 'Femenino',  '0965432109', 'm.gonzalez@email.com', 'Dermatologia',  'Acne severo'),
('Jorge',   'Castro',   55, 'Masculino', '0954321098', 'j.castro@email.com',   'Traumatologia', 'Fractura de muneca'),
('Patricia','Rojas',    41, 'Femenino',  '0943210987', 'p.rojas@email.com',    'Oftalmologia',  'Miopia progresiva');

-- ── Datos de prueba: MEDICAMENTOS ─────────────────────────────
INSERT INTO medicamentos_my (nombre, precio, cantidad, categoria, descripcion) VALUES
('Ibuprofeno 400mg',  2.50, 150, 'Analgesico',      'Analgesico y antiinflamatorio'),
('Amoxicilina 500mg', 5.80,  80, 'Antibiotico',     'Tratamiento de infecciones bacterianas'),
('Loratadina 10mg',   3.20,  60, 'Antihistaminico', 'Alergia y rinitis alergica'),
('Enalapril 10mg',    4.00, 100, 'Antihipertensivo','Control de presion arterial'),
('Vitamina C 500mg',  1.90, 200, 'Vitaminas',       'Suplemento vitaminico');

-- ── Verificar resultados ──────────────────────────────────────
SELECT 'usuarios'        AS tabla, COUNT(*) AS total FROM usuarios
UNION ALL
SELECT 'pacientes_my',   COUNT(*) FROM pacientes_my
UNION ALL
SELECT 'medicamentos_my', COUNT(*) FROM medicamentos_my;
