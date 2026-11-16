# Continuidad y propuesta evolutiva

## Orden de trabajo

1. P0: revisión privada de los seis respaldos SQLite ya versionados. Determinar si contienen información personal, quién puede descargarla y si hubo exposición. No asumir filtración sin evidencia. Si procede, acordar saneamiento y acceso del repositorio; no reescribir historia ni eliminar copias automáticamente.
2. P0/P1: ampliar revisión de todos los sumideros `innerHTML` y probar entradas históricas/importadas; corregida la ficha, quedan otros renderizadores por revisar. Revisar sesiones y abuso de login con pruebas de carga en desarrollo.
3. P1: limitación de intentos de login compatible con varios workers, revocación de cookies robadas, respuesta uniforme ante SQLite bloqueado/no disponible y límites de tamaño/longitud en la API.
4. P1: reglas de calendario e inasistencias, cierre de entradas posteriores a las 17:00, tiempo explícito Chile/DST, carrera entre bloqueo y registro RFID y retardo de eventos offline. Requieren definición institucional cuando cambien el significado de asistencia.
5. P1: runner de migraciones versionado, restauración ensayada, observabilidad y CI Python 3.12; matriz completa de CRUD/IDOR/exportaciones y QA visual.
6. P2: modularización gradual, integración MPAZ Web y evaluación PostgreSQL. Matrícula, notas, notificaciones y analítica requieren propuestas separadas; no son funcionalidades entregadas por esta auditoría.

La durabilidad básica de la cola JSON ya se corrigió y probó (corrupción, reemplazo interrumpido, hilos/procesos y reenvío sin perder altas nuevas). No se cambió la fecha de los eventos retardados ni se implementó firmware offline.

## PostgreSQL: propuesta, no migración ejecutada

Ventajas esperadas: coordinación de escrituras concurrentes, administración central, tipos y restricciones más fuertes, respaldos y recuperación gestionados. Costes: nuevo servicio, credenciales, monitorización, parches, almacenamiento, políticas de acceso y recuperación. No reemplaza controles de sesión, validaciones ni pruebas de permisos.

Impacto de código identificado:

- `base_datos.obtener_conexion` y todos los módulos con SQL SQLite; placeholders `?`, `lastrowid`, acceso por posición y excepciones `sqlite3`.
- DDL: `AUTOINCREMENT`, `PRAGMA`, afinidad de tipos, índices de expresión, collation NOCASE y ALTER de migración 004.
- Fechas: `datetime('now')`, `CURRENT_TIMESTAMP`, `date.today()` y valores TEXT deben mapearse con semántica explícita (hora Chile frente a instante UTC).
- Bloqueos `BEGIN IMMEDIATE`: rediseñar aislamiento y unicidad de eventos; no traducir literalmente a transacciones que admitan carreras.
- `ON CONFLICT`, inserciones con retorno de ID y claves foráneas; preservar IDs y referencias de alumnos, tarjetas, sesiones y seguimiento.
- Respaldos: API `Connection.backup` deja de aplicar; definir herramientas PostgreSQL y restauración compatible con el RPO/RTO acordado.

Plan por puertas de validación:

1. Construir interfaz de persistencia y pruebas de contrato sin cambiar reglas funcionales. Preparar PostgreSQL exclusivamente en desarrollo, con datos generados.
2. Crear esquema equivalente mediante migraciones revisadas; definir encoding, timezone, normalización RUT/UID y catálogo de roles. Estimar esfuerzo tras inventario de consultas, no ofrecer fecha sin medir.
3. Transformar dataset ficticio, preservar IDs y avanzar secuencias. Comparar conteos, unicidad, llaves foráneas, checksums normalizados y resultados de API en ambos motores.
4. Ejecutar concurrencia con múltiples workers, reintentos/eventos duplicados, cortes de red, rollback transaccional, permisos, exportaciones y límites de fechas/DST. Medir carga representativa, bloqueo, latencia y uso de recursos.
5. Ensayar respaldo/restauración y retorno a SQLite en entorno ficticio. Preferir corte de escrituras controlado; no introducir doble escritura sin diseño de reconciliación.
6. Solo tras autorización: plan privado de traslado de datos, ventana, responsables, respaldo verificado, reconciliación final y criterio de abortar. Mantener SQLite preservado durante la ventana de reversión.

No se instalaron drivers ni servicios PostgreSQL, ni se copiaron datos de producción.

## Estado actualizado de la continuación

Se implementaron y probaron límites persistentes de login, sesiones revocables, principales sumideros HTML dinámicos y reloj Chile explícito. Python 3.12 ya fue validado. No repetir esas tareas como pendientes de implementación; quedan revisión operativa/carga, QA visual y despliegue autorizado. Las reglas del calendario permanecen sin cambiar: ver CALENDARIO_DECISIONES.md. Incorporar las tablas de seguridad 005 al alcance de una futura migración PostgreSQL. La clasificación personal de respaldos antiguos continúa pendiente, sin bloquear desarrollo aislado.
