# Sistema MPAZ RFID

Plataforma de asistencia escolar de la Escuela Escritora Marcela Paz, San Bernardo, Chile. El sistema registra entradas y salidas mediante tarjetas RFID, administra estudiantes, tarjetas y tótems, y ofrece portal docente, sesiones de asistencia de aula, consulta administrativa de sesiones, calendario y Seguimiento Escolar.

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
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
node tests/test_interfaz.cjs
node tests/test_dom_seguro.cjs
node tests/test_tiempo_escolar.cjs
```

Las pruebas usan bases temporales vacías, cuentas ficticias y migraciones SQL 001–005. No ejecutar por descubrimiento los scripts históricos `probar_*.py`: algunos escriben datos al importarse o consultan un servidor configurable.

## Documentación técnica

- [Continuación: correcciones, Python 3.12 y pendientes](documentacion/tecnica/AUDITORIA_CONTINUACION_20261116.md).
- [Seguridad persistente y permisos](documentacion/tecnica/SEGURIDAD_WEB.md).
- [Calendario: decisiones institucionales pendientes](documentacion/tecnica/CALENDARIO_DECISIONES.md).
- [Comprobación visual manual](documentacion/tecnica/QA_MANUAL.md).
- [Auditoría, evidencias y pendientes](documentacion/tecnica/AUDITORIA_20261116.md).
- [Arquitectura y matriz de permisos](documentacion/tecnica/ARQUITECTURA.md).
- [Inventario de archivos y funciones Python](documentacion/tecnica/INVENTARIO_CODIGO.md).
- [Tablas, relaciones e índices](documentacion/tecnica/BASE_DATOS.md).
- [Rutas API y contratos principales](documentacion/tecnica/API.md).
- [Flujo de sesiones docentes y consulta administrativa](documentacion/tecnica/SESIONES_DOCENTES.md).
- [Respaldos, recuperación, despliegue y reversión](documentacion/tecnica/OPERACION.md).
- [Propuesta PostgreSQL y siguientes versiones](documentacion/tecnica/CONTINUIDAD.md).
- [Registro de cambios de esta auditoría](CHANGELOG.md).

`MANUAL_TECNICO.md` e `INFORME_EJECUTIVO_RECTOR.md` son antecedentes; algunas descripciones corresponden a versiones antiguas. La auditoría distingue comportamiento probado de alcance pendiente.

## Datos privados

No añadir `.env`, credenciales, bases, reportes ni datos personales a Git. Los seis archivos SQLite históricos que ya estaban versionados en esta rama se clasifican como **bases ficticias de prueba**, según confirmación expresa del responsable del proyecto. Por esa razón no se eliminan en este saneamiento. Esta clasificación procede de dicha confirmación; no equivale a una auditoría forense independiente. `.gitignore` evita incorporar nuevos archivos coincidentes, pero no deja de rastrear archivos que ya están versionados ni los borra del historial. No agregar nuevas bases ni copiar estos fixtures al servidor escolar.

Ninguna corrección de esta rama se considera desplegada por aparecer en Git. No ejecutar migraciones ni reiniciar producción sin autorización.

## Estado de la siguiente versión

La rama de auditoría requiere migración **005** para límites de login y sesiones persistentes. No desplegar solo el código: revisar y autorizar migración/release según OPERACION.md. Cookies antiguas exigirán login nuevo. Las reglas de calendario tienen defectos reproducidos pendientes de decisión; una suite aprobada no convierte esas reglas en cálculos institucionales correctos.
