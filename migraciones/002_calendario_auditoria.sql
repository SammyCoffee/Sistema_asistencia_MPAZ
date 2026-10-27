
-- MPAZ RFID - Migracion 002
-- Historial de cambios del calendario escolar.
-- NO ejecutar directamente en produccion.

CREATE TABLE IF NOT EXISTS calendario_auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    jornada_id INTEGER NOT NULL
        REFERENCES calendario_jornadas(id),

    accion TEXT NOT NULL CHECK (
        accion IN ('crear', 'editar')
    ),

    valor_anterior TEXT,
    valor_nuevo TEXT NOT NULL,

    actor TEXT NOT NULL
        DEFAULT 'panel_administrativo',

    registrado_en TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_calendario_auditoria_jornada
ON calendario_auditoria(jornada_id);

CREATE INDEX IF NOT EXISTS idx_calendario_auditoria_fecha
ON calendario_auditoria(registrado_en);
