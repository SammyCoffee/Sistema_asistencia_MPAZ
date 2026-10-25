# Control de evidencias técnicas — disponibles y pendientes

**Proyecto:** Sistema MPAZ RFID · Capstone APT122

Se recibieron seis imágenes técnicas y una nueva guía 2.4 con anexos. Además, el equipo compartió el resultado de una **prueba simulada el 25-10-2026** con Flask.test_client y SQLite temporal. «Documentado» significa respaldo disponible; **no significa aprobación docente ni validación del hardware físico**. La ejecución simulada fue informada por el equipo, no realizada de forma independiente aquí.

| N.º | Estado | Respaldo y alcance | Pendiente |
|---|---|---|---|
| 01 Arquitectura | Diseño disponible | [PDF y vistas previas](Evidencias_Documentacion/README_DIAGRAMAS.md), anexos A1–A3 | Validación de despliegue; dominio, HTTPS y roles docentes previstos. |
| 02 SQLite | Parcial documentado | [Tablas](Base_de_Datos/BD_01_Estructura_Tablas_SQLite.png) y [consulta demo](Base_de_Datos/BD_02_Consulta_Asistencia_Demo_2026-10-13.png) | Esquema completo, restricciones e integridad. |
| 03 Estado API | **Prueba simulada informada** | [GET /estado 200](Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md) | Falta TXT original y, si se exige, captura del servicio desplegado. |
| 04 Nueva asistencia | **Correlación simulada documentada** | [POST /lectura y SQLite con el mismo evento_id, 0→1](Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md). La [captura del ESP32](Evidencias_Sistema_Aplicacion/API_01_ESP32_Envio_Lectura_HTTP200.png) solo acredita comunicación. | Falta repetir correlación con tarjeta y tótem físico. |
| 05 Evento repetido | Documentado en pruebas aisladas | [Captura previa](Evidencias_Sistema_Aplicacion/API_02_Evento_Repetido_Sin_Duplicados.png) con 7→7 y [simulación nueva](Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md) con 1→1 | Falta validación física y otros casos de duplicidad diaria. |
| 06 Login | Pendiente | Sin captura adjunta | Acceso al panel sin exponer credenciales. |
| 07 Panel | Pendiente | La consulta SQL no sustituye la vista de interfaz | Pantalla con registros ficticios. |
| 08 Exportación | Pendiente | Sin reporte adjunto | Exportación y apertura de Excel. |
| 09 Tótem y lectura | Documentado parcialmente | [Montaje](Evidencias_Sistema_Aplicacion/HARDWARE_01_ESP32_PN532_Montaje.jpeg), [tarjeta](Evidencias_Sistema_Aplicacion/HARDWARE_02_Tarjeta_Prueba_PN532.jpeg) y [monitor serie](Evidencias_Sistema_Aplicacion/API_01_ESP32_Envio_Lectura_HTTP200.png) | Validación integral del dispositivo; fotos solas no acreditan registro. |
| 10 Integración completa | **Backend simulado demostrado; integración física pendiente** | [Simulación correlacionada solicitud→API→SQLite](Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md) | Faltan lectura física PN532/ESP32, transmisión Wi-Fi correlacionada y piloto escolar. |

[Inventario de las seis imágenes y limitaciones](README_EVIDENCIAS_2.4.md).

## Criterios de revisión

1. Distinguir diseño, evidencia de ejecución y aprobación académica.
2. Mantener las capturas originales con sus rutas del ZIP y emplear datos ficticios.
3. Vincular futuras pruebas a objetivo, resultado esperado y observado, evento y registro cuando corresponda.
4. Revisar requisitos formales con el docente; este control no sustituye la rúbrica.
5. No marcar como completadas las pruebas sin respaldo ni recalcular el avance declarado en la Ficha 04.

La planificación de Fase 1 se conserva; la evidencia de ejecución se reúne en Fase 2. Próximo respaldo necesario: TXT de la simulación y nueva asistencia correlacionada **desde el lector físico**, interfaz/exportación y piloto.
