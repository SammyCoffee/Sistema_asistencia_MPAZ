# Carga RFID local en Caldero — 19-11-2026

## Resultado y límites

Se ejecutó el plan sobre el commit base `5541554184715d91c92e3c89b47dd25581b6ed19`, en su rama de auditoría. **Las ráfagas de 10, 50 y 100 lecturas válidas de tarjetas distintas quedaron registradas y conciliadas con SQLite, con uno, dos y tres workers sync.** Hubo cinco repeticiones por combinación y fixtures nuevos por escenario. No se encontraron pérdidas ni efectos duplicados sin explicación en la matriz ejecutada después de corregir el reenvío.

Se completaron 603 casos/etapas en tmpfs y 612 en Btrfs (incluidos casos de recuperación sin nuevos reintentos). La segunda matriz agrega nueve casos de altas durante reenvío. En Btrfs se instrumentaron 35.538 solicitudes completadas por la API en las etapas medidas; se excluyen health checks, login, controles iniciales y entradas preparatorias del escenario de salida. Los 18 HTTP 503 de esa matriz fueron intencionados y se recuperaron. Los conteos no representan una única base acumulada: cada escenario tiene datos aislados. Las bases/colas se crearon y eliminaron exclusivamente en directorios temporales propios.

El máximo ensayado fue **100 emisores concurrentes**, no el máximo absoluto de la arquitectura. Una ráfaga superada no acredita carga sostenida ni latencia del servidor escolar. Cliente, servidor y generador comparten Caldero; loopback excluye LAN, TLS y proxy escolar, y la instrumentación tiene coste. La serie inicial en /tmp usa RAM; las cifras principales siguientes corresponden al almacenamiento Btrfs de Work.

## Entorno y recorrido probado

Python 3.12.16, SQLite 3.53.1, Gunicorn 27.0.1 de ensayo en /tmp, Linux 7.2.15-1-omarchy, 12 CPU lógicas. SQLite: journal DELETE, synchronous=2 (FULL), busy_timeout=5000 ms. No se modificó configuración del producto ni del sistema operativo.

Entrada: `POST /lectura`, con API key exclusivamente ficticia y payload `codigo_totem`, `uid`, `evento_id`. Recorrido: validar tótem → procesar tarjeta/alumno → cierre vigente → guardar asistencia en transacción BEGIN IMMEDIATE. El fixture incluye 201 estudiantes y tarjetas ficticias, tótem autorizado, tarjeta bloqueada y estudiante inactivo. Cuentas de control ficticias comprueban sesión bajo tráfico mixto.

Gunicorn escucha en TCP solo 127.0.0.1, puertos efímeros, workers sync 1/2/3, timeout de worker 30 s. La versión final del harness deshabilita además el socket Unix de control predeterminado de Gunicorn para evitar colisiones con otros ensayos; esta opción se validó en el complemento final. La serie no cambia preload; la compatibilidad con preload corresponde al ensayo de migración 005 y a la batería de regresión. El reloj del wrapper temporal fija 08:00 Chile; las salidas avanzan a 08:01. No se modificaron calendario, cierre ni antirrebote. No se usaron dispositivos RFID reales.

## Ráfagas válidas en disco: mediciones reales

Cada fila reúne cinco ráfagas. Media y P95 se calculan sobre las muestras de cliente de esas cinco ejecuciones. Tiempo total es el promedio de duración completa de una ráfaga, incluida preparación de emisores/barrera; throughput es N dividido por ese promedio. Recibidas significa solicitudes completadas por Flask e instrumentadas, no conexiones TCP meramente abiertas.

| Lecturas por ráfaga | Workers | Enviadas / recibidas / entradas | Media ms | P95 ms | Tiempo total medio s | Lecturas/s por ráfaga |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 1 | 50 / 50 / 50 | 42.97 | 73.65 | 0.076 | 131.7 |
| 10 | 2 | 50 / 50 / 50 | 49.29 | 94.38 | 0.092 | 108.9 |
| 10 | 3 | 50 / 50 / 50 | 47.30 | 85.90 | 0.088 | 113.1 |
| 50 | 1 | 250 / 250 / 250 | 181.65 | 334.09 | 0.358 | 139.7 |
| 50 | 2 | 250 / 250 / 250 | 181.95 | 333.74 | 0.368 | 136.0 |
| 50 | 3 | 250 / 250 / 250 | 194.62 | 342.39 | 0.396 | 126.3 |
| 100 | 1 | 500 / 500 / 500 | 376.98 | 688.33 | 0.744 | 134.5 |
| 100 | 2 | 500 / 500 / 500 | 357.90 | 658.34 | 0.717 | 139.4 |
| 100 | 3 | 500 / 500 / 500 | 361.60 | 669.64 | 0.767 | 130.3 |

