# Evidencias del sistema y la aplicación — Fase 2

## Evidencias disponibles para revisión

| Archivo | Resultado documentado | Límite |
|---|---|---|
| [Comunicación ESP32–API](API_01_ESP32_Envio_Lectura_HTTP200.png) | Lectura de UID, evento_id, envío JSON, HTTP 200 y respuesta de la API | La respuesta comienza «El alumno ya…». No demuestra inserción de una asistencia nueva. |
| [Prevención de evento repetido](API_02_Evento_Repetido_Sin_Duplicados.png) | Resultado evento_repetido, 7 registros antes y 7 después | Prueba aislada en COPIA DE PRUEBAS; no certifica todos los casos de asistencia duplicada diaria. |
| [Montaje ESP32 y PN532](HARDWARE_01_ESP32_PN532_Montaje.jpeg) | Hardware y conexiones | La fotografía no demuestra transmisión ni inserción. |
| [Tarjeta de prueba y lector](HARDWARE_02_Tarjeta_Prueba_PN532.jpeg) | Vista del ESP32 y PN532 conectados; la tarjeta se ve en la fotografía 1 | La respuesta de lectura se respalda por separado en el monitor serie. |

Son pruebas documentadas recibidas, **pendientes de revisión docente**. No se ejecutaron pruebas nuevas al incorporar estos archivos.

## Evidencias aún pendientes

- GET /estado.
- Nueva asistencia registrada desde el tótem, correlacionando solicitud, evento y registro SQLite.
- Otros casos de duplicados diarios y validaciones de tarjetas/tótems.
- Login y panel de asistencias con datos ficticios.
- Exportación y apertura de reporte Excel.
- Piloto escolar, validación de extremo a extremo y cierre completo.
- Dominio, HTTPS y roles docentes, si corresponden al alcance; no se consideran implementados ni aprobados.

[Inventario de anexos](../README_EVIDENCIAS_2.4.md) · [Plan de evidencias](../PLAN_EVIDENCIAS_PENDIENTES.md).

Código existente: [API](../../../../../api.py), [procesamiento](../../../../../procesar_lectura_totem.py), [panel](../../../../../interfaz_prueba/), [pruebas](../../../../../probar_api_automaticamente.py). Utilizar datos ficticios y omitir credenciales y datos reales del alumnado.
