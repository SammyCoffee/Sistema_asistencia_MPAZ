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

[Prueba Ficha 05 — API y SQLite temporal (25-10-2026)](F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md): entrada de prueba (0→1), mismo evento en SQLite, prevención de evento repetido (1→1), rechazo de tótem inactivo (403), rechazo sin clave (401) y GET /estado (200). **Prueba facilitada por el equipo; TXT original ya disponible** en el enlace siguiente. No emplea ESP32 físico.

TXT original: [F05_2026-10-25_PRUEBA_SIMULADA_TERMINAL_ORIGINAL.txt](F05_2026-10-25_PRUEBA_SIMULADA_TERMINAL_ORIGINAL.txt). Las capturas DOCENTE_01/02/03 están subidas; enlaces en la carga complementaria.

## Evidencias aún pendientes

- GET /estado **en el servicio desplegado** (en simulación test_client ya se informó HTTP 200).
- Nueva asistencia **desde el tótem físico** correlacionando lectura, evento y registro SQLite (la simulación ya demostró el flujo API→SQLite).
- Otros casos de duplicados diarios y validaciones de tarjetas/tótems.
- Evidencia de login; para el panel ya se dispone de tres capturas docentes, quedando pendiente comprobar persistencia tras recarga.
- Exportación y apertura de reporte Excel.
- Piloto escolar, validación de extremo a extremo y cierre completo.
- Dominio, HTTPS y roles docentes, si corresponden al alcance; no se consideran implementados ni aprobados.

[Inventario de anexos](../README_EVIDENCIAS_2.4.md) · [Plan de evidencias](../PLAN_EVIDENCIAS_PENDIENTES.md).

Código existente: [API](../../../../../api.py), [procesamiento](../../../../../procesar_lectura_totem.py), [panel](../../../../../interfaz_prueba/), [pruebas](../../../../../probar_api_automaticamente.py). Utilizar datos ficticios y omitir credenciales y datos reales del alumnado.


## Carga complementaria Ficha 05 — 25-10-2026

Los cuatro archivos originales están subidos con sus nombres conservados:

- [x] [DOCENTE_01_Sesiones_Asistencia_1A_2026-10-22(1).png](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/DOCENTE_01_Sesiones_Asistencia_1A_2026-10-22(1).png)
- [x] [DOCENTE_02_Registro_Parcial_2_de_5_2026-10-22(1).png](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/DOCENTE_02_Registro_Parcial_2_de_5_2026-10-22(1).png)
- [x] [DOCENTE_03_Sesion_Confirmada_4B_2026-10-21(1).png](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/DOCENTE_03_Sesion_Confirmada_4B_2026-10-21(1).png)
- [x] [Ficha_Avance_05_MPAZ_RFID_003D_ACTUALIZADA_2026-10-25_PARA_ENTREGA(2).docx](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Ficha_Avance_05_MPAZ_RFID_003D_ACTUALIZADA_2026-10-25_PARA_ENTREGA(2).docx)

La [Ficha 05 anterior](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Ficha_Avance_05_MPAZ_RFID_003D_PARA_REVISION.docx) se conserva sin cambios como **borrador histórico**. El Word actualizado es la versión preparada para entrega; revisión y aprobación docente pendientes. Las capturas respaldan sesiones del panel docente, registro parcial 2 de 5 y sesión confirmada. No acreditan por sí solas login, persistencia tras recarga, exportación, piloto ni integración física completa.

El TXT original de terminal y su informe técnico se conservan en sus rutas existentes, sin duplicarlos. Se mantiene la distinción entre simulación API/SQLite y validación física ESP32/PN532; no se recalcula el porcentaje histórico de la Ficha 04.