En estas ráfagas: cero rechazos, duplicados, errores HTTP o pérdidas. Se comprobó cada `evento_entrada_id`, alumno, fecha/hora y tótem; no hubo salidas. Las muestras completas y P99/dispersiones por lote se conservan fuera de Git. No se mezclan las latencias servidor de reenvíos multiproceso con las latencias cliente de esta tabla.

## Matriz funcional y conciliación en Btrfs

La columna HTTP incluye rechazos previstos y errores inyectados, separados por estado. El valor 0 es un fallo de transporte del cliente, no un código HTTP. En desconexión/respuesta perdida se suman primer envío y recuperación. En reenvío multiproceso se cuentan las solicitudes observadas por el servidor; son reintentos secuenciales por cada uno de los dos procesos, no otra ráfaga de N hilos.

| Escenario | Casos | Intentos medidos / recibidos | Resultados funcionales | HTTP/transporte |
|---|---:|---:|---|---|
| unicos | 45 | 2400 / 2400 | entrada_registrada: 2400 | {'200': 2400} |
| duplicados | 45 | 2400 / 2400 | entrada_registrada: 45; evento_repetido: 2355 | {'200': 2400} |
| mezcla | 45 | 2400 / 2400 | entrada_registrada: 1200; evento_repetido: 1200 | {'200': 2400} |
| antirrebote | 45 | 2400 / 2400 | entrada_registrada: 45; lectura_repetida: 2355 | {'200': 2400} |
| salida | 45 | 2400 / 2400 | salida_registrada: 2400 | {'200': 2400} |
| rechazos | 45 | 2400 / 2400 | alumno_inactivo: 795; tarjeta_bloqueada: 825; totem_no_autorizado: 780 | {'200': 1620, '403': 780} |
| mixto | 45 | 2400 / 2400 | entrada_registrada: 2400 | {'200': 2400} |
| bloqueo_corto | 45 | 2400 / 2400 | entrada_registrada: 2400 | {'200': 2400} |
| recuperacion_bloqueo | 54 | 18 / 18 | entrada_registrada: 18 | {'200': 18} |
| desconexion | 45 | 4800 / 2400 | entrada_registrada: 2400; sin_conexion: 2400 | {'0': 2400, '200': 2400} |
| respuesta_perdida | 45 | 4800 / 4800 | evento_repetido: 2400; sin_conexion: 2400 | {'0': 2400, '200': 2400} |
| reenvio_dos_procesos | 45 | 4800 / 4800 | entrada_registrada: 2400; evento_repetido: 2400 | {'200': 4800} |
| rechazo_pendiente | 45 | 2400 / 2400 | tarjeta_bloqueada: 2400 | {'200': 2400} |
| bloqueo_largo | 9 | 480 / 480 | base_datos_no_disponible: 18; entrada_registrada: 462 | {'200': 462, '503': 18} |
| altas_durante_reenvio | 9 | 1440 / 1440 | entrada_registrada: 960; evento_repetido: 480 | {'200': 1440} |

Los eventos repetidos, lecturas rápidas y jornada completa son decisiones del producto y no se cuentan como nuevas asistencias. Las tarjetas bloqueadas y alumnos inactivos devuelven HTTP 200 con rechazo funcional; un tótem no autorizado devuelve 403. Los ensayos exigen exactamente esos resultados y cero filas en los escenarios rechazados. Dos solicitudes con el mismo ID producen un efecto; las ráfagas de copias comprueban la misma propiedad con 10/50/100 solicitudes.

Cada etapa compara las respuestas de entrada/salida con los identificadores efectivamente almacenados y valida alumno, jornada y tótem, conteos, ausencia de salidas imprevistas, integrity_check=ok y foreign_key_check sin infracciones. Una solicitud API no equivale siempre a una fila: los duplicados y antirrebote deben conciliarse con su clasificación funcional. Los rechazos pendientes se conservan para revisión; no se presentan como entregas exitosas.

## Bloqueos SQLite y recuperación

