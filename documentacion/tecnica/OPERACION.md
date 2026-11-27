# Operación, respaldos y despliegue controlado

Este documento describe un procedimiento para revisión humana. **No se ejecutó ningún despliegue, cambio de entorno, migración, respaldo de producción ni reinicio de servicio durante la auditoría.**

## Estado observado por SSH el 16-11-2026

- `mpaz-rfid.service`: activo y ejecutándose.
- Directorio efectivo: `/home/mpaz-server/Proyectos/mpaz-versiones/release_d0d2c80_20261106`.
- HEAD: `d0d2c807710066fc41f5fe1922f4452c258b8270`; sin cambios informados por Git.
- Existe versión anterior `release_b1ec810_20261030`.
- Existen `/etc/systemd/system/mpaz-rfid.service.d/90-mpaz-release.conf`, `/etc/mpaz-rfid.env` y la ruta histórica `.../Sistema_asistencia_MPAZ/data/asistencia.db`. No se leyó su contenido.
- No se pudo confirmar el respaldo histórico `.../pre_cambio_d0d2c80_20261106_184652/asistencia.db` mediante el usuario SSH: el chequeo no devolvió existencia. Puede faltar permiso de recorrido; no afirmar que fue eliminado.
- No se certificaron configuración Nginx, timers, retención, versión de Gunicorn ni integridad de la base real.

El repositorio antiguo `~/Proyectos/Sistema_asistencia_MPAZ` estaba en `a356117` y contenía respaldos no rastreados. No es la versión efectiva del servicio; no sobrescribirlo.

## Respaldo seguro

El script corregido respeta `MPAZ_DB_PATH`, usa `Connection.backup()` con origen abierto en modo de solo lectura, reserva un archivo único con permisos 0600 y comprueba `integrity_check` y `foreign_key_check` en el destino. Esto incluye transacciones confirmadas en WAL; `shutil.copy2` del archivo principal no lo garantizaba. Referencia: [API SQLite de Python](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup).

Probar primero con la base ficticia. La ejecución contra producción necesita autorización y una ventana acordada. No copiar bases a desarrollo ni subirlas a Git.

El éxito devuelve la ruta del respaldo. La ausencia de archivo original actualmente imprime aviso y retorna `None`; falta convertirlo en un resultado inequívoco para monitorización. Si falla verificación, no utilizar el archivo parcial como copia válida. No hay eliminación automática ni retención implementada. Un servicio de respaldo debería registrar estado y alertar sin datos personales.

## Recuperación

1. Con autorización, identificar versión exacta de aplicación, esquema y respaldo verificado; calcular y conservar hash de la copia en un registro privado.
2. Ensayar recuperación sobre una **copia ficticia o entorno privado autorizado**, nunca sobre la base escolar activa. Abrir la copia y ejecutar integridad, llaves foráneas, conteos y pruebas funcionales.
3. Medir RPO (último dato conservado) y RTO (tiempo hasta validación). No se han definido objetivos institucionales.
4. En una restauración real, detener escrituras durante ventana autorizada, preservar base actual y auxiliares WAL/SHM, y restaurar mediante procedimiento SQLite aprobado. No mezclar un `.db` restaurado con un WAL de otra versión.
5. Verificar permisos de archivo, usuario del servicio y compatibilidad del esquema antes de retomar tráfico.

No se proporcionan comandos de sobrescritura automática. Un rollback de código no implica restauración de datos.

## Integración y despliegue propuesto

