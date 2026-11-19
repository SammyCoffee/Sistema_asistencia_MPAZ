# Migración 005: verificación local en Caldero — 19-11-2026

## Dictamen

La migración 005 es compatible con el esquema reconstruido desde `d0d2c807710066fc41f5fe1922f4452c258b8270`. Conservó todas las filas escolares, metadatos de secuencias y objetos previos examinados. Una segunda aplicación conservó también las sesiones e intentos de login ya almacenados. No fue necesario modificar el SQL.

Se detectó y corrigió una carrera en la validación de sesiones bajo solicitudes concurrentes. La corrección se limita a medir el tiempo después de adquirir el bloqueo de escritura. Resultado final: **71 pruebas Python aprobadas, 19.769 segundos, sin omisiones**, incluidas diez nuevas y un ensayo real con Gunicorn local.

**Preparada técnicamente para una futura aplicación controlada sobre el esquema probado, incorporando la corrección del backend y las comprobaciones previas descritas abajo.** No constituye autorización de despliegue ni comprobación de la base escolar actual: no se abrió ninguna base real y se desconoce cualquier divergencia de esquema que pudiera existir en ella.

## Qué incorpora la 005

Archivo: `migraciones/005_seguridad_web.sql`.

SHA-256 verificado: `84f462410d54d354e0fb3a26d0790308876b8bb75d41bc8bda31e21298e99428`.

| Estructura | Campos / restricciones | Uso |
|---|---|---|
| `web_login_intentos` | `clave TEXT PRIMARY KEY`, `cantidad INTEGER NOT NULL CHECK(cantidad >= 0)`, `expira REAL NOT NULL` | Contadores de intentos compartidos por cuenta y dirección IP |
| `idx_web_intentos_expira` | Índice sobre `web_login_intentos(expira)` | Eliminación de contadores vencidos |
| `web_sesiones` | `token_hash TEXT PRIMARY KEY`; `tipo TEXT NOT NULL CHECK(tipo IN ('operador','docente'))`; `identidad_id INTEGER NOT NULL`; `credencial_firma TEXT NOT NULL`; `creada`, `actividad`, `expira` como `REAL NOT NULL` | Registro persistente de sesiones, expiración y revocación |
| `idx_web_sesiones_expira` | Índice sobre `web_sesiones(expira)` | Limpieza de sesiones expiradas |

SQLite añade además dos índices automáticos de clave primaria. No se añaden columnas a tablas existentes, no se ejecutan UPDATE/DELETE/DROP sobre ellas y no se cambian roles, contraseñas, reglas escolares ni permisos. El script contiene `BEGIN IMMEDIATE` y `COMMIT`, con `IF NOT EXISTS` en tablas e índices.

Los tiempos nuevos son epoch UTC, independientes de las horas civiles escolares. `identidad_id` no tiene una FK única porque refiere, según `tipo`, a `seguimiento_operadores` o `usuarios`. Esa correspondencia y la cuenta activa/rol se revalidan en código. No se cambiaron estas decisiones de diseño.

## Componentes que usan las estructuras

`seguridad_web.py` centraliza el uso:

- `limitar_login`: reserva intentos con transacción SQLite, comparte los contadores entre procesos y aplica las ventanas existentes de 300 segundos, 10 intentos por cuenta y 200 por IP. Las claves son firmas HMAC, no nombres/IP en claro.
- `crear_sesion_web`: vuelve a comprobar credencial y cuenta, registra un token firmado y firma de contraseña/rol. La cookie conserva el token; SQLite conserva su huella HMAC.
- `validar_sesion_web`: verifica identidad, credencial/rol vigente, actividad y expiración; actualiza actividad o elimina una sesión inválida.
- `revocar` y el hook de logout: borran el registro para impedir reutilizar una cookie copiada.

`api.py` instala estos hooks y crea sesiones de Administración y docentes. `seguimiento_sesiones.py` crea sesiones individuales de operadores, incluida Dirección. Los tres accesos de login usan el mismo control persistente. Estos módulos necesitan la 005 antes de habilitar el nuevo backend; Flask no crea las tablas automáticamente. La ausencia de estructuras requeridas falla de forma cerrada con 503, ya cubierta por las regresiones existentes.

Todos los workers deben usar la misma ruta SQLite y el mismo secreto de sesión. Cambiar el secreto invalida cookies y las firmas de los registros; la 005 no administra secretos. No se añadió confianza en `X-Forwarded-For`: sigue pendiente validar la cadena de proxies antes de producción.

## Cómo se construyó la base de prueba