El escritor ficticio retiene BEGIN IMMEDIATE durante 200 ms o 5,5 s y luego hace rollback. Con 200 ms se esperan las escrituras y terminan todas las lecturas válidas. Con 5,5 s se reproduce `database is locked` en las primeras solicitudes y la API responde 503 sin revelar el error al cliente. Se conserva cada evento fallido en cola y se reenvía tras liberar el bloqueo.

| Workers | Ráfaga | HTTP 503 inyectados | Filas antes → después de reintentar | Máxima ejecución de escritura ms |
|---:|---:|---:|---:|---:|
| 1 | 10 | 1 | 9 → 10 | 5012.85 |
| 1 | 50 | 1 | 49 → 50 | 5013.24 |
| 1 | 100 | 1 | 99 → 100 | 5007.13 |
| 2 | 10 | 2 | 8 → 10 | 5011.33 |
| 2 | 50 | 2 | 48 → 50 | 5014.43 |
| 2 | 100 | 2 | 98 → 100 | 5012.42 |
| 3 | 10 | 3 | 7 → 10 | 5010.71 |
| 3 | 50 | 3 | 47 → 50 | 5012.81 |
| 3 | 100 | 3 | 97 → 100 | 5018.64 |

La instrumentación mide tiempo de ejecución de sentencias de escritura (incluida espera), y por separado BEGIN IMMEDIATE ejecutado por la conexión; no equivale a tiempo puro del lock ni a duración completa de commit. En particular la actualización de última conexión del tótem puede esperar antes de guardar asistencia. No se cambió WAL ni timeout para ocultar bloqueos.

No hubo 500/503 fuera del bloqueo largo inyectado en esta matriz. Los escenarios mixtos conservaron las sesiones válidas durante el tráfico RFID. Integridad y llaves foráneas siguieron correctas y la recuperación llegó al número esperado de registros. Un timeout de SQLite no implica pérdida si el cliente conserva el ID/evento y reintenta; un emisor que descarte el 503 sí presenta un riesgo operativo.

## Desconexión, respuesta perdida y altas concurrentes

Se reservaron puertos de loopback sin listener para producir una conexión rechazada real. Ningún evento llegó a Flask y todos permanecieron en cola hasta la recuperación. Para perder una respuesta después de persistir, un proxy temporal de loopback esperó el resultado real del backend y cerró sin encabezados: el cliente conservó el evento y el reintento devolvió evento_repetido, con una sola entrada y ninguna salida accidental.

Dos procesos de reenvío operaron sobre la misma cola ficticia. En el caso adicional ambos capturan la cola inicial antes de una barrera; al comenzar el reenvío se agregan N eventos nuevos. Tras completar el lote previo se exige que permanezcan exactamente los N nuevos, y después se procesan. Resultado final: 2N registros únicos y cero pendientes válidos, sin sobrescribir altas concurrentes.

Se añadió además un ensayo de timeout real de cliente: 50 ms frente a una respuesta demorada 250 ms después del commit, tres workers y cargas 10/50/100. Sus resultados se conservan en `complemento-final/complemento.jsonl`; conserva los eventos hasta confirmar mediante reenvío. Este timeout pertenece al generador, no cambia los 10 s del reenvío del producto.

## Fallos reproducidos y corrección

Antes de cambiar código, cuatro métodos nuevos reprodujeron ocho fallos y tres errores en subcasos:

- Cualquier HTTP 200 se consideraba confirmado, incluidos error_interno, tarjeta bloqueada o alumno inactivo, permitiendo borrar eventos sin registro.
- Una desconexión sin encabezados escapaba como RemoteDisconnected; el script abortaba antes de continuar con otros pendientes.
- JSON truncado, respuesta no objeto o UTF-8 inválido podían abortar o considerarse éxito.

`reenviar_pendientes.py` ahora confirma solo entrada_registrada, salida_registrada, evento_repetido y las respuestas terminales vigentes lectura_repetida/jornada_completa. Estas dos últimas no prometen una nueva fila: respetan la regla ya existente de descartar esa lectura. Los rechazos/errores/desconocidos quedan pendientes. JSON inválido/no objeto y falta de resultado se tratan como respuesta_invalida; cortes HTTP, reset y timeout se conservan como sin_conexion. La misma matriz de fallas de transporte/rechazos pasó con la corrección, tanto en tmpfs como en disco.

