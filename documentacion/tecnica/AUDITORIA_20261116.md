# Auditoría técnica MPAZ RFID — 16-11-2026

## A. Resumen ejecutivo y alcance real

Revisión inicial de arquitectura, rutas, permisos, persistencia, scripts, frontend y operación. Se añadieron correcciones locales verificadas; **no es una certificación de seguridad ni cierre total de las fases A–H**. La matriz indica qué se probó y qué sigue pendiente.

GitHub fue consultado mediante `git fetch origin` antes de editar. Integración continúa **17 commits por delante de main y 0 por detrás** (`git rev-list --left-right --count origin/main...origin/integration/seguridad-seguimiento`: `0 17`). Base de trabajo y release efectiva: `d0d2c80`. No se trabajó en main ni se modificaron evidencias capstone.

Consecuencia: main no representa producción ni contiene todas las funcionalidades de integración. Un clon por defecto o despliegue desde main puede perder funcionalidades y controles presentes en la rama desplegada. No se fusionaron ramas para resolverlo.

El árbol estaba limpio antes de crear `audit/seguridad-continuidad-20261116`. No se encontraron AGENTS.md aplicables en la búsqueda del proyecto. Se preservaron archivos existentes.

### Estado por fase

| Fase | Entregado | Límite pendiente |
|---|---|---|
| A | Estructura, entrada Flask, dependencias, tablas, migraciones, rutas, documentación y referencias Git | Análisis exhaustivo de código muerto/duplicación y contratos completos |
| B | Regresiones de autenticación/roles, revocación, CSRF, JSON, cookies, XSS de ficha y errores SQLite | Rate limiting, login CSRF, replay de cookies, todos los sumideros HTML y casos IDOR |
| C | RFID simulado, duplicados, 30 segundos, cierre, bloqueo e inactividad, concurrencia de un evento | Firmware, DST, eventos offline con retardo, carreras de cambio de estado y cortes reales |
| D | Tarjetas básicas, separación de roles, seguimiento completo ficticio y calendario con auditoría | CRUD completo, reportes y consistencia pedagógica/administrativa integral |
| E | Inspección de recursos y preferencias; prueba JS de ficha | Navegador inaccesible; no QA visual, teclado, contraste ni móvil |
| F | Esquema e índices ficticios, respaldo WAL y recuperación de copia verificada | Integridad y recuperación reales requieren procedimiento privado autorizado |
| G | Suite unittest y prueba JS, comparación contra referencia | Python 3.12/CI, cobertura cuantificada y matriz exhaustiva |
| H | Correcciones seguras, prioridades y propuesta PostgreSQL | Integración/release y decisiones institucionales no ejecutadas |

## B. Hallazgos con evidencia

Prioridad no equivale a explotación demostrada en producción. Las pruebas se ejecutaron solo con datos generados.

