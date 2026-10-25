# Evidencias del sistema y la aplicación — Fase 2

## Evidencias disponibles para revisión

| Archivo | Resultado documentado | Límite |
|---|---|---|
| [Comunicación ESP32–API](API_01_ESP32_Envio_Lectura_HTTP200.png) | Lectura de UID, evento_id, envío JSON, HTTP 200 y respuesta de la API | La respuesta comienza «El alumno ya…». No demuestra inserción de una asistencia nueva. |
| [Prevención de evento repetido](API_02_Evento_Repetido_Sin_Duplicados.png) | Resultado evento_repetido, 7 registros antes y 7 después | Prueba aislada en COPIA DE PRUEBAS; no certifica todos los casos de asistencia duplicada diaria. |
| [Montaje ESP32 y PN532](HARDWARE_01_ESP32_PN532_Montaje.jpeg) | Hardware y conexiones | La fotografía no demuestra transmisión ni inserción. |
| [Tarjeta de prueba y lector](HARDWARE_02_Tarjeta_Prueba_PN532.jpeg) | Vista del ESP32 y PN532 conectados; la tarjeta se ve en la fotografía 1 | La respuesta de lectura se respalda por separado en el monitor serie. |

Estas capturas están documentadas y **pendientes de revisión docente**. Adicionalmente, el equipo informó el 25-10-2026 una prueba en terminal de Flask y SQLite temporal que se registra a continuación; no la confundimos con ejecución en la escuela.

## Evidencia de simulación reciente

[Prueba Ficha 05 — API y SQLite temporal (25-10-2026)](F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md): entrada de prueba (0→1), mismo evento en SQLite, prevención de evento repetido (1→1), rechazo de tótem inactivo (403), rechazo sin clave (401) y GET /estado (200). **Transcripción facilitada por el equipo**, TXT original aún por subir. No emplea ESP32 físico.

## Evidencias aún pendientes

- GET /estado **en el servicio desplegado** (en simulación test_client ya se informó HTTP 200).
- Nueva asistencia **desde el tótem físico** correlacionando lectura, evento y registro SQLite (la simulación ya demostró el flujo API→SQLite).
- Otros casos de duplicados diarios y validaciones de tarjetas/tótems.
- Login y panel de asistencias con datos ficticios.
- Exportación y apertura de reporte Excel.
- Piloto escolar, validación de extremo a extremo y cierre completo.
- Dominio, HTTPS y roles docentes, si corresponden al alcance; no se consideran implementados ni aprobados.

[Inventario de anexos](../README_EVIDENCIAS_2.4.md) · [Plan de evidencias](../PLAN_EVIDENCIAS_PENDIENTES.md).

Código existente: [API](../../../../../api.py), [procesamiento](../../../../../procesar_lectura_totem.py), [panel](../../../../../interfaz_prueba/), [pruebas](../../../../../probar_api_automaticamente.py). Utilizar datos ficticios y omitir credenciales y datos reales del alumnado.
