# Esquema SQLite reproducido sin datos escolares

Origen: `base_datos.crear_tablas()` y migraciones SQL 001–004, ejecutadas únicamente sobre una base temporal vacía. No se inspeccionó la base de producción.

## alumnos

```sql
CREATE TABLE alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rut TEXT NOT NULL UNIQUE,
                nombre_completo TEXT NOT NULL,
                curso TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'activo',
                fecha_baja TEXT
            );
```

## asignaturas

```sql
CREATE TABLE asignaturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                estado TEXT NOT NULL DEFAULT 'activo'
                    CHECK (estado IN ('activo', 'inactivo'))
            );
```

## asistencias

```sql
CREATE TABLE asistencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumno_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,

                hora TEXT NOT NULL,
                totem_id INTEGER,
                evento_id TEXT,

                hora_entrada TEXT,
                hora_salida TEXT,
                tipo_salida TEXT,

                totem_entrada_id INTEGER,
                totem_salida_id INTEGER,

                evento_entrada_id TEXT,
                evento_salida_id TEXT,

                FOREIGN KEY (alumno_id)
                    REFERENCES alumnos(id),

                FOREIGN KEY (totem_id)
                    REFERENCES totems(id),

                FOREIGN KEY (totem_entrada_id)
                    REFERENCES totems(id),

                FOREIGN KEY (totem_salida_id)
                    REFERENCES totems(id)
            );
```

## asistencias_clase

```sql
CREATE TABLE asistencias_clase (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                sesion_clase_id INTEGER NOT NULL,

                alumno_id INTEGER NOT NULL,

                estado TEXT NOT NULL
                    CHECK (
                        estado IN (
                            'presente',
                            'atrasado',
                            'no_presente'
                        )
                    ),

                observacion TEXT,

                fecha_registro TEXT NOT NULL
                    DEFAULT (datetime('now')),

                FOREIGN KEY (sesion_clase_id)
                    REFERENCES sesiones_clase(id),

                FOREIGN KEY (alumno_id)
                    REFERENCES alumnos(id),

                UNIQUE (sesion_clase_id, alumno_id)
            );
```

## calendario_auditoria

```sql
CREATE TABLE calendario_auditoria (
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
```

## calendario_eventos

```sql
CREATE TABLE calendario_eventos (
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
```

## calendario_jornadas

```sql
CREATE TABLE calendario_jornadas (
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
```

## profesores_cursos

```sql
CREATE TABLE profesores_cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profesor_id INTEGER NOT NULL,
                curso TEXT NOT NULL,
                asignatura_id INTEGER NOT NULL,
                estado TEXT NOT NULL DEFAULT 'activo'
                    CHECK (estado IN ('activo', 'inactivo')),

                FOREIGN KEY (profesor_id)
                    REFERENCES usuarios(id),

                FOREIGN KEY (asignatura_id)
                    REFERENCES asignaturas(id),

                UNIQUE (profesor_id, curso, asignatura_id)
            );
```

## seguimiento_avisos

```sql
CREATE TABLE seguimiento_avisos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    caso_id INTEGER NOT NULL,

    destinatario_rol TEXT NOT NULL CHECK (
        destinatario_rol IN (
            'docente', 'administracion', 'direccion'
        )
    ),

    destinatario_usuario_id INTEGER,

    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    leido_en TEXT, destinatario_operador_id INTEGER
REFERENCES seguimiento_operadores(id),

    FOREIGN KEY (caso_id)
        REFERENCES seguimiento_casos(id),

    FOREIGN KEY (destinatario_usuario_id)
        REFERENCES usuarios(id)
);
```

## seguimiento_casos

```sql
CREATE TABLE seguimiento_casos (
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
    resuelto_en TEXT, creado_por_operador_id INTEGER
REFERENCES seguimiento_operadores(id),

    FOREIGN KEY (alumno_id)
        REFERENCES alumnos(id),

    FOREIGN KEY (sesion_clase_id)
        REFERENCES sesiones_clase(id),

    FOREIGN KEY (creado_por_usuario_id)
        REFERENCES usuarios(id)
);
```

## seguimiento_contactos

```sql
CREATE TABLE seguimiento_contactos (
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
        DEFAULT CURRENT_TIMESTAMP, registrado_por_operador_id INTEGER
REFERENCES seguimiento_operadores(id),

    FOREIGN KEY (caso_id)
        REFERENCES seguimiento_casos(id),

    FOREIGN KEY (registrado_por_usuario_id)
        REFERENCES usuarios(id)
);
```

## seguimiento_mensajes

```sql
CREATE TABLE seguimiento_mensajes (
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

    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, autor_operador_id INTEGER
REFERENCES seguimiento_operadores(id),

    FOREIGN KEY (caso_id)
        REFERENCES seguimiento_casos(id),

    FOREIGN KEY (autor_usuario_id)
        REFERENCES usuarios(id)
);
```

## seguimiento_operadores

```sql
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
```

## sesiones_clase