| ID | Severidad | Descripción y ubicación | Evidencia | Situación |
|---|---|---|---|---|
| H01 | P0 potencial | Seis respaldos `.db` ya versionados en `data/`; contenido desconocido | `git ls-files` enumera `asistencia_respaldo.db` y cinco variantes históricas | Sin abrir/eliminar; revisar privadamente antes de publicar. `.gitignore` no sanea historia |
| H02 | P0 | Ficha administrativa inserta UID y campos con `innerHTML`, `app.js:mostrarFichaEstudiante` | `node tests/test_interfaz.cjs` falla en d0d2c80 con UID HTML y pasa corregido | Corregido en desarrollo; otros renderizadores no certificados |
| H03 | P1 | `/profesor/sesion` seguía devolviendo sesión válida tras desactivar usuario | `test_docente_revocado`: 200 original, 401 corregido | Revalidación central por cuenta activa/rol |
| H04 | P1 | JSON lista/escalar produce AttributeError en `/lectura` y varios POST administrativos | `test_lectura_json_no_objeto`, `test_json_administrativo_no_objeto` | Respuestas 400 controladas |
| H05 | P1 | Logout panel/docente sin CSRF | `test_logout_csrf`, `test_logout_docente_csrf`: 200 sin token en referencia | Rechazo 403 y JS actualizado |
| H06 | P1 | CSV permite celdas fórmula y sobrescribe exportaciones con misma marca temporal | `test_exportacion_formula_y_nombres_unicos`, `test_exportacion_nombre_unico` | Neutralización de texto y nombres UUID; no se altera SQLite |
| H07 | P0 condicional | `respaldar_base_datos.py` copiaba solo el archivo principal y desconocía MPAZ_DB_PATH | `test_respaldo_wal`: copia original omite cambio confirmado en WAL | API backup, lectura de origen, verificación, 0600 y nombres únicos; no ejecutado en producción |
| H08 | P1 | Cookies sin Secure/SameSite explícitos y falta de no-store general | `test_cookie_y_cache`: cookie referencia no incluye Secure; inspección configuración Flask | Configuración explícita y cabeceras básicas; HTTPS por defecto |
| H09 | P1 | Error operativo SQLite escapa de `/lectura` sin respuesta controlada | `test_sqlite_no_disponible`: excepción original; 503 sin detalle corregido | Manejador general sin revelar texto de excepción |
| H10 | P1 | Sin límite de intentos de login en código revisado | Lectura de tres rutas login y funciones de autenticación | Pendiente mecanismo entre workers; controles externos no verificados |
| H11 | P1 | Tiempo implícito y cierre 17:00 para cualquier jornada | `base_datos.cerrar_jornadas_pendientes`, `registrar_asistencia.procesar_asistencia` | No se cambió regla; requiere especificación para después de las 17:00 y DST |
| H12 | P1 | Inasistencias dependen de fechas con RFID; atrasos usan 08:20 fijo, sin integración calendario | `consultar_asistencia.obtener_inasistencias`, `HORA_LIMITE_ATRASO` | Pendiente aprobación de semántica y pruebas institucionales |
| H13 | P0 | Cola JSON retorna [] si hay error de lectura/corrupción, pierde altas simultáneas y reenvío sobrescribe eventos nuevos | Cinco pruebas `tests/test_cola.py` fallan en referencia y pasan corregidas | Bloqueo Linux entre procesos/hilos, escritura atómica, error explícito y confirmación por evento; corregido en desarrollo |
| H14 | P1 | Migración 004 no repetible; migradores históricos con DROP/efectos al importarse | `migraciones/004_*`, `migrar_alumnos_sin_uid.py`, `migrar_tarjetas.py` | No ejecutados; falta runner versionado |
| H15 | P1 | Dependencias del despliegue no reproducibles completamente | `requirements.txt` no incluye Gunicorn; Python local 3.14.8 frente a objetivo 3.12 | Entorno local aislado instalado; fijación Gunicorn pendiente |
| H16 | P1 | Logout no revoca una cookie firmada previamente copiada | Sesiones Flask sin registro central de revocación | Pendiente diseño/ensayo, no declarar logout global |

Otros límites: sin CSP completa ni límites explícitos de tamaño del cuerpo; algunas comparaciones `compare_digest` con texto no ASCII y valores JSON anidados requieren fuzzing; no se declara robustez de todas las entradas. Las consultas examinadas usan parámetros para valores; no se probó una inyección SQL ni se certificó cada consulta histórica.

### Inventario funcional solicitado

«Parcial» significa que hay comportamiento comprobado, pero no evidencia suficiente del módulo completo. «Operativo» se limita expresamente al alcance indicado.

