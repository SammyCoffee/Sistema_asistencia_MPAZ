# Continuación de auditoría — 16-11-2026

## A. Correcciones realizadas

Se retomó `audit/seguridad-continuidad-20261116` desde `f894ac8`, con árbol limpio. Se localizaron y revisaron `20e404c` y `f894ac8`, el informe, operación y las pruebas existentes. No había cambios posteriores que preservar. No se repitió el inventario completo ni se accedió al servidor escolar.

Las 29 pruebas originales y la prueba JS se conservaron y validaron. La batería ampliada contiene **61 métodos Python**, incluidos **cinco de caracterización de defectos institucionales aún no corregidos**, y tres programas de prueba JavaScript.

| Implementado | Archivos principales | Evidencia |
|---|---|---|
| Límite de intentos compartido entre workers | `seguridad_web.py`, migración 005, logins API/Seguimiento | 429, recuperación a los 300 s, ambos accesos de operadores, docentes, rotación de usuario y tres procesos |
| Sesión persistente y revocación | Mismos módulos | Cookie copiada válida antes de logout, rechazada después; contraseña cambiada, expiración absoluta/inactividad, nuevo login, Dirección inactiva |
| Comprobación de credencial vigente al emitir sesión | `seguridad_web.py` y logins | Contraseña rotada entre autenticación y emisión: 401, no sesión nueva válida |
| Renderizado dinámico seguro | `dom-seguro.js`, `app.js`, HTML | Nodos de texto/dataset; se conservó escape de ficha y HTML constante seguro |
| Comparación robusta de tokens y JSON anidado | API, seguimiento y seguridad | Unicode indebido → 401/403; canal/estado con listas → 400, sin TypeError |
| Hora Chile explícita | `reloj_escolar.py`, backend y JS | DST abril/septiembre, cambio de fecha UTC→Chile, frontend bajo UTC/Tokio |
| Auditoría individual del calendario | `calendario_administracion.py`, API | Actor `operador:<id>` en cambios nuevos; habilitación y CSRF conservados |
| Timeout de reenvío | `reenviar_pendientes.py` | Timeout de 10 s controlado; evento permanece en cola |
| Vista previa ficticia reproducible | `herramientas/vista_previa_auditoria.py` | Fixture temporal; procedimiento manual, sin resultado visual inventado |

La migración 005 es aditiva, transaccional y repetible; añade dos tablas e índices. No altera alumnos, tarjetas, asistencias, contraseñas ni roles. Solo se ejecutó en bases temporales. No hay migración automática al iniciar Flask.

Se ajustaron dos pruebas previas para conservar su intención: el reloj se inyecta en el helper explícito y el rechazo de RUT ahora envía el campo `nombre` correcto y comprueba `rut_invalido`, en vez de aceptar cualquier 400 por campos faltantes. El reproductor histórico queda fijado a la suite de 20e404c; no se mezclan pruebas nuevas con dependencias inexistentes en d0d2c80.

## Revisión privada de las seis bases históricas

Autorizada en esta continuación; se abrieron solo archivos **locales ya versionados** mediante SQLite `mode=ro&immutable=1` y `query_only`. No se imprimieron nombres, RUT, UID ni muestras de registros. No se copiaron archivos de producción ni se modificaron estas bases.

| Archivos | Origen Git / estructura | Clasificación sustentada |
|---|---|---|
| `asistencia_respaldo.db` | Añadido en `028e585`, 13-07-2026; tablas antiguas alumnos/asistencia/asistencias | Respaldo histórico de desarrollo; 3 alumnos y pocos registros |
| `asistencia_respaldo_sin_uid20260716_112800.db` | Añadido en `f1e32b9`, 16-07-2026; todavía contiene columna UID antigua y tabla tarjetas | Copia previa a migración histórica; 3 alumnos, 4 tarjetas |
| Cuatro `asistencia_respaldo_tarjetas_*.db` | Añadidos en `3d60d27`, 15-07-2026; misma huella SHA-256 entre los cuatro; tarjetas vacía | Respaldos históricos idénticos previos a cambios de tarjetas; 3 alumnos |

Se compararon valores exclusivamente en memoria con literales de fuentes históricas: solo una coincidencia de nombre y una de UID por base; no basta para certificar todo el dataset como ficticio. Ningún nombre llevaba marca explícita demo/prueba/ficticio. **No se determinó autenticidad personal ni exposición efectiva.** La estructura, fecha y tamaño acreditan respaldos antiguos; la finalidad exacta y el carácter ficticio de todos los datos deben confirmarse con quien los creó. No corresponden al esquema completo actual de producción.

Tratamiento propuesto: conservarlos sin publicación nueva, confirmar procedencia privadamente y registrar clasificación. Si se confirma información auténtica, revisar visibilidad/permisos y acordar saneamiento y tratamiento de exposición antes de publicar; no borrar ni reescribir historia automáticamente. Esta incertidumbre no bloqueó las demás correcciones.

## B. Resultados de pruebas