La nueva batería `tests/test_migracion005.py` extrae de Git exclusivamente fuentes `.py` y `.sql` del commit exacto `d0d2c80`, dentro de una carpeta temporal. No extrae archivos `.db`, respaldos ni secretos.

En un subproceso aislado ejecuta el `crear_tablas()` de esa versión y sus migraciones **001–004**, sobre un archivo nuevo. Esto reconstruye el esquema previo; no se ejecutan migradores históricos ni se vuelve a ejecutar 004 sobre una base existente.

Inserta exclusivamente datos ficticios en todas las tablas funcionales: alumnos activos/inactivos, tarjetas activas/bloqueadas, tótem, asistencia con entrada/salida e identificadores de evento, asignatura/asignación, sesión docente confirmada y su asistencia, jornadas/eventos/auditoría de calendario y casos/mensajes/contactos/avisos de seguimiento. Las cuentas de Administración, Dirección y docencia tienen hashes generados para el ensayo.

Antes de migrar se capturan todas las filas, incluida `sqlite_sequence`, y todas las definiciones de `sqlite_master`. Se compara el contenido exacto tras aplicar 005 y tras los escenarios de uso. Se ejecutan `PRAGMA integrity_check` y `PRAGMA foreign_key_check`: resultado `ok` y ninguna infracción. Los archivos temporales se eliminan al terminar.

## Pruebas nuevas y resultados

| Prueba | Evidencia obtenida |
|---|---|
| Estructura y conservación desde d0d2c80 | Solo aparecen las dos tablas y cuatro índices, contando los dos automáticos; los objetos y filas previos permanecen iguales |
| Segunda aplicación con seguridad ya poblada | Esquema idéntico; conserva contadores, sesión y datos escolares |
| Error intermedio de DDL | Un conflicto ficticio al crear el último índice produce error; la transacción sigue abierta y un rollback restaura el esquema previo sin tablas parciales |
| Base ocupada por otro escritor | BEGIN IMMEDIATE falla con `database is locked`; no deja esquema parcial; al liberar el bloqueo la aplicación concluye correctamente |
| Tabla homónima incompatible | IF NOT EXISTS acepta una tabla `web_sesiones` incompleta; no la repara. El login devuelve 503 y no concede sesión. Exige comprobación de esquema antes de aplicar |
| Restricciones de seguridad | Rechaza contador negativo, tipo de sesión no permitido e identidad nula |
| Administración, Dirección y docencia | Login y consulta válidos, uso desde otro cliente, alcance de Dirección conservado, acceso docente a curso asignado y rechazo de cookie copiada tras logout |
| Actividad concurrente | Regresión determinista: reproduce el 401 erróneo antes de corregir y pasa después |
| Código d0d2c80 sobre base migrada | Login, consulta y logout de Administración y docencia funcionan; se conserva la base. Una copia de cookie sigue devolviendo 200 tras logout con el código antiguo: riesgo de reversión confirmado |
| Gunicorn real | Dos workers sync y tres workers sync con `--preload`, exclusivamente 127.0.0.1 y SQLite ficticio; controles compartidos verificados por PID |

La batería previa de 61 pruebas se ejecutó como regresión de la corrección de sesiones, no como repetición de la auditoría inicial. Conserva sus cinco caracterizaciones de defectos escolares pendientes. No hubo cambios JavaScript, de calendario ni de asistencia; no fue necesario repetir sus tres programas JS en esta etapa.

## Hallazgo corregido: falso cierre de sesión con concurrencia

Antes de la corrección, `validar_sesion_web` capturaba `time.time()` antes de `BEGIN IMMEDIATE`. Si otro worker escribía una actividad posterior mientras la solicitud esperaba el bloqueo, la expresión `0 <= ahora - actividad` fallaba y se borraba una sesión válida.

El ensayo inicial de Gunicorn falló con tres workers y preload: aparecieron 401 en solicitudes que debían devolver 200. La prueba determinista hizo avanzar la actividad desde otra conexión durante la espera simulada y reprodujo **401 frente al 200 esperado**.

Cambio en `seguridad_web.py`: medir `ahora` inmediatamente después de obtener `BEGIN IMMEDIATE`. El reloj y la fila se examinan así dentro del mismo tramo serializado. Se conservan plazos, validación de credenciales, revocación y autorización. La carrera no depende conceptualmente de preload; puede darse entre solicitudes concurrentes a la misma sesión.

No se modificó la migración ni se incorporaron nuevos mecanismos de persistencia o permisos. Esta corrección debe acompañar al backend de la futura release.

## Gunicorn y varios workers

