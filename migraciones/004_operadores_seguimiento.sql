
-- MPAZ RFID - Migracion 004
-- Cuentas individuales de seguimiento escolar.
-- No ejecutar directamente sobre produccion.

CREATE TABLE seguimiento_operadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo TEXT NOT NULL,
    usuario TEXT NOT NULL COLLATE NOCASE UNIQUE,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (
        rol IN ('administracion', 'direccion')
    ),
    estado TEXT NOT NULL DEFAULT 'activo'
        CHECK (estado IN ('activo', 'inactivo')),
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE seguimiento_casos
ADD COLUMN creado_por_operador_id INTEGER
REFERENCES seguimiento_operadores(id);

ALTER TABLE seguimiento_mensajes
ADD COLUMN autor_operador_id INTEGER
REFERENCES seguimiento_operadores(id);

ALTER TABLE seguimiento_contactos
ADD COLUMN registrado_por_operador_id INTEGER
REFERENCES seguimiento_operadores(id);

ALTER TABLE seguimiento_avisos
ADD COLUMN destinatario_operador_id INTEGER
REFERENCES seguimiento_operadores(id);

CREATE INDEX idx_seguimiento_operadores_rol
ON seguimiento_operadores(rol, estado);