No se cambió ninguna regla de asistencia, calendario, permiso, arquitectura ni la migración 005. Los eventos retenidos por bloqueo/inactividad requieren revisión operativa; no deben reenviarse indefinidamente sin clasificación. Reenviarlos mucho después puede cambiar la fecha/hora que el backend asigna: la semántica del instante offline original sigue pendiente y no se inventó en este ensayo.

## Regresiones y reproducción

Nuevas pruebas: `tests/test_reenvio_confirmacion.py`, cuatro métodos con múltiples subcasos sobre confirmación funcional, resultados terminales, desconexión y contenido inválido. **Batería completa posterior: 75 pruebas aprobadas en Python 3.12.16, 19.262 segundos, sin omisiones**, incluidos los ensayos Gunicorn de sesiones con dos workers y tres con preload. Los tres programas JavaScript también pasaron; el horario se ejecutó bajo UTC y Asia/Tokyo. Las cinco caracterizaciones escolares anteriores siguen describiendo defectos conocidos, no criterios institucionales aprobados.

Harness: `herramientas/carga_rfid.py` y `herramientas/verificar_recuperacion.py`. La ejecución genera únicamente fixtures propios, rechaza optimización Python (sus oráculos usan assert) y requiere un directorio de resultados nuevo. No se materializan bases históricas ni se consulta el servidor escolar.

```bash
# Gunicorn del ensayo ya preparado en /tmp; no es dependencia nueva de producción.
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python herramientas/carga_rfid.py --repo "$PWD" --gunicorn /tmp/mpaz-migracion005-gunicorn --salida /ruta/privada/nueva --repeticiones 5 --disco
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python herramientas/verificar_recuperacion.py --repo "$PWD" --gunicorn /tmp/mpaz-migracion005-gunicorn --salida /ruta/privada/nueva-complemento
PYTHONDONTWRITEBYTECODE=1 MPAZ_TEST_GUNICORN_PATH=/tmp/mpaz-migracion005-gunicorn .venv/bin/python -m unittest discover -s tests -v
```

Evidencia fuera del repositorio: `/home/coffeewitch/Work/MPAZ-carga-20261119/`, con regresion-antes.log, ejecucion.log, disco.log, entorno.json/resultados.jsonl/muestras.jsonl por ejecución, complemento y suite posterior. Las muestras contienen solo identificadores sintéticos y medidas; ninguna clave o cookie. El manejador del producto oculta el detalle SQLite: los logs normales de Gunicorn no lo imprimen. El wrapper temporal del complemento final capturó tres `OperationalError: database is locked` en `complemento-final/errores_sqlite.json`, preservando la respuesta 503 original. Se repitió allí un bloqueo largo de diez lecturas y se recuperaron sus tres rechazos; después se comprobó que otra conexión podía adquirir BEGIN IMMEDIATE. En los tres tamaños, la adquisición de escritura tras recuperación tardó aproximadamente 0,01 ms, sin transacción de escritura retenida. Este complemento no se suma a las 612 etapas de la matriz principal. No se incorporan a Git las bases, colas, trazas o logs.

## Uso escolar: recomendaciones y pendientes

1. El nivel de 100 lecturas fue fiable en las condiciones medidas, con reintento para errores inyectados. No fijar capacidad escolar máxima ni prometer este tiempo sobre red/servidor diferentes. Falta carga sostenida, concurrencia con operación escolar representativa y una meta de latencia acordada.
2. Más workers no crean más escritores SQLite. Comparar la tabla antes de aumentar procesos; medir cola, disco y latencia en un entorno de preproducción autorizado. Este ensayo no autoriza cambiar producción.
3. Exigir evento_id estable y cola duradera en el emisor ante timeout/503; perder una respuesta no permite generar un ID nuevo. No hay certificación de firmware ni cortes eléctricos del hardware.
4. Dar tratamiento explícito a rechazos retenidos, alertar por tamaño/antigüedad de cola y separar HTTP de resultado funcional. Definir la hora original offline antes de usar reenvío retardado como evidencia escolar oficial.
5. Mantener control de respaldos/restauración, métricas de bloqueo/503 y despliegue conjunto de código. No integrar Django/PostgreSQL ni cambiar 005 para resolver lo que aún no se ha medido. WAL o cambios de transacciones requieren una comparación posterior específica, sin tocar reglas institucionales.

Trabajo realizado exclusivamente en Caldero. Sin solicitudes a asistencia.empaz.cl, datos reales, servidor escolar, dispositivos RFID reales, cambios en main, push ni merge.