| Módulo | Archivos | Funcionalidad esperada | Estado real | Problemas/prioridad | Prueba/evidencia |
|---|---|---|---|---|---|
| Estado API | `api.py` | Disponibilidad básica | Operativo en prueba aislada | No verifica DB/hardware, P1 | `test_estado_y_rutas_privadas`: JSON y contrato básico, no solo 200 |
| Identidad administrativa | `api.py`, `seguimiento_identidad.py`, `seguimiento_sesiones.py` | Login individual/roles | Parcial | H10/H16; P1 | `test_administracion_direccion_y_csrf`, `test_sesion_antigua_y_operador_inactivo` |
| Identidad docente | `api.py`, `base_datos.py` | Login activo/curso/sesión | Parcial | H03 corregido; sesión robada pendiente, P1 | `test_docente_revocado`, `test_docente_idor_y_csrf`, logout docente |
| RFID | `procesar_lectura_totem.py`, `registrar_asistencia.py`, `base_datos.py` | Entrada/salida/idempotencia | Parcial | Tiempo, carrera de estados y firmware P1 | Tests RFID, tarjetas bloqueadas, cierre y dispositivos |
| Hardware/lector | `lector_nfc.py`, simuladores | Captura PN532/ESP32 | Sin verificar | Lector Python es consola; firmware ausente, P1 | Inspección; sin hardware ni firmware probado |
| Estudiantes | `base_datos.py`, `api.py`, `consultar_alumnos.py`, `directorio.js` | Alta/edición/estado/filtros | Parcial | Alta/edición completa y RUT normalizado pendientes, P1 | Consulta privada y rechazo RUT ficticio; no alta válida aprobada |
| Tarjetas | `base_datos.py`, scripts de tarjeta, `inventario-mpaz.js`, `vinculacion*.js` | Alta/vinculación/bloqueo/extravío | Parcial | Carreras e historial completo pendientes, P1 | `test_tarjetas_y_estados_administrativos`, duplicados y tarjeta bloqueada |
| Tótems | `base_datos.py`, `api.py` | Registro/estado/autorización | Parcial | Alta/edición completa no probada, P1 | Dispositivo desconocido e inactivo rechazados; CSRF |
| Consultas asistencia | `consultar_asistencia.py`, `api.py`, `asistencias-mpaz.js` | Listados y filtros | Parcial | Consistencia integral pendiente, P1 | RFID en SQLite y control anónimo; no reconciliación completa de UI |
| Inasistencias/atrasos | `consultar_asistencia.py`, scripts UI | Cálculos por jornada | Defectuoso respecto a integración esperada | H12, P1; no cambiar sin acuerdo | Evidencia estática de cálculo sin calendario; fórmulas nuevas no aprobadas |
| Reportes | `exportar_asistencias_csv.py`, `api.py` | CSV por periodo/curso | Parcial | H06 corregido; conciliación de todos los filtros pendiente, P1 | Exportación vacía, fórmulas y colisión de nombre |
| Calendario | `calendario_*.py`, migraciones 001/002, JS | Jornadas/auditoría | Parcial | H12 y actor genérico en historial, P1 | `test_calendario_prioridad_y_auditoria`; escritura HTTP habilitada no ejercida |
| Seguimiento Escolar | `seguimiento_*.py`, migraciones 003/004, UI | Casos/mensajes/contactos/estado | Parcial | Límites, concurrencia y UI pendientes, P1 | Flujo completo ficticio y rechazo de otro curso; Dirección no contacta |
| Portal docente/clases | `base_datos.py`, `api.py`, `profesor/` | Asistencia por asignación | Parcial | Confirmación completa y QA navegador pendientes, P1 | Restricción de otro curso, CSRF y seguimiento; no toda la matriz de clases |
| Cola/reenvío | `cola_pendientes.py`, `reenviar_pendientes.py`, simuladores | Reintentos de red | Parcial | H13 corregido; falta timeout explícito y semántica de evento retardado, P1 | Red simulada, corrupción, fallo de reemplazo, 30 altas en hilos y procesos, evento nuevo durante reenvío |
| Respaldos | `respaldar_base_datos.py` | Copia consistente/recuperable | Operativo en escenario WAL ficticio | Programación, alertas y recuperación real pendientes, P1 | Copia contiene cambio; integrity_check=ok y foreign_key_check vacío |
| UI/preferencias | `identidad-mpaz.*`, HTML/JS/CSS | Preferencias persistentes y accesibilidad | Sin verificar visualmente | P1 | Código usa localStorage y dataset; 37 recursos CSS/JS existentes; navegador inaccesible |
| Importaciones | `importar_estudiantes.py`, `revisar_excel_estudiantes.py`, `simular_importacion_estudiantes.py` | Excel validado | Sin verificar funcionalmente | P1 | Imports/dependencia comprobados; no se usaron planillas escolares |

## C. Correcciones realizadas

- `api.py`: cuenta docente vigente, CSRF de logout, objetos JSON válidos, cookie explícita, cabeceras/no-store y error operativo 503. No cambia consultas ni reglas RFID.
- `interfaz_prueba/app.js`: token para logout y escape de campos de ficha. `profesor/profesor.js`: token docente y comprobación de respuesta en logout. HTML de ambos paneles cambia versión del asset.
- `exportar_asistencias_csv.py`: neutraliza fórmulas en texto exportado y usa UUID para no sobrescribir reportes simultáneos. El contenido SQLite se conserva.
- `respaldar_base_datos.py`: backup consistente, origen de solo lectura, configuración por entorno, archivo privado único y validación de copia.
- `cola_pendientes.py` y `reenviar_pendientes.py`: no sobrescribir colas corruptas; bloqueo entre procesos/hilos, temporal sincronizado y reemplazo atómico. Confirmar solo eventos enviados para conservar altas concurrentes. Usa fcntl estándar de Linux; no hay nueva dependencia.
- `.gitignore`: exclusión adicional de bases/auxiliares/entornos privados. No elimina bases existentes ni modifica historia.
- `tests/`: regresiones aisladas y reproducción de referencia.
- README, instalación, changelog y `documentacion/tecnica/`: arquitectura, API, esquema, operación y propuesta evolutiva. Se conservaron documentos previos y evidencias académicas.

