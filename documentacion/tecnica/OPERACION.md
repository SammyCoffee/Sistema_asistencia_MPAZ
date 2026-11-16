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

1. Revisar commits de `audit/seguridad-continuidad-20261116`, ejecutar pruebas en Python 3.12 y resolver el tratamiento de bases ya rastreadas antes de cualquier publicación. No fusionar automáticamente.
2. Revisar aprobación institucional de reglas pendientes: calendario, cierre fuera de horario y sesiones. Esta rama no modifica esas reglas.
3. Preparar una nueva carpeta de release desde el commit aprobado. No editar release activa ni repositorio principal del servidor.
4. Reutilizar configuración privada del servidor sin imprimirla ni trasladarla. Verificar que `MPAZ_COOKIE_SECURE` permanezca activado para HTTPS. Probar el login local HTTP solo con `MPAZ_COOKIE_SECURE=0` en desarrollo.
5. No requiere cambios de esquema esta corrección. No ejecutar migraciones históricas. Revisar nuevas dependencias si se añaden en otra versión.
6. Comprobar respaldo reciente con prueba de recuperación y obtener autorización expresa antes de cambiar el drop-in de systemd, hacer daemon-reload o reiniciar Gunicorn.
7. Al desplegar, publicar juntos backend y JS: el cierre de sesión ahora exige CSRF. Verificar que el navegador reciba las versiones nuevas; un cliente antiguo podría no poder cerrar sesión desde su botón.
8. Tras autorización y despliegue, verificar estado, login/roles, sesión, assets y errores con cuentas institucionales de prueba aprobadas. No registrar lecturas ficticias contra datos escolares.

## Reversión

Conservar carpeta y configuración anterior, y anotar HEAD antes del cambio. Si falla la validación, revertir únicamente la referencia de release a la versión aprobada anterior, tras autorización para systemd/reinicio. Estas correcciones no tienen migraciones y no exigen restaurar SQLite. Volver a una versión anterior también reintroduce sus vulnerabilidades; evaluar el riesgo antes de hacerlo.
