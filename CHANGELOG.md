# Registro de cambios

## Saneamiento documental de sesiones docentes — 26 de noviembre de 2026

Cambios documentales en `feature/paso68h-sesiones-docentes-admin`; no se modificó código de aplicación ni se desplegó:

- Añadido `documentacion/tecnica/SESIONES_DOCENTES.md` con flujo docente, estados, permisos, separación RFID/aula, rutas, consulta administrativa y límites.
- Actualizado `API.md` con las rutas `/panel/sesiones-docentes` y `/panel/sesiones-docentes/<int:sesion_id>`, además de contratos de las operaciones docentes.
- Clasificados los seis SQLite históricos ya versionados como fixtures ficticios según confirmación expresa del responsable del proyecto. Se conservan; no se incorporaron bases nuevas ni se alteró el historial.
- Actualizados README e instrucciones de instalación para señalar la rama de trabajo y el estado real de la evidencia de pruebas.
- Documentada la automatización disponible `tests/navegador_paso65.py`; no se marcó como ejecutada ni aprobada.
- Conteo estático de la rama: 78 métodos `test_*` en 10 módulos Python. El último resultado documentado anterior a la integración es de 75 pruebas Python y tres programas JS aprobados el 19-11-2026. No se encontró ejecución posterior al commit de integración ni workflow de GitHub Actions asociado.
- No se modificaron `main`, bases de datos, credenciales, configuración, servidor escolar ni infraestructura.

## Continuación de auditoría — 16 de noviembre de 2026

Implementado y probado localmente; no desplegado:

- Limitación persistente de login entre workers, compartida para Administración/Dirección/Seguimiento, y ámbito docente; 429 y recuperación temporal.
- Sesiones registradas y revocables con duración absoluta/inactividad, detección de cambio de credencial/rol y revalidación al emitir sesión. Migración aditiva 005, aplicada solo en pruebas.
- Construcción segura de tablas/resultados/resúmenes dinámicos; HTML constante y escape de ficha conservados.
- Tokens Unicode y JSON anidado incorrectos rechazados sin errores internos.
- Reloj America/Santiago para flujos activos, fechas/horas del frontend y pruebas DST. Históricos intactos.
- Actor individual en auditoría de calendario, timeout de reenvío y vista previa ficticia para QA manual.
- Batería ampliada a 61 métodos Python y tres programas JS, verificada en Python 3.12.16 y 3.14.8. Cinco métodos caracterizan defectos de calendario pendientes, sin aprobarlos como reglas correctas.
- Revisión privada de estructura/procedencia de seis respaldos históricos: autenticidad de todos sus datos todavía sin certificar. No se eliminaron ni publicaron.

Requiere revisión/autorización: reglas del calendario, parámetros operativos de sesiones/proxy, migración y despliegue de producción. QA visual no ejecutada por navegador inaccesible.

## Auditoría de desarrollo — 16 de noviembre de 2026

Referencia inicial: `d0d2c80`, rama estable `integration/seguridad-seguimiento`. Cambios realizados únicamente en `audit/seguridad-continuidad-20261116`; pendientes de revisión e integración.

- Revalidación de identidad docente activa en las solicitudes con sesión.
- CSRF en logout administrativo y docente, con clientes JS correspondientes y URLs de assets actualizadas.
- Rechazo controlado de JSON de tipo incorrecto en rutas administrativas y RFID.
- Respuesta genérica 503 ante `sqlite3.OperationalError` fuera de los manejadores de blueprint existentes.
- Cookies HttpOnly/SameSite=Lax/Secure por defecto; excepción explícita para HTTP local. Cabeceras básicas y no-store en respuestas dinámicas.
- Escape de campos de la ficha administrativa para evitar HTML desde UID u otros datos.
- Exportación CSV neutraliza fórmulas y evita nombres de archivo coincidentes.
- Respaldo SQLite consistente mediante API de backup, permisos privados, nombres únicos, ruta configurable y verificación de integridad y referencias.
- Cola local con exclusión entre hilos/procesos y reemplazo atómico; corrupción explícita sin sobrescritura. El reenvío conserva eventos agregados durante el envío.
- Ampliación preventiva de `.gitignore`; los seis respaldos previamente versionados siguen intactos y requieren revisión privada.
- Pruebas de regresión aisladas y documentación técnica, operativa y de continuidad.

No se cambiaron reglas de asistencia, esquema de producción, datos escolares, roles institucionales ni infraestructura. No se ejecutó despliegue.