1. Revisar el diff de `feature/paso68h-sesiones-docentes-admin` frente a su commit padre y validar la documentación de sesiones docentes. Mantener la revisión separada de `main`; no fusionar automáticamente. Los seis SQLite versionados se clasifican como ficticios según confirmación del responsable del proyecto, pero `.gitignore` no los elimina del historial.
2. Revisar aprobación institucional de calendario, cierre fuera de horario y plazos de sesión. La continuación propone plazos de sesión; no cambia las reglas de asistencia.
3. Preparar una nueva carpeta de release desde el commit aprobado. No editar release activa ni repositorio principal del servidor.
4. Reutilizar configuración privada del servidor sin imprimirla ni trasladarla. Verificar que `MPAZ_COOKIE_SECURE` permanezca activado para HTTPS. Probar el login local HTTP solo con `MPAZ_COOKIE_SECURE=0` en desarrollo.
5. La primera corrección 20e404c no requería esquema nuevo; la continuación sí requiere la migración aditiva 005. No ejecutar migraciones históricas ni el bucle completo sobre producción. Ver procedimiento siguiente.
6. Comprobar respaldo reciente con prueba de recuperación y obtener autorización expresa antes de cambiar el drop-in de systemd, hacer daemon-reload o reiniciar Gunicorn.
7. Al desplegar, publicar juntos backend y JS: el cierre de sesión ahora exige CSRF. Verificar que el navegador reciba las versiones nuevas; un cliente antiguo podría no poder cerrar sesión desde su botón.
8. Tras autorización y despliegue, verificar estado, login/roles, sesión, assets y errores con cuentas institucionales de prueba aprobadas. No registrar lecturas ficticias contra datos escolares.

## Sesiones docentes y consulta administrativa

La rama incorpora el módulo de sesiones docentes y el blueprint de consulta administrativa. El detalle funcional y los contratos están en [SESIONES_DOCENTES.md](SESIONES_DOCENTES.md) y [API.md](API.md).

Antes de desplegarlo:

1. Comprobar por separado que el esquema institucional efectivo contenga las tablas docentes `profesores_cursos`, `sesiones_clase` y `asistencias_clase`, compatibles con el candidato. Estas tablas se definen en `base_datos.crear_tablas()` y **no** son creadas por la migración 004, que corresponde a operadores de Seguimiento Escolar. Verificar asimismo la presencia/compatibilidad de `web_login_intentos` y `web_sesiones`, que pertenecen a la migración 005. Si faltan tablas docentes, detener el despliegue y diseñar una regularización separada con autorización y respaldo; **no** ejecutar `crear_tablas()` ni reaplicar 004 automáticamente en producción. Aplicar 005 solo tras autorización específica.
2. Validar cuentas y asignaciones de docentes con usuarios de prueba institucionales autorizados; no usar datos reales en la vista ficticia.
3. Verificar que un docente solo consulte y gestione sus propias asignaciones, sesiones y estudiantes del curso autorizado.
4. Verificar que Administración pueda consultar el resumen y que Dirección no acceda al blueprint administrativo de sesiones.
5. Confirmar que las marcas de aula no alteren la tabla `asistencias` de RFID y que los estudiantes sin marca no se clasifiquen automáticamente como ausentes.
6. Publicar backend y assets del portal docente/administrativo como una misma release, después de pruebas y autorización.

La automatización Chromium `tests/navegador_paso65.py` está disponible, pero su existencia no acredita ejecución. Ver requisitos, comando y límites en [QA_MANUAL.md](QA_MANUAL.md). La revisión documental de esta rama no ejecutó navegador, migraciones ni operaciones en producción.

## Reversión

Conservar carpeta y configuración anterior, y anotar HEAD antes del cambio. Si falla la validación, revertir únicamente la referencia de release a la versión aprobada anterior, tras autorización para systemd/reinicio. La primera entrega no tenía migración; la continuación añade tablas de seguridad que pueden conservarse sin uso al revertir código. No exige restaurar ni eliminar SQLite. Volver a una versión anterior también reintroduce sus vulnerabilidades; evaluar el riesgo antes de hacerlo.

## Continuación: puerta de despliegue de seguridad persistente

**Requiere autorización; no ejecutado en el servidor.** El acceso a producción no se repitió en esta continuación; las rutas/estado anteriores son antecedentes, no una certificación actual.