Entorno medido: Python 3.12.16, SQLite 3.53.1 y **Gunicorn 27.0.1**, instalado únicamente en `/tmp/mpaz-migracion005-gunicorn`. Esta versión es la del ensayo, no la versión certificada del servidor ni una fijación de producción. Requirements y el entorno del proyecto no recibieron Gunicorn.

Por cada configuración, y tanto para Administración como para docencia:

- 36 consultas concurrentes de sesión devolvieron 200; las cabeceras de instrumentación temporal comprobaron que participaron todos los PIDs esperados.
- Tras logout, 18 reutilizaciones de la cookie devolvieron 401.
- 18 intentos concurrentes de login incorrecto produjeron exactamente diez respuestas 401 y ocho 429, con Retry-After positivo y contador máximo diez.

Total entre ambas configuraciones: **144 consultas válidas, 72 replays rechazados y 36 intentos de login**. No hubo 500/503 en estos escenarios después de corregir la carrera. La instrumentación de PID existe solo en un módulo temporal de prueba; no se añadió a la API del producto. Los procesos de ensayo terminaron al concluir.

La arquitectura de procesos de Gunicorn permite que cada worker atienda independientemente; compartir estado mediante el mismo archivo SQLite evita depender de memoria por worker. Véase [diseño oficial de Gunicorn](https://gunicorn.org/design/).

El ensayo acredita funcionamiento compartido con los workers sync probados. **No es una medición de capacidad ni de latencia representativa**, no valida proxies/HTTPS del servidor, no ensaya otros tipos de workers ni almacenamiento remoto. SQLite admite un escritor simultáneo; la seguridad añade escrituras a cada solicitud autenticada y puede producir contención. Véase [transacciones SQLite](https://www.sqlite.org/lang_transaction.html).

## Repetición, errores y requisitos de ejecución

Sobre un esquema correcto, repetir 005 es inocuo y conserva también sus datos de seguridad. Sin embargo, `IF NOT EXISTS` no comprueba definiciones de tablas o índices existentes; esto forma parte del comportamiento documentado de [CREATE TABLE en SQLite](https://www.sqlite.org/lang_createtable.html).

Antes de una aplicación futura debe confirmarse que los nombres nuevos están ausentes o que las definiciones ya existentes corresponden exactamente a la 005. Un resultado sin errores no basta por sí solo para certificar el esquema.

Si un comando intermedio falla, no debe continuarse ni hacerse commit: el proceso debe detenerse y ejecutar rollback, o cerrar sin confirmar la conexión. La prueba demuestra que `executescript` no hace rollback automático ante ese error. Evitar ejecutores que continúen hasta COMMIT después de un fallo. La transacción aporta atomicidad cuando el ejecutor maneja correctamente los errores; no sustituye ese manejo. Usar una conexión dedicada sin cambios pendientes, porque `executescript` puede confirmar transacciones anteriores según el modo de transacción de Python.

No se añadió un runner general ni se autorizó ejecutar 001–004 otra vez en un esquema ya migrado. La ventana controlada debe evitar escrituras concurrentes y validar integridad/esquema después. El bloqueo ensayado usa un timeout de 50 ms para reproducir rápidamente el error; no modifica el timeout del producto.

## Reversión a d0d2c80

**Compatibilidad estructural comprobada:** el código antiguo pudo leer la base migrada e iniciar/cerrar sesiones; las tablas nuevas no impiden ese uso y pueden conservarse sin uso. No es necesario borrar tablas, deshacer asistencia ni restaurar una base como consecuencia automática de volver al código anterior.

**Retroceso de seguridad comprobado:** d0d2c80 no consulta el registro de sesiones ni aplica estos contadores; una cookie copiada antes de logout sigue funcionando después. Volver atrás reintroduce además las limitaciones de seguridad documentadas para esa versión. No debe presentarse como una reversión sin riesgo.

Si se usa temporalmente una versión que no revoca sesiones persistentes, sus cambios de login/logout no quedan reflejados en `web_sesiones`. Al volver a habilitar el código nuevo hay que planificar expresamente la invalidación/reautenticación de sesiones previas; no asumir que el logout del código viejo las revocó. No se ejecutó ninguna invalidación real.

Debe evitarse mezclar workers de versiones viejas y nuevas atendiendo simultáneamente: las políticas de sesión divergen. Backend y assets deben publicarse coordinadamente. No se cambió el procedimiento institucional de release/reversión.

## Reproducción y evidencias

Desde la raíz del proyecto, con el entorno existente, sin datos institucionales:

```bash
# Nueve pruebas dirigidas sin servidor; Gunicorn se omite explícitamente.
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_migracion005.py -v

# Preparar la dependencia opcional de ensayo, fuera de requirements y de .venv.
UV_CACHE_DIR=/tmp/mpaz-uv-cache UV_LINK_MODE=copy uv pip install --python .venv/bin/python --target /tmp/mpaz-migracion005-gunicorn 'gunicorn==27.0.1'

# Las diez pruebas nuevas, con Gunicorn solo local.
PYTHONDONTWRITEBYTECODE=1 MPAZ_TEST_GUNICORN_PATH=/tmp/mpaz-migracion005-gunicorn .venv/bin/python -m unittest discover -s tests -p test_migracion005.py -v

# Batería completa ejecutada después de corregir.
PYTHONDONTWRITEBYTECODE=1 MPAZ_TEST_GUNICORN_PATH=/tmp/mpaz-migracion005-gunicorn .venv/bin/python -m unittest discover -s tests -v
```

Las pruebas requieren el objeto Git d0d2c80 local y solo consultan Git para extraer fuentes. El ensayo opcional requiere permiso para escuchar en loopback. Al omitir la variable de Gunicorn se informa explícitamente una prueba omitida; la ejecución final de esta revisión lo incluyó y no tuvo omisiones.

Evidencias en `/home/coffeewitch/Work/MPAZ-migracion005-20261119/`:

- `regresion-antes.log`: reproducción determinista del fallo antes de corregir.
- `gunicorn.log`: primer ensayo, con fallo en tres workers/preload.
- `pruebas-dirigidas.log`: ensayo inicial de estructura/datos; anterior a añadir la regresión de concurrencia.
- `suite-final.log`: 71 pruebas aprobadas y resultados por configuración Gunicorn después de corregir.

## Alcance final y preparación de una aplicación controlada

La 005 no requiere corrección SQL para el esquema probado. La aplicación sí necesitaba la corrección de concurrencia, ahora cubierta por prueba. Quedan como condiciones previas a producción: validar privadamente el esquema real y su versión SQLite, ausencia/compatibilidad de objetos homónimos, ruta/permisos/espacio, respaldo con restauración comprobada, versión/configuración real de Gunicorn, secreto compartido, proxies y carga representativa. Aplicar solo 005 mediante un ejecutor que aborte y haga rollback ante error, y comprobar después esquema, integridad y sesiones. Esas comprobaciones sobre producción requieren una autorización posterior y no se realizaron aquí.

Cambios de esta etapa: `seguridad_web.py`, nueva batería `tests/test_migracion005.py`, este informe y referencia en OPERACION.md. La verificación inicial terminó sin commit; el cierre local posterior se documenta a continuación. Sin push, merge ni modificación de main. Sin acceso al servidor, bases reales o respaldos históricos. No se cambiaron arquitectura, permisos institucionales, dependencias de producción ni reglas de asistencia/calendario.


## Revalidación y cierre local — 19-11-2026

Se revisaron el diff completo y los dos archivos nuevos antes de incorporarlos. La lectura del reloj permanece después de adquirir BEGIN IMMEDIATE y antes de consultar/actualizar la actividad. La regresión determinista comprueba que una actualización confirmada por otra conexión durante la espera no revoca la sesión. La batería compara todas las filas previas y secuencias, conserva los registros de seguridad al repetir 005 y exige que las consultas reales de Gunicorn sean atendidas por los dos o tres PIDs previstos.

Se repitió el comando completo con Python 3.12.16 y Gunicorn opcional habilitado: **71 pruebas, 19.291 segundos, OK, sin omisiones**. Pasaron nuevamente las configuraciones de dos workers y tres con preload, revocación y límites compartidos. Registro completo fuera del repositorio: `/home/coffeewitch/Work/MPAZ-migracion005-20261119/revalidacion-precommit.log`.

Se revisaron los cuatro archivos que componen el cambio, incluidos los valores literales de pruebas, y se buscaron formatos habituales de tokens, claves privadas, credenciales en URL, correos y RUT numéricos. No se identificaron secretos reales ni información personal nueva. Las cuentas y claves de prueba están marcadas como ficticias; los hashes se generan durante la ejecución. Solo se incorporan fuentes y Markdown: ninguna base, .env, log, caché o archivo temporal. Los respaldos históricos ya versionados no fueron abiertos ni modificados.

El cierre autorizado consiste en un commit exclusivamente local sobre `audit/seguridad-continuidad-20261116`; su identificador se obtiene de Git tras crearlo. El plan de carga RFID se preparará después de guardar este trabajo, fuera del repositorio para mantener limpio el árbol. No se ejecutaron escenarios nuevos de 10, 50 o 100 lecturas.
