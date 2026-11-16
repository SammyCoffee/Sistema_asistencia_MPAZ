-- Aditiva. Aplicar solo tras respaldo/revisión, nunca automáticamente al iniciar Flask.
-- No modifica alumnos, asistencia, contraseñas ni permisos existentes.
BEGIN IMMEDIATE;

CREATE TABLE IF NOT EXISTS web_login_intentos (
    clave TEXT PRIMARY KEY,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    expira REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_web_intentos_expira ON web_login_intentos(expira);
CREATE TABLE IF NOT EXISTS web_sesiones (
    token_hash TEXT PRIMARY KEY,
    tipo TEXT NOT NULL CHECK (tipo IN ('operador', 'docente')),
    identidad_id INTEGER NOT NULL,
    credencial_firma TEXT NOT NULL,
    creada REAL NOT NULL,
    actividad REAL NOT NULL,
    expira REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_web_sesiones_expira ON web_sesiones(expira);

COMMIT;