| Comando | Resultado |
|---|---|
| `/tmp/mpaz-venv312/bin/python -m unittest discover -s tests -v` | 61 métodos, OK, Python 3.12.16 |
| `.venv/bin/python -m unittest discover -s tests -v` | 61 métodos, OK, Python 3.14.8 |
| `node tests/test_interfaz.cjs` | OK, ficha escapada anterior |
| `node tests/test_dom_seguro.cjs` | OK, tres constructores de nodos con payload HTML |
| `TZ=UTC node tests/test_tiempo_escolar.cjs` y con `TZ=Asia/Tokyo` | OK, fecha/hora Chile independiente de zona del proceso |
| `node --check` en todos los JS | OK |
| Python 3.12 `compileall` excluyendo .venv/.git | OK |
| Recursos locales HTML | Sin scripts/hojas de estilo faltantes; prueba incorporada |
| `git diff --check` | OK |
| Navegador | No disponible; `getState()` devuelve host inaccesible y ninguna superficie |

Reproducciones previas: las seis pruebas iniciales nuevas de sesión/login mostraron 9 fallos en subcasos sobre el comportamiento anterior; tokens Unicode y JSON anidados produjeron TypeError; el actor de calendario era genérico; el reenvío anterior dejaba escapar TimeoutError. Esos escenarios pasan después de corregir. Una carrera detectada durante la implementación (rotación de contraseña antes de emitir sesión) también se reprodujo y corrigió con prueba específica.

No se midió cobertura porcentual ni carga representativa. Python 3.12 se instaló y usó exclusivamente en /tmp; uv se instaló solo en el entorno virtual local. Requirements y servidor no se modificaron. No se detectó incompatibilidad en las baterías ejecutadas en 3.12 y 3.14.

Las pruebas de IDOR amplían asignación ajena, sesión ajena, alumno de otro curso, lectura/escritura/confirmación e historial. Se añadió CRUD de estudiante generado, duplicado, edición, baja/reactivación; alta/duplicado/estado de tótem; extravío de tarjeta; flujo RFID completo por API y exportación HTTP filtrada. Identificadores sintéticos se generan para las pruebas, sin tomar datos de las bases históricas ni de producción.

## C. Pendientes

### P0 condicional

- Clasificación final privada de datos históricos antes de publicar. No hay confirmación de datos auténticos o exposición; no declarar filtración por el solo hecho de encontrar archivos .db.
- No se conocen otros P0 confirmados sin corrección local dentro de los escenarios ejercidos. Esto no certifica ausencia de vulnerabilidades en todo el sistema.

### P1

- Decidir reglas de calendario/inasistencias/atrasos/cierre. Cinco pruebas de caracterización reproducen defectos; **no significan que esas funciones estén aprobadas**. Ver [decisiones](CALENDARIO_DECISIONES.md).
- Validar la cadena de proxies y umbral por IP, duración de sesión y carga SQLite antes de desplegar seguridad persistente.
- Completar QA visual/teclado/contraste/móvil mediante [procedimiento manual](QA_MANUAL.md).
- RUT: normalización y unicidad entre formatos equivalentes e históricos; límites sintácticos completos. Duplicado idéntico está probado; no se certifica deduplicación global.
- Historial completo de tarjetas, todas las variantes de filtros/CRUD/IDOR, CSP, límites de tamaño y más fuzzing.
- Instante original de eventos offline, firmware, carreras de desactivación frente a lectura, hora repetida DST y sesiones en curso durante revocación.
- Recuperación real y monitorización/retención de respaldos; runner general de migraciones y fijación de Gunicorn. No se ensayó restauración escolar ni se leyó su base.

### P2

PostgreSQL, MPAZ Web y módulos institucionales evolutivos: conservar las propuestas existentes, ahora incluyendo tablas de seguridad. No se implementaron cambios arquitectónicos mayores.

## D. Riesgos antes de producción

Requiere autorización: aplicación de migración 005, nueva release, cambios de entorno y reinicio. No desplegar código sin la tabla de seguridad; fallará cerrado. El despliegue invalidará cookies antiguas y exigirá nuevo login.

Backend y assets nuevos deben publicarse juntos. Los plazos de sesión propuestos y el umbral por IP necesitan validación institucional/operativa. El reloj Chile cambia el comportamiento de nuevos registros si el host estaba en otra zona; no modifica históricos ni corrige ambigüedades de campos sin offset.

La limitación y el registro de actividad añaden escrituras SQLite; medir latencia/contención con dos workers y carga representativa. No se habilitó WAL ni se tocó configuración de red para resolverlo. La migración no es un despliegue autorizado.

## E. Estado de Git

Continúa la rama `audit/seguridad-continuidad-20261116`, desde `f894ac8`. Commits locales separados para seguridad y consistencia/documentación; consultar `git log f894ac8..HEAD --oneline`. Sin push, merge, cambios en main/capstone, modificaciones de bases históricas o acceso al servidor. Commits de implementación: `971e45f` (seguridad persistente) y `d5dff41` (renderizado, hora y reenvío). La documentación se registra por separado.

## F. Próxima etapa

1. Revisar diff de seguridad y migración; confirmar clasificación de respaldos históricos.
2. Ejecutar QA manual y carga con múltiples workers en entorno ficticio.
3. Aprobar calendario/horarios y convertir caracterizaciones en criterios de aceptación.
4. Preparar release controlada con respaldo/restauración autorizados y aplicación aislada de 005. Solicitar autorización antes de tocar producción.
