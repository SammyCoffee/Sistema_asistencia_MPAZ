# Sesiones docentes y consulta administrativa

Estado documental: describe el código de la rama \`feature/paso68h-sesiones-docentes-admin\`, consultado el 26-11-2026. No representa una certificación de producción ni acredita una ejecución visual reciente.

## Propósito y separación de registros

El módulo permite que cada docente gestione la asistencia de sus clases y que Administración consulte un resumen institucional de las sesiones. La autorización se aplica en el servidor: el navegador no decide a qué cursos o sesiones puede acceder una cuenta.

Hay dos registros distintos:

- **Asistencia de entrada/salida RFID:** tabla \`asistencias\`, alimentada por las lecturas del tótem.
- **Asistencia de aula:** tablas \`sesiones_clase\` y \`asistencias_clase\`, gestionadas desde el portal docente.

Las funciones de sesión docente declaran que no modifican las asistencias RFID. Las pruebas del flujo comparan la tabla \`asistencias\` antes y después para verificar que permanezca intacta. Una marca de entrada al establecimiento no sustituye la verificación de asistencia a una clase.

## Flujo de trabajo docente

1. **Ingreso:** el profesor inicia sesión en \`/profesor/login\`. La API valida una cuenta activa con rol \`profesor\`.
2. **Asignación:** el portal consulta \`/profesor/asignaciones\` y muestra las asignaciones activas del profesor autenticado (curso y asignatura).
3. **Crear o recuperar sesión:** el docente elige una asignación, fecha y hora de inicio. \`POST /profesor/sesiones\` crea una sesión \`borrador\`. Si ya existe la misma combinación única, la API devuelve la sesión existente para evitar duplicarla.
4. **Consultar nómina:** el portal carga el detalle de la sesión. En un borrador se consideran los estudiantes activos del curso asignado.
5. **Registrar marcas:** el docente registra para cada estudiante uno de estos estados:
   - \`presente\`
   - \`atrasado\`
   - \`no_presente\`
   
   La observación es opcional y admite hasta 500 caracteres. Una persona sin marca se presenta como \`sin_verificar\`; no se convierte automáticamente en ausente.
6. **Revisar pendientes:** la pantalla informa cuántos estudiantes siguen sin estado registrado. La API también valida la integridad de la nómina y la asignación antes de guardar.
7. **Confirmar:** \`POST /profesor/sesiones/{sesion_id}/confirmar\` confirma la sesión solo cuando todos los estudiantes activos del curso tienen una marca. Si falta alguna, responde \`409 asistencia_incompleta\`; si el curso no tiene estudiantes activos, responde \`409 curso_sin_alumnos\`.
8. **Historial:** la sesión confirmada queda bloqueada para modificaciones ordinarias. El detalle histórico conserva las marcas guardadas, incluso si posteriormente un estudiante cambia de curso o la asignación deja de estar activa.

## Estados

| Elemento | Estados | Significado |
|---|---|---|
| Sesión | \`borrador\` | En preparación; admite marcas mientras la asignación y el profesor sigan autorizados. |
| Sesión | \`confirmada\` | Cierre realizado; las marcas no admiten edición ordinaria. |
| Sesión | \`anulada\` | Estado contemplado en el esquema y en los filtros administrativos. No se encontró una ruta API de anulación en esta rama. |
| Marca de aula | \`presente\` | Estudiante presente en la clase. |
| Marca de aula | \`atrasado\` | Estudiante llegó atrasado. |
| Marca de aula | \`no_presente\` | Docente registró que no estuvo presente. |
| Vista docente | \`sin_verificar\` | No existe una marca guardada para ese estudiante en el borrador. No equivale a ausencia. |

## Permisos y rutas

### Portal docente

Las rutas docentes requieren una sesión de profesor activa. Las operaciones POST de escritura requieren además el token CSRF del dominio docente en la cabecera \`X-CSRF-Token\`.

| Método | Ruta | Uso |
|---|---|---|
| GET | \`/profesor/asignaciones\` | Consultar las asignaciones activas del profesor. |
| GET | \`/profesor/asignaciones/{asignacion_id}/sesiones\` | Consultar las sesiones de una asignación autorizada. |
| POST | \`/profesor/sesiones\` | Crear o recuperar una sesión. |
| GET | \`/profesor/sesiones/{sesion_id}\` | Consultar sesión y marcas de aula. |
| POST | \`/profesor/sesiones/{sesion_id}/asistencia\` | Registrar o corregir una marca mientras está en borrador. |
| POST | \`/profesor/sesiones/{sesion_id}/confirmar\` | Confirmar la sesión cuando no quedan pendientes. |

La API verifica en el servidor que la asignación, sesión y estudiante pertenezcan al ámbito autorizado del profesor. Cambiar identificadores en una petición no amplía los permisos.

### Consulta administrativa

El módulo \`sesiones_administracion.py\` registra un blueprint de solo consulta. Requiere operador activo de rol \`administracion\` y \`panel_autorizado = true\`. Dirección no obtiene acceso a este módulo.

| Método | Ruta | Uso |
|---|---|---|
| GET | \`/panel/sesiones-docentes\` | Listar y filtrar sesiones. |
| GET | \`/panel/sesiones-docentes/{sesion_id}\` | Consultar el resumen de una sesión. |

Filtros admitidos en el listado:

- \`fecha\`: fecha ISO \`AAAA-MM-DD\`.
- \`curso\`: máximo 20 caracteres.
- \`asignatura\`: máximo 100 caracteres.
- \`estado\`: \`borrador\`, \`confirmada\` o \`anulada\`.
- \`pagina\`: entero entre 1 y 1.000.000.

La paginación devuelve hasta 50 sesiones por página. La respuesta administrativa resume curso, asignatura, docente, fecha, estado y cantidades de presentes, atrasados, no presentes y pendientes. El detalle administrativo no devuelve nombres de estudiantes ni observaciones individuales. Las consultas activan \`PRAGMA query_only = ON\` y las respuestas llevan \`Cache-Control: no-store\`.

## Tablas y relaciones

- \`sesiones_clase\`: sesión asociada a una asignación de profesor/curso/asignatura, fecha, hora de inicio, modalidad y estado.
- \`asistencias_clase\`: una marca por estudiante y sesión, con estado, observación opcional y fecha de registro. La combinación \`(sesion_clase_id, alumno_id)\` es única.
- \`profesores_cursos\`: vincula profesor, curso y asignatura; la asignación debe estar activa.
- \`alumnos\`: la nómina de un borrador se calcula con estudiantes activos del curso asignado.

La estructura de estas tablas está documentada en [BASE_DATOS.md](BASE_DATOS.md). El esquema de sesiones procede de la migración 004; la migración 005 corresponde a seguridad web persistente, no a la creación de estas sesiones.

## Pruebas disponibles y límites de evidencia

- \`tests/test_sesiones_docentes.py\`: tres métodos de prueba para permisos, creación, marcas, confirmación, historial y consulta administrativa, usando fixtures ficticios.
- \`tests/test_permisos_crud.py\`: incluye pruebas de acceso indebido a asignaciones, sesiones y estudiantes de otros cursos.
- \`tests/navegador_paso65.py\`: automatización Chromium disponible para recorrer el flujo docente y administrativo, fallos de red/reintentos, filtros y detalle, expiración de sesión y conservación de la tabla RFID.

La automatización Chromium requiere \`/usr/bin/chromium\`, \`chromedriver\` disponible en PATH y el puerto local 9515 libre. Se ejecuta con una carpeta de salida nueva:

\`\`\`bash
.venv/bin/python tests/navegador_paso65.py /tmp/mpaz-capturas-sesiones
\`\`\`

La existencia del script no significa que se haya ejecutado. Al preparar esta documentación no se encontró un resultado de ejecución posterior al commit de integración ni una ejecución de GitHub Actions para ese commit. La matriz visual de escritorio, tablet, móvil, teclado y contraste sigue pendiente según [QA_MANUAL.md](QA_MANUAL.md).

## Límites conocidos

- No existe en esta rama una ruta API para anular una sesión.
- La confirmación bloquea la edición ordinaria; cualquier rectificación posterior requiere un procedimiento institucional definido, no una modificación directa de SQLite.
- La vista administrativa es un resumen y no reemplaza una ficha individual ni entrega observaciones de estudiantes.
- No hay una especificación OpenAPI completa para todos los endpoints.
- No se ha desplegado ni validado este módulo contra datos reales o el servidor escolar.
