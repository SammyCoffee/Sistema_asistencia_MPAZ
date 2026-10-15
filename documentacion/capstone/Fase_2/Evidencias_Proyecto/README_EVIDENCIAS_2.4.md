# Evidencias técnicas del documento 2.4 — MPAZ RFID

Se incluyen seis fotografías/capturas originales adjuntas por el equipo y la Guía 2.4 de **revisión**, con tres anexos gráficos de diseño (A1–A3) y tres anexos de ejecución (B1–B3).

## Alcance de las evidencias

| Archivo | Evidencia directa | Limitación |
| --- | --- | --- |
| [BD_01_Estructura_Tablas_SQLite.png](Base_de_Datos/BD_01_Estructura_Tablas_SQLite.png) | Existencia de tablas `alumnos`, `asistencias`, `tarjetas` y `totems` en SQLite | No certifica contenido ni integridad referencial por sí misma |
| [BD_02_Consulta_Asistencia_Demo_2026-10-13.png](Base_de_Datos/BD_02_Consulta_Asistencia_Demo_2026-10-13.png) | Consulta SQL de registro ficticio con entrada y salida | No confirma que corresponda al mismo evento que el monitor serie |
| [API_01_ESP32_Envio_Lectura_HTTP200.png](Evidencias_Sistema_Aplicacion/API_01_ESP32_Envio_Lectura_HTTP200.png) | UID de tarjeta de pruebas, `evento_id`, JSON, HTTP 200 y respuesta desde API | HTTP 200 **no equivale** a inserción de nueva asistencia; el mensaje visible empieza «El alumno ya…» |
| [API_02_Evento_Repetido_Sin_Duplicados.png](Evidencias_Sistema_Aplicacion/API_02_Evento_Repetido_Sin_Duplicados.png) | Prueba `evento_repetido` con 7 registros antes y después | Realizada en **copia de pruebas**, no en datos reales de alumnos |
| [HARDWARE_01_ESP32_PN532_Montaje.jpeg](Evidencias_Sistema_Aplicacion/HARDWARE_01_ESP32_PN532_Montaje.jpeg) | Foto del hardware y cableado | No demuestra por sí misma una transmisión exitosa |
| [HARDWARE_02_Tarjeta_Prueba_PN532.jpeg](Evidencias_Sistema_Aplicacion/HARDWARE_02_Tarjeta_Prueba_PN532.jpeg) | Tarjeta de prueba aproximada al lector | No demuestra por sí misma una inserción de asistencia |

Los **dos PDF originales de diagramas** ya están en `Evidencias_Documentacion/`, por lo que no se duplican en este paquete. La Guía 2.4 los contiene como anexos A1–A3.

## Estado de entrega

- **Borrador para revisión**: el DOCX aún requiere validación de tareas/responsables entre Samantha y Lucas y revisión docente.
- **Evidencias existentes**: las seis imágenes de prueba incluidas, más dos PDF previamente subidos de diagramas.
- **Evidencias pendientes**: piloto escolar, demostración de registros por interfaz, exportación y validación final completa, además del dominio/HTTPS/roles docentes si corresponde.

No publicar datos personales reales de estudiantes, contraseñas ni API keys. Las imágenes incluidas solo contienen referencias de prueba visibles.