1. Revisar `migraciones/005_seguridad_web.sql` y el diff de seguridad. La migración tiene BEGIN IMMEDIATE/COMMIT, CREATE IF NOT EXISTS e índices; dos ejecuciones sobre la base ficticia conservan alumnos y estructura. No hay DROP/ALTER/UPDATE de tablas escolares.
2. Antes de autorizar aplicación, comprobar de forma privada ruta real, esquema previo, espacio, permisos y respaldo/restauración verificados. No copiar datos escolares al notebook.
3. Aplicar **solo 005**, mediante procedimiento autorizado y sobre la base correcta. No ejecutar 004 otra vez. Conservar resultado de integridad y esquema sin imprimir registros ni credenciales. No se crea estructura automáticamente desde Flask.
4. Revisar `MPAZ_SESION_MAX_SEGUNDOS` (28800) y `MPAZ_SESION_INACTIVIDAD_SEGUNDOS` (1800), expiración y uso de polling. Confirmar la cadena proxy; el límite IP usa remote_addr y puede agrupar usuarios si todas las conexiones provienen de Nginx. No activar confianza en cabeceras sin revisión.
5. Medir carga con múltiples workers y datos ficticios: autenticación/actividad añaden escrituras SQLite. Verificar 429 y recuperación automática, cookies copiadas tras logout, cambio de contraseña y cuentas inactivas. No se actualiza Gunicorn ni se cambia journal/firewall/Tailscale como parte de esta entrega.
6. Publicar juntos backend, dom-seguro.js, tiempo-escolar.js y HTML/JS con versiones nuevas. Verificar Python 3.12 y disponibilidad de ZoneInfo America/Santiago. Los usuarios deberán reautenticarse: cookies anteriores no tienen registro de servidor.
7. Para revertir código, preservar las tablas nuevas y la base. La versión anterior no aplicará revocación persistente y reintroducirá sus limitaciones; registrar ese riesgo. No borrar tablas ni restaurar una base como efecto automático de rollback.

Estado de pruebas al revisar la rama el 26-11-2026: el árbol contiene estáticamente 78 métodos `test_*` en 10 módulos Python. El último resultado de ejecución documentado es de 75 pruebas Python aprobadas y tres programas JS aprobados el 19-11-2026, antes del commit de integración `054075b05fe192d4dcda6ee6a993d067d381a1fe`. No se encontró una ejecución posterior para ese commit ni ejecuciones de GitHub Actions asociadas. Por tanto, ejecutar de nuevo la batería completa en un entorno ficticio antes de aprobar una release. Cinco métodos de caracterización siguen describiendo defectos de calendario pendientes; no los convierten en reglas institucionales aprobadas.


## Verificación local de la migración 005 en Caldero — 19-11-2026

Ver [informe y reproducción](MIGRACION_005_VERIFICACION_20261119.md). Se verificaron conservación exacta de datos ficticios sobre el esquema d0d2c80, repetición, errores/rollback, sesiones y Gunicorn local con dos workers y tres con preload. Las 71 pruebas pasaron tras corregir una carrera de actividad de sesión en `seguridad_web.py`; esa corrección debe acompañar al backend de la release. El SQL 005 no cambió.

Antes de una futura aplicación, confirmar ausencia o estructura exacta de objetos homónimos: IF NOT EXISTS no valida compatibilidad. El ejecutor debe abortar y hacer rollback ante cualquier error, sin continuar hasta COMMIT. La reversión a d0d2c80 conserva compatibilidad estructural, pero reintroduce la reutilización de cookies tras logout. No hubo acceso a producción; permanecen las condiciones de autorización, respaldo/restauración y validación operativa de este documento.


## Carga RFID local en Caldero — 19-11-2026

Ver [resultados y reproducción](CARGA_RFID_20261119.md). Se verificaron ráfagas de 10, 50 y 100 lecturas, cinco repeticiones con 1/2/3 workers sync, sobre SQLite ficticio en tmpfs y Btrfs. Se conciliaron API, registros y cola, con duplicados, antirrebote, rechazos, bloqueo, pérdida de respuesta y reenvíos simultáneos. El máximo ensayado es 100 emisores en ráfaga; no acredita capacidad sostenida ni resultados del servidor escolar.

El reenvío ahora requiere un resultado funcional confirmado, conserva rechazos/errores ambiguos y controla respuestas cortadas o inválidas. Lectura repetida y jornada completa siguen siendo resultados terminales de las reglas actuales, sin promesa de nueva fila. Los rechazos retenidos necesitan tratamiento operativo; el instante original de eventos offline sigue pendiente. Batería posterior: 75 pruebas Python aprobadas y los tres programas JS aprobados. No se modificaron 005, reglas escolares ni configuración de producción.