Los valores por defecto de cookie siguen las recomendaciones de [seguridad de Flask](https://flask.palletsprojects.com/en/stable/web-security/). En desarrollo HTTP se documenta una excepción explícita, nunca para producción HTTPS.

## D. Pruebas ejecutadas y límites

Entorno: Python 3.14.8, Flask 3.1.3, Werkzeug 3.1.8, SQLite de biblioteca estándar, Node 26.12.0. Dependencias instaladas desde requirements en `.venv`, sin dependencias nuevas de producción.

| Comando/acción | Resultado real |
|---|---|
| `git fetch origin` | Aprobado tras habilitar red del entorno; referencias verificadas |
| `git rev-list --left-right --count origin/main...origin/integration/seguridad-seguimiento` | `0 17` |
| Suite final de 29 métodos contra copia temporal de d0d2c80 | FALLIDA esperada: 12 fallos y 15 errores en subcasos; falla JS por HTML ejecutable |
| Prueba adicional SQLite no disponible contra código anterior al manejador | FALLIDA esperada: 1 error OperationalError |
| `.venv/bin/python -m unittest discover -s tests -v` | 29 métodos aprobados tras las correcciones |
| `node tests/test_interfaz.cjs` | Aprobado: contenido HTML de UID escapado en función real |
| `.venv/bin/python -m compileall -q -x '/(\.venv|\.git)/' .` | Aprobado; no ejecuta scripts |
| `node --check` sobre todos los JS de `interfaz_prueba/` y `profesor/` | Aprobado |
| Inspección HTMLParser de referencias locales script/stylesheet | 37 referencias; ninguna faltante |
| AST de imports de módulos Python | Externos: flask, openpyxl, werkzeug; sin módulo externo faltante en entorno instalado |
| `git diff --check` | Aprobado |
| Navegador local ficticio | NO EJECUTADO visualmente: host de navegador inaccesible; servidor temporal detenido |
| Hardware, producción con datos, DST y Python 3.12 | NO EJECUTADOS |

Para repetir la comparación, ejecutar `.venv/bin/python tests/reproducir_base.py`. Copia únicamente archivos de código/SQL del commit y pruebas actuales a un directorio temporal, nunca `.db` ni configuración privada. La referencia debe fallar; no es el comando de CI. El número de errores puede crecer si se amplían las pruebas actuales. Los logs temporales contienen solo datos ficticios; no se versionan.

No se midió porcentaje de cobertura. Los scripts `probar_*.py` existentes no se ejecutaron indiscriminadamente porque algunos escriben al importarse, usan rutas por defecto o dependen de servidor/clave. La suite nueva reemplaza esos riesgos para los escenarios aquí enumerados, no garantiza cobertura de todo el sistema.

## E. Pendientes

Ver [plan priorizado](CONTINUIDAD.md). P0: revisión privada de archivos de datos ya versionados y cierre del análisis XSS completo. P1: timeout/reintentos offline, intentos repetidos, sesiones robadas, tiempo Chile/DST, calendario, CRUD completo, errores anidados, migraciones versionadas, CI 3.12 y recuperación operativa. P2: PostgreSQL e integraciones institucionales.

La revisión no demuestra explotación ni pérdida de datos en la escuela. No se cambiaron reglas o permisos institucionales para obtener pruebas aprobadas.

## F. Riesgos y mitigación

Las correcciones aún no protegen producción: falta revisión y despliegue autorizado. Publicar backend sin frontend nuevo puede romper los botones logout; ambos deben salir juntos y verificarse caché. Secure por defecto requiere HTTPS o excepción solo local. CSV antepone apóstrofo a texto potencialmente fórmula; el resultado visible en algunas herramientas puede incluir ese carácter.

El respaldo verificado requiere espacio suficiente y acceso de lectura al origen; no resuelve retención, cifrado externo ni alertas. Una copia fallida no debe usarse para restaurar. La autenticación depende de SQLite y fallará cerrada si no puede consultarse.

No abrir, trasladar ni publicar los seis .db versionados. La revisión/saneamiento necesita acuerdo privado y no debe destruir evidencia ni respaldos. No se ejecutó push.

## G. Próximos pasos

1. Revisión privada de bases rastreadas y revisión de diff de seguridad.
2. Ampliar sumideros HTML, semántica de eventos offline y sesiones; repetir suite en Python 3.12 y navegador real.
3. Acordar semántica de calendario/horario/offline con la escuela.
4. Ensayar respaldo/restauración y preparar release nueva conforme a [operación](OPERACION.md).
5. Solicitar autorización solo al llegar al cambio de producción, migración o decisiones institucionales.

## H. Estado Git

Base: `d0d2c80`; rama de trabajo: `audit/seguridad-continuidad-20261116`. Sin merge ni push. Correcciones y pruebas registradas en `20e404c`; documentación registrada en un commit separado. No se modificó main, rama estable, rama capstone, repositorio antiguo del servidor ni release desplegada. Consultar `git log d0d2c80..HEAD --oneline` para identificadores exactos de los commits de esta entrega.
