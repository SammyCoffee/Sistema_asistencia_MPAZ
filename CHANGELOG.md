# Registro de cambios

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
