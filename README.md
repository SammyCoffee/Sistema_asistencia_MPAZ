# Sistema MPAZ RFID

Plataforma de asistencia escolar de la Escuela Escritora Marcela Paz, San Bernardo, Chile. El sistema existente registra entradas y salidas mediante tarjetas RFID, administra estudiantes, tarjetas y tótems, y ofrece portal docente, calendario y Seguimiento Escolar.

## Arquitectura actual

```text
ESP32 + PN532 → HTTP /lectura → Flask (api:app) → SQLite
                                      ↑
Navegador → Cloudflare / Nginx → Gunicorn + systemd
```

El frontend está en `interfaz_prueba/` (el nombre es histórico: también se sirve en producción). `main.py` no inicia la aplicación; el punto de entrada WSGI es `api:app`.

- Backend: Python, Flask y Werkzeug; SQLite mediante biblioteca estándar.
- Frontend: HTML, CSS y JavaScript sin compilación.
- Importaciones Excel: openpyxl. Exportación HTTP existente: CSV.
- Hardware descrito: ESP32 DevKit V1 y PN532. `lector_nfc.py` es una entrada manual por consola, no un controlador del PN532. Este repositorio no contiene firmware ESP32 verificado.
- Producción: https://asistencia.empaz.cl. Nunca usarla para pruebas ficticias.

## Desarrollo y pruebas

Consulta [instalación de desarrollo](README_INSTALACION.md) antes de ejecutar scripts. No necesitas bases ni credenciales escolares.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
node tests/test_interfaz.cjs
```

Las pruebas usan bases temporales vacías, cuentas ficticias y migraciones SQL 001–004. No ejecutar por descubrimiento los scripts históricos `probar_*.py`: algunos escriben datos al importarse o consultan un servidor configurable.

## Documentación técnica

- [Auditoría, evidencias y pendientes](documentacion/tecnica/AUDITORIA_20261116.md).
- [Arquitectura y matriz de permisos](documentacion/tecnica/ARQUITECTURA.md).
- [Inventario de archivos y funciones Python](documentacion/tecnica/INVENTARIO_CODIGO.md).
- [Tablas, relaciones e índices](documentacion/tecnica/BASE_DATOS.md).
- [Rutas API y contratos principales](documentacion/tecnica/API.md).
- [Respaldos, recuperación, despliegue y reversión](documentacion/tecnica/OPERACION.md).
- [Propuesta PostgreSQL y siguientes versiones](documentacion/tecnica/CONTINUIDAD.md).
- [Registro de cambios de esta auditoría](CHANGELOG.md).

`MANUAL_TECNICO.md` e `INFORME_EJECUTIVO_RECTOR.md` son antecedentes; algunas descripciones corresponden a versiones antiguas. La auditoría distingue comportamiento probado de alcance pendiente.

## Datos privados

No añadir `.env`, credenciales, bases, reportes ni datos personales a Git. Se detectaron seis respaldos `.db` que **ya estaban versionados** en la referencia: `.gitignore` no los retira del historial. No se abrieron ni eliminaron durante esta auditoría. Su revisión privada y eventual saneamiento requieren un procedimiento acordado antes de publicar nuevas copias.

Ninguna corrección de esta rama se considera desplegada por aparecer en Git. No ejecutar migraciones ni reiniciar producción sin autorización.
