
-- MPAZ RFID - Calendario escolar
-- Migracion 001
-- No ejecutar directamente sobre produccion.

CREATE TABLE IF NOT EXISTS calendario_jornadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT NOT NULL,

    -- NULL significa toda la escuela.
    curso TEXT,

    condicion TEXT NOT NULL CHECK (
        condicion IN (
            'lectiva',
            'suspendida',
            'feriado',
            'reducida',
            'horario_especial'
        )
    ),

    hora_entrada TEXT,
    hora_salida TEXT,

    motivo TEXT NOT NULL,

    origen_registro TEXT NOT NULL
        DEFAULT 'panel_administrativo',

    creado_en TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    actualizado_en TEXT
);

-- Una configuracion por fecha y alcance.
-- COALESCE permite identificar el alcance general
-- aunque el curso sea NULL.

CREATE UNIQUE INDEX IF NOT EXISTS
    idx_calendario_jornada_fecha_curso
ON calendario_jornadas (
    fecha,
    COALESCE(curso, '')
);

CREATE INDEX IF NOT EXISTS
    idx_calendario_jornada_fecha
ON calendario_jornadas(fecha);


-- Actividades que no alteran por si mismas
-- las jornadas ni los calculos de asistencia.

CREATE TABLE IF NOT EXISTS calendario_eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT NOT NULL,

    -- NULL significa toda la escuela.
    curso TEXT,

    titulo TEXT NOT NULL,
    descripcion TEXT,

    tipo TEXT NOT NULL DEFAULT 'informativo'
        CHECK (
            tipo IN (
                'informativo',
                'actividad'
            )
        ),

    origen_registro TEXT NOT NULL
        DEFAULT 'panel_administrativo',

    creado_en TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS
    idx_calendario_eventos_fecha
ON calendario_eventos(fecha);