```sql
CREATE TABLE sesiones_clase (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                asignacion_id INTEGER NOT NULL,

                fecha TEXT NOT NULL,

                hora_inicio TEXT NOT NULL,

                modalidad TEXT NOT NULL DEFAULT 'por_clase'
                    CHECK (modalidad IN ('por_clase', 'diaria')),

                estado TEXT NOT NULL DEFAULT 'borrador'
                    CHECK (estado IN ('borrador', 'confirmada', 'anulada')),

                fecha_creacion TEXT NOT NULL
                    DEFAULT (datetime('now')),

                fecha_confirmacion TEXT,

                FOREIGN KEY (asignacion_id)
                    REFERENCES profesores_cursos(id),

                UNIQUE (
                    asignacion_id,
                    fecha,
                    modalidad,
                    hora_inicio
                )
            );
```

## tarjetas

```sql
CREATE TABLE tarjetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                alumno_id INTEGER,

                uid TEXT NOT NULL UNIQUE,

                estado TEXT NOT NULL
                DEFAULT 'disponible',

                fecha_registro TEXT NOT NULL,

                fecha_asignacion TEXT,

                fecha_bloqueo TEXT,

                fecha_extravio TEXT,

                FOREIGN KEY (alumno_id)
                    REFERENCES alumnos(id)
            );
```

## totems

```sql
CREATE TABLE totems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                ubicacion TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'activo',
                fecha_registro TEXT NOT NULL,
                ultima_conexion TEXT
            );
```

## usuarios

```sql
CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nombre_completo TEXT NOT NULL,

                usuario TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                rol TEXT NOT NULL
                    CHECK (rol IN ('administrador', 'profesor')),

                estado TEXT NOT NULL DEFAULT 'activo'
                    CHECK (estado IN ('activo', 'inactivo')),

                fecha_creacion TEXT NOT NULL
            );
```

## Índices explícitos

```sql
CREATE INDEX idx_calendario_auditoria_fecha
ON calendario_auditoria(registrado_en);
CREATE INDEX idx_calendario_auditoria_jornada
ON calendario_auditoria(jornada_id);
CREATE INDEX idx_calendario_eventos_fecha
ON calendario_eventos(fecha);
CREATE INDEX idx_calendario_jornada_fecha
ON calendario_jornadas(fecha);
CREATE UNIQUE INDEX idx_calendario_jornada_fecha_curso
ON calendario_jornadas (
    fecha,
    COALESCE(curso, '')
);
CREATE INDEX idx_seguimiento_alumno
    ON seguimiento_casos(alumno_id);
CREATE INDEX idx_seguimiento_avisos
    ON seguimiento_avisos(
        destinatario_rol,
        leido_en
    );
CREATE INDEX idx_seguimiento_contactos_caso
    ON seguimiento_contactos(caso_id);
CREATE INDEX idx_seguimiento_estado
    ON seguimiento_casos(estado, fecha_evento);
CREATE INDEX idx_seguimiento_mensajes_caso
    ON seguimiento_mensajes(caso_id, creado_en);
CREATE INDEX idx_seguimiento_operadores_rol
ON seguimiento_operadores(rol, estado);
CREATE UNIQUE INDEX indice_alumno_fecha_asistencias
            ON asistencias(alumno_id, fecha)
            ;
CREATE INDEX indice_asistencias_clase_alumno
            ON asistencias_clase(alumno_id)
            ;
CREATE UNIQUE INDEX indice_evento_entrada_asistencias
            ON asistencias(evento_entrada_id)
            ;
CREATE UNIQUE INDEX indice_evento_id_asistencias
            ON asistencias(evento_id)
            ;
CREATE UNIQUE INDEX indice_evento_salida_asistencias
            ON asistencias(evento_salida_id)
            ;
CREATE INDEX indice_sesiones_clase_fecha
            ON sesiones_clase(fecha, estado)
            ;
```

## Observaciones

- `obtener_conexion()` activa llaves foráneas por conexión. No configura WAL ni zona horaria.
- Una jornada RFID por alumno/fecha; tres índices únicos de eventos y comprobación cruzada bajo `BEGIN IMMEDIATE`.
- No existe un índice parcial que impida dos tarjetas activas por alumno; varias comprobaciones están en código. Requiere prueba de carrera antes de proponer migración.
- Las migraciones 001–003 usan CREATE IF NOT EXISTS; 004 contiene CREATE y ALTER no repetibles. No hay tabla de versiones ni ejecutor transaccional central.
- Los scripts históricos `migrar_*.py`/`agregar_*.py` no equivalen a un historial automático: algunos modifican estructura o ejecutan acciones al importarse. No importarlos en pruebas ni aplicarlos indiscriminadamente.
- `migrar_alumnos_sin_uid.py` reconstruye una tabla: exige revisión y autorización fuera del entorno de pruebas.

## Continuación: migración 005 (solo desarrollo hasta autorización)

Añade `web_login_intentos` (clave HMAC primaria, cantidad, expira) y `web_sesiones` (HMAC de token primaria, tipo, identidad_id, firma de credencial/rol, creada, actividad, expira), con índices por expiración. DDL exacto en `migraciones/005_seguridad_web.sql`; transaccional y repetible. No hay modificación de tablas anteriores ni de registros escolares.

La identidad es polimórfica (operador o docente); se valida contra la tabla y rol correspondientes en código, no mediante una llave foránea única. La falta de tablas se rechaza; no hay creación automática ni fallback inseguro. El registro de migraciones general sigue pendiente. Los tiempos de estas dos tablas son epoch UTC y no horas civiles escolares.
