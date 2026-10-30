
-- MPAZ RFID - Migracion 003
-- Seguimiento escolar y comunicacion interna.
-- No ejecutar directamente en produccion.

CREATE TABLE IF NOT EXISTS seguimiento_casos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    alumno_id INTEGER NOT NULL,
    sesion_clase_id INTEGER,

    curso TEXT NOT NULL,
    fecha_evento TEXT NOT NULL,

    tipo TEXT NOT NULL CHECK (
        tipo IN ('inasistencia', 'atraso', 'otro')
    ),

    estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (
        estado IN ('pendiente', 'en_gestion', 'resuelto')
    ),

    descripcion TEXT NOT NULL,

    creado_por_rol TEXT NOT NULL CHECK (
        creado_por_rol IN (
            'docente', 'administracion', 'direccion'
        )
    ),

    creado_por_usuario_id INTEGER,

    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TEXT,
    resuelto_en TEXT,

    FOREIGN KEY (alumno_id)
        REFERENCES alumnos(id),

    FOREIGN KEY (sesion_clase_id)
        REFERENCES sesiones_clase(id),

    FOREIGN KEY (creado_por_usuario_id)
        REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_seguimiento_alumno
    ON seguimiento_casos(alumno_id);

CREATE INDEX IF NOT EXISTS idx_seguimiento_estado
    ON seguimiento_casos(estado, fecha_evento);


CREATE TABLE IF NOT EXISTS seguimiento_mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    caso_id INTEGER NOT NULL,

    autor_rol TEXT NOT NULL CHECK (
        autor_rol IN (
            'docente', 'administracion', 'direccion'
        )
    ),

    autor_usuario_id INTEGER,

    mensaje TEXT NOT NULL CHECK (
        length(trim(mensaje)) BETWEEN 1 AND 1000
    ),

    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (caso_id)
        REFERENCES seguimiento_casos(id),

    FOREIGN KEY (autor_usuario_id)
        REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_seguimiento_mensajes_caso
    ON seguimiento_mensajes(caso_id, creado_en);


CREATE TABLE IF NOT EXISTS seguimiento_contactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    caso_id INTEGER NOT NULL,

    canal TEXT NOT NULL CHECK (
        canal IN (
            'telefonico', 'presencial', 'otro'
        )
    ),

    resultado TEXT NOT NULL,

    observacion TEXT,

    registrado_por_usuario_id INTEGER,

    fecha_contacto TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (caso_id)
        REFERENCES seguimiento_casos(id),

    FOREIGN KEY (registrado_por_usuario_id)
        REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_seguimiento_contactos_caso
    ON seguimiento_contactos(caso_id);


CREATE TABLE IF NOT EXISTS seguimiento_avisos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    caso_id INTEGER NOT NULL,

    destinatario_rol TEXT NOT NULL CHECK (
        destinatario_rol IN (
            'docente', 'administracion', 'direccion'
        )
    ),

    destinatario_usuario_id INTEGER,

    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    leido_en TEXT,

    FOREIGN KEY (caso_id)
        REFERENCES seguimiento_casos(id),

    FOREIGN KEY (destinatario_usuario_id)
        REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_seguimiento_avisos
    ON seguimiento_avisos(
        destinatario_rol,
        leido_en
    );
